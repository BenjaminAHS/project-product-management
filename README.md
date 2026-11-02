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
- **Trust level per step (S3 scope):** L1 entity suggestions; L3 internal tenant-scoped retrieval with human transaction confirmation; L2 cited drafting and validation; person-only customer sending; L4 bounded audit metadata. The model score cannot authorize data access. Dispute/KYC requests route to specialists. See `governance.md` Session 3 for updates to the earlier L4 matching proposal.
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
| `03_product_brief.md`, `03_design_details.md` | S3 | v1 ready; v2 pending interviews | Concise brief plus process, sorted RICE and model tables |
| `03_ai_lean_canvas.md` | S3 | drafted | All 14 blocks aligned with S1/S2 |
| `03_user_research.md` | S3 | protocol ready; not conducted | Three interviews and two unassisted tests to record |
| `03_prototype_link.md`, `/prototype` | S3 | local clickable v0.1 | Synthetic inbox, safe draft review and handover; browser screenshot pending |
| `spec.md` | S3 | skeleton v0 ready | Contracts, trust levels, edge cases and fallbacks |
| `/evals/eval_set_v0.csv` | S3 | 20 proposed cases | Synthetic inputs and AI-proposed labels; human approval pending |
| `04_architecture.md` | S4 | upcoming | Technical architecture, RAG pipelines, grounding evaluator, tool schemas |
| `05_metrics.md` | S5 | upcoming | Business & technical metrics, counter-metrics, eval-set definitions |
| `06_ab_protocol.md` | S6 | upcoming | Agent-level RCT experiment design, sample size calculation, MDE |
| `07_operations.md` | S7 | upcoming | Model monitoring, drift detection, incident playbooks, on-call runbooks |
| `08_launch_memo.md` | S8 | upcoming | Final launch memo, go/no-go criteria, executive readout |
| `product_brief.md` | final | upcoming | Consolidated deliverable for final oral defence |
| `/prototype`, `/evals` | S3 → S4 | S3 surface/seed ready; pipeline pending | Local HTML now; executable agent and evaluation runner in S4 |

## Assignment 3 — status and evidence

Start with [the brief](03_product_brief.md), [design details](03_design_details.md), [Lean Canvas](03_ai_lean_canvas.md), [specification](spec.md) and [prototype instructions](03_prototype_link.md). The original `S3_templates/` are preserved; deliverables live at root as requested. Governance S3 is integrated into `governance.md`; no duplicate root governance snippet is needed.

- Completed design artifacts: six-step process with source types/error assumptions/trust/metrics; eight ranked features, three MUST and five WON'T; component model choices; data audit; 20 self-contained synthetic proposed cases.
- Still needs human evidence: three 20-minute interviews, two unassisted usability tests, observed brief v2 changes, independent human label approval and each member's own authored commit. No interview, label sign-off or measured product performance has been invented.
- Prototype is local HTML, not an S4 agent. Browser rendering/keyboard checks and a screenshot remain to be done; see the prototype file for exact instructions.
- The assignment DOCX says **8 November 2026**; the template says **Friday 6 November, start of S5**. Aim for 6 November and confirm the official deadline with the lecturer. The criterion retains the DOCX's 8 November date; no prior 30 October test is backdated.
- S3 treats unsupported historical-data claims as scenario assumptions. Tracing-only validation does not establish the full S2 business case, which also includes dispute/compliance value.

## Rules
- Commit with your own Git account: the individual question at the oral is about a commit you signed.
- Tag the final version `v1.0` before the first oral of your cohort. No commits after the first oral starts.
