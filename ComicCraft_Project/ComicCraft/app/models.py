from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=2000)
    character_name: str = Field(default="Alex", min_length=1, max_length=100)
    setting: str = Field(default="enchanted forest", min_length=1, max_length=200)
    tone: str = Field(default="dramatic", min_length=1, max_length=100)
    art_style: str = Field(default="comic book", min_length=1, max_length=100)

class Panel(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str
    caption: str = ""
    narration: str = ""

class ComicResult(BaseModel):
    panels: list[Panel]
    pdf_path: str | None = None
