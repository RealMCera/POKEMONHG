#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit(
        "Pillow is required for title conversion. Run: python -m pip install pillow"
    ) from exc

DS_SIZE = (256, 192)
TILES_W = 32
TILES_H = 24


def prepare_png(src: Path, dst: Path) -> None:
    image = Image.open(src)
    if image.size != DS_SIZE:
        raise SystemExit(f"{src} must be exactly 256x192; got {image.size[0]}x{image.size[1]}")

    # Preserve the source PNG untouched. This build intermediate is the
    # palette-indexed representation required by Nintendo DS tiled BG hardware.
    rgb = image.convert("RGB")
    indexed = rgb.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    dst.parent.mkdir(parents=True, exist_ok=True)
    indexed.save(dst, format="PNG", optimize=False)


def write_tilemap(dst: Path) -> None:
    # nitrogfx's JSON->NSCR path expects Tiled-style 1-based tile indices.
    # A full 256x192 image is 32x24 tiles laid out in simple row-major order.
    data = list(range(1, TILES_W * TILES_H + 1))
    obj = {
        "height": TILES_H,
        "width": TILES_W,
        "layers": [{"data": data}],
        "tilesets": [{}],
    }
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(obj, separators=(",", ":")), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=Path, required=True)
    parser.add_argument("--bottom", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    prepare_png(args.top, args.out_dir / "first_movie_top.indexed.png")
    prepare_png(args.bottom, args.out_dir / "first_movie_bottom.indexed.png")
    write_tilemap(args.out_dir / "first_movie_top.json")
    write_tilemap(args.out_dir / "first_movie_bottom.json")


if __name__ == "__main__":
    main()
