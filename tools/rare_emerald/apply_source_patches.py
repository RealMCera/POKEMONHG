#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def patch_once(relpath: str, old: str, new: str, marker: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"[Rare Emerald] already patched: {relpath}")
        return
    if old not in text:
        raise SystemExit(f"[Rare Emerald] expected source anchor not found: {relpath}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"[Rare Emerald] patched: {relpath}")


# The native chooser receives Hoenn Pokemon objects from the field command,
# but HGSS still used the Johto species table for preview cries.
patch_once(
    "src/choose_starter_app.c",
    """static const int sSpecies[] = {\n    SPECIES_CHIKORITA,\n    SPECIES_CYNDAQUIL,\n    SPECIES_TOTODILE,\n};""",
    """/* RARE_EMERALD_NATIVE_STARTER_CRIES */\nstatic const int sSpecies[] = {\n    SPECIES_TREECKO,\n    SPECIES_TORCHIC,\n    SPECIES_MUDKIP,\n};""",
    "RARE_EMERALD_NATIVE_STARTER_CRIES",
)

# Finish the native starter transaction before Birch's Zigzagoon battle.
# ChooseStarter runs the app; ScrCmd_605 commits the selected Pokemon to the
# party, matching Elm's Lab's proven HGSS flow.
patch_once(
    "files/fielddata/script/scr_seq/scr_seq_0225_R29.s",
    """_RareEmeraldBirchRescue:\n\tScrCmd_609\n\tLockAll\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_RESCUE\n\tPlayCry RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, 0\n\tWaitCry\n\tChooseStarter\n\tWildBattle RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, RARE_EMERALD_BIRCH_ZIGZAGOON_LEVEL, 0\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_FIRST_BATTLE\n\tSetVar VAR_UNK_408B, 0\n\tReleaseAll\n\tEnd""",
    """_RareEmeraldBirchRescue:\n\t# RARE_EMERALD_ROUTE101_RESCUE_V2\n\tScrCmd_609\n\tLockAll\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_RESCUE\n\tPlayCry RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, 0\n\tWaitCry\n\tChooseStarter\n\tSetFlag FLAG_GOT_STARTER\n\tScrCmd_605 3, 2\n\tGetPartyMonSpecies 0, VAR_TEMP_x4001\n\tSetStarterChoice VAR_TEMP_x4001\n\tSetVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001\n\tWildBattle RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, RARE_EMERALD_BIRCH_ZIGZAGOON_LEVEL, 0\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_FIRST_BATTLE\n\tSetVar VAR_UNK_408B, 0\n\tReleaseAll\n\tEnd""",
    "RARE_EMERALD_ROUTE101_RESCUE_V2",
)

# Newer Rare Emerald branches replace the New Bark script wholesale with a
# Littleroot shell. Do not try to stack the older incremental T20 patches on
# top of that conversion: their anchors intentionally no longer exist.
t20_relpath = "files/fielddata/script/scr_seq/scr_seq_0842_T20.s"
t20_path = ROOT / t20_relpath
t20_text = t20_path.read_text(encoding="utf-8")

# Self-heal stale working trees produced by an older Rare Emerald patch that
# used a non-existent flag identifier. The live event data uses
# FLAG_HIDE_NEW_BARK_MOM.
if "FLAG_HIDE_NEW_BARK_TOWN_MOM" in t20_text:
    t20_text = t20_text.replace("FLAG_HIDE_NEW_BARK_TOWN_MOM", "FLAG_HIDE_NEW_BARK_MOM")
    t20_path.write_text(t20_text, encoding="utf-8")
    print(f"[Rare Emerald] repaired stale New Bark mom flag: {t20_relpath}")

if "Rare Emerald - Littleroot Town shell" in t20_text:
    print(f"[Rare Emerald] Littleroot shell already converted: {t20_relpath}")
else:
    # The first New Bark outdoor story scene is guaranteed in the stock
    # fresh-game path. Until the real Littleroot matrix is installed, divert
    # that scene into the Emerald Birch rescue so a new save visibly becomes
    # Rare Emerald instead of playing the Johto Marill tutorial.
    patch_once(
        t20_relpath,
        """#include \"constants/scrcmd.h\"\n#include \"fielddata/script/scr_seq/event_T20.h\"""",
        """#include \"constants/scrcmd.h\"\n#include \"constants/rare_emerald.h\"\n#include \"fielddata/script/scr_seq/event_T20.h\"""",
        "constants/rare_emerald.h",
    )

    patch_once(
        t20_relpath,
        """scr_seq_T20_002:\n\tScrCmd_609\n\tLockAll""",
        """scr_seq_T20_002:\n\tCompare VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_LITTLEROOT\n\tGoToIfEq _RareEmeraldFreshGameRescue\n\tScrCmd_609\n\tLockAll""",
        "_RareEmeraldFreshGameRescue",
    )

    patch_once(
        t20_relpath,
        """_075A:\n\tScrCmd_307 21, 12, 12, 9, 77""",
        """_RareEmeraldFreshGameRescue:\n\t# RARE_EMERALD_FRESH_GAME_RESCUE_V1\n\tScrCmd_609\n\tLockAll\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_RESCUE\n\tPlayCry RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, 0\n\tWaitCry\n\tChooseStarter\n\tSetFlag FLAG_GOT_STARTER\n\tScrCmd_605 3, 2\n\tGetPartyMonSpecies 0, VAR_TEMP_x4001\n\tSetStarterChoice VAR_TEMP_x4001\n\tSetVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001\n\tWildBattle RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, RARE_EMERALD_BIRCH_ZIGZAGOON_LEVEL, 0\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_FIRST_BATTLE\n\tSetVar VAR_SCENE_NEW_BARK_TOWN_OW, 2\n\tReleaseAll\n\tEnd\n\n_075A:\n\tScrCmd_307 21, 12, 12, 9, 77""",
        "RARE_EMERALD_FRESH_GAME_RESCUE_V1",
    )

print("[Rare Emerald] native source patches ready")
