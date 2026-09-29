import json
from google import genai
from google.genai import types
from app.config import settings
from app.models import Panel

def _client():
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured. Add it to .env.")
    return genai.Client(api_key=settings.gemini_api_key)

def generate_outline(story_prompt: str, character_name: str, setting: str,
                     tone: str, art_style: str) -> list[Panel]:
    prompt = f"""
Create a coherent 5-panel comic outline.

User story prompt: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY valid JSON matching this exact structure:
{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "short title",
      "scene_description": "visual scene description",
      "image_prompt": "detailed prompt for an image model"
    }}
  ]
}}

Rules:
- Exactly 5 panels.
- panel_number must be 1 through 5.
- Keep the same main character and visual identity across panels.
- Make each image prompt visually specific.
- Do not include markdown fences.
"""
    response = _client().models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.8,
        ),
    )
    raw = response.text or ""
    data = json.loads(raw)
    panels = data.get("panels", [])
    if len(panels) != 5:
        raise ValueError("Gemini did not return exactly 5 panels.")
    return [Panel(**p) for p in panels]
