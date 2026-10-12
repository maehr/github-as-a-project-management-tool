"""Crop, redact, and annotate raw GitHub screenshots for the course pages.

Input:  assets/screenshots/annotations.yml and the raw captures in
        assets/screenshots/raw/ (not committed; they can show account details).
Output: assets/screenshots/<file>.webp with numbered callouts and a caption bar
        that states the capture date.

Coordinates in annotations.yml refer to the raw capture (1200 x 735 pixels).
Run with ``npm run screenshots:annotate``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "assets" / "screenshots"
RAW = SHOTS / "raw"
SPEC = SHOTS / "annotations.yml"

ACCENT = (232, 89, 12)  # orange, distinct from GitHub's blue and green
WHITE = (255, 255, 255)
BAR = (36, 41, 47)
BAR_HEIGHT = 26
BADGE_RADIUS = 13


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return ImageFont.load_default(size=size)


def shift(box: list[int], crop: list[int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    return x0 - crop[0], y0 - crop[1], x1 - crop[0], y1 - crop[1]


def redact(image: Image.Image, box: tuple[int, int, int, int]) -> None:
    region = image.crop(box).filter(ImageFilter.GaussianBlur(8))
    image.paste(region, box)


def badge(draw: ImageDraw.ImageDraw, center: tuple[int, int], label: str) -> None:
    x, y = center
    r = BADGE_RADIUS
    draw.ellipse((x - r, y - r, x + r, y + r), fill=ACCENT, outline=WHITE, width=2)
    draw.text((x, y), label, fill=WHITE, font=font(15), anchor="mm")


def render(shot: dict[str, Any], captured_default: str) -> Path:
    source = RAW / shot["source"]
    image = Image.open(source).convert("RGB")
    crop = shot.get("crop", [0, 0, image.width, image.height])
    for box in shot.get("redact", []):
        redact(image, tuple(box))
    image = image.crop(tuple(crop))
    draw = ImageDraw.Draw(image)
    for number, callout in enumerate(shot.get("callouts", []), start=1):
        x0, y0, x1, y1 = shift(callout["box"], crop)
        draw.rounded_rectangle((x0, y0, x1, y1), radius=6, outline=ACCENT, width=3)
        bx = max(BADGE_RADIUS + 2, x0 - 4)
        by = max(BADGE_RADIUS + 2, y0 - 4)
        badge(draw, (bx, by), str(number))

    captured = shot.get("captured", captured_default)
    canvas = Image.new("RGB", (image.width, image.height + BAR_HEIGHT), BAR)
    canvas.paste(image, (0, 0))
    bar = ImageDraw.Draw(canvas)
    bar.text(
        (10, image.height + BAR_HEIGHT // 2),
        f"GitHub interface, captured {captured}. Annotations: PROJM course.",
        fill=WHITE,
        font=font(13),
        anchor="lm",
    )
    out = SHOTS / shot["file"]
    canvas.save(out, "WEBP", quality=85, method=6)
    return out


def main() -> None:
    spec = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    missing = [
        s["source"] for s in spec["screenshots"] if not (RAW / s["source"]).exists()
    ]
    if missing:
        raise SystemExit(f"Raw captures missing in {RAW}: {', '.join(missing)}")
    for shot in spec["screenshots"]:
        out = render(shot, str(spec["captured"]))
        print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
