from pathlib import Path
import re
import uuid
from PIL import Image
from app.config import settings

def _safe_name(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9_-]+", "_", text).strip("_")
    return text[:50] or "panel"

def generate_image(image_prompt: str, panel_number: int) -> str:
    if not settings.hf_api_key:
        raise RuntimeError("HF_API_KEY is not configured. Add it to .env.")

    # Hugging Face's hosted inference path avoids downloading a multi-GB model
    # into the student's laptop while still using a Stable-Diffusion-compatible
    # image model. The returned image is saved locally for preview/PDF export.
    from huggingface_hub import InferenceClient

    client = InferenceClient(
        provider="hf-inference",
        api_key=settings.hf_api_key,
    )
    final_prompt = (
        f"{image_prompt}. {settings.hf_image_model}. "
        "clean comic illustration, strong composition, consistent character, "
        "no text, no watermark."
    )
    image = client.text_to_image(
        prompt=final_prompt,
        model=settings.hf_image_model,
    )
    if not isinstance(image, Image.Image):
        raise RuntimeError("Image service did not return a valid image.")

    filename = f"panel_{panel_number}_{_safe_name(str(uuid.uuid4())[:8])}.png"
    # Use the application static/panels directory for both preview and PDF export.
    from app.config import PANELS_DIR
    output = PANELS_DIR / filename
    image.convert("RGB").save(output, format="PNG")
    return f"/static/panels/{filename}"

def generate_test_image(prompt: str) -> str:
    return generate_image(prompt, 0)
