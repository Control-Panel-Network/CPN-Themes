"""Bump themes to ship background image assets + scrims."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "themes"

SCRIMS = {
    "arctic-mint": {
        "body": "linear-gradient(180deg, rgba(240,253,250,0.82) 0%, rgba(204,251,241,0.78) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(255,255,255,0.92) 0%, rgba(236,254,255,0.94) 100%)",
    },
    "aurora-teal": {
        "body": "linear-gradient(165deg, rgba(4,16,24,0.72) 0%, rgba(7,24,32,0.78) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(4,16,24,0.88) 0%, rgba(7,24,32,0.92) 100%)",
    },
    "copper-circuit": {
        "body": "linear-gradient(155deg, rgba(7,16,28,0.7) 0%, rgba(10,21,36,0.78) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(10,20,34,0.9) 0%, rgba(7,16,28,0.94) 100%)",
    },
    "ember-forge": {
        "body": "linear-gradient(155deg, rgba(20,12,8,0.7) 0%, rgba(16,10,8,0.8) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(22,14,10,0.9) 0%, rgba(16,10,8,0.94) 100%)",
    },
    "forest-night": {
        "body": "linear-gradient(170deg, rgba(6,20,15,0.72) 0%, rgba(7,21,16,0.8) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(6,20,14,0.9) 0%, rgba(8,28,18,0.94) 100%)",
    },
    "graphite-terminal": {
        "body": "linear-gradient(180deg, rgba(5,7,5,0.72) 0%, rgba(7,10,8,0.82) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(8,12,9,0.92) 0%, rgba(5,7,5,0.95) 100%)",
    },
    "high-contrast": {
        "body": "linear-gradient(180deg, rgba(248,250,252,0.88) 0%, rgba(226,232,240,0.84) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(255,255,255,0.94) 0%, rgba(241,245,249,0.96) 100%)",
    },
    "ocean-blue": {
        "body": "linear-gradient(165deg, rgba(6,21,37,0.7) 0%, rgba(7,26,46,0.78) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(6,22,40,0.9) 0%, rgba(8,28,48,0.94) 100%)",
    },
    "sandstone-ops": {
        "body": "linear-gradient(160deg, rgba(28,25,20,0.72) 0%, rgba(24,20,15,0.8) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(32,28,22,0.9) 0%, rgba(24,20,15,0.94) 100%)",
    },
    "slate-pro": {
        "body": "linear-gradient(160deg, rgba(15,20,27,0.72) 0%, rgba(15,20,27,0.82) 100%)",
        "sidebar": "linear-gradient(180deg, rgba(18,24,32,0.92) 0%, rgba(15,20,27,0.95) 100%)",
    },
}


def css_for(name: str, body_scrim: str) -> str:
    return f"""/* {name}: photo background + readability overlay */
body::before {{
  content: \"\";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background-image: url(assets/bg.webp);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}}

body::after {{
  content: \"\";
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background: {body_scrim};
}}

.panel-layout {{ position: relative; z-index: 1; }}
.sidebar {{ backdrop-filter: blur(8px); }}
"""


def main() -> None:
    for tid, scrim in SCRIMS.items():
        path = ROOT / tid / "theme.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["author"] = "master3395"
        data["version"] = "1.2.0"
        bg = data.setdefault("background", {})
        bg["body"] = scrim["body"]
        bg["sidebar"] = scrim["sidebar"]
        bg["image"] = "assets/bg.webp"
        bg["preview_image"] = "assets/preview.webp"
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (ROOT / tid / "theme.css").write_text(
            css_for(data["name"], scrim["body"]), encoding="utf-8"
        )
        print("updated", tid)
    print("ok")


if __name__ == "__main__":
    main()
