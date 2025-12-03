from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv

# Load .env API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize client
client = genai.Client(api_key=API_KEY)

# Model ID from AI Studio
MODEL_ID = "gemini-3-pro-image-preview"

# Load blueprint image
blueprint = Image.open("blueprint.png")

# Basic prompt (you can refine later)
prompt = """
Convert this architectural floorplan into a photorealistic interior rendering.
Infer room layout, wall positions, window placement, and lighting direction.
Use a clean Scandinavian modern style. Render in perspective (3/4 angle) if possible.
"""

# Send prompt + image to the model
response = client.models.generate_content(
    model=MODEL_ID,
    contents=[prompt, blueprint],
    config=types.GenerateContentConfig(
        response_modalities=["Image"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",   # widescreen render
        )
    )
)

# Save output
for part in response.parts:
    image = part.as_image()
    if image:
        image.save("render.png")
        print("Saved render.png")
        break
