"""Render a borderless app gallery in Bookman Old Style for the GitHub README."""

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
SCALE, OUTPUT_SCALE = 6, 3
WIDTH, HEIGHT = 240, 204
DISPLAY_WIDTH = 196
COLUMNS = 4
START, END = "<!-- apps:start -->", "<!-- apps:end -->"
PALETTES = {
    "light": {"title": "#111111", "body": "#444444", "muted": "#858585"},
    "dark": {"title": "#f0f3f6", "body": "#c3c9d1", "muted": "#9199a3"},
}
BREWING = {
    "slug": "brewing",
    "name": "Code brewing...",
    "date": "",
    "description": "What’s the next one?",
    "tagline": "What’s the next one?",
}


def render(app, fonts, theme):
    colors = PALETTES[theme]
    title, date, body = (fonts[key] for key in ("title", "date", "body"))
    lines = app["tagline"].splitlines()
    if not 1 <= len(lines) <= 2:
        raise ValueError(f"Use one or two tagline lines: {app['name']}")
    if any(body.getlength(line) > (WIDTH - 24) * SCALE for line in lines):
        raise ValueError(f"Tagline is too wide: {app['name']}")

    name_width = title.getlength(app["name"])
    x = (WIDTH * SCALE - name_width) / 2
    if x < 12 * SCALE:
        raise ValueError(f"Name is too wide: {app['name']}")

    tile = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE))
    with Image.open(ASSETS / "icons" / f"{app['slug']}.png") as source:
        icon = source.convert("RGBA").resize(
            (112 * SCALE, 112 * SCALE), Image.Resampling.LANCZOS
        )
    placeholder = "url" not in app
    if placeholder:
        alpha = icon.getchannel("A")
        if theme == "dark":
            icon = Image.new("RGBA", icon.size, "#c3c9d1")
            alpha = alpha.point(lambda value: min(255, round(value * 1.6)))
        icon.putalpha(alpha)
    tile.alpha_composite(icon, ((WIDTH - 112) * SCALE // 2, -5 * SCALE))

    draw = ImageDraw.Draw(tile)
    draw.text((x, 119 * SCALE), app["name"], font=title, anchor="ls",
              fill=colors["muted"] if placeholder else colors["title"])
    # Center single-line captions in the same area used for two-line captions.
    baseline = 143 if len(lines) == 2 else 153
    for index, line in enumerate(lines):
        draw.text((WIDTH * SCALE / 2, (baseline + 21 * index) * SCALE), line,
                  font=body, fill=colors["muted"] if placeholder else colors["body"],
                  anchor="ms")
    if app["date"]:
        draw.text((WIDTH * SCALE / 2, 189 * SCALE), app["date"], font=date,
                  fill=colors["muted"], anchor="ms")
    return tile.resize((WIDTH * OUTPUT_SCALE, HEIGHT * OUTPUT_SCALE),
                       Image.Resampling.LANCZOS)


def image_grid(items):
    rows = []
    for index in range(0, len(items), COLUMNS):
        row = ['<p align="center">']
        for app in items[index:index + COLUMNS]:
            date = f" — {app['date']}" if app["date"] else ""
            separator = ". " if date else " "
            alt = html.escape(
                f"{app['name']}{date}{separator}{app['description']}", quote=True
            )
            # No whitespace inside the link: GitHub otherwise underlines it
            # beside the image on hover, leaving stray blue marks in the grid.
            picture = (
                '<picture><source media="(prefers-color-scheme: dark)" '
                f'srcset="./assets/apps/{app["slug"]}-dark.png" />'
                f'<img src="./assets/apps/{app["slug"]}.png" '
                f'alt="{alt}" width="{DISPLAY_WIDTH}" /></picture>'
            )
            if "url" in app:
                url = html.escape(app["url"], quote=True)
                row.append(f'  <a href="{url}">{picture}</a>')
            else:
                row.append(f'  {picture}')
        row.append('</p>')
        rows.append('\n'.join(row))
    return '\n\n'.join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, default=DEFAULT_FONT,
                        help="Path to the Bookman Old Style regular TTF/TTC font")
    parser.add_argument("--bold-font", type=Path,
                        help="Separate Bookman Old Style Bold font, if not in the TTC")
    args = parser.parse_args()
    if not args.font.is_file():
        parser.error("Bookman Old Style is missing; supply its path with --font.")
    font = ImageFont.truetype(str(args.font), 16)
    if font.getname() != ("Bookman Old Style", "Regular"):
        parser.error("The font must be Bookman Old Style Regular.")
    fonts = {
        key: ImageFont.truetype(str(args.font), round(size * SCALE))
        for key, size in {"date": 11, "body": 16.5}.items()
    }
    try:
        fonts["title"] = ImageFont.truetype(
            str(args.bold_font or args.font), 22 * SCALE,
            index=0 if args.bold_font else 1,
        )
    except OSError:
        parser.error("Bookman Old Style Bold is missing; supply --bold-font.")
    if fonts["title"].getname() != ("Bookman Old Style", "Bold"):
        parser.error("The title font must be Bookman Old Style Bold.")

    apps = json.loads((ASSETS / "apps.json").read_text())
    items = apps + [BREWING]
    readme_path = ROOT / "README.md"
    before, section = readme_path.read_text().split(START, 1)
    _, after = section.split(END, 1)
    images = [
        (app, theme, render(app, fonts, theme))
        for app in items for theme in PALETTES
    ]
    for app, theme, image in images:
        suffix = "-dark" if theme == "dark" else ""
        image.save(ASSETS / f"{app['slug']}{suffix}.png", optimize=True)
    readme_path.write_text(f"{before}{START}\n{image_grid(items)}\n{END}{after}")
    print(f"Generated {len(images)} theme images and updated the README gallery.")


if __name__ == "__main__":
    main()
