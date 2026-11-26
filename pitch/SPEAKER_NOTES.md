# FlowAssist — final pitch script

Friday 27 November 2026 · 8 minutes of pitch (hard stop), then 3 minutes of questions.
Files: [PPTX with notes](FlowAssist_Final_Pitch.pptx) · [PDF, 9 slides](FlowAssist_Final_Pitch.pdf) · [PDF with appendix](FlowAssist_Final_Pitch_with_appendix.pdf) · [demo video, 1:58](FlowAssist_Demo_Loom.mp4) (embedded in slide 5 of the PPTX, also [on Loom](https://www.loom.com/share/9daead1178a946f493772d29345e90f2)) · [older silent demo](FlowAssist_Demo.mp4) · live demo https://deploy-project-product-management.vercel.app/?demo

## Running order

| Slide | Speaker | Time | Clock at the end |
|---|---|---|---|
| 1 · Title | Lenny | 0:10 | 0:10 |
| 2 · Problem | Lenny | 0:35 | 0:45 |
| 3 · Solution | Antoine | 0:30 | 1:15 |
| 4 · What users changed | Antoine | 0:30 | 1:45 |
| 5 · Product + demo video | Colin | 2:15 | 4:00 |
| 6 · Business case | Benjamin | 0:45 | 4:45 |
| 7 · Three numbers, one test | Benjamin | 0:55 | 5:40 |
| 8 · What can go wrong | Benjamin | 0:35 | 6:15 |
| 9 · Decision and ask | Lenny | 0:40 | **6:55** |

About one minute of margin. The demo is a 1:58 video embedded in slide 5: it cannot be shortened, so everyone else keeps to their time. If the clock reads more than **1:55 when slide 5 starts**, Colin skips the sentence on the slide and plays the video straight away.

Slides 10–15 are hidden appendix slides for questions: in PowerPoint, type the slide number and press Enter to jump to one.

## Rules for the room

- Read the words below until you can say them without reading. Say them, don't read them from the screen.
- Hand over by name ("Antoine.") — no "so now I'll let…".
- Nobody adds to someone else's slide.
- Numbers exactly as written. If you forget one, say the sentence without it.

---

## 1 · Title — Lenny (0:10)

> Good morning. We are FlowAssist. We help payment specialists answer "where is my money?" in minutes, with proof — and a person always decides.

## 2 · Problem — Lenny (0:35)

> Meet Karim, a Tier-1 specialist at PayFlow. On an 18-minute ticket, he spends 7.2 minutes searching six tools for one payment. Across the team, that is €415k of specialist time a year — and the merchant waits four and a half hours.
>
> The cause is not the people: payment data is split across services, with no single view per merchant. And doing nothing has a price: 25 % more volume means four more hires, €220k a year.
>
> Antoine.

## 3 · Solution — Antoine (0:30)

> FlowAssist reads the request — money, legal or compliance goes straight to a person. It finds the payment in this merchant's records only, and drafts a reply where every fact cites its record. Nothing leaves without a person's approval.
>
> And it never sends on its own, never moves money, never shows another merchant's data, and never says "received" when the payment is only "sent" — a rule that came from users.

## 4 · What users changed — Antoine (0:30)

> We tested the prototype with three people. Two of three read our green "sent to bank" as money received — exactly the error we must prevent. So the status is now plain language in amber, with a checklist of verified facts.
>
> To be honest: only one of three finished unaided. The bar is four out of five, so we retest with five users before any pilot.
>
> Colin will show you the product.

## 5 · Product and demo video — Colin (2:15)

**On the slide (0:10):**

> Four fixed steps: a router, a scoped match, a cited draft, and a policy check on the server. A workflow, not an agent — and one switch turns it off. Here it is.

**Next click (or the clicker):** the video plays full screen (1:58, no sound). **Don't click again until it ends** — the next click goes to slide 6 and cuts the video. Say each line when the video reaches its time:

- **0:00** — A merchant asks where their 1,240 euros are. I open the ledger, then the clearing record.
- **0:13** — The status is in amber: sent to the bank, not yet received.
- **0:21** — The reply is already drafted, and every fact is checked against the records.
- **0:30** — I tick the box and approve. Nothing is sent from here: the specialist sends it from the support inbox.
- **0:41** — Next, a failed USD transfer. Same steps: two records, a cited draft.
- **0:57** — Now I replace the reply with a promise: "we will refund you next week". FlowAssist quotes it and blocks approval. If someone bypasses the screen, the server refuses it anyway.
- **1:17** — I put FlowAssist's reply back: that one can be approved.
- **1:25** — Last, a compliance hold. FlowAssist doesn't draft at all: it says why, and pre-fills the hand-over reason.
- **1:49** — I preview the hand-over and confirm it.

**When the video ends (back on slide 5):**

> Three tickets: approved, blocked, handed over. A person decided every time.
>
> Benjamin.

**If the video doesn't play:** open `FlowAssist_Demo_Loom.mp4` (same cut) or the Loom link https://www.loom.com/share/9daead1178a946f493772d29345e90f2 and say the same lines. The live app https://deploy-project-product-management.vercel.app/?demo stays open in Chrome for questions.

## 6 · Business case — Benjamin (0:45)

> Is it worth building? FlowAssist targets 54,000 of our 144,000 tickets a year. Across three scenarios, its expected value is €160k a year — more than the next-best project, a self-serve portal, at €125k, and doing nothing, at €58k.
>
> It only wins above 41.2 % of handling time saved. Our base case is 48 %, but that is a guess — so 41.2 % becomes our success criterion.
>
> One risk we name ourselves: at €6.88 per ticket instead of €10, the case falls below the hurdle. Finance confirms it first.
>
> So how do we prove it?

## 7 · Three numbers, one test — Benjamin (0:55)

> Three numbers. Active time per ticket: from 18 minutes to 10.6 or less — that is the 41.2 %. Cost per ticket: from €10 to €5.88 or less. And QA stays at 92 or more, in every language.
>
> To prove FlowAssist causes the saving, we run an A/B test on specialist-days: each specialist works some days with it and some without, in random order.
>
> The 7-day reopen rate sets the size: about 3,400 tickets per arm, seven weeks. We read it once, with the rule written before: ship at 41.2 % or more with every guardrail held, iterate between 13 and 41.2, kill below 13. We stop early only on harm.

## 8 · What can go wrong — Benjamin (0:35)

> What can go wrong? A wrong or foreign answer: the server refuses promises, invented amounts and another merchant's data — 30 out of 30 attacks blocked today.
>
> Rubber-stamping: we watch the edit rate and 7-day reopens per language. If French or German reopens exceed 1.5 times English for two weeks, that language drops to suggestions only.
>
> And anything we missed: the Head of Payment Operations switches it off in under 15 minutes. We rehearsed it on 18 November.
>
> Lenny.

## 9 · Decision and ask — Lenny (0:40)

> Our decision: no-go for a live rollout, go to prepare a controlled pilot.
>
> We know it routes correctly, never drafts what a person must handle, and can be stopped. We don't yet know that its replies are sendable at scale, that our AI judge is reliable — 73 % against an 80 % bar — or that it saves 41.2 %.
>
> So we ask for one step: approve Stage 1 — two weeks of shadow mode in staging, with no merchant exposed. If the pilot then misses 41.2 % or breaks a guardrail, it stops.
>
> Thank you.

Stay on slide 9 for the questions.

---

## Questions — 3 minutes, short and exact

One person answers, in two sentences at most. If an appendix slide helps, the person at the laptop jumps to it.

| Question | Who | Answer | Slide |
|---|---|---|---|
| Where is the AI? It looks like rules. | Anthony | On purpose: rules where a mistake costs money, a model only where it earns its place. Today the model is the offline AI judge; extraction and drafting move up a rung only if they beat the rules on the eval set. | 10, 14 |
| How do you know it saves time? | Benjamin | We don't yet: 48 % is a planning guess. The A/B on specialist-days is how we find out, and 41.2 % is the bar. | 7, 13 |
| Why is the kill threshold 13 %? | Benjamin | Below 13 %, FlowAssist is worth less than doing nothing (€58k a year). Finance sets that line, not us. | 13 |
| What if you can't randomise? | Benjamin | Two weeks of shadow mode on real tickets, then before/after against a queue that stays manual, with the confounders written down. | 13 |
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

- [ ] **Laptop 1 (presenting):** PPTX open in presenter view. In slide show, go to slide 5 and click once to check the video starts, then Esc. Chrome tab on https://deploy-project-product-management.vercel.app/?demo for questions; `FlowAssist_Demo_Loom.mp4` downloaded locally as a backup.
- [ ] **Laptop 2 (backup):** the PPTX and `FlowAssist_Demo_Loom.mp4`, downloaded locally, not only in the cloud.
- [ ] Notifications off, battery charged, HDMI / USB-C adapter in the bag.
- [ ] Phone charged: we grade the other teams in the Google Form during their questions.
- [ ] Connect our laptop while the team before us answers its questions.
- [ ] One full run-through with a stopwatch tonight, video included. Target 6:55.
