# 05 · Metrics — Team P2 · FlowAssist (payment-tracing copilot for PayFlow Tier-1)

> Session 5 deliverable. There are five sections, one per move of the session: place, stop, protect, derive, trust.
>
> **Number rule.** Every number below comes from `02_sizing.xlsx` (cited as *Sheet!Cell*), `02_investment_memo.md` (its derivation of the flip point from the workbook) or `evals/report_v0.md`. A few counts come from files already in the repo, and their path is given. Thresholds marked *decision* are choices the team made, not measurements.
>
> **Status, 17 Nov 2026: draft.** §1–§4 are complete. Three items in §5 need people and cannot be filled by an AI:
> - labels for 100 cases of `eval_set_v1.csv` (44 are in today);
> - a second human grader;
> - the human–human agreement rate.

## 1 · Place the number — the stack for FlowAssist

| Level | Question | Our metric | Value today | Produced by | Owner | Clock |
|---|---|---|---|---|---|---|
| 5 Business | Does it move the P&L? | Fully loaded cost per eligible tracing ticket | Baseline €10 (*Inputs!D9*); not measured with FlowAssist | Online A/B, then finance close | Head of Payment Operations | months |
| 4 Product | Does the specialist adopt it and get the job done? | Active handling time per eligible tracing ticket, closed with an approved reply | Baseline ~18 min (*Inputs!G9*). Paired active time not yet measured (*report_v0 §1*); instrumented as `handling_ms` on `reply_recorded` (`docs/TRACKING_PLAN.md`) | Online A/B; `make metrics` meanwhile | Head of Payment Operations (PM: Anthony) | weeks |
| 3 Guardrails & responsible AI | Does it stay inside the lines, for everyone? | Critical exposures: a draft on a human-only ticket, another merchant's data, or a missed attack | 0/13 drafts on human-only cases; 0/50 cases with another account's sources (*report_v0 §1*); 30 attack rows in `evals/adversarial_v0.csv`, 0 misses, run on every PR | Adversarial set + offline eval-set (CI) + `check_failed` monitoring | Antoine Rabeau (switch owner) until the pilot, then Head of Payment Operations | days |
| 2 AI system | Does the workflow complete the task? | **Replies two people would send without editing** | **Grader 1: 15/15 drafts = 15/50 cases** (*report_v0 §1*). Grader 2 pending, so not yet a two-grader number | Eval-set + two graders; LLM judge as a third reader | Antoine Rabeau (grader 1) | hours |
| 1 Model / component | Is each component right? | Expected route matched (router + match + policy check), per case | 50/50 on the development set after the fix; first run 37/50 (*report_v0 §1*). Routing alone not measured separately | Offline eval-set (`make eval`, every commit) | Lenny (engine) | seconds |

FlowAssist is a rung-1 workflow (rules and templates, no model choosing tools), so level 1 measures deterministic components rather than a model. "Retrieval hit@3" does not apply: lookup is by reference (*report_v0 §1*).

## 2 · Decide when to stop — the stop criterion

*"We stop improving **expected-route agreement on the development set** at **50/50**, because the level-2 number (replies sendable without editing) no longer responds: all 15 drafts already pass grader 1, and the 35/50 no-draft cases are mostly deliberate abstentions (13 human-only, plus ambiguity and blocks). The next point would cost **new labelled held-out cases** (`eval_set_v1.csv`), not engine work."*

- **Component metric and value:** expected route matched, 50/50 (*report_v0 §1*).
- **The level-above metric that stops responding:** replies sendable without editing. It is 15/15 on the drafts produced, so more route agreement on the same 50 cases cannot raise it. Those 50 are now development cases and cannot support a new claim (*report_v0 §4*).
- **Cost of the next point:**
  - labelling and grading the held-out set (evaluation line €22k/yr in the base case, *Decision!D10*);
  - every engine change re-runs the parity test and the regression.
- **The floor, not a stop (any miss blocks the release):**
  - zero drafts on human-only tickets;
  - zero data from another merchant;
  - zero misses on the attack set.

  These are the "zero critical exposures" gate of the memo (*02_investment_memo.md*). CI fails the PR on any miss.

## 3 · Choose what to protect — the hierarchy, by segment

| Kind | Metric | Numerator / denominator | Level | Lag | Source & owner |
|---|---|---|---|---|---|
| **Primary (1)** | Active handling time per eligible tracing ticket | Σ active time on eligible tickets closed with an approved reply / number of those tickets (median and p95) | 4 | same day | `reply_recorded.handling_ms` → `make metrics`; Head of Payment Operations |
| Guardrail | QA score on a weekly human sample of approved replies | Replies passing QA / replies sampled | 3 | weekly | QA lead; threshold **≥ 92 %** (*memo, report_v0 §1*) |
| Guardrail | Critical exposures | Drafts on human-only tickets + replies with another merchant's data + attack misses / all tickets | 3 | real time | CI attack set + `check_failed` events; Head of Payment Operations; threshold **0** (floor) |
| Guardrail | Match precision | Approved replies about the right transaction / approved replies checked | 2–3 | weekly | Human grading sample + LLM judge criterion 1; threshold **≥ 98 %** (*memo*). Each wrong answer costs ~€15 in rework (*Inputs!D30*) |
| Counter-metric | 7-day reopen rate | Approved replies reopened by the merchant within 7 days / approved replies | 4 | 7 days | Ticketing system; Head of Payment Operations |
| Counter-metric | Edit rate | Approved replies whose text differs from the pre-filled draft / approved replies | 4 | same day | `reply_recorded.edited` → `make metrics`; PM |

- **Segments reported** (the strata of the S3 audit and of `eval_set_v1.csv`):
  - merchant language (EN · FR · DE · other);
  - plan (SMB · Enterprise);
  - region;
  - rail (SEPA · SWIFT);
  - severity (routine · hard).
- **Fairness metric:** equal error rates across languages. QA pass rate and 7-day reopen rate are compared FR vs EN and DE vs EN.

  Why this matters: our only disagreements with the LLM judge were a language defect that grader 1 missed. English merchants received replies in French or German (F22, F23, F25, F26; spec line S5-M01, *report_v0 §6*).
- **Harm threshold** (*decision*; copied into `governance.md`): if the FR or DE 7-day reopen rate is above 1.5 × the EN rate for two weekly reads in a row, FlowAssist goes to suggestions-only for that language. The same applies if QA falls below 92 % in any language segment. Owner: Head of Payment Operations, who flips the switch (`ASSIST_MODE`).
- **How it could be gamed → the repair:**
  - **Gaming:** the primary rewards speed, so a specialist could approve the pre-filled reply without reading it.
  - **Repair:** an edit rate near zero together with a rising 7-day reopen rate flags rubber-stamping. The weekly QA sample over-samples unedited approvals. The approval itself stays one explicit human action: the system never ticks it (PR #3).

## 4 · Derive the business metrics — three, with expected effects (the oral)

The expected effect is the **flip point**: a 41.2 % saving of active time on eligible tracing work. That is the saving at which net value clears the €125k hurdle (*02_investment_memo.md*, from *Decision!D23* and *Decision!A31:F36*). The base-case guess is 48 % (*Inputs!D22*).

| Business metric | Baseline (`02_sizing.xlsx`) | Expected effect | Lag | Read date | It is a hypothesis about… |
|---|---|---|---|---|---|
| Active time per eligible tracing ticket | ~18 min (*Inputs!G9*) | ≤ 10.6 min (18 × (1 − 0.412)); base guess 9.4 min at 48 % | 1 week | week 4 of the A/B | a cited draft with verified facts replaces manual lookup in the ledger and clearing logs |
| Fully loaded cost per eligible tracing ticket | €10 (*Inputs!D9*) | ≤ €5.88 (10 × 0.588); base guess €5.20 | 1 month | month 2 | time saved turns into handling capacity, not idle time |
| QA score of approved replies | QA ≥ 92 % (*memo*) | **Non-effect: unchanged, ≥ 92 %.** Stop band: below 92 % on a weekly read stops the test | 1 week | weekly, from week 1 | speed does not cost correctness or tone |

**Eligible volume** (the denominator): 12,000 tickets/month (*Inputs!D6*) × 50 % tracing (*Inputs!D14*) × 75 % answerable from ledger and clearing (*Inputs!D18*) = 4,500 tickets/month.

**The tree** (component → AI system → product → business):

```
Router + match + policy check right            (L1: 50/50 dev, report_v0)
  └─> drafts sendable without editing          (L2: 15/15 drafts, grader 1; two-grader pending)
        └─> pre-filled cited reply is used and approved
              └─> active time per eligible ticket −41.2 % (flip) … −48 % (base)    (L4)
                    └─> cost per eligible ticket €10 → ≤ €5.88                       (L5)
                          └─> net annual value €141k base year 1 (Decision!D17),
                              clears the €125k hurdle only above the flip point
   guarded by: QA ≥ 92 % (non-effect) · 0 critical exposures · match precision ≥ 98 %
   watched by: 7-day reopen · edit rate, per language segment
```

## 5 · Make the judge trustworthy — the evaluation plan

- **Eval-set v1** (`evals/eval_set_v1.csv`):
  - 200 synthetic inputs, stratified by language, plan, region, rail and severity, all tagged "AI-generated synthetic input".
  - **Labels: 44/200 submitted** (Lenny, V001–V040 and V197–V200, AI-proposed and accepted, disclosed; see `evals/v1/submissions/README.md`). **To do (people): at least 100 labelled by a person** before the freeze.
  - Golden set: 30 rows that never change, to pick from the labelled rows across all strata (**to do**).
  - The v0 set (50) stays a development regression only (*report_v0 §4*).
- **Grading guideline:** `evals/README.md` (v1.1). It has four binary criteria (right payment, no invented fact, no promise or action, sendable as is) and one verdict (`sendable` · `needs_edit` · `escalate`), with boundary examples. It was written before grading.
- **Human–human agreement: pending.** Grader 1 (Antoine) has graded; grader 2 must grade the same 30 rows independently. `scripts/labelling/merge_grades_v0.py` computes the rate. **To do (people).**
- **Judge:**
  - OpenAI `gpt-6-luna`, with a prompt identical to the guideline (`evals/judge_prompt.txt`, run by `make judge`).
  - Human–judge agreement: **11/15 = 73 %** with grader 1. This is partial: it uses the same 15 cases we read to fix the guideline once (v1.0 → v1.1 on 17 Nov 2026; v1.0 scored 8/15).
  - Known-bad drafts escalated: **41/41**, 0 over-accepted (*report_v0 §6*).
  - Shared-model bias: none. The drafter is templates, not an LLM, so judge and drafter do not share a model family.
  - Known judge bias found: none yet. Its 4 remaining disagreements were a real defect that grader 1 missed (reply language; S5-M01).
- **Cadence:**
  - eval-set and attack set on every change (CI);
  - judge on every engine or template change;
  - a human re-grades a random 5 % of judged replies plus every human–judge disagreement, weekly.
- **Red rows (optional):** `evals/adversarial_v0.csv` has 30 attacks (OWASP LLM01, LLM02, LLM06, LLM09, plus legal and specialist-route rows) with 0 misses, and CI fails on any miss. Our own variant of the "assertions on every commit" idea is the parity test plus the regression, instead of promptfoo.
