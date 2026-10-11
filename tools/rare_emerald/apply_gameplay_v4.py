#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(relpath: str, old: str, new: str, marker: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if new in text:
        print(f"[Rare Emerald V4] already fixed: {relpath} ({marker})")
        return
    if old not in text:
        raise SystemExit(
            f"[Rare Emerald V4] expected source anchor not found in {relpath}: {marker}"
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"[Rare Emerald V4] fixed: {relpath} ({marker})")


# Route 101: SetVar stores a literal. The starter species is held in another
# script variable, so this must be CopyVar or a save/reload remembers 0x4001
# instead of Treecko/Torchic/Mudkip.
route101 = "files/fielddata/script/scr_seq/scr_seq_0225_R29.s"
route101_text = (ROOT / route101).read_text(encoding="utf-8")
if "RARE_EMERALD_ROUTE101_RESCUE_V3" not in route101_text:
    raise SystemExit("[Rare Emerald V4] Route 101 V3 patch must run before V4")

replace_once(
    route101,
    "\tSetVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001",
    "\tCopyVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001",
    "persist selected starter species",
)

print("[Rare Emerald V4] gameplay corrections ready")
