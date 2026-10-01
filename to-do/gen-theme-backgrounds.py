"""Generate original abstract ops-friendly theme backgrounds (WebP)."""
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1] / "themes"


def clamp(v: float) -> int:
    return max(0, min(255, int(v)))


def mix(a, b, t):
    return tuple(clamp(a[i] + (b[i] - a[i]) * t) for i in range(3))


def noise(img, amount=18, seed=1):
    rnd = random.Random(seed)
    px = img.load()
    w, h = img.size
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            n = rnd.randint(-amount, amount)
            r, g, b = px[x, y][:3]
            c = (clamp(r + n), clamp(g + n), clamp(b + n))
            px[x, y] = c
            if x + 1 < w:
                px[x + 1, y] = c
            if y + 1 < h:
                px[x, y + 1] = c
            if x + 1 < w and y + 1 < h:
                px[x + 1, y + 1] = c
    return img


def vignette(img, strength=0.45):
    w, h = img.size
    overlay = Image.new("RGB", (w, h), (0, 0, 0))
    mask = Image.new("L", (w, h), 0)
    m = mask.load()
    cx, cy = w / 2, h / 2
    maxd = math.hypot(cx, cy)
    for y in range(h):
        for x in range(w):
            d = math.hypot(x - cx, y - cy) / maxd
            m[x, y] = clamp(255 * (d**1.6) * strength)
    return Image.composite(overlay, img, mask)


def linear_base(size, c0, c1, angle_deg=160):
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    ang = math.radians(angle_deg)
    dx, dy = math.cos(ang), math.sin(ang)
    corners = [(0, 0), (w, 0), (0, h), (w, h)]
    projs = [x * dx + y * dy for x, y in corners]
    pmin, pmax = min(projs), max(projs)
    span = max(1e-6, pmax - pmin)
    for y in range(h):
        for x in range(w):
            t = (x * dx + y * dy - pmin) / span
            px[x, y] = mix(c0, c1, t)
    return img


def radial_blob(img, center, radius, color, alpha=0.35):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = center
    for i in range(12, 0, -1):
        rr = int(radius * i / 12)
        a = int(255 * alpha * (i / 12) ** 2)
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(*color, a))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def soft_bands(img, color, y0, amp=40, phase=0.0, alpha=0.25):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = overlay.load()
    for y in range(h):
        for x in range(w):
            wave = math.sin((x / w) * math.pi * 2 * 1.4 + phase) * amp
            d = abs(y - (y0 + wave))
            if d < 90:
                a = int(255 * alpha * (1 - d / 90) ** 2)
                px[x, y] = (*color, a)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def grid_lines(img, color, step=36, alpha=0.12, thick=1):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    col = (*color, int(255 * alpha))
    for x in range(0, w, step):
        draw.line([(x, 0), (x, h)], fill=col, width=thick)
    for y in range(0, h, step):
        draw.line([(0, y), (w, y)], fill=col, width=thick)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def circuits(img, color, seed=7, n=28):
    rnd = random.Random(seed)
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    col = (*color, 160)
    for _ in range(n):
        x = rnd.randint(20, w - 20)
        y = rnd.randint(20, h - 20)
        for __ in range(rnd.randint(3, 7)):
            nx = x + rnd.choice([-1, 0, 1]) * rnd.randint(20, 90)
            ny = y if rnd.random() < 0.55 else y + rnd.choice([-1, 1]) * rnd.randint(16, 70)
            nx = max(10, min(w - 10, nx))
            ny = max(10, min(h - 10, ny))
            draw.line([(x, y), (nx, y)], fill=col, width=2)
            draw.line([(nx, y), (nx, ny)], fill=col, width=2)
            draw.ellipse([nx - 3, ny - 3, nx + 3, ny + 3], fill=(*color, 200))
            x, y = nx, ny
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def dots(img, color, step=22, alpha=0.18, r=1):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    a = int(255 * alpha)
    for y in range(step // 2, h, step):
        for x in range(step // 2, w, step):
            draw.ellipse([x - r, y - r, x + r, y + r], fill=(*color, a))
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def scanlines(img, color, alpha=0.08):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    a = int(255 * alpha)
    for y in range(0, h, 3):
        draw.line([(0, y), (w, y)], fill=(*color, a), width=1)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def strata(img, color, spacing=16, alpha=0.08):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    a = int(255 * alpha)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=(*color, a), width=2)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def brushed(img):
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(-100, h + 220, 10):
        draw.line([(0, y), (w, y - 220)], fill=(148, 163, 184, 18), width=1)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def make_preview(bg: Image.Image) -> Image.Image:
    w, h = bg.size
    top = int(h * 0.18)
    crop = bg.crop((0, top, w, top + int(h * 0.42)))
    return crop.resize((720, 220), Image.Resampling.LANCZOS)


def build(tid: str) -> Image.Image:
    if tid == "arctic-mint":
        return dots(
            vignette(noise(linear_base((1280, 720), (240, 253, 250), (204, 251, 241), 180), 12, 11), 0.25),
            (13, 148, 136),
            22,
            0.22,
            1,
        )
    if tid == "aurora-teal":
        base = vignette(noise(linear_base((1280, 720), (4, 16, 24), (7, 24, 32), 165), 10, 21), 0.5)
        base = radial_blob(base, (int(1280 * 0.3), int(720 * 0.12)), 320, (45, 212, 191), 0.28)
        base = radial_blob(base, (int(1280 * 0.75), int(720 * 0.2)), 260, (103, 232, 249), 0.22)
        base = soft_bands(base, (45, 212, 191), 90, 55, 0.2, 0.22)
        return soft_bands(base, (20, 184, 166), 520, 40, 1.4, 0.16)
    if tid == "copper-circuit":
        base = vignette(noise(linear_base((1280, 720), (7, 16, 28), (12, 26, 46), 155), 8, 31), 0.4)
        return circuits(grid_lines(base, (217, 119, 6), 32, 0.1), (217, 119, 6), 9, 34)
    if tid == "ember-forge":
        base = vignette(noise(linear_base((1280, 720), (20, 12, 8), (36, 20, 12), 155), 12, 41), 0.55)
        base = radial_blob(base, (int(1280 * 0.7), int(720 * 0.92)), 380, (245, 158, 11), 0.32)
        return radial_blob(base, (int(1280 * 0.15), int(720 * 0.2)), 220, (234, 88, 12), 0.16)
    if tid == "forest-night":
        base = vignette(noise(linear_base((1280, 720), (6, 20, 15), (16, 42, 28), 170), 10, 51), 0.5)
        base = radial_blob(base, (int(1280 * 0.15), 0), 300, (52, 211, 153), 0.2)
        return radial_blob(base, (int(1280 * 0.85), 720), 340, (16, 185, 129), 0.16)
    if tid == "graphite-terminal":
        base = vignette(linear_base((1280, 720), (5, 7, 5), (10, 15, 11), 180), 0.4)
        return scanlines(noise(base, 16, 61), (74, 222, 128), 0.1)
    if tid == "high-contrast":
        base = noise(linear_base((1280, 720), (248, 250, 252), (226, 232, 240), 180), 6, 71)
        return grid_lines(base, (15, 23, 42), 28, 0.06)
    if tid == "ocean-blue":
        base = vignette(noise(linear_base((1280, 720), (6, 21, 37), (10, 58, 92), 165), 10, 81), 0.45)
        base = radial_blob(base, (int(1280 * 0.2), int(720 * 0.1)), 340, (56, 189, 248), 0.22)
        base = radial_blob(base, (int(1280 * 0.9), int(720 * 0.85)), 300, (14, 116, 144), 0.24)
        return soft_bands(base, (56, 189, 248), 260, 35, 0.6, 0.12)
    if tid == "sandstone-ops":
        base = vignette(noise(linear_base((1280, 720), (28, 25, 20), (42, 36, 28), 160), 14, 91), 0.4)
        return strata(base, (180, 83, 9), 16, 0.1)
    if tid == "slate-pro":
        base = vignette(noise(linear_base((1280, 720), (15, 20, 27), (26, 34, 46), 160), 10, 101), 0.35)
        return brushed(base)
    raise KeyError(tid)


def main() -> None:
    for tid in sorted(
        [
            "arctic-mint",
            "aurora-teal",
            "copper-circuit",
            "ember-forge",
            "forest-night",
            "graphite-terminal",
            "high-contrast",
            "ocean-blue",
            "sandstone-ops",
            "slate-pro",
        ]
    ):
        out_dir = ROOT / tid / "assets"
        out_dir.mkdir(parents=True, exist_ok=True)
        print("generating", tid, "...")
        bg = build(tid)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=0.6))
        bg = ImageEnhance.Contrast(bg).enhance(1.05)
        preview = make_preview(bg)
        bg_path = out_dir / "bg.webp"
        prev_path = out_dir / "preview.webp"
        bg.save(bg_path, "WEBP", quality=78, method=6)
        preview.save(prev_path, "WEBP", quality=80, method=6)
        print(f"  bg={bg_path.stat().st_size // 1024}KB preview={prev_path.stat().st_size // 1024}KB")
    print("done")


if __name__ == "__main__":
    main()
