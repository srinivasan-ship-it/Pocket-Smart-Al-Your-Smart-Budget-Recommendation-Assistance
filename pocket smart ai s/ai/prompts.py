
def build_home_prompt(
    budget: float,
    room_type: str,
    style: str,
    priority: str = "balanced",
    additional_requirements: str = "",
) -> str:
    """
    Build prompt for Home Interior Planner.
    """

    return f"""
{SYSTEM_INSTRUCTION}

You are now helping the user plan a home interior.

USER DETAILS:

Budget:
₹{budget:,.2f}

Room:
{room_type}

Preferred Style:
{style}

Priority:
{priority}

Additional Requirements:
{additional_requirements or "None"}

Create a practical home interior recommendation.

Return exactly this JSON structure:

{{
    "planner_type": "home",
    "budget": {budget},
    "summary": "Short summary of the recommended plan",
    "recommendations": [
        {{
            "name": "Item name",
            "description": "Short useful description",
            "estimated_price": 0,
            "category": "Furniture"
        }}
    ],
    "total_estimated_cost": 0,
    "savings": 0,
    "tips": [
        "Money saving tip"
    ]
}}

Include suitable categories such as:

- Furniture
- Lighting
- Decoration
- Storage
- Curtains
- Flooring
- Wall decoration

Keep the total estimated cost within the given budget.
"""


def build_party_prompt(
    budget: float,
    guests: int,
    occasion: str,
    venue: str = "home",
    food_preference: str = "mixed",
    additional_requirements: str = "",
) -> str:
    """
    Build prompt for Party Budget Planner.
    """

    return f"""
{SYSTEM_INSTRUCTION}

You are now helping the user plan a party.

USER DETAILS:

Budget:
₹{budget:,.2f}

Number of Guests:
{guests}

Occasion:
{occasion}

Venue:
{venue}

Food Preference:
{food_preference}

Additional Requirements:
{additional_requirements or "None"}

Create a complete party budget recommendation.

Consider:

- Food
- Drinks
- Decorations
- Venue
- Invitations
- Entertainment
- Photography
- Miscellaneous expenses

Return exactly this JSON structure:

{{
    "planner_type": "party",
    "budget": {budget},
    "summary": "Short summary of the party plan",
    "recommendations": [
        {{
            "name": "Expense or service",
            "description": "Short description",
            "estimated_price": 0,
            "category": "Food"
        }}
    ],
    "total_estimated_cost": 0,
    "savings": 0,
    "tips": [
        "Money saving tip"
    ]
}}

Keep the total estimated cost within the given budget.
"""


def build_jewelry_prompt(
    budget: float,
    occasion: str,
    jewelry_type: str = "any",
    metal_preference: str = "any",
    style: str = "traditional",
    additional_requirements: str = "",
) -> str:
    """
    Build prompt for Jewelry Planner.
    """

    return f"""
{SYSTEM_INSTRUCTION}

You are now helping the user choose jewelry according to
their occasion and budget.

USER DETAILS:

Budget:
₹{budget:,.2f}

Occasion:
{occasion}

Jewelry Type:
{jewelry_type}

Metal Preference:
{metal_preference}

Style:
{style}

Additional Requirements:
{additional_requirements or "None"}

Create a practical jewelry recommendation.

Consider:

- Necklace
- Earrings
- Bracelet
- Ring
- Chain
- Pendant
- Traditional jewelry
- Contemporary jewelry

Return exactly this JSON structure:

{{
    "planner_type": "jewelry",
    "budget": {budget},
    "summary": "Short summary of the jewelry recommendation",
    "recommendations": [
        {{
            "name": "Jewelry item",
            "description": "Short description",
            "estimated_price": 0,
            "category": "Necklace"
        }}
    ],
    "total_estimated_cost": 0,
    "savings": 0,
    "tips": [
        "Money saving tip"
    ]
}}

Keep the total estimated cost within the given budget.

Mention that jewelry prices can vary based on:
- metal purity
- weight
- gemstone
- making charges
- seller
- current market price
"""