"""The server enforces the rules even when the browser is bypassed."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.index import app
from flowassist import flags, telemetry
from tests.cases import demo_data

client = TestClient(app)
READY = next(t for t in demo_data()["tickets"] if t["key"] == "ready")


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.delenv("POSTHOG_PROJECT_KEY", raising=False)
    monkeypatch.delenv("ASSIST_MODE", raising=False)
    telemetry.reset()
    flags.reset_cache()
    yield
    telemetry.reset()
    flags.reset_cache()


def analyze(message: str | None = None, **extra):
    ticket = {**READY, **({"message": message} if message is not None else {})}
    return client.post("/api/analyze", json={"ticket": ticket, **extra})


def draft() -> str:
    return analyze().json()["draft"]


def test_health_and_config():
    assert client.get("/api/health").json()["status"] == "ok"
    config = client.get("/api/config").json()
    assert config["assist_mode"] == "on" and config["assist_mode_source"] == "env"


def test_analyze_returns_verified_draft():
    body = analyze().json()
    assert body["state"] == "draft_ready"
    assert body["transaction"] == "TX-100"
    assert [s["id"] for s in body["sources"]] == ["LED-100", "CLE-100"]


def test_client_cannot_inject_evidence():
    ticket = {**READY}
    response = client.post("/api/analyze", json={"ticket": ticket, "data": {"transactions": []}})
    assert response.status_code == 422  # unknown fields are rejected


def test_foreign_reference_returns_nothing():
    body = analyze("Where is BETA-PRIVATE?").json()
    assert body["state"] != "draft_ready" and body["sources"] == [] and body["draft"] is None


@pytest.mark.parametrize(
    "extra",
    [
        "We will credit back the amount next week.",
        "Nous vous rembourserons sous 3 jours.",
        "Your payment was definitely paid.",
        "See BETA-PRIVATE.",
    ],
)
def test_reply_with_forbidden_claim_is_refused(extra):
    response = client.post("/api/check", json={"ticket": READY, "text": f"{draft()} {extra}", "action": "reply"})
    assert response.status_code == 422
    assert response.json()["allowed"] is False


def test_canonical_reply_is_allowed():
    response = client.post("/api/check", json={"ticket": READY, "text": draft(), "action": "reply"})
    assert response.status_code == 200 and response.json()["passed"] is True


def test_edited_reply_needs_manual_review_but_is_allowed():
    response = client.post("/api/check", json={"ticket": READY, "text": f"{draft()} Thanks for your patience.", "action": "reply"})
    body = response.json()
    assert response.status_code == 200 and body["manual_review"] is True and body["passed"] is False


def test_reply_on_human_only_ticket_is_refused():
    ticket = {**READY, "message": "Please reimburse INV-DEMO"}
    response = client.post("/api/check", json={"ticket": ticket, "text": "Done.", "action": "reply"})
    assert response.status_code == 422 and "no_transaction" in response.json()["codes"]


@pytest.mark.parametrize("mode", ["suggest_only", "off"])
def test_global_switch_blocks_insertion(monkeypatch, mode):
    text = draft()
    monkeypatch.setenv("ASSIST_MODE", mode)
    flags.reset_cache()
    response = client.post("/api/check", json={"ticket": READY, "text": text, "action": "insert"})
    assert response.status_code == 409


def test_switch_off_withholds_drafts(monkeypatch):
    monkeypatch.setenv("ASSIST_MODE", "off")
    body = analyze().json()
    assert body["assist_mode"] == "off" and body["draft"] is None and body["state"] == "draft_ready"


def test_unknown_mode_fails_safe(monkeypatch):
    monkeypatch.setenv("ASSIST_MODE", "yolo")
    assert client.get("/api/config").json()["assist_mode"] == "suggest_only"


def test_posthog_failure_fails_safe(monkeypatch):
    class Broken:
        def get_feature_flag(self, *a, **k):
            raise RuntimeError("network")

    monkeypatch.setattr(telemetry, "posthog_client", lambda: Broken())
    assert flags.assist_mode() == ("suggest_only", "fail_safe")


def test_posthog_flag_drives_mode(monkeypatch):
    class Flag:
        def get_feature_flag(self, *a, **k):
            return "off"

    monkeypatch.setattr(telemetry, "posthog_client", lambda: Flag())
    assert flags.assist_mode() == ("off", "posthog")


def test_handover_requires_reason_and_redacts_note():
    bad = client.post("/api/handover", json={"ticket": READY, "reason": " ", "note": ""})
    assert bad.status_code == 422
    good = client.post("/api/handover", json={"ticket": READY, "reason": "Merchant asked for a person", "note": "password: hunter2"})
    packet = good.json()["packet"]
    assert "hunter2" not in packet["note"] and packet["queue"] == "Tier-2 payments"


def test_oversized_message_is_rejected():
    assert analyze("x" * 3001).status_code == 422
