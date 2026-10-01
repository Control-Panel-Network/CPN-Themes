# CPN-Themes

Design themes for **CPN Panel** (Settings > Design > Theme Store).

CPN Panel fetches the `main` branch tarball and lists folders under `themes/` that contain `theme.json`.

## Package layout

Each theme lives in `themes/<id>/`:

- `theme.json` (required): id, name, description, tokens, optional `background`
- `theme.css` (optional): extra panel CSS (same-origin asset urls only; no remote `url(http...)`)
- `assets/` (recommended): self-hosted background images (`bg.webp`, `preview.webp`)

### Tokens

Accent colors, radius, density, and font scale applied as Custom Design.

### Background

Optional object applied panel-wide on Install/Apply:

| Field | Purpose |
| --- | --- |
| `color_mode` | Preferred `light` or `dark` when applying |
| `body` | CSS scrim / wash for `body` / `.panel-layout` (color or gradient overlay) |
| `sidebar` | CSS background for `.sidebar` |
| `image` | Relative path to a package image (e.g. `assets/bg.webp`) layered under the scrim |
| `preview_image` | Relative path for Theme Store card thumbnails |
| `surface` / `canvas` / `surface_soft` | Hex surface tokens |
| `ink` / `muted` / `hairline` | Hex text and border tokens |
| `preview` | Fallback CSS swatch when no `preview_image` is available |

Background colors/gradients must be hex colors or CSS gradients. External image hotlinks are rejected. Package images must live under `assets/` and use `.webp`, `.jpg`, `.jpeg`, `.png`, or `.svg`.

`theme.css` may reference package files with relative urls such as `url(assets/bg.webp)`. The panel rewrites those to authenticated same-origin asset routes when Apply runs.

## Catalog

See `catalog.json` for the indexed theme list (10 packages).

Author for packages in this repo: **master3395**. Panel UI must use CPN branding only.
