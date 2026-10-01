"""Simplify theme.css to layout helpers; panel layers image + scrim."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "themes"

CSS = """/* {name}: keep chrome readable over the photo background */
.panel-layout {{ position: relative; z-index: 1; }}
.sidebar {{ backdrop-filter: blur(8px); }}
"""


def main() -> None:
    for path in sorted(ROOT.glob("*/theme.json")):
        import json

        data = json.loads(path.read_text(encoding="utf-8"))
        name = data.get("name", path.parent.name)
        (path.parent / "theme.css").write_text(CSS.format(name=name), encoding="utf-8")
        print("css", path.parent.name)
    print("ok")


if __name__ == "__main__":
    main()
