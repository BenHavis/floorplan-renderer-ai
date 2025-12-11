# Floorplan to Render

Convert architectural floorplans into photorealistic interior renderings using Google's Gemini image generation API.

## Overview

This project uses Gemini's multimodal capabilities to interpret 2D architectural blueprints and generate 3D photorealistic interior renders. The model infers spatial relationships, room layouts, window placement, and lighting to produce stylized visualizations.

## Features

- Accepts standard floorplan images (PNG, JPG)
- Generates photorealistic interior renders in 16:9 aspect ratio
- Configurable design styles (default: Scandinavian modern)
- Perspective rendering with inferred lighting

## Requirements

- Python 3.9+
- Google Gemini API access

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/floorplan-to-render.git
cd floorplan-to-render

# Install dependencies
pip install google-genai pillow python-dotenv

# Set up environment variables
cp .env.example .env
# Add your GEMINI_API_KEY to .env
```

## Usage

1. Place your floorplan image in the project directory as `blueprint.png`
2. Run the script:

```bash
python main.py
```

# Floorplan to Render

Convert architectural floorplans into photorealistic interior renderings using Google's Gemini image generation API.

## Overview

This project uses Gemini's multimodal capabilities to interpret 2D architectural blueprints and generate photorealistic interior renders. The model infers spatial relationships, room layouts, window placement, and lighting to produce stylized visualizations.

## Features

- Accepts standard floorplan images (PNG, JPG)
- Generates photorealistic interior renders in 16:9 aspect ratio
- Configurable design styles (default: Scandinavian modern)
- Perspective rendering with inferred lighting

## Requirements

- Python 3.9+
- Google Gemini API access (set `GEMINI_API_KEY`)

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file containing your Gemini API key:

```bash
# .env
GEMINI_API_KEY=your_api_key_here
```

Optionally copy from an example file if present:

```bash
cp .env.example .env
# then edit .env to add your key
```

## Usage

1. Place your floorplan image in the project directory as `blueprint.png` (or update `main.py` to load a different filename).
2. Run the script:

```bash
python main.py
```

3. The rendered output will be saved to `render.png` if generation succeeds.

## Quick Notes

- The script expects `blueprint.png` to be present in the working directory.
- If the Gemini client fails, ensure `GEMINI_API_KEY` is correct and network access is available.
- Adjust `ANALYSIS_MODEL` and `IMAGE_MODEL` in `main.py` if you want different Gemini models.

## Configuration and Customization

- Styles are defined in `main.py` under the `STYLES` dictionary; you can add or modify entries.
- Prompts for analysis and rendering are in `analyze_floorplan` and `generate_render` respectively — tweak them for different visual outcomes.

## Next Steps / Suggestions

- Add a CLI wrapper (argparse) to pass input/output filenames and style choices.
- Add `tests/` with basic unit tests and a GitHub Actions workflow to run them.
- Add an `examples/` folder with a sample `blueprint.png` for quick demos.

## License

MIT

## Contributing

Pull requests welcome. For major changes, please open an issue first to discuss proposed modifications.
