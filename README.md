# CPN-Themes

Design themes for **CPN Panel** (Settings > Design > Theme Store).

CPN Panel fetches the `main` branch tarball and lists folders under `themes/` that contain `theme.json`.

## Package layout

Each theme lives in `themes/<id>/`:

- `theme.json` (required): id, name, description, tokens, optional `background`
- `theme.css` (optional): extra panel CSS (gradients / patterns only; no remote `url()`)

### Tokens

Accent colors, radius, density, and font scale applied as Custom Design.

### Background

Optional object applied panel-wide on Install/Apply:

| Field | Purpose |
| --- | --- |
| `color_mode` | Preferred `light` or `dark` when applying |
| `body` | CSS background for `body` / `.panel-layout` (color or gradient) |
| `sidebar` | CSS background for `.sidebar` |
| `surface` / `canvas` / `surface_soft` | Hex surface tokens |
| `ink` / `muted` / `hairline` | Hex text and border tokens |
| `preview` | Theme Store card swatch (falls back to `body`) |

Background values must be hex colors or CSS gradients. External image hotlinks are rejected.

## Catalog

See `catalog.json` for the indexed theme list (10 packages).

Panel UI must use CPN branding only.
