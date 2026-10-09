#!/usr/bin/env python3
"""Correlate Magma Ruby's Platinum-format Hoenn donor maps for Rare Emerald.

This tool is intentionally metadata-only: it does not copy donor assets into the
repository. It decodes the matrix NARC, identifies the early Hoenn cluster that
Magma Ruby placed into Platinum's overworld matrix, and records the land/header
relationships that the HGSS emitter must translate.

Rare Emerald architecture:
    Pokemon Emerald -> story/progression authority
    Magma Ruby      -> DS Hoenn map/visual donor
    pokeplatinum    -> donor-format decoder/reference
    pokeheartgold   -> final engine/runtime and emitted resource format
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

# Platinum map-header slots repurposed by the Magma Ruby early demo.
# Ambiguous multi-cell regions stay grouped until event/script correlation
# resolves their exact Hoenn boundaries.
EARLY_HOENN_HEADER_ROLES = {
    411: "LITTLEROOT_TOWN",        # Platinum Twinleaf Town slot
    342: "ROUTE_101",              # Platinum Route 201 slot
    418: "OLDALE_TOWN",            # Platinum Sandgem Town slot
    343: "ROUTE_102_REGION",       # Platinum Route 202 slot
    344: "ROUTE_103_REGION",       # Platinum Route 203 slot
    3: "PETALBURG_REGION",         # Platinum Jubilife City slot
    345: "ROUTE_104_REGION",       # Platinum Route 204 South slot
    346: "PETALBURG_WOODS_REGION", # Platinum Route 204 North slot
}

PLATINUM_HEADER_NAMES = {
    3: "MAP_HEADER_JUBILIFE_CITY",
    342: "MAP_HEADER_ROUTE_201",
    343: "MAP_HEADER_ROUTE_202",
    344: "MAP_HEADER_ROUTE_203",
    345: "MAP_HEADER_ROUTE_204_SOUTH",
    346: "MAP_HEADER_ROUTE_204_NORTH",
    411: "MAP_HEADER_TWINLEAF_TOWN",
    418: "MAP_HEADER_SANDGEM_TOWN",
}


def narc_members(path: Path) -> list[bytes]:
    data = path.read_bytes()
    if data[:4] != b"NARC":
        raise ValueError(f"not a NARC: {path}")
    pos = 0x10
    fat = fimg = None
    while pos + 8 <= len(data):
        tag = data[pos:pos + 4]
        size = int.from_bytes(data[pos + 4:pos + 8], "little")
        if size < 8 or pos + size > len(data):
            raise ValueError(f"bad NARC block in {path} at {pos:#x}")
        if tag in (b"BTAF", b"FATB"):
            fat = data[pos:pos + size]
        elif tag in (b"GMIF", b"FIMG"):
            fimg = data[pos:pos + size]
        pos += size
    if fat is None or fimg is None:
        raise ValueError(f"missing FAT/FIMG in {path}")
    count = int.from_bytes(fat[8:10], "little")
    payload = fimg[8:]
    out: list[bytes] = []
    for i in range(count):
        off = 12 + i * 8
        start = int.from_bytes(fat[off:off + 4], "little")
        end = int.from_bytes(fat[off + 4:off + 8], "little")
        out.append(payload[start:end])
    return out


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def parse_matrix(blob: bytes) -> dict:
    if len(blob) < 5:
        raise ValueError("matrix member too small")
    width, height, has_headers, has_altitudes, name_len = blob[:5]
    n = width * height
    cursor = 5
    name = blob[cursor:cursor + name_len].rstrip(b"\0").decode("ascii", "replace")
    cursor += name_len
    if has_headers:
        headers = list(struct.unpack_from(f"<{n}H", blob, cursor))
        cursor += n * 2
    else:
        headers = [None] * n
    if has_altitudes:
        altitudes = list(blob[cursor:cursor + n])
        cursor += n
    else:
        altitudes = [0] * n
    if cursor + n * 2 > len(blob):
        raise ValueError("matrix map-model section truncated")
    maps = list(struct.unpack_from(f"<{n}H", blob, cursor))
    return {
        "width": width,
        "height": height,
        "has_headers": bool(has_headers),
        "has_altitudes": bool(has_altitudes),
        "name": name,
        "headers": headers,
        "altitudes": altitudes,
        "maps": maps,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path, help="Extracted POKEMON_MAGMA_RUBY_decomp root")
    ap.add_argument("--out", type=Path, default=Path("build/rare_emerald/magma_ruby_bridge.json"))
    args = ap.parse_args()
    root = args.root.resolve()

    matrix_path = root / "filesystem/fielddata/mapmatrix/map_matrix.narc"
    land_path = root / "filesystem/fielddata/land_data/land_data.narc"
    event_path = root / "filesystem/fielddata/eventdata/zone_event.narc"
    script_path = root / "filesystem/fielddata/script/scr_seq.narc"
    for p in (matrix_path, land_path, event_path, script_path):
        if not p.is_file():
            raise SystemExit(f"missing donor resource: {p}")

    matrices = narc_members(matrix_path)
    lands = narc_members(land_path)
    events = narc_members(event_path)
    scripts = narc_members(script_path)
    overworld = parse_matrix(matrices[0])

    cells = []
    by_role: dict[str, list[dict]] = {}
    for idx, land_id in enumerate(overworld["maps"]):
        header_id = overworld["headers"][idx]
        if header_id not in EARLY_HOENN_HEADER_ROLES:
            continue
        role = EARLY_HOENN_HEADER_ROLES[header_id]
        z, x = divmod(idx, overworld["width"])
        entry = {
            "x": x,
            "z": z,
            "land_member": land_id,
            "land_size": len(lands[land_id]) if land_id < len(lands) else None,
            "land_sha256": sha256(lands[land_id]) if land_id < len(lands) else None,
            "platinum_header_id": header_id,
            "platinum_header_name": PLATINUM_HEADER_NAMES.get(header_id),
            "rare_emerald_role": role,
            "altitude": overworld["altitudes"][idx],
        }
        cells.append(entry)
        by_role.setdefault(role, []).append(entry)

    # Changed donor geometry is concentrated in members 0..19. Preserve all of
    # them in the report, including cells whose exact Hoenn role still needs
    # event/script correlation.
    early_land = []
    for land_id in range(min(20, len(lands))):
        uses = [c for c in cells if c["land_member"] == land_id]
        early_land.append({
            "land_member": land_id,
            "size": len(lands[land_id]),
            "sha256": sha256(lands[land_id]),
            "matrix_uses": uses,
        })

    report = {
        "format": 1,
        "policy": {
            "engine": "HGSS",
            "story_authority": "Pokemon Emerald",
            "donor": "Pokemon Magma Ruby (Platinum-family)",
            "decoder": "pokeplatinum",
            "rule": "Translate donor IDs/headers/events/scripts/land sections into HGSS-native resources; do not copy whole Platinum-family NARCs into HGSS.",
        },
        "donor_counts": {
            "matrices": len(matrices),
            "land_members": len(lands),
            "zone_event_members": len(events),
            "script_members": len(scripts),
        },
        "overworld_matrix": {
            "matrix_member": 0,
            "name": overworld["name"],
            "width": overworld["width"],
            "height": overworld["height"],
        },
        "early_hoenn_cells": cells,
        "early_hoenn_by_role": by_role,
        "early_land_members_0_19": early_land,
        "next_stage": [
            "Correlate each repurposed Platinum header with its Magma Ruby zone-event and script member.",
            "Translate object/warp/script IDs to HGSS constants.",
            "Translate each donor land member's Platinum field-map sections into HGSS land-data sections.",
            "Emit dedicated HGSS matrices/land/event/script sources for Littleroot, Route 101, Oldale, Route 103, then continue through Hoenn.",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"[Rare Emerald] wrote {args.out}")
    print(f"[Rare Emerald] early donor cells: {len(cells)}")
    for role, entries in by_role.items():
        ids = ",".join(str(x["land_member"]) for x in entries)
        print(f"  {role}: land {ids}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
