"""
Feature flag client — wraps Unleash SDK calls.

When ``UNLEASH_URL`` is set, flags are evaluated via the Unleash Python SDK
against a real Unleash instance.  Otherwise falls back to a static dict so
the service can run without an external dependency.
"""

from __future__ import annotations

import logging
import os
import threading

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Static fallback (used when UNLEASH_URL is not configured)
# ---------------------------------------------------------------------------
_FLAG_OVERRIDES: dict[str, bool] = {
    "show-redesigned-dashboard": True,      # Always-on for 95 days   -> STALE
    "use-v2-pricing-engine": False,         # Always-off for 100 days -> STALE
    "rollout-search-suggestions": True,     # Active 50% rollout      -> SKIP
    "enable-dark-mode": True,               # Turned on 10 days ago   -> SKIP (too recent)
}

# ---------------------------------------------------------------------------
# Unleash SDK client (lazy-initialised)
# ---------------------------------------------------------------------------
_UNSET = object()
_unleash_client = _UNSET  # type: ignore[assignment]
_init_lock = threading.Lock()


def _get_unleash_client():
    """Return the shared UnleashClient, initialising on first call.

    Uses double-checked locking to prevent duplicate SDK clients from
    leaking background threads when called concurrently.
    """
    global _unleash_client
    if _unleash_client is not _UNSET:
        return _unleash_client

    with _init_lock:
        # Re-check after acquiring lock
        if _unleash_client is not _UNSET:
            return _unleash_client

        unleash_url = os.getenv("UNLEASH_URL", "")
        if not unleash_url:
            _unleash_client = None
            return None

        from UnleashClient import UnleashClient  # noqa: N811

        api_url = f"{unleash_url}/api"
        api_token = os.getenv(
            "UNLEASH_CLIENT_TOKEN",
            "default:development.unleash-insecure-client-api-token",
        )
        app_name = os.getenv("UNLEASH_APP_NAME", "logiops")

        client = UnleashClient(
            url=api_url,
            app_name=app_name,
            custom_headers={"Authorization": api_token},
        )
        client.initialize_client()
        _unleash_client = client
        logger.info("Unleash client initialised: %s", api_url)
        return _unleash_client


def is_enabled(flag_key: str, default: bool = False) -> bool:
    """Return whether *flag_key* is enabled.

    Uses the Unleash SDK when available, otherwise falls back to the
    static ``_FLAG_OVERRIDES`` dict.
    """
    client = _get_unleash_client()
    if client is not None:
        return client.is_enabled(flag_key, fallback_function=lambda feature_name, context: default)
    return _FLAG_OVERRIDES.get(flag_key, default)
