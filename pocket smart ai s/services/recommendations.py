from urllib.parse import quote_plus

from typing import Any


PLATFORM_SEARCH = {

    "Amazon":
        "https://www.amazon.in/s?k={q}",

    "Flipkart":
        "https://www.flipkart.com/search?q={q}",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q={q}",

    "Swiggy":
        "https://www.swiggy.com/search?query={q}",

    "Zomato":
        "https://www.zomato.com/chennai/search?q={q}",

    "OYO":
        "https://www.oyorooms.com/search?location={q}",
}


def search_url(
    platform: str,
    query: str
) -> str:

    template = PLATFORM_SEARCH.get(
        platform,
        PLATFORM_SEARCH["Amazon"]
    )

    return template.format(
        q=quote_plus(query)
    )


def home_fallback(
    data: dict[str, Any]
) -> dict:

    budget = float(
        data["budget"]
    )

    items = (
        data.get("items")
        or [
            "Lighting",
            "Ceiling Fan",
            "Storage",
            "Wall Decor"
        ]
    )

    number_of_items = len(items)

    per_item = (
        budget /
        max(number_of_items, 1)
    )

    recommendations = []

    platforms = [
        "IKEA",
        "Amazon",
        "Flipkart"
    ]

    for index, item in enumerate(items):

        price = round(
            min(
                per_item * 0.82,
                budget * 0.35
            ),
            2
        )

        platform = platforms[
            index % len(platforms)
        ]

        recommendations.append({

            "category":
                "Home Interior",

            "name":
                f"{data['style']} {item}",

            "description":
                (
                    f"Budget-friendly "
                    f"{item.lower()} "
                    f"suitable for a "
                    f"{data['room_type'].lower()}."
                ),

            "estimated_price":
                price,

            "platform":
                platform,

            "search_url":
                search_url(
                    platform,
                    item
                )
        })

    return {

        "planner":
            "Home",

        "budget":
            budget,

        "currency":
            "INR",

        "summary":
            (
                f"A {data['style']} "
                f"{data['room_type']} "
                f"plan for "
                f"₹{budget:,.0f}."
            ),

        "allocation": {

            "Furniture":
                round(
                    budget * 0.40,
                    2
                ),

            "Lighting":
                round(
                    budget * 0.15,
                    2
                ),

            "Decor":
                round(
                    budget * 0.20,
                    2
                ),

            "Storage":
                round(
                    budget * 0.15,
                    2
                ),

            "Buffer":
                round(
                    budget * 0.10,
                    2
                )
        },

        "recommendations":
            recommendations,

        "tips": [

            "Compare final prices and delivery charges before buying.",

            "Keep about 10% as a contingency buffer.",

            (
                "Use the platform links as "
                "search links; verify the "
                "actual listing before purchase."
            )
        ],

        "source":
            "deterministic_demo_fallback"
    }


def party_fallback(
    data: dict[str, Any]
) -> dict:

    budget = float(
        data["budget"]
    )

    guests = int(
        data["guests"]
    )

    event = data["event_type"]

    recommendations = [

        {

            "category":
                "Catering",

            "name":
                (
                    f"{event} menu package "
                    f"for {guests} guests"
                ),

            "description":
                (
                    "Compare local catering "
                    "and food-delivery options "
                    "within the food allocation."
                ),

            "estimated_price":
                round(
                    budget * 0.45,
                    2
                ),

            "platform":
                "Swiggy",

            "search_url":
                search_url(
                    "Swiggy",
                    f"{event} catering"
                )
        },

        {

            "category":
                "Venue",

            "name":
                f"{event} venue shortlist",

            "description":
                (
                    "Use the venue allocation "
                    "to compare local halls, "
                    "restaurants or stays."
                ),

            "estimated_price":
                round(
                    budget * 0.25,
                    2
                ),

            "platform":
                "OYO",

            "search_url":
                search_url(
                    "OYO",
                    data.get(
                        "city",
                        "Chennai"
                    )
                )
        },

        {

            "category":
                "Decoration",

            "name":
                f"{event} decoration kit",

            "description":
                (
                    "Simple theme decoration "
                    "suitable for the guest count."
                ),

            "estimated_price":
                round(
                    budget * 0.15,
                    2
                ),

            "platform":
                "Amazon",

            "search_url":
                search_url(
                    "Amazon",
                    f"{event} decoration"
                )
        },

        {

            "category":
                "Entertainment",

            "name":
                "Music / activity budget",

            "description":
                (
                    "Reserve this amount "
                    "for music, games or "
                    "a small entertainment service."
                ),

            "estimated_price":
                round(
                    budget * 0.10,
                    2
                ),

            "platform":
                "Zomato",

            "search_url":
                search_url(
                    "Zomato",
                    f"{event} party"
                )
        }
    ]

    return {

        "planner":
            "Party",

        "budget":
            budget,

        "currency":
            "INR",

        "summary":
            (
                f"A {event} plan "
                f"for {guests} guests "
                f"with a controlled "
                f"₹{budget:,.0f} budget."
            ),

        "allocation": {

            "Catering":
                round(
                    budget * 0.45,
                    2
                ),

            "Venue":
                round(
                    budget * 0.25,
                    2
                ),

            "Decoration":
                round(
                    budget * 0.15,
                    2
                ),

            "Entertainment":
                round(
                    budget * 0.10,
                    2
                ),

            "Emergency":
                round(
                    budget * 0.05,
                    2
                )
        },

        "recommendations":
            recommendations,

        "tips": [

            "Confirm per-person food pricing and taxes.",

            (
                "Book the venue before spending "
                "heavily on decoration."
            ),

            (
                "Keep the emergency allocation "
                "untouched until final payments."
            )
        ],

        "source":
            "deterministic_demo_fallback"
    }


def jewelry_fallback(
    data: dict[str, Any]
) -> dict:

    budget = float(
        data["budget"]
    )

    style = data["style"]

    occasion = data["occasion"]

    color = data["outfit_color"]

    pieces = [

        ("Earrings", 0.35),

        ("Necklace", 0.40),

        ("Bangle / Bracelet", 0.15)
    ]

    recommendations = []

    for name, fraction in pieces:

        price = round(
            budget * fraction,
            2
        )

        query = (
            f"{style} "
            f"{name} "
            f"{color} "
            f"{occasion}"
        )

        platform = (
            "Amazon"
            if name != "Necklace"
            else "Flipkart"
        )

        recommendations.append({

            "category":
                "Jewelry",

            "name":
                f"{style} {name}",

            "description":
                (
                    f"Suggested for "
                    f"{occasion} with a "
                    f"{color} outfit."
                ),

            "estimated_price":
                price,

            "platform":
                platform,

            "search_url":
                search_url(
                    platform,
                    query
                )
        })

    return {

        "planner":
            "Jewelry",

        "budget":
            budget,

        "currency":
            "INR",

        "summary":
            (
                f"{style} jewelry ideas "
                f"for a {occasion}, "
                f"coordinated with {color}."
            ),

        "allocation": {

            "Necklace":
                round(
                    budget * 0.40,
                    2
                ),

            "Earrings":
                round(
                    budget * 0.35,
                    2
                ),

            "Bracelet/Bangles":
                round(
                    budget * 0.15,
                    2
                ),

            "Buffer":
                round(
                    budget * 0.10,
                    2
                )
        },

        "recommendations":
            recommendations,

        "tips": [

            (
                "Match metal tone with "
                "the outfit and occasion."
            ),

            (
                "Check material, size, "
                "return policy and seller rating."
            ),

            (
                "For an uploaded outfit, "
                "use the AI result as styling "
                "guidance rather than a guarantee "
                "of color accuracy."
            )
        ],

        "source":
            "deterministic_demo_fallback"
    }