These PNGs form the clickable app gallery in the profile README.

- `apps.json` contains application names, dates, descriptions, and destinations.
  The README generator sorts by `YYYY/MM`, newest first, keeping the existing
  order within the same month.
- `icons/` contains the source logos with their original shadows and transparent
  backgrounds.
- `<slug>.png` and `<slug>-dark.png` contain the light and dark versions of each
  application tile.
- `explore-desktop.png` and `explore-desktop-dark.png` form the image button
  linking to https://feedthis.dev below the app gallery.

Each transparent tile is 444 × 426 px, displayed at 148 × 142 px. It shows only
the original logo, a Helvetica Neue Medium name, and the release month beneath
in Helvetica Neue Regular. Logos fit an 88 px area including their shadows.
The website entry matches the app icons: a white rounded square with a subtle
shadow and a monochrome outward arrow, labeled “Explore more” beneath it. It is
444 × 366 px, displayed at 148 × 122 px, with no subtitle or visible URL.
Font files are not included in the repository.

All apps are shown, in groups of four: the current eight apps occupy two rows
in a wide README. Narrow layouts wrap naturally, with two columns at a typical
phone width. Each app and the website button is independently clickable and
includes descriptive alt text. Additional apps create more rows without hiding
older entries. App descriptions remain in the manifest for the personal website;
they are not displayed in the README gallery. Research projects stay in the
README's separate text section. The older `brewing*.png` assets are unused.

The rendering tools are maintained locally and are not included in this repository.
