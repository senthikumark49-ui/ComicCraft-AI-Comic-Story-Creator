from pathlib import Path
from datetime import datetime
from fpdf import FPDF
from PIL import Image
from app.config import BASE_DIR, EXPORTS_DIR

def _absolute_static_path(web_path: str) -> Path:
    # /static/panels/x.png -> project/static/panels/x.png
    relative = web_path.lstrip("/").replace("/", "/")
    return BASE_DIR / relative

def save_pdf(layout: list[dict]) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comiccraft_{timestamp}.pdf"
    output = EXPORTS_DIR / filename

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, f"Panel {panel['panel_number']}: {panel['title']}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        image_path = _absolute_static_path(panel["image_path"])
        if image_path.exists():
            with Image.open(image_path) as im:
                width, height = im.size
            max_w, max_h = 180, 105
            ratio = min(max_w / width, max_h / height)
            w, h = width * ratio, height * ratio
            pdf.image(str(image_path), x=(210 - w) / 2, w=w, h=h)
            pdf.ln(5)

        pdf.set_font("Helvetica", "I", 11)
        pdf.multi_cell(0, 7, panel["scene_description"])
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 7, f"Caption: {panel['caption']}")
        pdf.ln(1)

        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, f"Narration: {panel['narration']}")

    pdf.output(str(output))
    return f"/static/exports/{filename}"
