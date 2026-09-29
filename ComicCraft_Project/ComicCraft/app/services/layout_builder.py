from app.models import Panel

def build_comic_layout(panels: list[Panel], image_paths: list[str]) -> list[dict]:
    if len(panels) != len(image_paths):
        raise ValueError("Every panel must have exactly one image.")
    return [
        {
            "panel_number": panel.panel_number,
            "title": panel.title,
            "image_path": image_path,
            "scene_description": panel.scene_description,
            "image_prompt": panel.image_prompt,
            "caption": panel.caption,
            "narration": panel.narration,
        }
        for panel, image_path in zip(panels, image_paths)
    ]
