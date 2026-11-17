# Tracking plan — FlowAssist (pre-launch baseline)

What we measure before launch, where each event comes from, and which course
metric it feeds (S5 five-level stack, S7 four monitoring layers). PostHog EU,
project `FlowAssist`; every event carries `env` (`demo` until a pilot).

**Privacy rule:** no event carries ticket, draft, note or reply text, nor any
amount or reference. Autocapture and session recording are off; persistence is
in memory only. Segments are coarse (language, plan, rail).

## Events

| Event | Sent from | Key properties | Course metric (level / layer) |
|---|---|---|---|
| `ticket_opened` | browser | `language`, `plan`, `rail`, `state`, `gate`, `intent`, `assist_mode` | volume; draft-ready rate by segment (L2 AI system) |
| `source_inspected` | browser | `source_kind` (ledger/clearing), `order` | D10: is the ledger opened first? (L4 product) |
| `draft_used` | browser, after server `/api/check` | segment props | draft acceptance (L4 product) |
| `reply_recorded` | browser, after server `/api/check` | `handling_ms`, `sources_checked`, `edited`, `manual_review`, segment | active handling time vs the 41.2 % flip point (L4→L5); edit rate |
| `handover_recorded` | browser, after server `/api/handover` | `queue`, `reason`, segment | escalation rate (L4) |
| `manual_mode_toggled` | browser | `to`, segment | per-ticket switch use (L3 guardrails) |
| `api_unavailable` | browser | `endpoint` | infrastructure layer (S7) |
| `guardrail_blocked` | server `/api/analyze` | `gate`, `layer` (input/scope/output), `intent`, segment | guardrail layer: blocks by reason (L3) |
| `check_failed` | server `/api/check` | `action` (insert/reply), `codes`, segment | attempted unsafe insert/reply; floor = 0 harmful sent (L3) |
| `$pageview` / `$pageleave` | browser | — | sessions |

Server traces: one JSON line per request in Vercel logs (`trace_id`, route,
status, latency, spans `analyze` / `evaluate_draft`, engine version, assist
mode). That is the S7 trace; PostHog holds the product view.

## Dashboards (PostHog)

1. **Funnel** `ticket_opened` → `source_inspected` → `draft_used` → `reply_recorded` (where value leaks).
2. **Guardrails** `guardrail_blocked` + `check_failed` by `gate` / `codes`, weekly (should be stable; a jump = drift).
3. **Handling time** p50/p95 of `handling_ms` by `language`, then `plan` (Simpson check: never the average alone).
4. **Escalation** `handover_recorded` / `ticket_opened` by queue.
5. **Switch & infra** share of `assist_mode`, count of `api_unavailable`.

## Feature flags

| Flag | Variants | Use |
|---|---|---|
| `assist-mode` | `on` / `suggest_only` / `off` | global override switch (S7). Server re-reads every 30 s; unknown or unreachable → `suggest_only`. |
| `copilot-ab` | `control` / `copilot` (0 % until the protocol is signed) | future A/B (S6): unit, sample size and decision rule in `06_07_experiments_operations.md` before any rollout. |

## Pre-launch thresholds (proposal for `05_metrics.md` / `06_07`)

| Layer | Metric | Pages someone when | Clock | Owner |
|---|---|---|---|---|
| Infrastructure | `api_unavailable`, p95 API latency (trace) | errors > 1 % for 10 min · p95 > 4 s | real time | on-call engineer |
| Model quality | weekly human sample vs judge agreement | agreement < 80 % | weekly | PM |
| Product & guardrails | `check_failed` on `reply`, drafts on human-only tickets | any human-only draft · `check_failed` spike ×2 week on week | daily | Head of Payment Ops |
| Business | p50 `handling_ms` vs manual baseline, by segment | saving < 41.2 % on eligible tickets at read date | weekly/monthly | Head of Payment Ops + CFO |
