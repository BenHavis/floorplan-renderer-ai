from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# Two models: one for spatial analysis, one for image generation
ANALYSIS_MODEL = "gemini-2.5-pro"
IMAGE_MODEL = "gemini-3-pro-image-preview"

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

def analyze_floorplan(blueprint):
    """Use Gemini's text model to extract spatial information from floorplan."""
    
    analysis_prompt = """
Analyze this architectural floorplan and provide a detailed spatial description.

Extract and describe:
1. ROOM LIST: Each room with its name, approximate square footage, and shape
2. WALL LAYOUT: Which rooms share walls, where solid walls separate spaces
3. OPENINGS: Door locations, archways, open passages between rooms
4. WINDOWS: Window positions and which direction they likely face
5. KITCHEN/BATH: Note appliance positions, fixture locations
6. SPATIAL FLOW: How rooms connect, what you'd see from each doorway

Be precise about what IS and IS NOT open concept. If rooms have walls between them, say so explicitly.

Format as a detailed scene description that could guide an interior rendering.
"""
    
    response = client.models.generate_content(
        model=ANALYSIS_MODEL,
        contents=[analysis_prompt, blueprint]
    )
    
    return response.text

def generate_render(style: str):
    blueprint = Image.open("blueprint.png")
    
    # Step 1: Analyze the floorplan
    print("\n🔍 Analyzing floorplan layout...")
    spatial_analysis = analyze_floorplan(blueprint)
    print("\n📐 Spatial Analysis:")
    print("-" * 40)
    print(spatial_analysis)
    print("-" * 40)
    
    # Step 2: Generate image using the analysis
    render_prompt = f"""
Based on this floorplan and spatial analysis, generate a photorealistic interior render.

SPATIAL ANALYSIS OF THIS FLOORPLAN:
{spatial_analysis}

CRITICAL RENDERING RULES:
- Follow the wall positions described above exactly
- Rooms that are described as separate must have visible walls between them
- Room proportions must match the square footage analysis
- Do not default to open concept unless the analysis confirms open passages
- Ceiling height: 9ft standard
- Camera: 3/4 perspective showing the main living areas

INTERIOR STYLE: {style}

Generate a photorealistic render that accurately reflects THIS specific floorplan's layout.
"""
    
    response = client.models.generate_content(
        model=IMAGE_MODEL,
        contents=[render_prompt, blueprint],
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