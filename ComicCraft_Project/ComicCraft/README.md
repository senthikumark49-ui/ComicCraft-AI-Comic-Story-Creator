# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI web application based on the supplied project documentation. It collects a story prompt, character, setting, tone and art style, then generates a 5-panel comic outline, narration/dialogue, illustrations and a downloadable PDF.

## Architecture

Browser → FastAPI/Jinja2 → Gemini outline → Gemini story → Hugging Face Stable-Diffusion-compatible image generation → layout builder → FPDF PDF export.

## Project structure

```text
ComicCraft/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── config.py
│   └── services/
│       ├── gemini_flash.py
│       ├── gemini_pro.py
│       ├── image_generator.py
│       ├── layout_builder.py
│       └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── style.css
│   ├── panels/
│   └── exports/
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## VS Code setup — Windows

1. Install Python 3.11 or newer.
2. Open this folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create the environment:

```powershell
python -m venv .venv
```

5. Activate it:

```powershell
.venv\Scripts\activate
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Create `.env` by copying `.env.example`.
8. Put your Gemini API key in `GEMINI_API_KEY`.
9. Put your Hugging Face access token in `HF_API_KEY`.

## Run

```powershell
uvicorn app.main:app --reload
```

Open:

- Website: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Test

Run the local tests:

```powershell
pip install pytest
pytest
```

Then test the website with a small prompt such as:

> A brave fox discovers a glowing door in an enchanted forest.

Choose a character, setting, tone and art style, then click **Generate My Comic**.

## API example

POST `/generate-comic/json`:

```json
{
  "story_prompt": "A brave fox discovers a glowing door in an enchanted forest.",
  "character_name": "Finn",
  "setting": "enchanted forest",
  "tone": "mysterious",
  "art_style": "comic book"
}
```

The API returns the generated panel layout and PDF path.

## Important notes

- Never commit `.env` or API keys to Git.
- Five image-generation calls can take significantly longer than text generation.
- The supplied documentation describes local Hugging Face Diffusers. This implementation uses Hugging Face hosted inference so a student laptop does not need to download a large Stable Diffusion model. The image model remains configurable through `HF_IMAGE_MODEL`.
- If a selected Hugging Face model/provider is unavailable to your account, change `HF_IMAGE_MODEL` in `.env` to a model supported by your account.
- The Gemini and Hugging Face model names are configurable rather than hard-coded into the application logic.
