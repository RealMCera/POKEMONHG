#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def replace_once(relpath: str, old: str, new: str, marker: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if marker in text or new in text:
        print(f"[Rare Emerald V6] already fixed: {relpath} ({marker})")
        return
    if old not in text:
        raise SystemExit(
            f"[Rare Emerald V6] expected source anchor not found in {relpath}: {marker}"
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"[Rare Emerald V6] fixed: {relpath} ({marker})")


def append_once(relpath: str, block: str, marker: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"[Rare Emerald V6] already appended: {relpath} ({marker})")
        return
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block, encoding="utf-8")
    print(f"[Rare Emerald V6] appended: {relpath} ({marker})")


def set_gmm_english(relpath: str, row_id: str, english: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(<row id="{re.escape(row_id)}"[^>]*>.*?<language name="English">)(.*?)(</language>)',
        re.S,
    )
    match = pat.search(text)
    if not match:
        raise SystemExit(f"[Rare Emerald V6] GMM row not found: {row_id}")
    if match.group(2) == english:
        print(f"[Rare Emerald V6] message already set: {row_id}")
        return
    text = text[:match.start(2)] + english + text[match.end(2):]
    path.write_text(text, encoding="utf-8")
    print(f"[Rare Emerald V6] message set: {row_id}")


# ---------------------------------------------------------------------------
# Route 103: match Emerald. Winning the first rival battle does NOT award the
# Pokedex/Poke Balls on the route; May/Brendan sends the player back to Birch.
# ---------------------------------------------------------------------------
route103 = "files/fielddata/script/scr_seq/scr_seq_0227_R30.s"
replace_once(
    route103,
    """_RareEmeraldRoute103Rewards:
\tHealParty
\tGivePokedex
\tSetFlag FLAG_GOT_POKEDEX
\tGiveItemNoCheck ITEM_POKE_BALL, 5
\tSetVar VAR_SCENE_ROUTE_30_PHONE_CALL, 0
\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_OLDALE
\tReleaseAll
\tEnd""",
    """_RareEmeraldRoute103Rewards:
\t# RARE_EMERALD_ROUTE103_RETURN_TO_LAB_V6
\tSetVar VAR_SCENE_ROUTE_30_PHONE_CALL, 0
\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_RIVAL_BATTLE
\tReleaseAll
\tEnd""",
    "RARE_EMERALD_ROUTE103_RETURN_TO_LAB_V6",
)

route103_msg = "files/msgdata/msg/msg_0375_R30.gmm"
set_gmm_english(
    route103_msg,
    "msg_0375_R30_00001",
    "MAY: I think I know why my dad has an eye out for you now.\\rYour Pokémon already likes you.\\rWell, it's time to head back to the LAB.",
)
set_gmm_english(
    route103_msg,
    "msg_0375_R30_00006",
    "BRENDAN: I think I get why Dad has his eye out for you.\\rYour Pokémon already likes you.\\rWe should head back to the LAB.",
)


# ---------------------------------------------------------------------------
# Birch Lab: after Route 103, trigger a second Rare Emerald lab event. Birch
# gives the Pokedex here, then the player receives the first five Poke Balls.
# ---------------------------------------------------------------------------
lab_hdr = "files/fielddata/script/scr_seq/scr_seq_0616_T20R0101_hdr.s"
replace_once(
    lab_hdr,
    """scr_seq_T20R0101_map_scripts_2:
\tInitScriptGoToIfEqual VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_LAB, _EV_scr_seq_T20R0101_016 + 1
\tInitScriptGoToIfEqual VAR_UNK_40FC, 2, _EV_scr_seq_T20R0101_015 + 1""",
    """scr_seq_T20R0101_map_scripts_2:
\tInitScriptGoToIfEqual VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_LAB, _EV_scr_seq_T20R0101_016 + 1
\tInitScriptGoToIfEqual VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_RIVAL_BATTLE, _EV_scr_seq_T20R0101_017 + 1
\tInitScriptGoToIfEqual VAR_UNK_40FC, 2, _EV_scr_seq_T20R0101_015 + 1""",
    "RARE_EMERALD_CHAPTER_RIVAL_BATTLE, _EV_scr_seq_T20R0101_017",
)

event_hdr = "files/fielddata/script/scr_seq/event_T20R0101.h"
replace_once(
    event_hdr,
    "#define _EV_scr_seq_T20R0101_016            16\n",
    "#define _EV_scr_seq_T20R0101_016            16\n#define _EV_scr_seq_T20R0101_017            17\n",
    "_EV_scr_seq_T20R0101_017",
)

lab_script = "files/fielddata/script/scr_seq/scr_seq_0843_T20R0101.s"
replace_once(
    lab_script,
    "\tScrDef scr_seq_T20R0101_016\n\tScrDefEnd",
    "\tScrDef scr_seq_T20R0101_016\n\tScrDef scr_seq_T20R0101_017\n\tScrDefEnd",
    "ScrDef scr_seq_T20R0101_017",
)

append_once(
    lab_script,
    """
/* RARE_EMERALD_BIRCH_POKEDEX_V6 */
scr_seq_T20R0101_017:
\tScrCmd_609
\tLockAll
\tBufferPlayersName 0
\tNPCMsg msg_0543_T20R0101_00036
\tCloseMsg
\tGivePokedex
\tSetFlag FLAG_GOT_POKEDEX
\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_POKEDEX
\tNPCMsg msg_0543_T20R0101_00037
\tCloseMsg
\tGiveItemNoCheck ITEM_POKE_BALL, 5
\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_OLDALE
\tReleaseAll
\tEnd
""",
    "RARE_EMERALD_BIRCH_POKEDEX_V6",
)

lab_msg = "files/msgdata/msg/msg_0543_T20R0101.gmm"
set_gmm_english(
    lab_msg,
    "msg_0543_T20R0101_00036",
    "Professor Birch: I heard you beat my kid on Route 103!\\rYou have an extensive history as a Trainer in the making.\\rHere, take this Pokédex and help us record the Pokémon of Hoenn!",
)
set_gmm_english(
    lab_msg,
    "msg_0543_T20R0101_00037",
    "Professor Birch: And take these five Poké Balls.\\rNow you can catch Pokémon of your own.\\rYour Hoenn journey starts for real now!",
)

print("[Rare Emerald V6] Emerald-aligned Route 103 -> Birch Lab progression ready")
