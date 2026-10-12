#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def set_gmm_english(relpath: str, row_id: str, english: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(<row id="{re.escape(row_id)}"[^>]*>.*?<language name="English">)(.*?)(</language>)',
        re.S,
    )
    match = pat.search(text)
    if not match:
        raise SystemExit(f"[Rare Emerald V7] GMM row not found: {row_id}")
    if match.group(2) == english:
        print(f"[Rare Emerald V7] message already set: {row_id}")
        return
    text = text[:match.start(2)] + english + text[match.end(2):]
    path.write_text(text, encoding="utf-8")
    print(f"[Rare Emerald V7] message set: {row_id}")


# HGSS msgenc does not accept straight ASCII apostrophes in these GMM strings.
# Keep the Route 103 dialogue contraction-free so it compiles cleanly and does
# not depend on a typography-specific character mapping.
route103_msg = "files/msgdata/msg/msg_0375_R30.gmm"
set_gmm_english(
    route103_msg,
    "msg_0375_R30_00000",
    "MAY: Oh, hi!\\rI was checking the Pokémon around here.\\rLet us have a quick battle!",
)
set_gmm_english(
    route103_msg,
    "msg_0375_R30_00001",
    "MAY: I think I know why my dad has an eye out for you now.\\rYour Pokémon already likes you.\\rWell, it is time to head back to the LAB.",
)
set_gmm_english(
    route103_msg,
    "msg_0375_R30_00005",
    "BRENDAN: Hey!\\rI was checking the Pokémon around here.\\rLet us have a quick battle!",
)
set_gmm_english(
    route103_msg,
    "msg_0375_R30_00006",
    "BRENDAN: I think I get why Dad has his eye out for you.\\rYour Pokémon already likes you.\\rWe should head back to the LAB.",
)

print("[Rare Emerald V7] Route 103 message encoding normalized")
