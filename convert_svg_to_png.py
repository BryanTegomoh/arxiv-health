#!/usr/bin/env python3
"""
Convert profilepic.svg to profilepic.png
"""
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from pathlib import Path

# Paths
svg_path = Path("docs/profilepic.svg")
png_path = Path("docs/profilepic.png")

print("Converting profilepic.svg to profilepic.png...")

# Load SVG
drawing = svg2rlg(svg_path)

# Render to PNG at 400x400
renderPM.drawToFile(drawing, str(png_path), fmt="PNG", dpi=72)

print(f"✅ Created {png_path}")
print(f"✅ SVG file at {svg_path}")
print("\nProfile pictures are ready to use!")
print("- Twitter/X: Use profilepic.png")
print("- GitHub: Use profilepic.png or profilepic.svg")
print("- LinkedIn: Use profilepic.png")
