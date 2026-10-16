# Governance — our living file

> Created for Assignment 1, one line added every session. One question at the oral is drawn from this file.  
> Answers are provisional: write what you know today, and mark what you still have to check.

## Session 1 — the six questions
| # | Question | Our answer (provisional) | To check with |
|---|---|---|---|
| 1 | **EU AI Act:** which risk tier is our agent in, and why? (minimal · limited — transparency: tell the user it is an AI · high-risk · prohibited) | **Limited risk (transparency obligations under Art. 50).** FlowAssist is an internal agent-assist copilot (Trust Level L2) assisting human support agents; it does NOT make automated decisions granting or denying access to essential financial services (credit, insurance, or account opening), which avoids the High-Risk tier (Annex III). We must log internal AI usage, maintain an AI transparency notice for agents, and ensure auditability. | Legal Counsel / Compliance Officer (confirm interpretation with ACPR/BaFin guidelines) |
| 2 | **Data:** whose data does it use, and on what legal basis? (GDPR art. 6; what the B2B contract allows) | **Merchant enterprise account and payment transaction data.** Legal basis: **GDPR Art. 6(1)(b)** (performance of the B2B merchant payment processing contract) and **Art. 6(1)(f)** (legitimate interest for support optimization and fraud triage). FlowAssist queries data stored within PayFlow's AWS EU-West-3 (Paris) VPC. Model API calls to LLM providers (Anthropic Claude 3.5 Sonnet / OpenAI) enforce zero data retention (ZDR) and zero model training on customer payloads. Strict cryptographic tenant-isolation (row-level security on `merchant_id`) prevents cross-tenant data leakage. | Data Protection Officer (DPO) & Information Security (CISO) |
| 3 | **Accountability:** who is accountable when it is wrong — and where is the human? | **The human Tier-1 payment operations specialist who reviews, edits, and sends the response is operationally accountable.** The **Head of Payment Operations** owns overall support SLA and answer quality. The **VP of Product** owns model performance and guardrails. The copilot operates strictly at Trust Level L2: it cannot send messages, execute fund transfers, or modify ledger records autonomously. "The AI made a mistake" is explicitly rejected as an operational or legal defense (Moffatt v. Air Canada precedent). | Head of Payment Operations & VP Product |
| 4 | **Never:** what must it never do? (our first guardrail) | **The agent must NEVER send an outbound message directly to a merchant, NEVER execute or authorize any monetary transfer, refund, or settlement release, and NEVER disclose transaction details without a cryptographically verified merchant account ID match (preventing cross-tenant data leaks).** | VP Engineering & Payment Ops QA Lead |
| 5 | **Explainability:** explainable to whom — the customer, the support agent, the auditor? | **To all three, at different levels of abstraction:**<br>1) *The Support Agent:* The Zendesk sidebar displays exact source citations with direct hyperlinks to internal transaction UUIDs, clearing house batch IDs, and database timestamps, plus a Grounding Confidence Score.<br>2) *The Merchant / Customer:* The drafted text explains the payment status in clear, human-readable plain language (e.g. "funds cleared French SEPA interbank clearing at 14:15 CET, pending beneficiary bank credit") without internal database jargon.<br>3) *The Auditor / Regulator (ACPR/BaFin):* Complete immutable JSON audit trail logging: incoming ticket, retrieved ledger records, prompt template, raw LLM draft, grounding evaluator score, agent edit diff, and final approved message with agent ID. | Payment Operations Lead & Internal Audit |
| 6 | **The people it cannot serve:** what happens to them? | **Edge cases and ungrounded queries are automatically escalated to human Tier-2 specialists.** If the Grounding Evaluator score is below 0.95 (ambiguous entities, multiple conflicting transactions, or unparseable inquiries), the copilot suppresses the draft and displays a "Context Only — No Draft Generated" banner. Complex dispute arbitration, suspected fraud syndicates, or legal subpoena requests bypass the copilot entirely via automated Zendesk priority routing. Multilingual inquiries (French, German, English) are handled through standardized English ledger normalization. | Tier-2 Escalations Manager |

## Session 2 — the cost of error
- **Which cost-of-error line is a legal or reputational risk, not just money?**  
  **Category 2 (Dispute deadlines & scheme rules) and Category 3 (KYC, Onboarding & PSD2 Regulatory Holds / Cross-tenant data leakage).**  
  While an error in Category 1 (Payment Tracing) merely causes merchant annoyance and agent re-investigation labor (~€15–€25/ticket), an error in Category 3 carries existential legal and regulatory exposure:
  1. *Cross-Tenant Data Leakage:* Displaying or sending Merchant A the transaction details, customer names, or bank account numbers of Merchant B violates banking secrecy laws and GDPR Art. 33/34. This triggers mandatory 72-hour regulatory breach notifications, potential GDPR fines up to 4 % of global annual turnover, and acute loss of enterprise merchant trust.
  2. *Regulatory Hold Misinformation:* Misinforming a merchant regarding PSD2 Strong Customer Authentication (SCA) exemptions or AML compliance reserve freezes can lead to wrongful fund retention claims, regulatory audits by financial supervisory authorities (ACPR in France, BaFin in Germany, FCA in the UK), and jeopardy of PayFlow’s payment institution license.
  3. *Missed Dispute Deadlines:* In Category 2, hallucinating a false card network dispute submission window (e.g. telling a merchant they have 30 days when Visa card scheme rules enforce a strict 14-day cutoff) causes the merchant to permanently forfeit chargeback rights, generating direct financial liability and contractual litigation.
- **Who in the company owns that risk?**  
  - **Regulatory & Data Compliance:** The **Chief Compliance Officer (CCO)** and the **Data Protection Officer (DPO)** own the regulatory liability, reporting to financial supervisory authorities, and GDPR breach management.  
  - **Operational & Scheme Liability:** The **Head of Payment Operations** owns the QA protocol, agent training, and dispute submission timelines.  
  - **Technical Guardrail Enforcement:** The **VP of Engineering** and **AI Product Lead** own the dual-LLM Grounding Evaluator, tenant-isolation query firewalls, and automated circuit breakers that suppress unverified drafts.

## Session 3 — data (to come)
*Data inventory, retrieval schemas, tenant isolation, and preprocessing pipelines.*

## Session 4 — human-in-the-loop points and the override switch (to come)
*L2 approval interfaces, diff tracking, grounding threshold circuit breaker, and one-click agent override switches.*

## Session 5 — counter-metrics and the segments we report (to come)
*Primary metric (AHT), counter-metrics (QA score, 7-day reopen rate, agent override rate), and protected reporting segments.*

## Session 6 — protected segments and the harm threshold that stops an experiment (to come)
*A/B trial experiment guardrails, enterprise merchant protection, and safety thresholds for experiment termination.*

## Session 7 — accountable owner, rollback authority, incident path (to come)
*Rollback triggers, operational on-call rotation, kill-switch authority, and incident post-mortem playbooks.*
