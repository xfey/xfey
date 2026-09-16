"""Render app cards with Bookman Old Style and update the README image grid."""

import argparse
import html
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "apps"
DEFAULT_FONT = Path(
    "/System/Library/PrivateFrameworks/FontServices.framework/Versions/A/"
    "Resources/Fonts/ApplicationSupport/BookmanOldStyle.ttc"
)
SCALE = 12  # Supersample the text, rounded corners, and fractional border width.
OUTPUT_SCALE = 3
WIDTH, HEIGHT = 480, 164
BORDER_COLOR = "#ccd6dd"  # Sampled from the straight edge of header.png.
CARD_WIDTH_PERCENT = 49
# The original 5610 px header has a 7 px stroke. Keep the same visible stroke
# when a card occupies 49% of the space previously occupied by the header.
BORDER_WIDTH = 7 * WIDTH / (5610 * CARD_WIDTH_PERCENT / 100)
START, END = "<!-- apps:start -->", "<!-- apps:end -->"


def wrap(text, font, width):
    lines = []
    for word in text.split():
        if font.getlength(word) > width:
            raise ValueError(f"Word is too wide for the card: {word}")
        candidate = f"{lines[-1]} {word}" if lines else word
        if lines and font.getlength(candidate) <= width:
            lines[-1] = candidate
        else:
            lines.append(word)
    return lines


def render(app, font_path):
    title = ImageFont.truetype(str(font_path), 27 * SCALE)
    date = ImageFont.truetype(str(font_path), 16 * SCALE)
    body = ImageFont.truetype(str(font_path), round(17.5 * SCALE))
    if title.getlength(app["name"]) > 332 * SCALE:
        raise ValueError(f"Title is too wide: {app['name']}")
    lines = wrap(app["description"], body, 424 * SCALE)
    if len(lines) > 2:
        raise ValueError(f"Description needs more than two lines: {app['name']}")

    frame = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE))
    draw = ImageDraw.Draw(frame)
    draw.rounded_rectangle(
        (1, 1, frame.width - 2, frame.height - 2),
        radius=18 * SCALE,
        fill="white",
        outline=BORDER_COLOR,
        width=round(BORDER_WIDTH * SCALE),
    )
    card = Image.new("RGBA", frame.size)
    draw = ImageDraw.Draw(card)
    with Image.open(ASSETS / "icons" / f"{app['slug']}.png") as source:
        icon = source.convert("RGBA").resize(
            (96 * SCALE, 96 * SCALE), Image.Resampling.LANCZOS
        )
    card.alpha_composite(icon, (14 * SCALE, 2 * SCALE))
    draw.text((120 * SCALE, 25 * SCALE), app["name"], font=title,
              fill="#111111", anchor="lt")
    draw.text((120 * SCALE, 63 * SCALE), app["date"], font=date,
              fill="#888888", anchor="lt")
    for index, line in enumerate(lines):
        draw.text((28 * SCALE, (102 + 24 * index) * SCALE), line,
                  font=body, fill="#111111", anchor="lt")
    size = (WIDTH * OUTPUT_SCALE, HEIGHT * OUTPUT_SCALE)
    # Area sampling preserves the exact border color without ringing, while
    # Lanczos keeps the logo and text crisp.
    result = frame.resize(size, Image.Resampling.BOX)
    result.alpha_composite(card.resize(size, Image.Resampling.LANCZOS))
    return result


def image_grid(apps):
    rows = []
    for index in range(0, len(apps), 2):
        row = ['<p align="center">']
        for app in apps[index:index + 2]:
            alt = html.escape(
                f"{app['name']} — {app['date']}. {app['description']}", quote=True
            )
            row.extend([
                f'  <a href="{html.escape(app["url"], quote=True)}">',
                f'    <img src="./assets/apps/{app["slug"]}.png" '
                f'alt="{alt}" width="{CARD_WIDTH_PERCENT}%" />',
                '  </a>',
            ])
        row.append('</p>')
        rows.append('\n'.join(row))
    return '\n\n'.join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=DEFAULT_FONT,
                        help="Path to the Bookman Old Style regular TTF/TTC font")
    args = parser.parse_args()
    if not args.font.is_file():
        parser.error("Bookman Old Style is missing; supply its path with --font.")
    font = ImageFont.truetype(str(args.font), 16)
    if font.getname() != ("Bookman Old Style", "Regular"):
        parser.error("The font must be Bookman Old Style Regular.")

    apps = json.loads((ASSETS / "apps.json").read_text())
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text()
    before, section = readme.split(START, 1)
    _, after = section.split(END, 1)
    cards = [(app, render(app, args.font)) for app in apps]
    for app, card in cards:
        card.save(ASSETS / f"{app['slug']}.png", optimize=True)
    readme_path.write_text(f"{before}{START}\n{image_grid(apps)}\n{END}{after}")
    print(f"Generated {len(cards)} cards and updated the README grid.")


if __name__ == "__main__":
    main()
