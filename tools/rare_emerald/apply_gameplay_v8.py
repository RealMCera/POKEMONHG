#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]


def replace_regex_once(relpath: str, pattern: str, replacement: str, marker: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"[Rare Emerald V8] already fixed: {relpath} ({marker})")
        return
    new_text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"[Rare Emerald V8] expected source block not found in {relpath}: {marker}")
    path.write_text(new_text, encoding="utf-8")
    print(f"[Rare Emerald V8] fixed: {relpath} ({marker})")


def replace_whole_file(relpath: str, replacement: str, marker: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"[Rare Emerald V8] already fixed: {relpath} ({marker})")
        return
    path.write_text(replacement, encoding="utf-8")
    print(f"[Rare Emerald V8] replaced: {relpath} ({marker})")


def set_gmm_english(relpath: str, row_id: str, english: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(<row id="{re.escape(row_id)}"[^>]*>.*?<language name="English">)(.*?)(</language>)',
        re.S,
    )
    match = pat.search(text)
    if not match:
        raise SystemExit(f"[Rare Emerald V8] GMM row not found: {row_id}")
    if match.group(2) == english:
        print(f"[Rare Emerald V8] message already set: {row_id}")
        return
    text = text[:match.start(2)] + english + text[match.end(2):]
    path.write_text(text, encoding="utf-8")
    print(f"[Rare Emerald V8] message set: {row_id}")


# ---------------------------------------------------------------------------
# Player house: replace the stock HGSS Lyra/Ethan/Elm opening with a clean
# Emerald-style Littleroot introduction.  We keep the native HGSS map shell,
# menu unlock flags and Mom NPC, but none of the Johto opening state machine.
# ---------------------------------------------------------------------------
house_script = "files/fielddata/script/scr_seq/scr_seq_0845_T20R0201.s"

replace_regex_once(
    house_script,
    r"scr_seq_T20R0201_000:\n.*?(?=\n\t\.balign 4, 0\n_00A4:)",
    """scr_seq_T20R0201_000:\n\t# RARE_EMERALD_PLAYER_HOUSE_INTRO_V8\n\tScrCmd_609\n\tLockAll\n\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_LITTLEROOT\n\tSetFlag FLAG_GOT_BAG\n\tSetFlag FLAG_GOT_TRAINER_CARD\n\tSetFlag FLAG_GOT_SAVE_BUTTON\n\tSetFlag FLAG_GOT_OPTIONS_BUTTON\n\tSetFlag FLAG_HIDE_NEW_BARK_MARILL\n\tSetFlag FLAG_HIDE_NEW_BARK_FRIEND\n\tSetFlag FLAG_HIDE_NEW_BARK_FRIEND_2\n\tSetFlag FLAG_HIDE_NEW_BARK_RIVAL\n\tSetFlag FLAG_HIDE_NEW_BARK_MOM\n\tSetFlag FLAG_HIDE_ROUTE_29_FRIEND\n\tSetFlag FLAG_HIDE_ROUTE_29_MARILL\n\tBufferPlayersName 0\n\tNPCMsg msg_0545_T20R0201_00000\n\tCloseMsg\n\tSetVar VAR_SCENE_PLAYERS_HOUSE_1F, 1\n\tReleaseAll\n\tEnd\n""",
    "RARE_EMERALD_PLAYER_HOUSE_INTRO_V8",
)

# Disable the second stock house intro hook completely.  It is tied to the
# Johto scene variable and can otherwise replay Elm-oriented dialogue later.
replace_regex_once(
    house_script,
    r"scr_seq_T20R0201_006:\n.*?(?=\nscr_seq_T20R0201_001:)",
    """scr_seq_T20R0201_006:\n\t# RARE_EMERALD_PLAYER_HOUSE_NO_JOHTO_REPLAY_V8\n\tEnd\n\n""",
    "RARE_EMERALD_PLAYER_HOUSE_NO_JOHTO_REPLAY_V8",
)

# Mom remains usable as an ordinary NPC, but her dialogue is chapter-aware and
# no longer grants the Pokegear or points the player toward Professor Elm.
replace_regex_once(
    house_script,
    r"scr_seq_T20R0201_001:\n.*?(?=\nscr_seq_T20R0201_002:)",
    """scr_seq_T20R0201_001:\n\t# RARE_EMERALD_MOM_DIALOGUE_V8\n\tPlaySE SEQ_SE_DP_SELECT\n\tLockAll\n\tFacePlayer\n\tCompare VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_LAB\n\tGoToIfGe _RareEmeraldMomAfterStarterV8\n\tNPCMsg msg_0545_T20R0201_00006\n\tWaitButton\n\tCloseMsg\n\tReleaseAll\n\tEnd\n\n_RareEmeraldMomAfterStarterV8:\n\tNPCMsg msg_0545_T20R0201_00007\n\tWaitButton\n\tCloseMsg\n\tReleaseAll\n\tEnd\n\n""",
    "RARE_EMERALD_MOM_DIALOGUE_V8",
)


# ---------------------------------------------------------------------------
# Littleroot outdoor shell: remove the stock New Bark on-frame/on-resume hooks.
# Those hooks own the Lyra/Marill/Elm scenes and were also capable of leaving
# the field in a locked/waiting state after the player walked out of the house.
# Native map transitions remain, and the existing west-edge coordinate script
# still advances Rare Emerald from Littleroot to Route 101.
# ---------------------------------------------------------------------------
replace_whole_file(
    "files/fielddata/script/scr_seq/scr_seq_0615_T20_hdr.s",
    """#include \"constants/scrcmd.h\"\n#include \"constants/rare_emerald.h\"\n#include \"fielddata/script/scr_seq/event_T20.h\"\n#include \"constants/init_script_types.h\"\n\t.include \"asm/macros/script.inc\"\n\n\t.rodata\n\t.option alignment off\n\n\t# RARE_EMERALD_LITTLEROOT_HEADER_V8\n\t# No stock New Bark OnFrame/OnResume story hooks.\n\tInitScriptEntry_OnTransition _EV_scr_seq_T20_006 + 1\n\tInitScriptEntryEnd\n\n\tInitScriptEnd\n""",
    "RARE_EMERALD_LITTLEROOT_HEADER_V8",
)


# ---------------------------------------------------------------------------
# Emerald-correct opening dialogue for the temporary HGSS player-house shell.
# The wording follows Emerald's moving-in/Littleroot setup while staying short
# enough for the current DS scene.  No Lyra, Ethan, Marill, Elm or Johto task
# language is allowed in these opening rows.
# ---------------------------------------------------------------------------
house_msg = "files/msgdata/msg/msg_0545_T20R0201.gmm"
set_gmm_english(
    house_msg,
    "msg_0545_T20R0201_00000",
    "MOM: See, {STRVAR_1 3, 0, 0}?\\nIt is nice in here, too!\\rThe movers and their POKEMON did all\\nthe work of moving us in.\\rThis is so convenient!\\rPROF. BIRCH lives nearby.\\rGo explore LITTLEROOT when you are ready.",
)
set_gmm_english(
    house_msg,
    "msg_0545_T20R0201_00001",
    "MOM: See, {STRVAR_1 3, 0, 0}?\\nIt is nice in here, too!\\rThe movers and their POKEMON did all\\nthe work of moving us in.\\rThis is so convenient!\\rPROF. BIRCH lives nearby.\\rGo explore LITTLEROOT when you are ready.",
)
set_gmm_english(
    house_msg,
    "msg_0545_T20R0201_00006",
    "MOM: PROF. BIRCH studies POKEMON\\nout in the field.\\rGo explore LITTLEROOT, dear.",
)
set_gmm_english(
    house_msg,
    "msg_0545_T20R0201_00007",
    "MOM: Welcome home!\\rTake care of your POKEMON, and be\\nsafe out there.",
)
set_gmm_english(
    house_msg,
    "msg_0545_T20R0201_00033",
    "MOM: PROF. BIRCH is usually out\\nstudying POKEMON.\\rGo see what is happening around town.",
)
set_gmm_english(
    house_msg,
    "msg_0545_T20R0201_00034",
    "MOM: PROF. BIRCH is usually out\\nstudying POKEMON.\\rGo see what is happening around town.",
)

print("[Rare Emerald V8] Emerald opening state machine installed")
print("[Rare Emerald V8] Stock New Bark Lyra/Marill/Elm opening hooks disabled")
