from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

ANALYSIS_MODEL = "gemini-2.5-pro"
IMAGE_MODEL = "gemini-3-pro-image-preview"

# Style lookup table (backend keeps your original descriptions)
STYLES = {
    "1": ("Scandinavian Modern", "clean lines, light wood, white walls, minimal decor, natural light"),
    "2": ("Mid-Century Modern", "warm woods, organic shapes, vintage furniture, bold accent colors"),
    "3": ("Industrial Loft", "exposed brick, metal fixtures, concrete floors, open ductwork"),
    "4": ("Minimalist Japanese", "tatami elements, shoji screens, natural materials, zen simplicity"),
    "5": ("Contemporary Luxury", "high-end finishes, marble accents, designer furniture, dramatic lighting"),
    "6": ("Coastal/Hamptons", "white and blue palette, natural textures, airy and bright, beach-inspired"),
    "7": ("Art Deco", "geometric patterns, rich colors, gold accents, glamorous details"),
    "8": ("Rustic Farmhouse", "reclaimed wood, vintage fixtures, cozy textiles, warm neutrals"),
}

app = FastAPI()

# Allow Next.js frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def analyze_floorplan(image: Image.Image) -> str:
    """Use Gemini's text model to extract spatial info."""
    analysis_prompt = """
Analyze this architectural floorplan and provide a detailed spatial description.

Extract and describe:
1. ROOM LIST with approx square footage
2. WALL LAYOUT and room adjacency
3. OPENINGS and door placements
4. WINDOWS and probable directions
5. KITCHEN/BATH appliance/fixture positions
6. SPATIAL FLOW and how rooms connect

Be precise about what IS and IS NOT open concept.
"""

    response = client.models.generate_content(
        model=ANALYSIS_MODEL,
        contents=[analysis_prompt, image]
    )

    return response.text


@app.post("/generate")
async def generate_interior(
    file: UploadFile = File(...),
    style_number: str = Form(...)
):
    """Main endpoint: upload blueprint + choose style number."""

    # Validate style
    if style_number not in STYLES:
        return JSONResponse({"error": "Invalid style selection"}, status_code=400)

    style_name, style_desc = STYLES[style_number]
    full_style_prompt = f"{style_name} style — {style_desc}"

    # Load image from upload
    blueprint = Image.open(file.file)

    # Step 1 — analyze plan
    analysis_text = analyze_floorplan(blueprint)

    # Step 2 — generate render
    render_prompt = f"""
Based on this floorplan and spatial analysis, generate a photorealistic interior render.

SPATIAL ANALYSIS:
{analysis_text}

RENDER RULES:
- Follow wall positions accurately
- Maintain room proportions
- No open concept unless analysis confirms it
- Show realistic Scandinavian/MidCentury/etc style as defined
- Camera: 3/4 perspective
- Ceiling: 9 ft

INTERIOR STYLE: {full_style_prompt}
"""

    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[render_prompt, blueprint],
        config=types.GenerateContentConfig(
            response_modalities=["Image"],
            image_config=types.ImageConfig(aspect_ratio="16:9")
        )
    )

    # Save output
    output_path = "render.png"

    for part in response.parts:
        img = part.as_image()
        if img:
            img.save(output_path)
            return FileResponse(output_path, media_type="image/png")

    return JSONResponse({"error": "Image generation failed"}, status_code=500)
