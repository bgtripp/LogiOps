# LogiOps

Internal logistics platform powering order management, pricing, dashboards, and search.

## Modules

| Module | Description |
|---|---|
| `checkout` | Multi-step order checkout with promo support |
| `pricing` | Tiered pricing engine for line items |
| `dashboard_ui` | Internal operations dashboard layout |
| `search` | Product/order search with suggestions |
| `settings` | User preferences and theming |

## Feature Flags

LogiOps uses [Unleash](https://github.com/Unleash/unleash) for feature flag management.
Flags are evaluated via `logiops.feature_flags.is_enabled()`, which uses the
Unleash Python SDK when `UNLEASH_URL` is set, or falls back to a static dict
for offline development.

### Local Unleash Setup

```bash
# Start Unleash + PostgreSQL
docker-compose up -d

# Unleash UI: http://localhost:4242
# Login: admin / unleash4all
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `UNLEASH_URL` | Unleash server URL | _(unset — uses static fallback)_ |
| `UNLEASH_CLIENT_TOKEN` | Unleash client API token | `default:development.unleash-insecure-client-api-token` |
| `UNLEASH_APP_NAME` | App name for SDK registration | `logiops` |

### Hosted Flag Service

The CodeCull demo uses a hosted flag service at:
`https://unleash-flag-service-ddyinhlr.fly.dev`

## Development

```bash
poetry install
poetry run pytest
```
