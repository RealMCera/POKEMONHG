#!/usr/bin/env python3
"""Normalize the HGSS starter overlay before Rare Emerald's main patch pass.

This intentionally touches only the tiny species table used by the native HGSS
starter-selection overlay. It is idempotent and accepts either the stock Johto
trio or an already-converted Emerald trio.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "src/choose_starter_app.c"
MARKER = "RARE_EMERALD_NATIVE_STARTER_CRIES"

OLD = """static const int sSpecies[] = {\n    SPECIES_CHIKORITA,\n    SPECIES_CYNDAQUIL,\n    SPECIES_TOTODILE,\n};"""
NEW = """/* RARE_EMERALD_NATIVE_STARTER_CRIES */\nstatic const int sSpecies[] = {\n    SPECIES_TREECKO,\n    SPECIES_TORCHIC,\n    SPECIES_MUDKIP,\n};"""
ALREADY = """static const int sSpecies[] = {\n    SPECIES_TREECKO,\n    SPECIES_TORCHIC,\n    SPECIES_MUDKIP,\n};"""

text = PATH.read_text(encoding="utf-8")
if MARKER in text:
    print("[Rare Emerald] starter overlay already normalized")
elif OLD in text:
    PATH.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    print("[Rare Emerald] starter overlay converted to Treecko/Torchic/Mudkip")
elif ALREADY in text:
    PATH.write_text(text.replace(ALREADY, NEW, 1), encoding="utf-8")
    print("[Rare Emerald] starter overlay marker restored")
else:
    raise SystemExit("[Rare Emerald] unexpected starter overlay species table")
