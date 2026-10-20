These PNGs form the clickable app gallery in the profile README.

- `apps.json` contains application names, dates, descriptions, and destinations.
  Dates use `YYYY/MM` or `YYYY/MM/DD` when a day is known. The README generator
  sorts newest first, keeping the existing order for equal dates. Entries with
  a known day precede month-only entries in the same month.
- `icons/` contains the source logos with their original shadows and transparent
  backgrounds.
- `<slug>.png` and `<slug>-dark.png` contain the light and dark versions of each
  application tile.

Each transparent tile is 444 × 450 px, displayed at 148 × 150 px. It shows only
the original logo, a Helvetica Neue Medium name, and the release date beneath
in Helvetica Neue Regular. Logos fit a 96 px area including their shadows.
Font files are not included in the repository.

All apps are shown, in groups of four in a wide README.
Narrow layouts wrap naturally, with two columns at a typical
phone width. Each app is independently clickable and
includes descriptive alt text. Additional apps create more rows without hiding
older entries. App descriptions remain in the manifest for the personal website;
they are not displayed in the README gallery. Research projects stay in the
README's separate text section. The older `brewing*.png` assets are unused.

The rendering tools are maintained locally and are not included in this repository.
