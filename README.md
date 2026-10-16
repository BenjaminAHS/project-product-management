# PayFlow B2B — Agent-Assist Copilot for B2B Payments

**Course:** Data & AI Product: From Diagnosis to Delivery (MSA-DAT07-04) · Albert School & Mines Paris-PSL · shared project with Agentic Workflows  
**Cohort:** M2-INTER-1  

## Team
| Name | Git handle | Also in the Agentic Workflows team? |
|---|---|---|
| Lenny Santus | @lsantus-mines | no |
| Anthony Rascle | @antotototototo18 | no |
| Antoine Rabeau | @arabeau | no |
| Benjamin Caujolle | @BenjaminAHS | no |
| Colin Sibieude | @csibieude | no |

## Our agent
- **Starting point:** Proposal P2 — Agent-assist copilot for a fintech (B2B payments).
- **The company:** PayFlow B2B — European B2B payments fintech, 800 merchant enterprise & marketplace customers, 12,000 support tickets / month, support team of 18 Tier-1 payment operations specialists.
- **The job, in one sentence:** When a merchant opens a support ticket regarding a transaction, payout, or dispute, the agent pre-reads the merchant's account and transaction ledgers, flags regulatory constraints (PSD2 SCA, AML/KYC status), and drafts a cited response with transaction links in the Zendesk sidebar for the human agent to review, edit, and send.
- **Trust level per step:**
  - *Data Ingestion & Ledger Querying:* **L4** (autonomous retrieval and timeline reconstruction across core ledger, SEPA/SWIFT clearing feeds, and compliance DB within secure tenant VPC).
  - *Grounding & Entity Matching Evaluator:* **L4** (automated scoring model validating transaction IDs, amounts, and currency; drops draft to "context-only" if score < 0.95).
  - *Response Drafting:* **L2** (copilot generates draft in the agent sidebar; never visible to customer).
  - *Customer Reply & Monetary Actions:* **L1 (Human Only)** (the human agent reviews, edits, and sends every message; the copilot has zero write permissions on bank funds or ledger state).
- **One thing it must never do:** It must **never** send a reply directly to a merchant, **never** execute or promise a fund transfer, refund, or settlement release, and **never** match or disclose transaction details without cryptographically verified merchant account ID match (preventing cross-tenant data leakage).

## Repository structure
One numbered file per session. Every member authors commits in at least four of the numbered files.

| File | Session | Status | Description |
|---|---|---|---|
| `00_pitch.md` | before S3 | done | Half-page pitch & 7-point checklist (Proposal P2 adapted) |
| `01_problem_statement.md` | S1–S2 — Assignment 1 | done | Problem statement, 5 Whys, AI justification, press release, hypotheses |
| `governance.md` | created for S1, updated S2 | done | EU AI Act tier, GDPR basis, accountability, guardrails, cost-of-error owners |
| `02_sizing.xlsx` | S2 — Assignment 2 | done | Bottom-up financial model (3 scenarios, 7 cost lines, sensitivity, build vs buy) |
| `02_investment_memo.md` | S2 — Assignment 2 | done | One-page CFO investment memo (CONDITIONAL GO, €159.8k EV, 41.2% flip point) |
| `03_product_brief.md` | S3 | upcoming | User journeys, UX specifications, system prompts, edge case specs |
| `04_architecture.md` | S4 | upcoming | Technical architecture, RAG pipelines, grounding evaluator, tool schemas |
| `05_metrics.md` | S5 | upcoming | Business & technical metrics, counter-metrics, eval-set definitions |
| `06_ab_protocol.md` | S6 | upcoming | Agent-level RCT experiment design, sample size calculation, MDE |
| `07_operations.md` | S7 | upcoming | Model monitoring, drift detection, incident playbooks, on-call runbooks |
| `08_launch_memo.md` | S8 | upcoming | Final launch memo, go/no-go criteria, executive readout |
| `spec.md`, `product_brief.md` | final | upcoming | Consolidated deliverables for final oral defence |
| `/prototype`, `/evals` | from S4 | upcoming | Python agent prototype, test datasets, automated evaluation harness |

## Rules
- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.
