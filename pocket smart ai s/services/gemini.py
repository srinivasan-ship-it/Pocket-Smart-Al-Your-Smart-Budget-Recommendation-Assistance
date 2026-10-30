import json
import logging

from typing import Any

from app.config import settings

from services.recommendations import (
    home_fallback,
    party_fallback,
    jewelry_fallback,
    search_url
)


logger = logging.getLogger(__name__)


SYSTEM_RULES = """
You are PocketSmart AI, a budget-aware recommendation assistant.

Return ONLY valid JSON.

Required JSON format:

{
  "planner": "Home|Party|Jewelry",
  "budget": number,
  "currency": "INR",
  "summary": "string",
  "allocation": {
    "category": number
  },
  "recommendations": [
    {
      "category": "string",
      "name": "string",
      "description": "string",
      "estimated_price": number,
      "platform": "Amazon|Flipkart|IKEA|Swiggy|Zomato|OYO",
      "search_url": "string"
    }
  ],
  "tips": [
    "string"
  ],
  "source": "gemini"
}

Rules:

1. Respect the user's total budget.
2. Prices are estimates.
3. Never claim live marketplace access unless a real API supplied the data.
4. Keep recommendations practical.
5. Use INR.
6. Provide 4-8 useful recommendations when appropriate.
7. Keep total allocation at or below the user's budget.
"""


class GeminiService:

    def __init__(self):

        self.client = None

        if (
            settings.ai_enabled
            and settings.gemini_api_key
        ):

            try:

                from google import genai

                self.client = genai.Client(
                    api_key=settings.gemini_api_key
                )

            except Exception as exc:

                logger.warning(
                    "Gemini client unavailable: %s",
                    exc
                )

    def _prompt(
        self,
        planner: str,
        data: dict[str, Any],
        image_note: str = ""
    ) -> str:

        return (
            SYSTEM_RULES
            + "\n\nPlanner: "
            + planner
            + "\n\nInput:\n"
            + json.dumps(
                data,
                ensure_ascii=False
            )
            + "\n"
            + image_note
            + "\nGenerate useful budget-aware recommendations."
        )

    def _fallback(
        self,
        planner: str,
        data: dict[str, Any]
    ) -> dict:

        if planner == "Home":

            return home_fallback(
                data
            )

        if planner == "Party":

            return party_fallback(
                data
            )

        return jewelry_fallback(
            data
        )

    def generate(
        self,
        planner: str,
        data: dict[str, Any],
        image_bytes: bytes | None = None
    ) -> dict:

        fallback = self._fallback(
            planner,
            data
        )

        if not self.client:

            return fallback

        try:

            contents: list[Any] = [

                self._prompt(
                    planner,
                    data,
                    (
                        "An outfit image is attached. "
                        "Use it only for broad color "
                        "and style coordination."
                        if image_bytes
                        else ""
                    )
                )
            ]

            if image_bytes:

                from PIL import Image

                import io

                image = Image.open(
                    io.BytesIO(
                        image_bytes
                    )
                )

                contents.append(
                    image
                )

            response = (
                self.client.models.generate_content(
                    model=settings.gemini_model,
                    contents=contents
                )
            )

            raw = (
                response.text
                or ""
            ).strip()

            if raw.startswith(
                "```json"
            ):

                raw = raw[
                    len("```json"):
                ]

            if raw.endswith(
                "```"
            ):

                raw = raw[:-3]

            raw = raw.strip()

            result = json.loads(
                raw
            )

            result["source"] = "gemini"

            for item in result.get(
                "recommendations",
                []
            ):

                if not item.get(
                    "search_url"
                ):

                    item["search_url"] = search_url(
                        item.get(
                            "platform",
                            "Amazon"
                        ),
                        item.get(
                            "name",
                            "product"
                        )
                    )

            return result

        except Exception as exc:

            logger.warning(
                "Gemini generation failed; "
                "using fallback: %s",
                exc
            )

            return fallback


gemini_service = GeminiService()