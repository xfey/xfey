Titles use Bookman Old Style Bold; captions and dates use Regular. The gallery
preserves the original app logos and their shadows on transparent images, with
no surrounding frames or backgrounds. Separate light and dark text variants
blend into GitHub's theme.

To add or update an app:

1. Add a square, transparent logo with room for its shadow to `icons/<slug>.png`.
2. Edit `apps.json`. Use `tagline` for one or two short display lines, separated
   by `\n`; `description` retains the full text for image accessibility. The
   array order determines display order; add new releases at the beginning.
3. From the repository root, run:

   ```sh
   python3 -m pip install Pillow
   python3 scripts/generate_app_cards.py
   ```

The script uses the macOS Bookman Old Style font by default. On other systems,
pass `--font /path/to/BookmanOldStyle.ttf` with the regular font installed locally
and `--bold-font /path/to/BookmanOldStyle-Bold.ttf` for the title font. The default
macOS TTC includes both weights.
Font files are not included in this repository.

Each image is 720 × 612 pixels. Four 196 px images fit in a normal desktop
GitHub README; on narrower screens they wrap without shrinking the text.
The `picture` element selects the dark text variant when the browser prefers
a dark color scheme. Each app remains individually clickable. The muted
“Code brewing…” placeholder always follows the apps and is not linked. With
eight apps it occupies a third row of its own, ready for future additions.
Titles sit slightly farther below their logos; dates are centered below the
descriptions.

The script updates only the image grid between the `apps:start` and `apps:end`
markers in the root README. The Featured text links can be edited separately.

The original `header.png` remains the source artwork. Existing logos and the
“Code brewing…” icon were cropped from it; the white background outside each
rounded logo was removed while retaining its shadow. Adding new apps does not
require editing the header.
