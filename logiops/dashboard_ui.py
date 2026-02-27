"""Dashboard UI module."""


def get_dashboard_layout() -> dict:
    """Return the dashboard layout configuration."""
    return {
        "layout": "grid",
        "widgets": ["revenue-chart", "active-users", "conversion-funnel", "alerts"],
        "sidebar": True,
        "theme": "modern",
    }


def render_widget(widget_name: str) -> str:
    """Render a single dashboard widget."""
    return f'<div class="widget widget--modern">{widget_name}</div>'
