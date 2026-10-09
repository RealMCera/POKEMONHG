#!/usr/bin/env python3
"""Inventory a Pokémon Magma Ruby decomp for Rare Emerald migration.

Usage:
    python tools/rare_emerald/magma_ruby_manifest.py /path/to/POKEMON_MAGMA_RUBY_decomp

The tool does not copy proprietary assets. It records the resources that are
present, their hashes/sizes, and how each category should be treated when
migrating the Platinum-family project into the HGSS Rare Emerald engine.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

CATEGORIES = {
    "field_scripts": ("filesystem/fielddata/script/scr_seq.narc", "translate_platinum_to_hgss"),
    "zone_events": ("filesystem/fielddata/eventdata/zone_event.narc", "translate_platinum_to_hgss"),
    "land_data": ("filesystem/fielddata/land_data/land_data.narc", "translate_platinum_to_hgss"),
    "map_matrix": ("filesystem/fielddata/mapmatrix/map_matrix.narc", "translate_platinum_to_hgss"),
    "encounters": ("filesystem/fielddata/encountdata/pl_enc_data.narc", "translate_platinum_to_hgss"),
    "trainer_data": ("filesystem/poketool/trainer/trdata.narc", "translate_platinum_to_hgss"),
    "trainer_parties": ("filesystem/poketool/trainer/trpoke.narc", "translate_platinum_to_hgss"),
    "title_demo": ("filesystem/demo/title/titledemo.narc", "reference_or_extract"),
    "map_names": ("filesystem/fielddata/maptable/mapname.bin", "reference_only"),
    "arm9_strings": ("analysis/arm9_strings.txt", "reference_only"),
    "overlay_map": ("analysis/overlay_map.csv", "reference_only"),
    "header": ("metadata/header.json", "reference_only"),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def narc_member_count(path: Path) -> int | None:
    """Read the FATB entry count from a standard Nitro NARC."""
    try:
        data = path.read_bytes()
        if data[:4] != b"NARC":
            return None
        pos = 0x10
        while pos + 8 <= len(data):
            tag = data[pos:pos + 4]
            size = int.from_bytes(data[pos + 4:pos + 8], "little")
            if tag in (b"BTAF", b"FATB") and pos + 12 <= len(data):
                return int.from_bytes(data[pos + 8:pos + 10], "little")
            if size < 8:
                break
            pos += size
    except OSError:
        pass
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path, help="Extracted POKEMON_MAGMA_RUBY_decomp directory")
    ap.add_argument("--out", type=Path, default=Path("build/rare_emerald/magma_ruby_manifest.json"))
    args = ap.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        raise SystemExit(f"not a directory: {root}")

    rom_info = root / "ROM_INFO.txt"
    manifest = {
        "format": 1,
        "source": "POKEMON MAGMA RUBY decomp",
        "source_root": str(root),
        "policy": {
            "engine": "HGSS",
            "story_authority": "Pokemon Emerald",
            "magma_ruby_role": "DS Hoenn reference and migration source",
            "rule": "Never copy Platinum-family field resources into HGSS blindly; translate IDs, headers, scripts, events, matrices and archive layouts first.",
        },
        "rom_info": rom_info.read_text(encoding="utf-8", errors="replace").splitlines() if rom_info.exists() else [],
        "resources": {},
    }

    for name, (rel, mode) in CATEGORIES.items():
        p = root / rel
        entry = {"path": rel, "mode": mode, "present": p.is_file()}
        if p.is_file():
            entry["size"] = p.stat().st_size
            entry["sha256"] = sha256(p)
            count = narc_member_count(p)
            if count is not None:
                entry["members"] = count
        manifest["resources"][name] = entry

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"[Rare Emerald] wrote {args.out}")
    for name, entry in manifest["resources"].items():
        if entry["present"]:
            suffix = f" ({entry['members']} members)" if "members" in entry else ""
            print(f"  {name}: {entry['mode']}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
