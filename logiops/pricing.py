"""Pricing engine — flat-rate with premium discount."""


def calculate_price(base_price: float, quantity: int, tier: str = "standard") -> float:
    """Calculate the final price for a line item."""
    if tier == "premium":
        return round(base_price * quantity * 0.85, 2)
    return round(base_price * quantity, 2)


def get_pricing_tier_info(tier: str) -> dict:
    """Return metadata about a pricing tier."""
    return {
        "tier": tier,
        "engine": "v1",
        "features": ["flat-rate", "premium-discount"],
    }
