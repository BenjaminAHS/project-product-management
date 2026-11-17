# FlowAssist — final pitch: speaker notes

Ten slides, one per course beat, then an appendix for questions (hidden when presenting). For each slide: what it is about, what to say, and **the code and documents behind it**.
Files: [PDF (10 slides)](FlowAssist_Final_Pitch.pdf) · [PPTX with notes and appendix](FlowAssist_Final_Pitch.pptx) · live demo: https://deploy-project-product-management.vercel.app/?demo

## 1. FlowAssist
*Data & AI Product · Final pitch*

**What this slide is about:** the promise in one line. FlowAssist is a copilot for payment-operations specialists at a B2B payments company.

**Say it:** "Ten slides, one per course step. We built it, measured it, and we ask you for a conditional go."

**In the code:** repo BenjaminAHS/project-product-management — start at README.md and spec.md (the full specification). Live demo: deploy-project-product-management.vercel.app.

## 2. Specialists spend 40 % of every ticket searching.
*01 · Problem · Course S1*

**What this slide is about:** the pain and its price — the course's "symptom → cause" and "the do-nothing has a price".

**Say it:** Karim, Tier-1 specialist, spends 5.7 min searching and 4.8 min drafting per ticket. Root cause: payment data split across services with no merchant view.

**In the code / docs:** 01_problem_statement.md (problem sentence, persona, problem tree, do-nothing), governance.md S1. Figures are course scenario assumptions.

**If asked:** why AI and not rules? Macros cover ~15 %; fuzzy references and fees need matching — but a wrong match is worse than no draft, so it is a copilot (appendix: architecture).

## 3. FlowAssist finds the payment and drafts the reply. The specialist decides.
*02 · Solution · Course S1–S3*

**What this slide is about:** the agent's job in one sentence and its trust level per step (L1 read, L3 scoped lookup, L2 draft, person-only send).

**Say it:** walk left to right; stop on the green box.

**In the code:** prototype/engine.js (browser preview) and flowassist/engine.py (server authority): classify() reads the request, analyze() finds the payment within the assigned merchant, make_draft()/source_records() draft with citations, evaluate_draft() checks. There is deliberately no send function: the app records a reply only after human review (recordReply in prototype/app.js).

## 4. Users showed us what we couldn’t see.
*03 · Validation · Course S3*

**What this slide is about:** the design loop — users change the design, not the threshold.

**Say it:** be honest about the gate: 1 of 3 finished unaided (course gate: 4 of 5), so desirability is not validated yet.

**In the code:** D08 = STATUS map + plainStatus() in prototype/app.js (amber "Sent to recipient's bank · not yet received"); D09 = renderFacts() and #verified-facts in prototype/index.html; D10 = sourceGuide() in renderSources(). The v0.8 three-step flow is a design hypothesis, not a user finding: it is what we retest with 5 users (gate: 4 of 5 finish unaided). Evidence: 03_user_research.md.

## 5. We size the workload, not a market report.
*04 · Market · Course S2*

**What this slide is about:** bottom-up sizing of an internal product: tickets × share × success rate × value per ticket, net of AI and error cost.

**Say it:** the one branch that decides everything is the time saved per eligible ticket (48 % base, a guess to test).

**In the code / docs:** 02_sizing.xlsx (Inputs, Upside, Decision tabs), 02_investment_memo.md. The €175k is the full-scope gross value before costs (also covers disputes and KYC tickets at lower rates).

## 6. Four fixed steps. A person decides.
*05 · Product · Course S4*

**What this slide is about:** the product beat = live demo + the AI architecture decoded (graded at the oral). Workflow, not agent: four fixed steps, one rung per step (all rung 1: rules and templates, they pass the development set), a trust level per step (L1 router, L3 scoped lookup, L2 draft, person approves), human checkpoints ⊘ (abstention on sensitive or unclear tickets; one approval in step 3) and one override switch ⏻ with a named owner.

DEMO SCRIPT (open the link with ?demo so the tour stays closed): (1) DEMO-01: step 1, open the ledger then the clearing record; the cited reply appears in step 2 with the verified facts; step 3, tick "I checked the facts and the wording", click Approve & close · demo. (2) DEMO-05: add "We will refund you next week." to the reply: the screen blocks it before any server call (red notice quoting the sentence, approval box disabled), and the server would refuse it anyway (HTTP 422) even if the screen were bypassed. Click "Put FlowAssist’s reply back". (3) DEMO-03 (compliance): one clear card saying why and what to do, the hand-over reason already suggested: preview, confirm. Each closed case shows its outcome and "Next open ticket".

**In the code:** classify() and analyze() in flowassist/engine.py (mirrored in prototype/engine.js), make_draft()/source_records(), evaluate_draft(); api/index.py (/api/check, /api/handover); ASSIST_MODE in flowassist/flags.py; maybePrefill(), recordReply(), nextStepText() in prototype/app.js. Diagram and component table: 04_architecture.md, spec.md §3.

**Backup:** if the network fails, the banner says "Assistant server unavailable" and the page falls back to manual handling (designed outage behaviour).

## 7. Conditional GO: worth it above 41.2 % time saved.
*06 · Business case · Course S2*

**What this slide is about:** a number, an alternative, a threshold. EV €159.8k (pessimistic −€59.8k p 0.2, base €141.3k p 0.6, optimistic €434.9k p 0.2) vs do-nothing €57.6k vs hurdle €125k. The pessimistic case doesn't clear the hurdle, hence conditional.

**Say it:** say the weakness first (cost per ticket). Build/buy/orchestrate → orchestrate (4.35 vs 3.15 vs 2.15), see appendix.

**In the code / docs:** 02_sizing.xlsx Decision and Build-or-buy tabs; 02_investment_memo.md. The 41.2 % flip point is the success criterion in 03_product_brief.md §7 and spec.md §1.

## 8. Three promises, and how we’ll prove them.
*07 · Proof · Course S5–S6*

**What this slide is about:** the two graded points "3 business metrics with expected effects" (S5, level 5 of the stack) and "A/B protocol with sample size" (S6). The eval numbers (levels 1–3) move to the footnote.

**The metrics:** baselines from 02_sizing.xlsx; expected effects derived from the 41.2 % flip point (18.0 min × 0.588 = 10.6 min; €10 × 0.588 = €5.88); QA stated as a non-effect with a stop band. Counter-metrics (slide 9): 7-day reopen and edit rate.

**The a/b:** unit = the eligible tracing ticket (18 agents would give 9 per arm, too few; risk: agents learn from drafts → report it). n per arm = 2 (z0.975 + z0.80)² σ² / Δ² = 2 × 2.80² × 18² / 3.6² ≈ 393, with σ = 18 min an assumption (CV 1) to measure in shadow mode before the start, and Δ = 3.6 min (20 %), the smallest saving that changes the decision (below it: kill). ≈ 786 tickets ≈ one week of eligible traffic (≈ 1,040 a week), but we run 4 weeks because QA is read weekly and reopen needs 7 days. Decision rule written before: ship ≥ 41.2 % with every guardrail held; iterate 20–41 %; kill < 20 % or any guardrail broken; stop early only on harm (a draft on a human-only ticket, another merchant's data). Segments pre-registered: language, plan.

**In the code:** handling time = activeTime() in prototype/app.js, sent as handling_ms on reply_recorded; make metrics → metrics/report.md (p50/p95 by language and plan). Full protocol: 06_07_experiments_operations.md (to write); appendix slide "Experiment".

## 9. One owner can stop it fast.
*08 · Risks · Course S7*

**What this slide is about:** adverse effects, monitoring and rollback (graded point). Guardrail on the server, counter-metrics with a harm threshold and an owner, and the switch as the rollback.

**Say it:** Air Canada 2024 — the company answers for its bot, so the switch has an owner, not the developer. A pre-filled reply invites approval without reading (automation bias): the edit rate and the 7-day reopen rate are watched for that.

**In the code / docs:** /api/check → HTTP 422 (api/index.py, evaluate_draft() in flowassist/engine.py); ASSIST_MODE on | suggest_only | off in flowassist/flags.py (unknown → suggest_only); markServerDown() in prototype/app.js (fail-closed); events reply_recorded (edited, handling_ms) and check_failed → make metrics; four monitoring layers with thresholds in docs/TRACKING_PLAN.md and spec.md §7; harm threshold and owners in governance.md S5–S7; release path .github/workflows/ci.yml and sync-deploy.yml (smoke test on production).

## 10. Conditional GO for a 4-week pilot on tracing tickets.
*09 · The ask · Course S8*

**What this slide is about:** the decision we ask for. A conditional GO for a 4-week shadow + A/B pilot on tracing tickets only, with four preconditions; a clear no-go if the pilot misses 41.2 % or breaks a guardrail.

**Say it:** end on the decision, not the technology. Then each member names their part (fill the “who did what” line before the oral).

**In the code / docs:** preconditions map to open items in spec.md §11 (grader 2, held-out eval_set_v1, loaded cost per ticket, Legal on scope). The launch memo goes in 08_launch_memo.md with the final tag v1.0.

**Course point (s8):** go / no-go and the launch plan.

---

# Appendix (for questions, hidden when presenting)

## 11. A workflow you can draw, and a server that has the last word
*Appendix · Architecture*

**What this slide is about:** the architecture decoded. Four steps in a fixed workflow (router, routing rule, drafter, policy checker) and a server that re-checks every recorded action. A global switch can reduce the assistant to suggestions or turn it off.

**Say it:** “It is a workflow, not an agent: every path is drawn in advance, no model chooses a tool.”

**In the code:** prototype/engine.js = instant preview in the browser; flowassist/engine.py = the authority (same logic, kept identical by tests/test_parity.py: 123 cases, 468 draft checks). api/index.py (FastAPI on Vercel): /api/analyze, /api/check, /api/handover. Switch: flowassist/flags.py, env ASSIST_MODE = on | suggest_only | off. Browser client: prototype/server.js; fail-closed path markServerDown() in prototype/app.js. Diagram: 04_architecture.md and spec.md §3.

**Course point (s4):** decode the architecture, human checkpoints ⊘ and one override switch ⏻ with an owner.

## 12. What we promise, and what must not break
*Appendix · Metrics*

**What this slide is about:** three business metrics with expected effects (time per eligible ticket 18.0 → ≤ 10.6 min, cost €10 → ≤ €5.88, QA ≥ 92 % unchanged as a stated non-effect), then what to protect: primary, guardrails, counter-metrics.

**Say it:** “The expected effects are derived from the S2 flip point, not measured; the reopen rate is the counter-metric so we don’t reward closing without solving.”

**In the code:** local metrics, no third-party analytics. The page sends allowlisted events (track() in prototype/app.js → POST /api/events); flowassist/telemetry.py drops unknown keys and long text and writes JSON lines; make dev writes metrics/events.jsonl; make metrics runs scripts/metrics_report.py → metrics/report.md (funnel, blocks, p50/p95 by language and plan, escalation, infra). Event list and thresholds: docs/TRACKING_PLAN.md.

**Course point (s5):** five-level stack; Goodhart; report by segment; harm threshold.

## 13. An LLM judge we checked before trusting
*Appendix · AI judge*

**What this slide is about:** the LLM-as-a-judge and how we validated it. Guideline v1.0 gave 53 % agreement with our human grader; reading the disagreements showed two ambiguities in our own rubric; after one fix (v1.1) agreement is 73 % and the judge escalates 41/41 known-bad drafts with 0 over-accepted. The 4 remaining disagreements are a real defect the human missed: English messages answered in French or German.

**Say it:** “We read the disagreements, fixed the rubric once, re-measured — and the judge found a bug we had missed.”

**In the code:** evals/judge/rubric.md (guideline, written before grading), evals/judge/judge_prompt.txt (= rubric copied), scripts/judge.py (make judge; OpenAI gpt-6-luna, structured yes/no output; key in .env). Results: evals/judge_report.md (v1.1), evals/judge_report_v1.0.md, evals/report_v0.md §6. Open defect: S5-M01 in spec.md.

**Course point (s5):** make the judge trustworthy: rubric first, human–human then human–judge agreement, fix once, re-measure.

## 14. How we would prove it caused the saving
*Appendix · Experiment*

**What this slide is about:** how we would prove causality. The hypothesis sentence, the design chain (shadow → A/B on tickets for 4 weeks → 5 % holdout) and the decision rule written before looking (ship / iterate / kill; stop early only on harm).

**Say it:** “Unit = the ticket: 18 agents would give 9 per arm, too few. Duration is set by the slowest guardrail, not the first good number.” Sample size: 393 per arm to detect a 20 % saving (3.6 min) at α 5 %, power 80 %, with σ = 18 min assumed (to measure in shadow mode).

**In the code:** assist modes in flowassist/flags.py give shadow-like operation (suggest_only = drafts visible, never used); handling time is measured per ticket (activeTime() in prototype/app.js, sent as handling_ms in reply_recorded events). The A/B assignment itself is deliberately not coded before the protocol is signed (docs/TRACKING_PLAN.md).

**Course point (s6):** randomise the right unit; size it and decide before; no peeking; pre-register segments.

## 15. We orchestrate: our rules and data, a rented model only where it earns its place
*Appendix · Build or buy*

**What this slide is about:** build, buy or orchestrate, scored on the course’s ten questions: orchestrate 4.35, build 3.15, buy 2.15.

**Say it:** give the counter-argument yourself: a vendor at €0.92 per resolution would cost ~€34k a year less at base volume; we pay that for data control and the ability to leave.

**In the code / docs:** 02_sizing.xlsx Build or buy tab (weights, scores, break-even). In the product, “orchestrate” means our own rules and data (flowassist/), with a rented model only where it earns its place: today only the offline judge (scripts/judge.py, OpenAI gpt-6-luna).

**Course point (s2):** build/buy/orchestrate; the real competitor is the next-best project.
