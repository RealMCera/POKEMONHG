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


def append_once(relpath: str, block: str, marker: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"[Rare Emerald] already appended: {relpath}")
        return
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block, encoding="utf-8")
    print(f"[Rare Emerald] appended: {relpath}")


# ---------------------------------------------------------------------------
# Native HGSS starter chooser -> Emerald trio
# ---------------------------------------------------------------------------
# The field-side chooser creates Treecko/Torchic/Mudkip on the rare-emerald
# branch.  The overlay also has its own species table for preview sprites/cries,
# so keep the overlay table in sync with the Pokemon actually being created.
patch_once(
    "src/choose_starter_app.c",
    """static const int sSpecies[] = {\n    SPECIES_CHIKORITA,\n    SPECIES_CYNDAQUIL,\n    SPECIES_TOTODILE,\n};""",
    """/* RARE_EMERALD_NATIVE_STARTER_CRIES */\nstatic const int sSpecies[] = {\n    SPECIES_TREECKO,\n    SPECIES_TORCHIC,\n    SPECIES_MUDKIP,\n};""",
    "RARE_EMERALD_NATIVE_STARTER_CRIES",
)


# ---------------------------------------------------------------------------
# Route 101 / Birch rescue
# ---------------------------------------------------------------------------
# First normalize older working trees to the V2 transaction if needed.
patch_once(
    "files/fielddata/script/scr_seq/scr_seq_0225_R29.s",
    """_RareEmeraldBirchRescue:\n\tScrCmd_609\n\tLockAll\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_RESCUE\n\tPlayCry RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, 0\n\tWaitCry\n\tChooseStarter\n\tWildBattle RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, RARE_EMERALD_BIRCH_ZIGZAGOON_LEVEL, 0\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_FIRST_BATTLE\n\tSetVar VAR_UNK_408B, 0\n\tReleaseAll\n\tEnd""",
    """_RareEmeraldBirchRescue:\n\t# RARE_EMERALD_ROUTE101_RESCUE_V2\n\tScrCmd_609\n\tLockAll\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_RESCUE\n\tPlayCry RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, 0\n\tWaitCry\n\tChooseStarter\n\tSetFlag FLAG_GOT_STARTER\n\tScrCmd_605 3, 2\n\tGetPartyMonSpecies 0, VAR_TEMP_x4001\n\tSetStarterChoice VAR_TEMP_x4001\n\tSetVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001\n\tWildBattle RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, RARE_EMERALD_BIRCH_ZIGZAGOON_LEVEL, 0\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_FIRST_BATTLE\n\tSetVar VAR_UNK_408B, 0\n\tReleaseAll\n\tEnd""",
    "RARE_EMERALD_ROUTE101_RESCUE_V",
)

# V3 owns the whole Emerald transaction on Route 101: save the selected starter,
# derive May/Brendan's counter-pick, fight Zigzagoon, heal, then go to Birch Lab.
patch_once(
    "files/fielddata/script/scr_seq/scr_seq_0225_R29.s",
    """_RareEmeraldBirchRescue:\n\t# RARE_EMERALD_ROUTE101_RESCUE_V2\n\tScrCmd_609\n\tLockAll\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_RESCUE\n\tPlayCry RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, 0\n\tWaitCry\n\tChooseStarter\n\tSetFlag FLAG_GOT_STARTER\n\tScrCmd_605 3, 2\n\tGetPartyMonSpecies 0, VAR_TEMP_x4001\n\tSetStarterChoice VAR_TEMP_x4001\n\tSetVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001\n\tWildBattle RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, RARE_EMERALD_BIRCH_ZIGZAGOON_LEVEL, 0\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_FIRST_BATTLE\n\tSetVar VAR_UNK_408B, 0\n\tReleaseAll\n\tEnd""",
    """_RareEmeraldBirchRescue:\n\t# RARE_EMERALD_ROUTE101_RESCUE_V3\n\tScrCmd_609\n\tLockAll\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_RESCUE\n\tPlayCry RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, 0\n\tWaitCry\n\tChooseStarter\n\tSetFlag FLAG_GOT_STARTER\n\tGetPartyMonSpecies 0, VAR_TEMP_x4001\n\tSetStarterChoice VAR_TEMP_x4001\n\tSetVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001\n\tCompare VAR_TEMP_x4001, RARE_EMERALD_STARTER_TREECKO\n\tGoToIfEq _RareEmeraldRivalTorchic\n\tCompare VAR_TEMP_x4001, RARE_EMERALD_STARTER_TORCHIC\n\tGoToIfEq _RareEmeraldRivalMudkip\n\tSetVar VAR_RARE_EMERALD_RIVAL_SPECIES, RARE_EMERALD_RIVAL_FOR_MUDKIP\n\tGoTo _RareEmeraldStarterStored\n\n_RareEmeraldRivalTorchic:\n\tSetVar VAR_RARE_EMERALD_RIVAL_SPECIES, RARE_EMERALD_RIVAL_FOR_TREECKO\n\tGoTo _RareEmeraldStarterStored\n\n_RareEmeraldRivalMudkip:\n\tSetVar VAR_RARE_EMERALD_RIVAL_SPECIES, RARE_EMERALD_RIVAL_FOR_TORCHIC\n\n_RareEmeraldStarterStored:\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_STARTER_SELECTED\n\tWildBattle RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, RARE_EMERALD_BIRCH_ZIGZAGOON_LEVEL, 0\n\tHealParty\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_LAB\n\tSetVar VAR_UNK_408B, 0\n\tReleaseAll\n\tWarp MAP_RARE_EMERALD_BIRCH_LAB, 0, 4, 13, DIR_NORTH\n\tEnd""",
    "RARE_EMERALD_ROUTE101_RESCUE_V3",
)


# ---------------------------------------------------------------------------
# Littleroot shell -> Route 101 handoff
# ---------------------------------------------------------------------------
t20_relpath = "files/fielddata/script/scr_seq/scr_seq_0842_T20.s"
t20_path = ROOT / t20_relpath
t20_text = t20_path.read_text(encoding="utf-8")

# Self-heal stale working trees produced by an older Rare Emerald patch that
# used a non-existent flag identifier.
if "FLAG_HIDE_NEW_BARK_TOWN_MOM" in t20_text:
    t20_text = t20_text.replace("FLAG_HIDE_NEW_BARK_TOWN_MOM", "FLAG_HIDE_NEW_BARK_MOM")
    t20_path.write_text(t20_text, encoding="utf-8")
    print(f"[Rare Emerald] repaired stale New Bark mom flag: {t20_relpath}")

if "Rare Emerald - Littleroot Town shell" in t20_text:
    # Converted shells used to run the entire starter/battle sequence at the
    # Littleroot west edge.  V3 makes that edge only change campaign state;
    # R29/Route 101 owns the rescue exactly once.
    patch_once(
        t20_relpath,
        """_RareEmeraldLittlerootExit:\n\tLockAll\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_RESCUE\n\tPlayCry RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, 0\n\tWaitCry\n\tChooseStarter\n\tSetFlag FLAG_GOT_STARTER\n\tScrCmd_605 3, 2\n\tGetPartyMonSpecies 0, VAR_TEMP_x4001\n\tSetStarterChoice VAR_TEMP_x4001\n\tSetVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001\n\tWildBattle RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, RARE_EMERALD_BIRCH_ZIGZAGOON_LEVEL, 0\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_FIRST_BATTLE\n\tSetVar VAR_SCENE_NEW_BARK_WEST_EXIT, 1\n\tSetFlag FLAG_HIDE_NEW_BARK_MOM\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_LAB\n\tReleaseAll\n\tWarp MAP_RARE_EMERALD_BIRCH_LAB, 0, 4, 13, DIR_NORTH\n\tEnd""",
        """_RareEmeraldLittlerootExit:\n\t# RARE_EMERALD_LITTLEROOT_ROUTE101_HANDOFF_V3\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_ROUTE_101\n\tSetVar VAR_SCENE_NEW_BARK_WEST_EXIT, 1\n\tEnd""",
        "RARE_EMERALD_LITTLEROOT_ROUTE101_HANDOFF_V3",
    )
    patch_once(
        t20_relpath,
        """scr_seq_T20_009:\n\tCompare VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_LITTLEROOT\n\tGoToIfEq _RareEmeraldLittlerootExit\n\tEnd""",
        """scr_seq_T20_009:\n\t# RARE_EMERALD_LITTLEROOT_NO_RESUME_RESCUE_V3\n\tEnd""",
        "RARE_EMERALD_LITTLEROOT_NO_RESUME_RESCUE_V3",
    )
    print(f"[Rare Emerald] Littleroot shell upgraded to Route 101 handoff: {t20_relpath}")
else:
    # Compatibility path for an older stock-New-Bark working tree.
    patch_once(
        t20_relpath,
        """#include \"constants/scrcmd.h\"\n#include \"fielddata/script/scr_seq/event_T20.h\"""",
        """#include \"constants/scrcmd.h\"\n#include \"constants/rare_emerald.h\"\n#include \"fielddata/script/scr_seq/event_T20.h\"""",
        "constants/rare_emerald.h",
    )
    print(f"[Rare Emerald] stock T20 compatibility path retained: {t20_relpath}")


# ---------------------------------------------------------------------------
# Birch Lab post-rescue handoff
# ---------------------------------------------------------------------------
patch_once(
    "files/fielddata/script/scr_seq/scr_seq_0616_T20R0101_hdr.s",
    """#include \"constants/scrcmd.h\"\n#include \"fielddata/script/scr_seq/event_T20R0101.h\"""",
    """#include \"constants/scrcmd.h\"\n#include \"constants/rare_emerald.h\"\n#include \"fielddata/script/scr_seq/event_T20R0101.h\"""",
    "constants/rare_emerald.h",
)
patch_once(
    "files/fielddata/script/scr_seq/scr_seq_0616_T20R0101_hdr.s",
    """scr_seq_T20R0101_map_scripts_2:\n\tInitScriptGoToIfEqual VAR_UNK_40FC, 2, _EV_scr_seq_T20R0101_015 + 1""",
    """scr_seq_T20R0101_map_scripts_2:\n\tInitScriptGoToIfEqual VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_LAB, _EV_scr_seq_T20R0101_016 + 1\n\tInitScriptGoToIfEqual VAR_UNK_40FC, 2, _EV_scr_seq_T20R0101_015 + 1""",
    "_EV_scr_seq_T20R0101_016",
)

patch_once(
    "files/fielddata/script/scr_seq/event_T20R0101.h",
    "#define _EV_scr_seq_T20R0101_015            15\n",
    "#define _EV_scr_seq_T20R0101_015            15\n#define _EV_scr_seq_T20R0101_016            16\n",
    "_EV_scr_seq_T20R0101_016",
)

patch_once(
    "files/fielddata/script/scr_seq/scr_seq_0843_T20R0101.s",
    """#include \"constants/scrcmd.h\"\n#include \"fielddata/script/scr_seq/event_T20R0101.h\"""",
    """#include \"constants/scrcmd.h\"\n#include \"constants/rare_emerald.h\"\n#include \"fielddata/script/scr_seq/event_T20R0101.h\"""",
    "constants/rare_emerald.h",
)
patch_once(
    "files/fielddata/script/scr_seq/scr_seq_0843_T20R0101.s",
    """\tScrDef scr_seq_T20R0101_015\n\tScrDefEnd""",
    """\tScrDef scr_seq_T20R0101_015\n\tScrDef scr_seq_T20R0101_016\n\tScrDefEnd""",
    "ScrDef scr_seq_T20R0101_016",
)

append_once(
    "files/fielddata/script/scr_seq/scr_seq_0843_T20R0101.s",
    """\n/* RARE_EMERALD_BIRCH_LAB_HANDOFF_V1 */\nscr_seq_T20R0101_016:\n\tScrCmd_609\n\tLockAll\n\tBufferPlayersName 0\n\tBufferMonSpeciesName 1, 0\n\tNPCMsg msg_0543_T20R0101_00007\n\tPlayFanfare SEQ_ME_POKEGET\n\tWaitFanfare\n\tTouchscreenMenuHide\n\tBufferMonSpeciesName 1, 0\n\tNPCMsg msg_0543_T20R0101_00008\n\tGetMenuChoice VAR_SPECIAL_RESULT\n\tCloseMsg\n\tCompare VAR_SPECIAL_RESULT, 0\n\tCallIfEq _02EE\n\tTouchscreenMenuShow\n\tNPCMsg msg_0543_T20R0101_00010\n\tCloseMsg\n\tNPCMsg msg_0543_T20R0101_00011\n\tCloseMsg\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_ROUTE_103\n\tReleaseAll\n\tEnd\n""",
    "RARE_EMERALD_BIRCH_LAB_HANDOFF_V1",
)

# Keep Birch's lab text aligned with Emerald while reusing HGSS message slots.
patch_once(
    "files/msgdata/msg/msg_0543_T20R0101.gmm",
    "{STRVAR_1 3, 0, 0} received {STRVAR_1 0, 1, 0}\\nfrom Professor Elm!",
    "Professor Birch: {STRVAR_1 3, 0, 0}!\\nThanks for saving me out there.\\rThat {STRVAR_1 0, 1, 0} battled really well.\\rI want you to keep it!",
    "Thanks for saving me out there.",
)
patch_once(
    "files/msgdata/msg/msg_0543_T20R0101.gmm",
    "Professor Elm: How do you like walking\\nwith your Pokémon? It’s not bad, is it?\\rYou can take it all the way to\\nMr. Pokémon’s house.\\rIf your Pokémon gets hurt...\\r",
    "Professor Birch: You already have a good\\nfeel for Pokémon.\\rMy kid is up on Route 103 helping\\nwith field research.\\rGo introduce yourself and have a battle!",
    "My kid is up on Route 103",
)
patch_once(
    "files/msgdata/msg/msg_0543_T20R0101.gmm",
    "You should heal it with this machine.\\rIt’s so easy to use.\\nJust check the PC on my desk!\\r",
    "Professor Birch: Head north through\\nRoute 101 and Oldale Town.\\rRoute 103 is just beyond it.\\rI’ll be waiting to hear how it goes!",
    "Route 103 is just beyond it.",
)

print("[Rare Emerald] native source patches ready (opening V3)")
