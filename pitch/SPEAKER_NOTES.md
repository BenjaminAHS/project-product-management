# FlowAssist — final pitch: speaker notes

One section per slide: what the slide is about, what to say, **the components of the code and documents behind it**, and the course point it answers.
Files: [PDF](FlowAssist_Final_Pitch.pdf) · [PPTX with these notes](FlowAssist_Final_Pitch.pptx) · live demo: https://deploy-project-product-management.vercel.app

## 1. FlowAssist
*Data & AI Product · From Diagnosis to Delivery · Final pitch*

**What this slide is about:** the product in one sentence. FlowAssist helps a Tier-1 payment specialist answer “where is my money?” with evidence; the specialist always sends.

**Say it:** “We followed the course loop end to end: diagnose, size, design, build, measure, operate. Each slide shows the course checkpoint it answers.”

**In the code:** the whole product is in the repo BenjaminAHS/project-product-management. Start at README.md, then spec.md v3 (the full specification, S1–S7). Live demo: deploy-project-product-management.vercel.app.

**Course point:** the oral is a 10-beat pitch (Airbnb style), not a technical demo.

## 2. Specialists spend 40 % of every ticket hunting through six tools
*Beat 1 · Problem — Course S1: symptom → cause, the do-nothing has a price*

**What this slide is about:** the pain and its price. 40 % of an 18-minute ticket is spent searching six tools; that is about €415k a year of investigation labour and a 4.5 h median first response.

**Say it:** start from Karim’s day (search 5.7 min, drafting 4.8 min), then the root cause (fragmented payment data), then the do-nothing with a price.

**In the code / docs:** 01_problem_statement.md (problem sentence, persona, problem tree, 5 Whys, do-nothing), governance.md section S1 (the six governance questions). All figures are course scenario assumptions, labelled as such.

**Course point (s1):** symptom ≠ cause; the do-nothing is not zero.

## 3. Four questions before saying “AI”
*Beat 2 · Solution — Course S1: is AI the right tool, and at which level?*

**What this slide is about:** why AI, and why only a copilot. The four course questions answered for our case.

**Say it:** “Rules alone can’t match vague references with fees; but one wrong match is worse than no draft, so the person keeps the send button.”

**In the code / docs:** 01_problem_statement.md §3 (Is AI the right tool?) and §4 (four selection questions); governance.md S1 Q1–Q6 (EU AI Act tier, data, accountability, never-do list).

**Course point (s1):** rule for 80 %? prediction or organisational decision? data and rights? cost of one error?

## 4. Find the payment, draft a cited reply, let the specialist decide
*Beat 2 · Solution — Course S1–S3: one job, a trust level per step*

**What this slide is about:** the agent’s job in one sentence and a trust level per step (L1 intent, L3 scoped lookup, L2 draft, person-only send), plus the never-do list.

**Say it:** walk left to right; stop on the green box: nothing reaches a merchant without a person.

**In the code:** the four steps live in prototype/engine.js (browser preview) and flowassist/engine.py (server authority): classify() = read intent, analyze() = find the payment within the assigned merchant, make_draft() / source_records() = cited reply, evaluate_draft() = checks. The send step does not exist in the code by design: the app only records a local reply after human review (prototype/app.js, recordReply).

**Course point (s1–s3):** one job, one sentence; a trust level per step, at least one below L4.

## 5. An internal product: we size the workload, not a market report
*Beat 4 · Market — Course S2: bottom-up, a source per branch, value is net*

**What this slide is about:** bottom-up sizing of an internal product. We size tickets and minutes, not a market report: 144k tickets × 50 % tracing × 75 % eligible × 48 % time saved (base guess).

**Say it:** name the source type of each branch (measured / tag share / guess) and point at the one branch that decides everything: time saved.

**In the code / docs:** 02_sizing.xlsx (Inputs, Upside, Decision tabs: low/base/high, source type per input, adoption ramp by quarter); 02_investment_memo.md.

**Course point (s2):** bottom-up with a source per branch; ranges, not points; value is net (minus AI cost and error cost); adoption is staged.

## 6. Conditional GO: it beats the next-best project only above 41.2 % time saved
*Beat 6 · Business case — Course S2: three scenarios, do-nothing, the hurdle*

**What this slide is about:** the decision. Three scenarios with probabilities give an expected value of €159.8k, above do-nothing (€57.6k) and above the hurdle (€125k, the self-serve portal). The pessimistic case does not clear the hurdle, so the answer is a conditional GO. Flip point: 41.2 % time saved.

**Say it:** be the first to say what could flip it: the sheet’s own check row implies €6.875 per ticket, not €10; at that cost the base case drops to ~€87k.

**In the code / docs:** 02_sizing.xlsx Decision tab (EV, comparisons, sensitivity table); 02_investment_memo.md (the four CFO questions, sensitivity paragraph). The 41.2 % threshold is reused as the success criterion in 03_product_brief.md §7 and spec.md §1.

**Course point (s2):** a number, an alternative, a threshold; the hurdle is another project.

## 7. We orchestrate: our rules and data, a rented model only where it earns its place
*Beat 7 · Alternatives — Course S2: build, buy or orchestrate · the hurdle is another project*

**What this slide is about:** build, buy or orchestrate, scored on the course’s ten questions: orchestrate 4.35, build 3.15, buy 2.15.

**Say it:** give the counter-argument yourself: a vendor at €0.92 per resolution would cost ~€34k a year less at base volume; we pay that for data control and the ability to leave.

**In the code / docs:** 02_sizing.xlsx Build or buy tab (weights, scores, break-even). In the product, “orchestrate” means our own rules and data (flowassist/), with a rented model only where it earns its place: today only the offline judge (scripts/judge.py, OpenAI gpt-6-luna).

**Course point (s2):** build/buy/orchestrate; the real competitor is the next-best project.

## 8. The smallest product that can pass or fail the 41.2 % test
*Beat 5 · Product — Course S3: map the process, cut until it can fail, climb the ladder only when needed*

**What this slide is about:** the MVP. Process redesign (18 → 7.6 min, a hypothesis), MoSCoW (3 MUST, 5 WON’T), the model ladder (rung 1 rules on all four steps) and the one-sentence success criterion.

**Say it:** “We cut until it could fail. The draft is a MUST because it tests the flip assumption, even with a lower RICE score.”

**In the code / docs:** 03_product_brief.md (process, MoSCoW, criterion), 03_design_details.md (RICE table, eight automation tests), spec.md §2 (scope) and §3 (one rung per component: classify, analyze, make_draft, evaluate_draft are all rules/templates).

**Course point (s3):** map the process first; MUST ≤ 4, WON’T ≥ 5; climb the ladder only when the rung below fails.

## 9. Users found what we couldn’t see: “sent to bank” read as “received”
*Beat 3 · Validation — Course S3: the design loop, users change the design, not the threshold*

**What this slide is about:** what users changed. 2 of 3 testers read the green “sent to bank” chip as money received. That produced D08–D10, now shipped.

**Say it:** be honest about the gate: only 1 of 3 finished unaided (the course gate is 4 of 5), so desirability is not validated yet; we retest on v0.5.

**In the code:** prototype/app.js STATUS map + plainStatus() = D08 plain-language amber/green/red status; renderFacts() and the #verified-facts box in prototype/index.html = D09 checklist; sourceGuide() in renderSources() = D10 “what each source confirms, ledger first”; styles in prototype/styles.css (.status-wait/.status-done/.status-stop, .facts). Evidence: 03_user_research.md.

**Course point (s3):** Mom Test, five users, users change the design but not the threshold.

## 10. A workflow you can draw, and a server that has the last word
*Beat 5 · Product — Course S4: decode the architecture · workflow or agent?*

**What this slide is about:** the architecture decoded. Four steps in a fixed workflow (router, routing rule, drafter, policy checker) and a server that re-checks every recorded action. A global switch can reduce the assistant to suggestions or turn it off.

**Say it:** “It is a workflow, not an agent: every path is drawn in advance, no model chooses a tool.”

**In the code:** prototype/engine.js = instant preview in the browser; flowassist/engine.py = the authority (same logic, kept identical by tests/test_parity.py: 123 cases, 468 draft checks). api/index.py (FastAPI on Vercel): /api/analyze, /api/check, /api/handover. Switch: flowassist/flags.py, env ASSIST_MODE = on | suggest_only | off. Browser client: prototype/server.js; fail-closed path markServerDown() in prototype/app.js. Diagram: 04_architecture.md and spec.md §3.

**Course point (s4):** decode the architecture, human checkpoints ⊘ and one override switch ⏻ with an owner.

## 11. Live demo
*Beat 5 · Product — Course S4: a live demo on real tickets, not a mockup*

**What this slide is about:** the live demo, three moves.

**Demo script:** (1) DEMO-01: open the ledger, then the clearing record, tick the review, insert the cited draft, record the reply. (2) In the editor, add “We will refund you next week” and try to record: the server refuses it with HTTP 422 and the case stays open. (3) DEMO-03 (compliance hold): no draft; prepare and record a handover with a reason.

**In the code:** (1) renderSources(), applyDraft(), recordReply() in prototype/app.js, each gated by serverGate() → POST /api/check. (2) evaluate_draft() in flowassist/engine.py, code “commitment”; COMMITMENT_RE lists the EN/FR/DE promises. (3) classify() routes to “compliance”; analyze() returns human_only; handover() builds the redacted packet, POST /api/handover.

**Backup:** if the network fails, the banner shows “Assistant server unavailable” and the page continues in manual mode: that is the designed outage behaviour.

## 12. What the prototype proves today, and what it doesn’t
*Beat 8 · Proof — Course S4–S5: demo data ≠ eval data · guardrails tested under attack*

**What this slide is about:** what the prototype proves and what it doesn’t. 50/50 expected states, 0 drafts on the 13 human-only cases, 30/30 attacks caught, never a source from another merchant. The 50 cases are regression only.

**Say it:** “Demo data and evaluation data never meet: these 50 were examined while fixing bugs, so the real number will come from 200 held-out tickets.”

**In the code:** make eval → scripts/eval_s4.cjs on evals/eval_set_v0.csv + evals/fixtures_v0.json (results in evals/results_v0.json, report evals/report_v0.md). make adversarial → scripts/run_adversarial.py on evals/adversarial_v0.csv (OWASP LLM01/02/06/09 rows); one miss fails CI (.github/workflows/ci.yml). Guardrail layers: input = INJECTION_RE, SECRET_RE, ROUTES; scope = analyze(); output = PROMISE_RE, COMMITMENT_RE, citation and amount checks in evaluate_draft().

**Course point (s4–s5):** demo ≠ eval data; every miss becomes a spec line; red-team the guardrails.

## 13. What we promise, and what must not break
*Beat 8 · Proof — Course S5: 3 business metrics with expected effects · what to protect*

**What this slide is about:** three business metrics with expected effects (time per eligible ticket 18.0 → ≤ 10.6 min, cost €10 → ≤ €5.88, QA ≥ 92 % unchanged as a stated non-effect), then what to protect: primary, guardrails, counter-metrics.

**Say it:** “The expected effects are derived from the S2 flip point, not measured; the reopen rate is the counter-metric so we don’t reward closing without solving.”

**In the code:** local metrics, no third-party analytics. The page sends allowlisted events (track() in prototype/app.js → POST /api/events); flowassist/telemetry.py drops unknown keys and long text and writes JSON lines; make dev writes metrics/events.jsonl; make metrics runs scripts/metrics_report.py → metrics/report.md (funnel, blocks, p50/p95 by language and plan, escalation, infra). Event list and thresholds: docs/TRACKING_PLAN.md.

**Course point (s5):** five-level stack; Goodhart; report by segment; harm threshold.

## 14. An LLM judge we checked before trusting
*Beat 8 · Proof — Course S5: make the judge trustworthy · fix once, re-measure*

**What this slide is about:** the LLM-as-a-judge and how we validated it. Guideline v1.0 gave 53 % agreement with our human grader; reading the disagreements showed two ambiguities in our own rubric; after one fix (v1.1) agreement is 73 % and the judge escalates 41/41 known-bad drafts with 0 over-accepted. The 4 remaining disagreements are a real defect the human missed: English messages answered in French or German.

**Say it:** “We read the disagreements, fixed the rubric once, re-measured — and the judge found a bug we had missed.”

**In the code:** evals/judge/rubric.md (guideline, written before grading), evals/judge/judge_prompt.txt (= rubric copied), scripts/judge.py (make judge; OpenAI gpt-6-luna, structured yes/no output; key in .env). Results: evals/judge_report.md (v1.1), evals/judge_report_v1.0.md, evals/report_v0.md §6. Open defect: S5-M01 in spec.md.

**Course point (s5):** make the judge trustworthy: rubric first, human–human then human–judge agreement, fix once, re-measure.

## 15. How we would prove it caused the saving
*Beat 8 · Proof — Course S6: randomise the right unit · size it and decide before you look*

**What this slide is about:** how we would prove causality. The hypothesis sentence, the design chain (shadow → A/B on tickets for 4 weeks → 5 % holdout) and the decision rule written before looking (ship / iterate / kill; stop early only on harm).

**Say it:** “Unit = the ticket: 18 agents would give 9 per arm, too few. Duration is set by the slowest guardrail, not the first good number.” The sample size per arm is still to compute in 06_07_experiments_operations.md.

**In the code:** assist modes in flowassist/flags.py give shadow-like operation (suggest_only = drafts visible, never used); handling time is measured per ticket (activeTime() in prototype/app.js, sent as handling_ms in reply_recorded events). The A/B assignment itself is deliberately not coded before the protocol is signed (docs/TRACKING_PLAN.md).

**Course point (s6):** randomise the right unit; size it and decide before; no peeking; pre-register segments.

## 16. Something will go wrong; one person can stop it in minutes
*Beat 9 · Risks — Course S7: four layers, an owner each, a switch that is a tested procedure*

**What this slide is about:** operation. Four monitoring layers with a paging threshold and an owner each, the switch as a rollback procedure, the release path and the drifts to watch.

**Say it:** “Rolling back is one setting changed by a role, not by the developer: on → suggest-only → off in under 15 minutes.” Mention Air Canada 2024: the company answers for its bot.

**In the code:** switch = ASSIST_MODE in flowassist/flags.py (any unknown value fails safe to suggest_only); traces = Trace in flowassist/telemetry.py (one JSON line per request); release path = .github/workflows/ci.yml (make ci on every PR) then .github/workflows/sync-deploy.yml (deploy only after green CI, then scripts/smoke.py on production). Rollback plan, incident classes and drift: spec.md §7 and governance.md S7. Setup: docs/SETUP_CI.md.

**Course point (s7):** four layers, four clocks, four owners; the switch is a tested procedure; the company answers for the bot.

## 17. Conditional GO: a 4-week shadow + A/B pilot, tracing tickets only
*Beat 10 · The ask — Course S8: go / no-go and the launch plan*

**What this slide is about:** the decision we ask for. A conditional GO for a 4-week shadow + A/B pilot on tracing tickets only, with four preconditions; a clear no-go if the pilot misses 41.2 % or breaks a guardrail.

**Say it:** end on the decision, not the technology. Then each member names their part (fill the “who did what” line before the oral).

**In the code / docs:** preconditions map to open items in spec.md §11 (grader 2, held-out eval_set_v1, loaded cost per ticket, Legal on scope). The launch memo goes in 08_launch_memo.md with the final tag v1.0.

**Course point (s8):** go / no-go and the launch plan.
