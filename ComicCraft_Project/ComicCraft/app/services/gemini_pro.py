import json
from google import genai
from google.genai import types
from app.config import settings
from app.models import Panel

def _client():
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env.")
    return genai.Client(api_key=settings.gemini_api_key)

def generate_story(panels: list[Panel], character_name: str, tone: str) -> list[Panel]:
    outline = [p.model_dump() for p in panels]
    prompt = f"""
Expand this 5-panel comic outline into polished comic narration and dialogue.

Main character: {character_name}
Tone: {tone}

Outline:
{json.dumps(outline, ensure_ascii=False)}

Return ONLY valid JSON:
{{
  "panels": [
    {{
      "panel_number": 1,
      "caption": "short ambient caption",
      "narration": "short engaging narration and/or dialogue"
    }}
  ]
}}

Rules:
- Exactly 5 panels, same numbering.
- Keep the story coherent from panel 1 to 5.
- Use concise comic-book text suitable for a web page and PDF.
- Do not rewrite scene_description or image_prompt.
- No markdown fences.
"""
    response = _client().models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.9,
        ),
    )
    data = json.loads(response.text or "")
    story_panels = data.get("panels", [])
    if len(story_panels) != 5:
        raise ValueError("Gemini did not return story text for all 5 panels.")

    by_number = {int(p["panel_number"]): p for p in story_panels}
    result = []
    for panel in panels:
        extra = by_number.get(panel.panel_number, {})
        result.append(panel.model_copy(update={
            "caption": str(extra.get("caption", "")),
            "narration": str(extra.get("narration", "")),
        }))
    return result
