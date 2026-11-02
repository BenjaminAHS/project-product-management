# 03 — Prototype link · FlowAssist

**Version:** v0.1 · 2 November 2026 · local S3 surface, synthetic data only.

- **Link:** [Open the prototype source](prototype/index.html). Download/clone the repository and open `prototype/index.html` in a browser; GitHub's file view shows source rather than executing HTML. No installation, account, API key or server is required.
- **Optional HTTP preview:** from repository root, run `python -m http.server 8000 --bind 127.0.0.1`, then open `http://127.0.0.1:8000/prototype/`. Stop with Ctrl-C.
- **Tool:** Codex-assisted HTML/CSS/JavaScript; Sites local-only workflow. Local artifact follows the assignment's repository deliverable; no hosted URL or production integration is claimed.
- **Time box:** designed as an under-one-hour surface exercise; actual elapsed build time was not instrumented and is not presented as a measurement.
- **Versions:** v0.1 has ready/ambiguous/compliance/access-denied cases, source inspection, review, editor insertion and context handover. v0.2/v0.3 await observed user feedback; no fabricated iteration history.

## The prompt used — the brief in three paragraphs

```text
Paragraph 1 — user and job:
Build a local clickable FlowAssist prototype for Karim, a Tier-1 PayFlow B2B payment operations specialist. Place it in an internal Zendesk-like inbox. He investigates a merchant's missing payment, checks transaction evidence, reviews a cited reply, and either places it in his human editor or escalates. Use fictional tickets and records only. This is a scripted S3 research surface, not a live bank or LLM implementation.

Paragraph 2 — screen and controls:
Show an assigned-ticket list, original message and human reply editor, plus a payment investigation sidebar with verified merchant, transaction, source IDs and timestamps, editable draft and source detail. Require source inspection and explicit review before Use draft in editor. Invalidate review after a draft edit and clear state on ticket selection. Add a handover reason, safe agent note, Escalate with context, Continue manually and Reset test. Show the handover packet locally. Make the page responsive, keyboard usable and explicit that no message is sent.

Paragraph 3 — routing and trust:
Include one grounded tracing example, an ambiguous two-candidate payment, a compliance-hold request and a denied foreign reference. Keep drafts suppressed for blocked cases and show no unauthorized source details. Explain context-only versus human-only in plain language. Retrieval candidates are L3, drafts L2, customer send person-only; no refunds, hold release, ledger writes or autonomous replies. Use synthetic data, no API calls, external assets or persistence. Keep all interactions local and label every simulation.
```

## Test walkthrough (facilitator only)
1. Start at DEMO-01: inspect CLE-100, distinguish sent-to-bank from beneficiary credit, review, insert into editor. Try editing a draft and observe that review resets.
2. Open DEMO-02: two authorized candidates, no draft. Choose “Ambiguous transaction”, optionally add safe notes, escalate and inspect preserved source IDs.
3. DEMO-03 routes compliance to a person. DEMO-04 exposes no transaction evidence. Switching tickets clears review/editor; reset restores DEMO-01.
4. Use the **unassisted task** in `03_user_research.md` with two participants; this walkthrough is not a completed test or an instruction to coach them.

## Verification and screenshot
The JavaScript parsed and passed 12 state/interaction assertions using the system JavaScript engine and a minimal DOM harness: approval needs source inspection; edits invalidate review; ambiguous/sensitive/denied tickets suppress draft; ticket selection clears editor; escalation requires a reason and preserves only authorized source IDs; reset restores safe state. This is not a rendering or accessibility browser test. CSV/HTML/link checks are separate structural checks.

**Screenshot: pending browser capture.** Browser automation is unavailable in this environment; no rendered screenshot is claimed. Open the local page, capture the initial workspace without personal information, save as `prototype/screenshot_v0_1.png`, and link it here after capture. Complete a visual/keyboard check on desktop and mobile before user tests. No model accuracy or 41.2% time saving has been measured.
