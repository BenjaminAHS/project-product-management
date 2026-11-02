# 03 — User research · FlowAssist

**2 November 2026 · Ready-to-run protocol; no completed interviews or tests supplied.** The assignment explicitly prohibits invented quotes and observations. All slots below are unfilled records, not simulated research. Classmates may play roles if identified as such. AI helped prepare the guide, not participant evidence.

## Recruitment and consent
Recruit one current/former payment or support specialist and two people experienced with B2B tools; if unavailable, recruit three classmates in those roles. Use participant IDs only; request permission to take anonymised notes, avoid real merchant/payment information, and do not record audio by default. One interviewer and one note-taker; ask for the last actual experience before showing the solution. For role-play, supply a fictional prior incident and label every observation role-play; it is not evidence of workplace frequency.

## Who we talked to
| ID | Target role, no personal data | Real user or classmate in role? | Date / duration | Interviewer · note-taker | Status |
|---|---|---|---|---|---|
| I1 | Current/former payment/support specialist | To record | To record / 20 min planned | To assign | Not conducted |
| I2 | B2B tool user handling payment questions | To record | To record / 20 min planned | To assign | Not conducted |
| I3 | Support lead / B2B tool user handling escalations | To record | To record / 20 min planned | To assign | Not conducted |

## Interview guide — 20 minutes per conversation
- 0–2 min: role, context and consent; no solution pitch.
- 2–7 min: “Tell me about the last time you investigated a missing payment. What did you open first? What happened next?” Ask for steps and approximate active time, separating queue waiting from work.
- 7–11 min: “Where did the transaction reference come from? When were there multiple possible matches? What did you do then?” Ask about the actual most recent ambiguity.
- 11–15 min: “The last time a status was wrong or stale, how did you discover it? Who did you contact? What work did you repeat?”
- 15–18 min: “Show or describe the last handover without exposing customer data. What did you include? What did Tier-2 ask you for afterwards?”
- 18–20 min: “What workaround did you use? What did it cost in time? What deadline did you have?” Recap facts and check accuracy.

Never ask “Would you use an AI?”, “Do you like our idea?” or hypothetical willingness to pay. Do not turn a guess about time into a measurement. Ask whether participants want to add anything in their own words; do not solicit the desired quote.

## What we heard — evidence register
| Interview ID / note line | Verbatim quote or observed past behaviour | Context / source type | Brief section confirmed or contradicted | Proposed change |
|---|---|---|---|---|
| Not available | No conversation supplied | No evidence | None yet | None attributed to users |

For each I1–I3, record the last incident, tools in order, reported time, failure/handover, workaround and unexpected fact. Distinguish verbatim quote, paraphrase, observed action and interviewer inference. Ask participant to correct the recap; preserve anonymised notes for v2 evidence.

## Usability test — two users, one task, think aloud
**Prototype:** [local clickable inbox](prototype/index.html), instructions in `03_prototype_link.md`. Use I1 and I2 (record actual IDs). Reset before each test; do not show them a walkthrough. Suggested 20-minute session: 2 min instructions, up to 10 min task, 5 min retrospective, 3 min notes.

**Exact task:** “You are covering merchant M-ALPHA's support queue. A merchant asks about a €1,240 payment. Decide whether you can prepare a reply, check its source, and place an appropriate reply in the editor. Then open the ticket with two possible €500 payments and hand it over with the information the next specialist needs. Do not send any message.”

**Observer-only completion rubric:** first ticket: verify M-ALPHA/TX-100, inspect source CLE-100, distinguish sent-to-bank from beneficiary credited, explicitly review, transfer draft to editor. Second ticket: identify ambiguity, keep draft suppressed, provide a reason, and use escalation; do not choose an arbitrary transaction. All steps without hints = success. Stop at 10 min, log failure and then debrief. Record task time but do not equate mock-interface timing with full handling-time savings.

| Test | Participant / date | Finished without help? | Task time | Hesitation and expected behaviour | Evidence / brief change |
|---|---|---|---|---|---|
| U1 | To record | Not tested | Not measured | No observations yet | Pending |
| U2 | To record | Not tested | Not measured | No observations yet | Pending |

Observer prompts only: “Please keep thinking aloud.” After completion: “What did you expect here?” Log any assistance, wrong merchant choice, assumed settlement promise or attempted send.

## Desirability gate
- [ ] 2 of 2 finish the complete task without help.
- [ ] Past behaviours are documented from three 20-minute conversations (or explicit classmate role-play).
- [ ] At least one spontaneously identifies an urgent use occasion (“I want this before…” or equivalent, recorded accurately).
- [ ] Evidence changes the brief/out-of-scope list; the economic threshold stays 41.2%.

**Decision: gate pending; no user-validated GO.** Complete the records, update brief §9 with traceable evidence, then mark v2. If task completion fails, revise the surface and test again. User enthusiasm cannot establish the financial, legal or technical gates.
