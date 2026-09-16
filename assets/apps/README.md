App cards use Bookman Old Style Regular. The PNGs in `icons/` were cropped
from the original `header.png`, including its existing shadows and rounded corners.
The font is rendered into each card, so GitHub visitors do not need it installed.

To add or update an app:

1. Add its square logo image, including space around any shadow, to `icons/<slug>.png`.
2. Edit `apps.json`. Its order determines the two-column layout.
3. From the repository root, run:

   ```sh
   python3 -m pip install Pillow
   python3 scripts/generate_app_cards.py
   ```

The script uses the macOS Bookman Old Style font by default. On other systems,
pass `--font /path/to/BookmanOldStyle.ttf` with the regular font installed locally.
Font files are not included in this repository.

Each card is 1440 × 492 pixels, rendered at 3× resolution. The script updates
only the image grid between the `apps:start` and `apps:end` markers in the root
README. The Featured text links can be edited separately.

The border color is `#CCD6DD`, sampled from the original header. Its thickness
is scaled from the original 7 px stroke at 5610 px image width to preserve the
same visible weight in the 49%-width, two-column layout. Supersampling keeps
the fractional stroke and rounded corners smooth.

The original `header.png` is retained as the source artwork; adding new apps
does not require editing it.
