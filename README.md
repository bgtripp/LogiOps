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

LogiOps uses LaunchDarkly for feature flag management. Flags are evaluated via
`logiops.feature_flags.is_enabled()`.

## Development

```bash
poetry install
poetry run pytest
```
