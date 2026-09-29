from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from app.models import PromptRequest
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image, generate_test_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf

router = APIRouter()

def _generate_comic(data: PromptRequest):
    panels = generate_outline(
        data.story_prompt, data.character_name, data.setting,
        data.tone, data.art_style
    )
    panels = generate_story(panels, data.character_name, data.tone)

    image_paths = []
    for panel in panels:
        image_paths.append(generate_image(panel.image_prompt, panel.panel_number))

    layout = build_comic_layout(panels, image_paths)
    pdf_path = save_pdf(layout)
    return layout, pdf_path

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        data = PromptRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )
        layout, pdf_path = _generate_comic(data)
        return request.app.state.templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={"layout": layout, "pdf_path": pdf_path},
        )
    except Exception as exc:
        return request.app.state.templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc)},
            status_code=500,
        )

@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        layout, pdf_path = _generate_comic(payload)
        return JSONResponse({"success": True, "layout": layout, "pdf_path": pdf_path})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf: str = ""):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_path": pdf},
    )

@router.post("/test-image")
async def test_image(prompt: str = Form(...)):
    try:
        return {"success": True, "image_path": generate_test_image(prompt)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
