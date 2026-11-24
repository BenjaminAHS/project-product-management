# FlowAssist — final pitch: speaker notes

Ten slides, one per course beat, then an appendix for questions (hidden when presenting). For each slide: **who presents**, what to say, the hand-over to the next speaker, and **the code and documents behind it**.
Files: [PDF (10 slides)](FlowAssist_Final_Pitch.pdf) · [PPTX with notes and appendix](FlowAssist_Final_Pitch.pptx) · live demo: https://deploy-project-product-management.vercel.app/?demo (interface v0.9)

## Who presents what

| Slides | Speaker | Beat | Time |
|---|---|---|---|
| 1–2 | **Lenny** | Opening · Problem (S1) | 1 min 30 |
| 3–4 | **Antoine** | Solution · Validation with users (S1–S3) | 1 min 30 |
| 5 | **Benjamin** | Market sizing (S2) | 45 s |
| 6 | **Anthony** | Product: live demo v0.9 + architecture (S4) | 3 min |
| 7 | **Benjamin** | Business case and alternatives (S2) | 1 min |
| 8–9 | **Colin** | Proof: metrics and A/B · Risks (S5–S7) | 1 min 45 |
| 10 | **Lenny** | The ask, then everyone says their line (S8) | 1 min |

About 10–11 minutes. Questions (appendix): 11 architecture and 13 AI judge → **Anthony** · 12 metrics → **Colin** · 14 experiment and switch → **Antoine** · 15 build or buy → **Benjamin**. Swap freely, but keep one owner per slide so nobody talks over anyone.

## Before the oral: the deck lags behind the final deliverables

The deck was frozen on 17 Nov. On 18 Nov, `06_07_experiments_operations.md` and `08_launch_memo.md` changed the protocol and the decision. The jury reads both, so **say the deliverable numbers**, not the old ones on the slide (or update slides 8, 10 and 14 first):

| Slide | Still on the slide | Final (06_07, 08) |
|---|---|---|
| 8 · Proof | A/B on **tickets**, **4 weeks**, **393 / arm**, iterate 20–41 %, kill < 20 % | A/B on **specialist-days**, **~3,400 / arm (~6,800 tickets)**, **7 weeks + 7 days**; iterate 13–41.2 %, kill < 13 % |
| 10 · The ask | "Conditional GO for a 4-week pilot" | **NO-GO for live rollout · GO to prepare a controlled pilot** (gates 0–3); ask = approve Stage 1 |
| 10 · Who did what | Colin · [to fill] | Colin writes his own line (see slide 10) |
| 14 · Experiment (appendix) | unit = the ticket, 393 / arm | same as slide 8 |
| 4 · Validation | "the new 3-step flow" | still true: v0.9 is the same 3-step flow, also not user-tested |

---

## 1. FlowAssist — Lenny
*Data & AI Product · Final pitch*

**What this slide is about:** the promise in one line. FlowAssist is a copilot for payment-operations specialists at PayFlow B2B (course scenario).

**Say it:** "FlowAssist answers 'where is my money?' in minutes, with proof — and a person always decides. Ten slides, one per course step: we built it, we measured what we could, and we'll tell you exactly what we are asking for, and what we are not."

**Hand-over:** go straight into slide 2.

**In the code:** repo BenjaminAHS/project-product-management — start at README.md and spec.md. Live demo: deploy-project-product-management.vercel.app.

## 2. Specialists spend 40 % of every ticket searching. — Lenny
*01 · Problem · Course S1*

**What this slide is about:** the pain and its price — symptom → cause, and "doing nothing has a price".

**Say it:** "Meet Karim, Tier-1 specialist. On an 18-minute ticket he spends 7.2 minutes hunting through six tools — €415k of specialist time a year — and the merchant waits 4.5 hours to learn where the money is. The cause is not lazy people: payment data is split across services with no merchant view. And doing nothing isn't free: 25 % more volume means four more hires, €220k."

**Hand-over:** "Antoine will show you what we built about it."

**In the code / docs:** 01_problem_statement.md (problem sentence, persona, problem tree, do-nothing), governance.md S1. Figures are course scenario assumptions.

**If asked:** why AI and not rules? Macros cover ~15 %; fuzzy references and fees need matching — but a wrong match is worse than no draft, so it is a copilot, not an autopilot.

## 3. FlowAssist finds the payment and drafts the reply. The specialist decides. — Antoine
*02 · Solution · Course S1–S3*

**What this slide is about:** the agent's job in one sentence, and its trust level per step (L1 read, L3 scoped lookup, L2 draft, person-only send).

**Say it:** walk left to right. "It reads the request — money, legal or compliance go straight to a person. It finds the payment in this merchant's records only. It drafts a reply where every fact cites its record. And nothing leaves without a person." Stop on the bottom line: "It never sends on its own, never moves money, never shows another merchant's data, and never says 'received' when it's only 'sent'."

**Hand-over:** go to slide 4 — that last "never" came from users.

**In the code:** prototype/engine.js (browser preview) and flowassist/engine.py (server authority): classify() reads the request, analyze() finds the payment within the assigned merchant, make_draft()/source_records() draft with citations, evaluate_draft() checks. There is deliberately no send function: the app records a reply only after human approval (recordReply in prototype/app.js).

## 4. Users showed us what we couldn't see. — Antoine
*03 · Validation · Course S3*

**What this slide is about:** the design loop — users changed the design, not the threshold.

**Say it:** "2 of our 3 testers read the green 'sent to bank' as money received — the exact error we must prevent. So we changed the product: plain-language status in amber, a verified-facts checklist, and guidance on which record to open first. Now the honest part: only 1 of 3 finished unaided, and the course gate is 4 of 5. The guided 3-step flow you'll see in the demo is a design hypothesis — we retest it with 5 users before any pilot."

**Hand-over:** "Is it worth building? Benjamin."

**In the code:** D08 = STATUS map + plainStatus() in prototype/app.js ("Sent to recipient's bank · not yet received"); D09 = renderFacts() and #verified-facts in prototype/index.html; D10 = sourceGuide() in renderSources(). v0.8–v0.9 (three steps, outcome card, visible refusals) are not user findings: prototype/CHANGELOG.md. Evidence: 03_user_research.md.

## 5. We size the workload, not a market report. — Benjamin
*04 · Market · Course S2*

**What this slide is about:** bottom-up sizing of an internal product: tickets × share × eligible × time saved, net of costs.

**Say it:** "It's an internal tool, so the market is the workload: 144k tickets a year, half are payment tracing, three quarters of those are answerable — 54k tickets. At 48 % time saved that's €175k of specialist time a year, gross. Every input has a low, base and high with its source. The one number that decides everything is the 48 % — it's a guess, and the rest of the pitch is about testing it."

**Hand-over:** "Anthony will show you the product live."

**In the code / docs:** 02_sizing.xlsx (Inputs, Upside, Decision tabs), 02_investment_memo.md. The €175k is the full-scope gross value before costs.

## 6. Four fixed steps. A person decides. — Anthony (live demo)
*05 · Product · Course S4*

**What this slide is about:** the product beat = live demo + the architecture decoded (graded at the oral). Workflow, not agent: four fixed steps, all rung 1 (rules and templates), a trust level per step, human checkpoints ⊘ and one switch ⏻ with a named owner.

**Say it (15 s on the slide):** "Four fixed steps: a router, a scoped match, a cited draft, a policy check. Every path is drawn in advance and no model picks a tool — it's a workflow, not an agent. ⊘ marks where a person takes over; ⏻ is the switch, owned by the Head of Payment Ops." Then switch to the browser.

**Demo script (v0.9, open the link with `?demo` so the tour stays closed; ~2 min 30):**
1. **DEMO-01 · Where is my payment? — the happy path.** Step 1 "Check the payment": open the ledger, then the clearing record; point at the amber "Sent to recipient's bank · not yet received". Step 2: the cited reply is pre-filled with the verified facts beside it. Step 3: tick "I checked the facts and the wording", click **Approve & close · demo**. Show the outcome card: "nothing is sent from here — the specialist sends from the support inbox". Click **Next open ticket**.
2. **DEMO-05 · A USD transfer has failed — a refused edit.** Add "We will refund you next week." to the reply. The red notice quotes the sentence and the approval box is disabled before any server call. "And if someone bypasses the screen, the server refuses it anyway — HTTP 422." Click **Put FlowAssist's reply back**.
3. **DEMO-03 · Release the compliance hold — a person's job.** No draft: one clear card says why and what to do; the hand-over reason is already suggested. Preview, then **Confirm hand-over · demo**.
4. *If time allows:* **DEMO-02 · Two possible payments** — FlowAssist won't guess: both candidates are listed with reference, amount and status, so the specialist knows what to ask.

**Close the demo:** "Three tickets, three outcomes: drafted and approved, refused, handed over. In every case a person decided."

**Hand-over:** "Benjamin, is it worth it?"

**Backup:** if the network fails, the banner says "Assistant server unavailable · continue manually" and the page falls back to manual handling — that is the designed outage behaviour, say so. Keep the PDF screenshot on slide 6 as a fallback.

**In the code:** classify() and analyze() in flowassist/engine.py (mirrored in prototype/engine.js), make_draft()/source_records(), evaluate_draft() (code `commitment` for the refund sentence); api/index.py (/api/check, /api/handover); ASSIST_MODE in flowassist/flags.py; maybePrefill(), recordReply(), nextStepText() in prototype/app.js. Diagram: 04_architecture.md, spec.md §3.

## 7. Conditional GO: worth it above 41.2 % time saved. — Benjamin
*06 · Business case · Course S2 (includes the "alternatives" beat)*

**What this slide is about:** a number, an alternative, a threshold. EV €159.8k (pessimistic −€59.8k p 0.2, base €141.3k p 0.6, optimistic €434.9k p 0.2) vs do-nothing €57.6k vs the next-best project (self-serve portal) €125k.

**Say it:** start with the weakness. "The sheet's own headcount check gives €6.88 per ticket, not €10 — at that cost the base case falls under the hurdle. So we confirm the loaded cost first. With €10: €160k expected value, above the €125k portal and the €58k we get by doing nothing. It flips at 41.2 % time saved — that's our success criterion. And we orchestrate rather than build or buy: 4.35 vs 3.15 vs 2.15 on the course's ten questions."

**Hand-over:** "Colin: how we'll prove the 41.2 %."

**In the code / docs:** 02_sizing.xlsx Decision and Build-or-buy tabs; 02_investment_memo.md. The 41.2 % flip point is the success criterion in 03_product_brief.md §7 and spec.md §1.

## 8. Three promises, and how we'll prove them. — Colin
*07 · Proof · Course S5–S6*

**What this slide is about:** the two graded points: 3 business metrics with expected effects (S5) and an A/B protocol with a sample size (S6).

**Say it:** "Three promises. Active time per eligible ticket: 18 minutes down to 10.6 or less — that's the 41.2 %. Cost per eligible ticket: €10 down to €5.88. And QA must not move: 92 or more in every language. We prove it with an A/B on specialist-days: each specialist works some days assisted, some manual, in random order — tickets would leak, and 18 specialists give only 9 per arm. The primary needs ~600 tickets per arm, but the reopen guardrail needs much more: ~3,400 per arm, about 6,800 tickets, 7 weeks. The slowest guardrail sets the size, not the first good number. One read date, rule written before: ship at 41.2 % or more with every guardrail held, iterate between 13 and 41.2 %, kill below 13 %. We stop early only on harm."

⚠ The slide still shows the 17 Nov version (tickets, 4 weeks, 393 / arm, 20 % thresholds). Say the numbers above, which are the submitted 06_07, or update the slide.

**What's measured today (footnote):** 50/50 expected outcomes on development cases · 0 drafts on human-only tickets · 30/30 attacks blocked · 41/41 bad drafts flagged by the AI judge. Not yet: 100 held-out labels, second grader, judge ≥ 80 % (73 % today).

**Hand-over:** stay on — slide 9 is also yours.

**In the code:** handling time = activeTime() in prototype/app.js, sent as handling_ms on reply_recorded; make metrics → metrics/report.md (p50/p95 by language and plan). Full protocol: 06_07_experiments_operations.md §1–2; metrics: 05_metrics.md.

**If asked:** why 13 %? Below it FlowAssist loses to doing nothing (net value = €26.4k + €239.4k × saving). Plan B if we can't randomise: two weeks of shadow mode on real tickets, then before/after against a queue that stays manual.

## 9. One owner can stop it fast. — Colin
*08 · Risks · Course S7*

**What this slide is about:** adverse effects, monitoring and rollback (graded point).

**Say it:** "Three protections. The server says no: promises, invented amounts or another merchant's data are refused server-side, even if the screen is bypassed — you saw it in the demo. Counter-metrics: a pre-filled reply invites approval without reading, so we watch the edit rate and the 7-day reopen rate together; the harm threshold is FR or DE reopens above 1.5 × English for two weeks. And the switch: Air Canada 2024 taught that the company answers for its bot, so one owner — the Head of Payment Ops, on-call at night — moves FlowAssist to suggestions only or off in under 15 minutes, and the page falls back to manual work. We rehearsed it on 18 November: on → suggest-only → off → on."

**Hand-over:** "Lenny, the ask."

**In the code / docs:** /api/check → HTTP 422 (api/index.py, evaluate_draft() in flowassist/engine.py); ASSIST_MODE on | suggest_only | off in flowassist/flags.py (unknown → suggest_only); markServerDown() in prototype/app.js (fail-closed); rehearsal: scripts/verify/rehearse_switch.py and docs/evidence/s7/switch-rehearsal-2026-11-18.txt (local; staging rehearsal with both holders still to do); four layers with thresholds, clocks and owners in 06_07 §3 and docs/TRACKING_PLAN.md; release path .github/workflows/ci.yml (tests + attack set before every deploy).

## 10. The ask — Lenny, then everyone
*09 · The ask · Course S8*

**What this slide is about:** the decision we ask for, and who did what.

**Say it:** "Our decision: **no-go for live rollout, go to prepare a controlled pilot.** Today we know the workflow routes correctly and never drafts what a person must handle. We don't yet know that its replies are sendable at scale, that the judge is trustworthy, or that it saves 41.2 %. So we ask you to approve Stage 1: two weeks of shadow mode in staging on real data, with the second grader at 80 %, the loaded cost per ticket confirmed and Legal and the DPO on the scope. If the pilot then saves less than 41.2 % or breaks any guardrail, it stops — and the self-serve portal gets the team."

⚠ The slide title still says "Conditional GO for a 4-week pilot". Say the 08_launch_memo.md decision above, or update the title to match.

**Who did what — each person says their own line (5 × ~8 s):**
- **Lenny:** "Prototype engine and interface, spec v3, S1–S3 documents, S5–S8 first drafts."
- **Antoine:** "Architecture, user research and the prototype test, grader 1, switch owner, S5–S8 rework and the switch rehearsal."
- **Anthony:** "FastAPI server and global switch, attack set, LLM judge, CI/CD and deployment, interface v0.9, the pitch."
- **Benjamin:** "Sizing and investment memo, CI workflow, every pull-request review and merge."
- **Colin:** *[Colin: write your line before the oral — no commit of yours is on `main` yet, and the individual question is about a commit you signed.]*

**End on:** "We built it, we know what it can't prove yet, and we're asking for the step that will." Then stop talking.

**In the code / docs:** 08_launch_memo.md (decision, evidence table, gates 0–3 with signers, risks, ask, who did what); spec.md §11 open items. Final tag v1.0 before the first oral.

---

# Appendix (for questions, hidden when presenting)

## 11. A workflow you can draw, and a server that has the last word — Anthony
*Appendix · Architecture*

**What this slide is about:** four steps in a fixed workflow (router, routing rule, drafter, policy checker) and a server that re-checks every recorded action. A global switch can reduce the assistant to suggestions or turn it off.

**Say it:** "It is a workflow, not an agent: every path is drawn in advance, no model chooses a tool. The browser previews, the server decides."

**In the code:** prototype/engine.js = instant preview; flowassist/engine.py = the authority (same logic, kept identical by tests/test_parity.py: 123 cases, 468 draft checks). api/index.py (FastAPI on Vercel): /api/analyze, /api/check, /api/handover. Switch: flowassist/flags.py, env ASSIST_MODE. Browser client: prototype/server.js; fail-closed markServerDown() in prototype/app.js. Diagram: 04_architecture.md, spec.md §3.

**Course point (S4):** decode the architecture, human checkpoints ⊘ and one override switch ⏻ with an owner.

## 12. What we promise, and what must not break — Colin
*Appendix · Metrics*

**What this slide is about:** three business metrics with expected effects (18.0 → ≤ 10.6 min, €10 → ≤ €5.88, QA ≥ 92 unchanged as a stated non-effect), then what to protect: primary, guardrails, counter-metrics, reported per language, plan, rail and severity.

**Say it:** "The expected effects are derived from the S2 flip point, not measured. The reopen rate is the counter-metric, so we don't reward closing without solving — that's Goodhart. And we stopped improving the dev set at 50/50 because the metric no longer responds; the next point costs new labels, not engine work."

**In the code:** local metrics, no third-party analytics: track() in prototype/app.js → POST /api/events; flowassist/telemetry.py drops unknown keys and long text; make metrics → metrics/report.md. Event list and thresholds: docs/TRACKING_PLAN.md; stop criterion and hierarchy: 05_metrics.md.

**Course point (S5):** five-level stack; stop criterion; Goodhart; report by segment; harm threshold.

## 13. An LLM judge we checked before trusting — Anthony
*Appendix · AI judge*

**What this slide is about:** guideline v1.0 gave 53 % agreement with our human grader; the disagreements showed two ambiguities in our own rubric; after one fix (v1.1) agreement is 73 % (11/15) and the judge escalates 41/41 known-bad drafts with 0 over-accepted. The 4 remaining disagreements are a real defect the human missed: English messages answered in French or German (S5-M01).

**Say it:** "We read the disagreements, fixed the rubric once, re-measured — and the judge found a bug we had missed. 73 % is still below the 80 % bar, so we don't trust it alone yet: that's a Stage 0 gate."

**In the code:** evals/judge/rubric.md, evals/judge_prompt.txt, scripts/eval/judge.py (make judge; OpenAI gpt-6-luna, pinned). Results: evals/judge/judge_report.md (v1.1), evals/judge/judge_report_v1.0.md. Open defect: S5-M01 in spec.md.

**Course point (S5):** rubric first, human–human then human–judge agreement, fix once, re-measure.

## 14. How we would prove it caused the saving — Antoine
*Appendix · Experiment*

**What this slide is about:** the hypothesis sentence, the design chain (shadow → A/B → stepped rollout → 5 % holdout for 6 months) and the decision rule written before looking.

**Say it (final protocol, 06_07 §1–2):** "Unit = one specialist on one working day, randomised within specialist: tickets would leak — a specialist who sees drafts in the morning answers differently in the afternoon — and 18 specialists give 9 per arm. Size: MDE 13 % (below it we lose to doing nothing); ~600 per arm for time, ~2,210 for the reopen guardrail, × 1.54 for clustering → ~3,400 per arm, 7 weeks, read once at week 7 + 7 days. SD, reopen rate and ICC are assumptions we measure in two weeks of shadow mode, then freeze."

⚠ The slide still shows the ticket-level design (393 / arm, 3.6 min, 4 weeks).

**In the code:** ASSIST_MODE in flowassist/flags.py gives shadow-like operation (suggest_only); handling time per ticket via activeTime() → handling_ms. Per-specialist assignment is deliberately not coded before the protocol is signed (06_07 build note).

**Course point (S6):** randomise the right unit; size it and decide before; no peeking; pre-register segments; the four lies (peeking, novelty, post-hoc segments, Simpson).

## 15. We orchestrate: our rules and data, a rented model only where it earns its place — Benjamin
*Appendix · Build or buy*

**What this slide is about:** build, buy or orchestrate, scored on the course's ten questions: orchestrate 4.35, build 3.15, buy 2.15.

**Say it:** give the counter-argument yourself: "A vendor at €0.92 per resolution would cost ~€34k a year less at base volume; we pay that for data control and the ability to leave."

**In the code / docs:** 02_sizing.xlsx Build-or-buy tab. In the product, "orchestrate" means our own rules and data (flowassist/), with a rented model only where it earns its place: today only the offline judge (scripts/eval/judge.py).

**Course point (S2):** build/buy/orchestrate; the real competitor is the next-best project.
