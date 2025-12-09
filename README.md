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

Or if you're on pycharm click run

3. Find your rendered output in `render.png`

## Configuration

Edit the prompt in `main.py` to customize the output style:

```python
prompt = """
Convert this architectural floorplan into a photorealistic interior rendering.
Infer room layout, wall positions, window placement, and lighting direction.
Use a clean Scandinavian modern style. Render in perspective (3/4 angle) if possible.
"""
```

### Supported Styles

- Scandinavian modern (default)
- Mid-century modern
- Industrial loft
- Minimalist Japanese
- Contemporary luxury

## API Reference

This project uses the `gemini-3-pro-image-preview` model. See [Google AI Studio](https://aistudio.google.com/) for API key setup and documentation.

## Limitations

- Output quality depends on floorplan clarity and detail
- Complex multi-story layouts may produce inconsistent results
- Model interprets ambiguous elements based on training data

## License

MIT

## Contributing

Pull requests welcome. For major changes, please open an issue first to discuss proposed modifications.
