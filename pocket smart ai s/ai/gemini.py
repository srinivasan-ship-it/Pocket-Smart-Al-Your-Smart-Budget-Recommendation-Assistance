"""
Gemini AI integration for PocketSmart AI.

The application can work in two modes:

1. AI MODE
   Uses Google's Gemini API when GEMINI_API_KEY is configured.

2. DEMO/FALLBACK MODE
   Uses the local recommendation engine when Gemini is unavailable.
"""

import json
import re
from typing import Any, Dict, Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

from app.config import settings
from app.ai.prompts import (
    build_home_prompt,
    build_party_prompt,
    build_jewelry_prompt,
)
from app.ai.fallback import (
    fallback_home_recommendation,
    fallback_party_recommendation,
    fallback_jewelry_recommendation,
)


def _extract_json(text: str) -> Dict[str, Any]:
    """
    Extract JSON from Gemini's response.

    Gemini normally returns JSON when requested, but this function
    also handles responses surrounded by markdown code fences.
    """

    if not text:
        raise ValueError("Empty response received from Gemini.")

    text = text.strip()

    # Remove ```json ... ``` blocks
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find the first JSON object in the response.
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError(
            "Gemini response does not contain valid JSON."
        )

    json_text = text[start:end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Unable to parse Gemini JSON response."
        ) from exc


def _generate_with_gemini(prompt: str) -> Dict[str, Any]:
    """
    Send a prompt to Gemini and return a Python dictionary.
    """

    if not settings.GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    if genai is None or types is None:
        raise RuntimeError(
            "google-genai is not installed. "
            "Run: pip install -r requirements.txt"
        )

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7,
            response_mime_type="application/json",
        ),
    )

    if not response or not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return _extract_json(response.text)


def generate_home_recommendation(
    budget: float,
    room_type: str,
    style: str,
    priority: str = "balanced",
    additional_requirements: str = "",
) -> Dict[str, Any]:
    """
    Generate Home Interior recommendations.
    """

    prompt = build_home_prompt(
        budget=budget,
        room_type=room_type,
        style=style,
        priority=priority,
        additional_requirements=additional_requirements,
    )

    if settings.DEMO_MODE:
        return fallback_home_recommendation(
            budget=budget,
            room_type=room_type,
            style=style,
            priority=priority,
        )

    try:
        result = _generate_with_gemini(prompt)
        result["source"] = "Gemini AI"
        return result

    except Exception as exc:
        print(
            f"[Gemini] Home recommendation failed: {exc}"
        )

        result = fallback_home_recommendation(
            budget=budget,
            room_type=room_type,
            style=style,
            priority=priority,
        )

        result["source"] = "Fallback"
        return result


def generate_party_recommendation(
    budget: float,
    guests: int,
    occasion: str,
    venue: str = "home",
    food_preference: str = "mixed",
    additional_requirements: str = "",
) -> Dict[str, Any]:
    """
    Generate Party Budget recommendations.
    """

    prompt = build_party_prompt(
        budget=budget,
        guests=guests,
        occasion=occasion,
        venue=venue,
        food_preference=food_preference,
        additional_requirements=additional_requirements,
    )

    if settings.DEMO_MODE:
        return fallback_party_recommendation(
            budget=budget,
            guests=guests,
            occasion=occasion,
            venue=venue,
            food_preference=food_preference,
        )

    try:
        result = _generate_with_gemini(prompt)
        result["source"] = "Gemini AI"
        return result

    except Exception as exc:
        print(
            f"[Gemini] Party recommendation failed: {exc}"
        )

        result = fallback_party_recommendation(
            budget=budget,
            guests=guests,
            occasion=occasion,
            venue=venue,
            food_preference=food_preference,
        )

        result["source"] = "Fallback"
        return result


def generate_jewelry_recommendation(
    budget: float,
    occasion: str,
    jewelry_type: str = "any",
    metal_preference: str = "any",
    style: str = "traditional",
    additional_requirements: str = "",
) -> Dict[str, Any]:
    """
    Generate Jewelry recommendations.
    """

    prompt = build_jewelry_prompt(
        budget=budget,
        occasion=occasion,
        jewelry_type=jewelry_type,
        metal_preference=metal_preference,
        style=style,
        additional_requirements=additional_requirements,
    )

    if settings.DEMO_MODE:
        return fallback_jewelry_recommendation(
            budget=budget,
            occasion=occasion,
            jewelry_type=jewelry_type,
            metal_preference=metal_preference,
            style=style,
        )

    try:
        result = _generate_with_gemini(prompt)
        result["source"] = "Gemini AI"
        return result

    except Exception as exc:
        print(
            f"[Gemini] Jewelry recommendation failed: {exc}"
        )

        result = fallback_jewelry_recommendation(
            budget=budget,
            occasion=occasion,
            jewelry_type=jewelry_type,
            metal_preference=metal_preference,
            style=style,
        )

        result["source"] = "Fallback"
        return result