# FlowAssist — one entry point for local work and CI.
# `make help` lists the targets. Python 3.12 + Node 20+ required.

PY ?= .venv/bin/python
PORT ?= 8000
URL ?= http://127.0.0.1:$(PORT)

.PHONY: help install dev test test-py test-js eval adversarial judge metrics lint fmt export-data check-data ci smoke

help: ## List the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

install: ## Create .venv and install runtime + dev dependencies
	python3.12 -m venv .venv || uv venv --python 3.12 .venv
	$(PY) -m pip install -q -r requirements-dev.txt || uv pip install -q --python $(PY) -r requirements-dev.txt

dev: ## Run the API and the prototype on $(URL); events go to metrics/events.jsonl
	FLOWASSIST_SERVE_STATIC=1 METRICS_FILE=metrics/events.jsonl $(PY) -m uvicorn api.index:app --reload --port $(PORT)

test: test-py test-js ## All unit, API, parity and interface tests

test-py: ## pytest: engine parity JS/Python, API guardrails, attacks
	$(PY) -m pytest

test-js: ## Node: interface workflow and labelling page
	node scripts/verify/test_app.cjs
	node scripts/verify/test_labeller.cjs

eval: ## Development regression: 50/50 states, artefact and hash checks
	node scripts/eval/eval_s4.cjs
	git diff --exit-code -- evals/v0/results_v0.json || (echo "evals/v0/results_v0.json changed: rerun and commit it"; exit 1)
	$(PY) scripts/verify/verify_s3.py
	$(PY) scripts/verify/verify_s4.py

adversarial: ## Attack set (OWASP LLM rows): any miss fails
	$(PY) scripts/eval/run_adversarial.py

judge: ## LLM-as-a-judge on the graded drafts (OPENAI_API_KEY in .env, model gpt-6-luna)
	$(PY) scripts/eval/judge.py

metrics: ## Pre-launch metrics report from metrics/events.jsonl → metrics/report.md
	$(PY) scripts/eval/metrics_report.py

lint: ## ruff checks
	$(PY) -m ruff check flowassist api tests scripts/eval/run_adversarial.py scripts/eval/judge.py scripts/eval/metrics_report.py
	$(PY) -m ruff format --check flowassist api tests scripts/eval/run_adversarial.py scripts/eval/judge.py scripts/eval/metrics_report.py

fmt: ## Format Python code
	$(PY) -m ruff check --fix flowassist api tests scripts/eval/run_adversarial.py scripts/eval/judge.py scripts/eval/metrics_report.py
	$(PY) -m ruff format flowassist api tests scripts/eval/run_adversarial.py scripts/eval/judge.py scripts/eval/metrics_report.py

export-data: ## Regenerate flowassist/fixtures.json from prototype/data.js
	node scripts/eval/export_data.cjs

check-data:
	node scripts/eval/export_data.cjs --check

ci: lint check-data test eval adversarial ## Everything CI runs

smoke: ## Check a running or deployed instance: make smoke URL=https://...
	$(PY) scripts/verify/smoke.py $(URL)
