#!/usr/bin/env python3
"""Rare Emerald: inspect a local Pokemon Magma Ruby extraction.

This tool deliberately never copies ROM/NARC data into the source tree. It
unpacks selected NARCs into a local work directory and emits JSON manifests.
If a clean Platinum extraction is supplied, it also identifies exactly which
archive members Magma Ruby changed, which is the fastest way to isolate its
Hoenn-specific DS maps, events, scripts, textures, and building models.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import Path

ARCHIVES = {
    "land_data": "filesystem/fielddata/land_data/land_data.narc",
    "map_matrix": "filesystem/fielddata/mapmatrix/map_matrix.narc",
    "zone_event": "filesystem/fielddata/eventdata/zone_event.narc",
    "scr_seq": "filesystem/fielddata/script/scr_seq.narc",
    "area_data": "filesystem/fielddata/areadata/area_data.narc",
    "map_tex_set": "filesystem/fielddata/areadata/area_map_tex/map_tex_set.narc",
    "build_model": "filesystem/fielddata/build_model/build_model.narc",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class NarcMember:
    index: int
    data: bytes


def _u16(data: bytes, off: int) -> int:
    return struct.unpack_from("<H", data, off)[0]


def _u32(data: bytes, off: int) -> int:
    return struct.unpack_from("<I", data, off)[0]


def unpack_narc(path: Path) -> list[NarcMember]:
    blob = path.read_bytes()
    if blob[:4] != b"NARC":
        raise ValueError(f"not a NARC: {path}")

    pos = 0x10
    if blob[pos:pos + 4] != b"BTAF":
        raise ValueError(f"missing BTAF: {path}")
    btaf_size = _u32(blob, pos + 4)
    count = _u16(blob, pos + 8)
    entries = []
    ent = pos + 0x0C
    for i in range(count):
        start = _u32(blob, ent + i * 8)
        end = _u32(blob, ent + i * 8 + 4)
        entries.append((start, end))

    pos += btaf_size
    if blob[pos:pos + 4] != b"BTNF":
        raise ValueError(f"missing BTNF: {path}")
    pos += _u32(blob, pos + 4)
    if blob[pos:pos + 4] not in (b"GMIF", b"FIMG"):
        raise ValueError(f"missing GMIF/FIMG: {path}")
    data_base = pos + 8

    return [NarcMember(i, blob[data_base + a:data_base + b]) for i, (a, b) in enumerate(entries)]


def archive_manifest(path: Path) -> dict:
    members = unpack_narc(path)
    return {
        "path": str(path),
        "archive_sha256": sha256(path.read_bytes()),
        "member_count": len(members),
        "members": [
            {"index": m.index, "size": len(m.data), "sha256": sha256(m.data)}
            for m in members
        ],
    }


def write_members(path: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for member in unpack_narc(path):
        (out_dir / f"{member.index:04d}.bin").write_bytes(member.data)


def diff_archives(mod_path: Path, base_path: Path) -> dict:
    mod = {m.index: m.data for m in unpack_narc(mod_path)}
    base = {m.index: m.data for m in unpack_narc(base_path)}
    indexes = sorted(set(mod) | set(base))
    changed = []
    for i in indexes:
        a, b = mod.get(i), base.get(i)
        if a == b:
            continue
        changed.append({
            "index": i,
            "magma_size": None if a is None else len(a),
            "platinum_size": None if b is None else len(b),
            "magma_sha256": None if a is None else sha256(a),
            "platinum_sha256": None if b is None else sha256(b),
            "status": "added" if b is None else "removed" if a is None else "changed",
        })
    return {
        "magma_member_count": len(mod),
        "platinum_member_count": len(base),
        "changed_count": len(changed),
        "changed": changed,
    }


def resolve_root(path: Path) -> Path:
    path = path.resolve()
    if (path / "metadata" / "header.json").exists():
        return path
    children = [p for p in path.iterdir() if p.is_dir()] if path.is_dir() else []
    matches = [p for p in children if (p / "metadata" / "header.json").exists()]
    if len(matches) == 1:
        return matches[0]
    raise SystemExit(f"Could not identify extraction root under {path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("magma", type=Path, help="POKEMON_MAGMA_RUBY_decomp extraction directory")
    ap.add_argument("--platinum", type=Path, help="optional clean Platinum extraction in the same extractor layout")
    ap.add_argument("--out", type=Path, default=Path(".rare_emerald/magma_ruby"))
    ap.add_argument("--unpack", action="store_true", help="write selected member binaries to the local work directory")
    args = ap.parse_args()

    magma = resolve_root(args.magma)
    platinum = resolve_root(args.platinum) if args.platinum else None
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    header = json.loads((magma / "metadata" / "header.json").read_text(encoding="utf-8"))
    result = {
        "source": {
            "title": header.get("title"),
            "game_code": header.get("game_code"),
            "root": str(magma),
        },
        "archives": {},
    }

    for name, rel in ARCHIVES.items():
        mod_path = magma / rel
        if not mod_path.exists():
            raise SystemExit(f"Missing required Magma Ruby archive: {mod_path}")
        entry = archive_manifest(mod_path)
        if args.unpack:
            write_members(mod_path, out / "members" / name)
        if platinum:
            base_path = platinum / rel
            if base_path.exists():
                entry["platinum_diff"] = diff_archives(mod_path, base_path)
            else:
                entry["platinum_diff"] = {"error": f"missing {rel}"}
        result["archives"][name] = entry
        extra = ""
        if "platinum_diff" in entry and "changed_count" in entry["platinum_diff"]:
            extra = f", {entry['platinum_diff']['changed_count']} changed vs Platinum"
        print(f"[Rare Emerald] {name}: {entry['member_count']} members{extra}")

    manifest = out / "manifest.json"
    manifest.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"[Rare Emerald] wrote {manifest}")
    if platinum:
        candidates = {
            name: [x["index"] for x in data.get("platinum_diff", {}).get("changed", [])]
            for name, data in result["archives"].items()
        }
        cpath = out / "changed_members.json"
        cpath.write_text(json.dumps(candidates, indent=2) + "\n", encoding="utf-8")
        print(f"[Rare Emerald] wrote {cpath}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
