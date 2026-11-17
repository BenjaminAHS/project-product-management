"""Global assist-mode switch (the S7 override switch).

on            drafts can be inserted after the human checks
suggest_only  drafts are shown, never insertable (L1)
off           no draft at all: humans-only mode

Resolution: the PostHog feature flag `assist-mode` when PostHog is configured,
else the ASSIST_MODE environment variable (default "on"). If PostHog is
configured but cannot answer, the switch fails safe to suggest_only.
"""

from __future__ import annotations

import os
import time

from flowassist import telemetry

MODES = ("on", "suggest_only", "off")
FLAG_KEY = "assist-mode"
CACHE_SECONDS = 30
_cache: dict[str, tuple[float, str, str]] = {}


def _env_mode() -> str:
    mode = os.environ.get("ASSIST_MODE", "on").strip().lower()
    return mode if mode in MODES else "suggest_only"


def assist_mode() -> tuple[str, str]:
    """Return (mode, source). Cached for CACHE_SECONDS."""
    cached = _cache.get("mode")
    if cached and time.monotonic() - cached[0] < CACHE_SECONDS:
        return cached[1], cached[2]
    client = telemetry.posthog_client()
    if client is None:
        mode, source = _env_mode(), "env"
    else:
        try:
            value = client.get_feature_flag(FLAG_KEY, "flowassist-server")
        except Exception:  # noqa: BLE001 - any flag failure must fail safe
            value = None
        if isinstance(value, str) and value in MODES:
            mode, source = value, "posthog"
        else:
            mode, source = "suggest_only", "fail_safe"
    _cache["mode"] = (time.monotonic(), mode, source)
    return mode, source


def reset_cache() -> None:
    _cache.clear()
