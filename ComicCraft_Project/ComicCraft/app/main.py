from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import BASE_DIR, STATIC_DIR
from app.routes import router

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    version="1.0.0",
    description="Generate 5-panel AI comics with Gemini and Stable Diffusion-compatible image generation.",
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.state.templates = templates
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}
