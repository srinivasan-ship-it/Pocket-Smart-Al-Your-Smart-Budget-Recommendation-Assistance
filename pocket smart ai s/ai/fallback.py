"""
Local fallback recommendation engine.

This module is used when:

- DEMO_MODE=true
- Gemini API key is missing
- Gemini API is temporarily unavailable
- Gemini returns an invalid response

The application therefore remains usable during development.
"""

from typing import Any, Dict, List


def _safe_budget(budget: float) -> float:
    """
    Make sure budget is positive.
    """

    try:
        budget = float(budget)
    except (TypeError, ValueError):
        return 0.0

    return max(budget, 0.0)


def _calculate_total(
    recommendations: List[Dict[str, Any]]
) -> float:
    """
    Calculate total estimated price.
    """

    total = 0.0

    for item in recommendations:
        price = item.get("estimated_price", 0)

        try:
            total += float(price)
        except (TypeError, ValueError):
            continue

    return round(total, 2)


# ---------------------------------------------------------
# HOME INTERIOR
# ---------------------------------------------------------

def fallback_home_recommendation(
    budget: float,
    room_type: str,
    style: str,
    priority: str = "balanced",
) -> Dict[str, Any]:
    """
    Generate a simple home interior plan without AI.
    """

    budget = _safe_budget(budget)

    # Basic percentage allocation
    furniture_budget = budget * 0.40
    lighting_budget = budget * 0.15
    decoration_budget = budget * 0.15
    storage_budget = budget * 0.15
    curtains_budget = budget * 0.10

    recommendations = [
        {
            "name": f"Main {room_type} furniture",
            "description": (
                f"Budget-friendly furniture suitable for a "
                f"{style} {room_type}."
            ),
            "estimated_price": round(
                furniture_budget,
                2,
            ),
            "category": "Furniture",
        },
        {
            "name": "LED lighting",
            "description": (
                "Energy-efficient lighting suitable for the room."
            ),
            "estimated_price": round(
                lighting_budget,
                2,
            ),
            "category": "Lighting",
        },
        {
            "name": "Wall and table decoration",
            "description": (
                f"Simple decorative elements matching the "
                f"{style} theme."
            ),
            "estimated_price": round(
                decoration_budget,
                2,
            ),
            "category": "Decoration",
        },
        {
            "name": "Storage solution",
            "description": (
                "Practical shelves or storage furniture "
                "for better organization."
            ),
            "estimated_price": round(
                storage_budget,
                2,
            ),
            "category": "Storage",
        },
        {
            "name": "Curtains",
            "description": (
                "Simple curtains that complement the selected style."
            ),
            "estimated_price": round(
                curtains_budget,
                2,
            ),
            "category": "Curtains",
        },
    ]

    total = _calculate_total(recommendations)

    savings = max(
        budget - total,
        0,
    )

    return {
        "planner_type": "home",
        "budget": budget,
        "summary": (
            f"A {style} {room_type} interior plan "
            f"focused on {priority} spending."
        ),
        "recommendations": recommendations,
        "total_estimated_cost": total,
        "savings": round(savings, 2),
        "tips": [
            "Compare prices from multiple stores before buying.",
            "Prioritize essential furniture first.",
            "Use LED lights to reduce electricity consumption.",
            "Choose multifunctional furniture when space is limited.",
            "Add decorative items gradually instead of buying everything at once.",
        ],
        "source": "Fallback",
    }


# ---------------------------------------------------------
# PARTY
# ---------------------------------------------------------

def fallback_party_recommendation(
    budget: float,
    guests: int,
    occasion: str,
    venue: str = "home",
    food_preference: str = "mixed",
) -> Dict[str, Any]:
    """
    Generate a simple party plan without AI.
    """

    budget = _safe_budget(budget)

    guests = max(
        int(guests),
        1,
    )

    food_budget = budget * 0.45
    decoration_budget = budget * 0.15
    venue_budget = budget * 0.15
    entertainment_budget = budget * 0.10
    miscellaneous_budget = budget * 0.15

    recommendations = [
        {
            "name": "Food and refreshments",
            "description": (
                f"Food plan for approximately {guests} guests "
                f"with {food_preference} preferences."
            ),
            "estimated_price": round(
                food_budget,
                2,
            ),
            "category": "Food",
        },
        {
            "name": "Party decorations",
            "description": (
                f"Simple decorations suitable for a {occasion}."
            ),
            "estimated_price": round(
                decoration_budget,
                2,
            ),
            "category": "Decoration",
        },
        {
            "name": "Venue",
            "description": (
                f"Budget allocation for the selected venue: {venue}."
            ),
            "estimated_price": round(
                venue_budget,
                2,
            ),
            "category": "Venue",
        },
        {
            "name": "Entertainment",
            "description": (
                "Simple entertainment such as music, games, "
                "or a small activity setup."
            ),
            "estimated_price": round(
                entertainment_budget,
                2,
            ),
            "category": "Entertainment",
        },
        {
            "name": "Miscellaneous",
            "description": (
                "Buffer for invitations, transportation, "
                "small purchases and unexpected costs."
            ),
            "estimated_price": round(
                miscellaneous_budget,
                2,
            ),
            "category": "Miscellaneous",
        },
    ]

    total = _calculate_total(
        recommendations
    )

    savings = max(
        budget - total,
        0,
    )

    per_person = round(
        total / guests,
        2,
    )

    return {
        "planner_type": "party",
        "budget": budget,
        "summary": (
            f"A {occasion} party plan for {guests} guests "
            f"using a {venue} venue. Estimated cost per guest "
            f"is ₹{per_person:,.2f}."
        ),
        "recommendations": recommendations,
        "total_estimated_cost": total,
        "savings": round(savings, 2),
        "tips": [
            "Prepare a guest list before finalizing food quantities.",
            "Choose a home venue when possible to reduce venue costs.",
            "Buy decorations in bulk.",
            "Compare catering options before booking.",
            "Keep a small amount of the budget for unexpected expenses.",
        ],
        "source": "Fallback",
    }


# ---------------------------------------------------------
# JEWELRY
# ---------------------------------------------------------

def fallback_jewelry_recommendation(
    budget: float,
    occasion: str,
    jewelry_type: str = "any",
    metal_preference: str = "any",
    style: str = "traditional",
) -> Dict[str, Any]:
    """
    Generate a simple jewelry recommendation without AI.
    """

    budget = _safe_budget(budget)

    # Allocation based on the user's total budget
    main_piece_budget = budget * 0.50
    earrings_budget = budget * 0.20
    bracelet_budget = budget * 0.15
    ring_budget = budget * 0.10
    reserve_budget = budget * 0.05

    main_name = (
        "Statement Necklace"
        if jewelry_type.lower() in ("any", "necklace")
        else f"Main {jewelry_type}"
    )

    recommendations = [
        {
            "name": main_name,
            "description": (
                f"A {style} main jewelry piece suitable "
                f"for {occasion}. Preferred metal: "
                f"{metal_preference}."
            ),
            "estimated_price": round(
                main_piece_budget,
                2,
            ),
            "category": "Main Jewelry",
        },
        {
            "name": "Matching Earrings",
            "description": (
                "Earrings selected to complement the main jewelry."
            ),
            "estimated_price": round(
                earrings_budget,
                2,
            ),
            "category": "Earrings",
        },
        {
            "name": "Bracelet",
            "description": (
                "A simple matching bracelet."
            ),
            "estimated_price": round(
                bracelet_budget,
                2,
            ),
            "category": "Bracelet",
        },
        {
            "name": "Ring",
            "description": (
                "A complementary ring within the remaining budget."
            ),
            "estimated_price": round(
                ring_budget,
                2,
            ),
            "category": "Ring",
        },
    ]

    total = _calculate_total(
        recommendations
    )

    savings = max(
        budget - total,
        0,
    )

    return {
        "planner_type": "jewelry",
        "budget": budget,
        "summary": (
            f"A {style} jewelry combination for {occasion}, "
            f"with a preference for {metal_preference}."
        ),
        "recommendations": recommendations,
        "total_estimated_cost": total,
        "savings": round(savings, 2),
        "tips": [
            "Compare making charges between different jewelers.",
            "Check the purity and weight before purchasing.",
            "Ask for a detailed bill.",
            "Compare the current metal price before buying.",
            "Keep some budget reserved for taxes and making charges.",
        ],
        "source": "Fallback",
    }