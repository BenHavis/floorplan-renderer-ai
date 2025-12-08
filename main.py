from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-3-pro-image-preview"

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


def display_styles():
    print("\n🎨 Available Interior Styles:\n")
    for key, (name, desc) in STYLES.items():
        print(f"  [{key}] {name}")
        print(f"      {desc}\n")


def get_style_choice():
    display_styles()
    print("  [C] Custom - describe your own style\n")

    choice = input("Select a style (1-8) or C for custom: ").strip().upper()

    if choice == "C":
        custom = input("Describe your desired style: ").strip()
        return f"custom style: {custom}"
    elif choice in STYLES:
        name, desc = STYLES[choice]
        return f"{name} style with {desc}"
    else:
        print("Invalid choice, defaulting to Scandinavian Modern")
        return f"{STYLES['1'][0]} style with {STYLES['1'][1]}"


def generate_render(style: str):
    blueprint = Image.open("blueprint.png")

    prompt = f"""
Convert this architectural floorplan into a photorealistic interior rendering.
Infer room layout, wall positions, window placement, and lighting direction.
Use a {style}.
Render in perspective (3/4 angle) showing the interior space.
"""

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt, blueprint],
        config=types.GenerateContentConfig(
            response_modalities=["Image"],
            image_config=types.ImageConfig(aspect_ratio="16:9")
        )
    )

    for part in response.parts:
        image = part.as_image()
        if image:
            image.save("render.png")
            print("\n✅ Saved render to render.png")
            return True

    print("❌ No image generated")
    return False


if __name__ == "__main__":
    style = get_style_choice()
    print(f"\n🏠 Generating render with {style}...")
    generate_render(style)