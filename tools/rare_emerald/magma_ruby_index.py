#!/usr/bin/env python3
"""Build a per-member index of Magma Ruby NARCs for Rare Emerald.

This is deliberately read-only. It gives each member a stable category/index,
size and SHA-256 so map/script/event/trainer correlations can be recorded
without copying Platinum-family archives into HGSS.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ARCHIVES = {
    "script": "filesystem/fielddata/script/scr_seq.narc",
    "event": "filesystem/fielddata/eventdata/zone_event.narc",
    "land": "filesystem/fielddata/land_data/land_data.narc",
    "matrix": "filesystem/fielddata/mapmatrix/map_matrix.narc",
    "encounter": "filesystem/fielddata/encountdata/pl_enc_data.narc",
    "trainer_data": "filesystem/poketool/trainer/trdata.narc",
    "trainer_party": "filesystem/poketool/trainer/trpoke.narc",
    "title": "filesystem/demo/title/titledemo.narc",
}


def members(path: Path) -> list[bytes]:
    data = path.read_bytes()
    if data[:4] != b"NARC":
        raise ValueError(f"not a NARC: {path}")
    pos = 0x10
    fat = None
    fimg = None
    while pos + 8 <= len(data):
        tag = data[pos:pos + 4]
        size = int.from_bytes(data[pos + 4:pos + 8], "little")
        if size < 8 or pos + size > len(data):
            break
        if tag in (b"BTAF", b"FATB"):
            fat = data[pos:pos + size]
        elif tag in (b"GMIF", b"FIMG"):
            fimg = data[pos:pos + size]
        pos += size
    if fat is None or fimg is None:
        raise ValueError(f"missing FAT/FIMG blocks: {path}")
    count = int.from_bytes(fat[8:10], "little")
    payload = fimg[8:]
    out = []
    for i in range(count):
        off = 12 + i * 8
        start = int.from_bytes(fat[off:off + 4], "little")
        end = int.from_bytes(fat[off + 4:off + 8], "little")
        out.append(payload[start:end])
    return out


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    ap.add_argument("--out-dir", type=Path, default=Path("build/rare_emerald/magma_ruby_index"))
    args = ap.parse_args()
    root = args.root.resolve()
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    combined = []
    summary = {}
    for category, rel in ARCHIVES.items():
        path = root / rel
        if not path.is_file():
            summary[category] = {"present": False, "path": rel}
            continue
        blobs = members(path)
        rows = []
        for i, blob in enumerate(blobs):
            row = {
                "category": category,
                "member": i,
                "size": len(blob),
                "sha256": digest(blob),
            }
            rows.append(row)
            combined.append(row)
        summary[category] = {"present": True, "path": rel, "members": len(rows)}
        with (out_dir / f"{category}.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=("category", "member", "size", "sha256"))
            w.writeheader()
            w.writerows(rows)

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with (out_dir / "all_members.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=("category", "member", "size", "sha256"))
        w.writeheader()
        w.writerows(combined)
    print(f"[Rare Emerald] indexed {len(combined)} Magma Ruby archive members into {out_dir}")
    for k, v in summary.items():
        if v.get("present"):
            print(f"  {k}: {v['members']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
