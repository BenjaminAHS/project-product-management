# FlowAssist — final pitch script

Friday 27 November 2026 · 8 minutes of pitch (hard stop), then 3 minutes of questions.
Files: [PPTX with notes](FlowAssist_Final_Pitch.pptx) · [PDF, 9 slides](FlowAssist_Final_Pitch.pdf) · [PDF with appendix](FlowAssist_Final_Pitch_with_appendix.pdf) · [demo video](FlowAssist_Demo.mp4) · live demo https://deploy-project-product-management.vercel.app/?demo

## Running order

| Slide | Speaker | Time | Clock at the end |
|---|---|---|---|
| 1 · Title | Lenny | 0:10 | 0:10 |
| 2 · Problem | Lenny | 0:45 | 0:55 |
| 3 · Solution | Antoine | 0:35 | 1:30 |
| 4 · What users changed | Antoine | 0:35 | 2:05 |
| 5 · Product + live demo | Anthony | 2:15 | 4:20 |
| 6 · Business case | Benjamin | 0:50 | 5:10 |
| 7 · Three numbers, one test | Colin | 1:05 | 6:15 |
| 8 · What can go wrong | Colin | 0:45 | 7:00 |
| 9 · Decision and ask | Lenny | 0:40 | **7:40** |

20 seconds of margin. If the clock reads more than **4:30 when Benjamin starts**, Colin skips the "not on tickets" sentence on slide 7 and Lenny skips the "we know / we don't know" sentence on slide 9.

Slides 10–15 are hidden appendix slides for questions: in PowerPoint, type the slide number and press Enter to jump to one.

## Rules for the room

- Read the words below until you can say them without reading. Say them, don't read them from the screen.
- Hand over by name ("Antoine.") — no "so now I'll let…".
- Nobody adds to someone else's slide.
- Numbers exactly as written. If you forget one, say the sentence without it.

---

## 1 · Title — Lenny (0:10)

> Good morning. We are FlowAssist. We help payment specialists answer one question — "where is my money?" — in minutes, with proof. And a person always decides.

## 2 · Problem — Lenny (0:45)

> Meet Karim, a Tier-1 specialist at PayFlow. A merchant asks where a payment is. On an 18-minute ticket, Karim spends 7.2 minutes searching through six tools. Across the team, that is €415k of specialist time a year — and the merchant waits four and a half hours for an answer.
>
> The cause is not the people. Payment data is split across services, with no single view per merchant.
>
> And doing nothing has a price: if volume grows 25 %, we need four more hires — €220k a year.
>
> Antoine.

## 3 · Solution — Antoine (0:35)

> FlowAssist does four things. It reads the request — anything about money, legal or compliance goes straight to a person. It finds the payment, in this merchant's records only. It drafts a reply where every fact cites its record. And nothing leaves without a person's approval.
>
> Just as important is what it never does: it never sends on its own, never moves money, never shows another merchant's data, and never says "received" when the payment is only "sent". That last rule came from users.

## 4 · What users changed — Antoine (0:35)

> We tested the prototype with three people. Two of three read our green "sent to bank" as money received — exactly the error we must prevent. So we changed the product: a plain-language status in amber, a checklist of verified facts, and guidance on which record to open first.
>
> To be honest: only one of three finished unaided. The bar is four out of five, so we retest the new flow with five users before any pilot.
>
> Anthony will show you the product.

## 5 · Product and live demo — Anthony (2:15)

**On the slide (0:15):**

> Under the hood, four fixed steps: a router, a scoped match, a cited draft, and a policy check on the server. Every path is drawn in advance — it is a workflow, not an agent. And one switch, owned by the Head of Payment Operations, turns it to suggestions or off.

**Switch to the browser** (tab already open on `…/?demo`). **2:00:**

1. **DEMO-01 · Where is my payment? (0:55)**
   > A merchant asks where their 1,240 euros are. I open the ledger, then the clearing record. The status is in amber: sent to the recipient's bank, not yet received. The reply is already drafted, with the verified facts next to it. I check them, tick the box, and approve. Nothing is sent from here: the specialist sends it from the support inbox.

   Click **DEMO-05** in the inbox list on the left (not "Next open ticket": that button goes to DEMO-02).
2. **DEMO-05 · A USD transfer has failed (0:35)**: open the two source records (the reply fills in once both are open), then type *"We will refund you next week."* at the end of the reply.
   > Now I try to make a promise we can't keep. FlowAssist quotes the sentence and blocks approval. And if someone bypasses the screen, the server refuses it anyway.

   Click **Put FlowAssist's reply back**.
3. **DEMO-03 · Release the compliance hold (0:25)**
   > A compliance hold. FlowAssist doesn't draft at all: it says why, and pre-fills the hand-over reason. I confirm the hand-over.

   Click **Confirm hand-over · demo**.

**Back to the slides:**

> Three tickets, three outcomes: approved, refused, handed over. A person decided every time.
>
> Benjamin.

**If the demo breaks:** say "Here is the same flow on video", play `FlowAssist_Demo.mp4` (1:56, no sound, same three tickets in the same order) and narrate the same lines over it. If the page shows "Assistant server unavailable · continue manually", that is the designed outage behaviour: say so in one sentence, then play the video.

## 6 · Business case — Benjamin (0:50)

> Is it worth building? FlowAssist targets 54,000 of our 144,000 tickets a year: the payment-tracing tickets it can answer. Across three scenarios, its expected value is €160k a year. That beats the next-best project, a self-serve portal, at €125k — and doing nothing, at €58k.
>
> It only wins above 41.2 % of handling time saved. Our base case is 48 %, but that is a guess — so 41.2 % becomes our success criterion.
>
> One risk we name ourselves: if the real cost per ticket is €6.88 instead of €10, the case falls below the hurdle. Finance confirms it first.
>
> Colin — how do we prove it?

## 7 · Three numbers, one test — Colin (1:05)

> Three numbers. Active time per ticket: from 18 minutes to 10.6 or less — that is the 41.2 %. Cost per ticket: from €10 to €5.88 or less. And quality must not drop: QA stays at 92 or more, in every language.
>
> To prove that FlowAssist causes the saving, we run an A/B test on specialist-days: each specialist works some days with FlowAssist and some days without, in random order. Not on tickets — a specialist who sees drafts in the morning answers differently in the afternoon.
>
> The size is set by the slowest guardrail, the 7-day reopen rate: about 3,400 tickets per arm, 6,800 in total, seven weeks. We read it once, with the rule written before: ship at 41.2 % or more with every guardrail held, iterate between 13 and 41.2, kill below 13. We stop early only on harm — never on a good number.

## 8 · What can go wrong — Colin (0:45)

> What can go wrong? Three things.
>
> A wrong or foreign answer: the server refuses promises, invented amounts and another merchant's data — even if someone bypasses the screen. Today, 30 out of 30 attacks are blocked.
>
> Rubber-stamping: a pre-filled reply invites approval without reading. So we watch the edit rate and the 7-day reopens, per language. If French or German reopens exceed 1.5 times English for two weeks, that language drops to suggestions only.
>
> And anything we missed: one owner, the Head of Payment Operations, switches it to suggestions or off in under 15 minutes. We rehearsed it on 18 November.
>
> Lenny.

## 9 · Decision and ask — Lenny (0:40)

> Our decision: no-go for a live rollout, go to prepare a controlled pilot.
>
> We know it routes correctly, never drafts what a person must handle, and can be stopped. We don't yet know that its replies are sendable at scale, that our AI judge is reliable — 73 % against an 80 % bar — or that it saves 41.2 %.
>
> So we ask for one step: approve Stage 1 — two weeks of shadow mode in staging, on real data, with no merchant exposed. If the pilot then misses 41.2 % or breaks a guardrail, it stops, and the portal gets the team.
>
> Thank you.

Stay on slide 9 for the questions.

---

## Questions — 3 minutes, short and exact

One person answers, in two sentences at most. If an appendix slide helps, the person at the laptop jumps to it.

| Question | Who | Answer | Slide |
|---|---|---|---|
| Where is the AI? It looks like rules. | Anthony | On purpose: rules where a mistake costs money, a model only where it earns its place. Today the model is the offline AI judge; extraction and drafting move up a rung only if they beat the rules on the eval set. | 10, 14 |
| How do you know it saves time? | Colin | We don't yet: 48 % is a planning guess. The A/B on specialist-days is how we find out, and 41.2 % is the bar. | 7, 13 |
| Why is the kill threshold 13 %? | Colin | Below 13 %, FlowAssist is worth less than doing nothing (€58k a year). Finance sets that line, not us. | 13 |
| What if you can't randomise? | Colin | Two weeks of shadow mode on real tickets, then before/after against a queue that stays manual, with the confounders written down. | 13 |
| €6.88 or €10 per ticket? | Benjamin | The sheet's headcount check gives €6.88; at that cost the base case falls below the €125k hurdle. Finance confirms the loaded cost before the pilot — it is a gate. | 6 |
| Why not buy a vendor? | Benjamin | A vendor at €0.92 per resolution is about €34k a year cheaper. We pay that for control of the data and the ability to leave: orchestrate scored 4.35, build 3.15, buy 2.15. | 14 |
| Can you trust the AI judge? | Anthony | Not alone yet: 73 % agreement with our human grader, the bar is 80 %. It already escalated 41 of 41 bad drafts and found a defect we had missed — replies in the wrong language. | 12 |
| What if it shows another merchant's data? | Anthony | It can't by design: the match only searches the assigned merchant, and the server re-checks every action. One occurrence is a critical exposure: assistance off, DPO informed. | 8, 10 |
| Who presses the switch? | Antoine | Today me, as the named owner. In a pilot, the Head of Payment Operations by day and the on-call engineer by night — never only the person who wrote the code. | 8 |
| Only three users? | Antoine | Yes, and we say it: 1 of 3 finished unaided. We retest with five before any pilot; the bar is 4 of 5. | 4 |
| What about personal data? | Lenny | No ticket or draft text in the logs, no third-party analytics, 30-day retention pending the DPO's approval. The DPO signs Stage 1. | 15 |
| What would make you stop? | Lenny | One critical exposure stops it the same day. Otherwise below 13 % saved, or any guardrail broken, at the read date. | 7, 15 |
| What did you personally do? | Each person | Your own line, in one sentence, from `08_launch_memo.md` → Who did what. | — |

---

## Before 9:00 on Friday

- [ ] **Laptop 1 (presenting):** PPTX open in presenter view; Chrome tab on https://deploy-project-product-management.vercel.app/?demo, zoom at 125 %; `FlowAssist_Demo.mp4` open in QuickTime and paused at 0:00.
- [ ] **Laptop 2 (backup):** the same three files, downloaded locally, not only in the cloud.
- [ ] Reload the demo tab just before our slot, so the tickets start fresh.
- [ ] Notifications off, battery charged, HDMI / USB-C adapter in the bag.
- [ ] Phone charged: we grade the other teams in the Google Form during their questions.
- [ ] Connect our laptop while the team before us answers its questions.
- [ ] One full run-through with a stopwatch tonight. Target 7:40.
