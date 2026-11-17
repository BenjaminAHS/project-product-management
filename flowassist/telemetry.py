"""Trace and product events. Never sends ticket, draft or note text.

Every request emits one JSON trace line on stdout (Vercel runtime logs keep
it): spans per pipeline step with their outcome and duration. Guardrail
decisions are also sent to PostHog when POSTHOG_PROJECT_KEY is set.
"""

from __future__ import annotations

import json
import os
import sys
import time
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

_client: Any = None
_client_ready = False


def posthog_client() -> Any:
    """Server PostHog client, or None when not configured (local, CI)."""
    global _client, _client_ready
    if _client_ready:
        return _client
    _client_ready = True
    key = os.environ.get("POSTHOG_PROJECT_KEY", "").strip()
    if not key:
        return None
    from posthog import Posthog

    _client = Posthog(
        key,
        host=os.environ.get("POSTHOG_HOST", "https://eu.i.posthog.com"),
        personal_api_key=os.environ.get("POSTHOG_PERSONAL_API_KEY") or None,
        sync_mode=True,  # serverless: send before the function freezes
        timeout=3,
        feature_flags_request_timeout_seconds=2,
    )
    return _client


def reset() -> None:
    global _client, _client_ready
    _client, _client_ready = None, False


def capture(event: str, distinct_id: str, properties: dict[str, Any]) -> None:
    client = posthog_client()
    if client is None:
        return
    try:
        client.capture(
            event,
            distinct_id=distinct_id,
            properties={**properties, "env": os.environ.get("FLOWASSIST_ENV", "demo"), "$process_person_profile": False},
        )
    except Exception:  # noqa: BLE001 - analytics must never break the request
        pass


class Trace:
    def __init__(self, route: str) -> None:
        self.trace_id = uuid.uuid4().hex
        self.route = route
        self.started = time.perf_counter()
        self.spans: list[dict[str, Any]] = []
        self.attributes: dict[str, Any] = {}

    @contextmanager
    def span(self, name: str, **attributes: Any) -> Iterator[dict[str, Any]]:
        record: dict[str, Any] = {"name": name, **attributes}
        start = time.perf_counter()
        try:
            yield record
        finally:
            record["ms"] = round((time.perf_counter() - start) * 1000, 2)
            self.spans.append(record)

    def emit(self, status: int) -> None:
        line = {
            "trace_id": self.trace_id,
            "route": self.route,
            "status": status,
            "ms": round((time.perf_counter() - self.started) * 1000, 2),
            **self.attributes,
            "spans": self.spans,
        }
        print(json.dumps(line, ensure_ascii=False), file=sys.stdout, flush=True)
