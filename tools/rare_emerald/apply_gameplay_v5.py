#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]


def replace_once(relpath: str, old: str, new: str, marker: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    if marker in text or new in text:
        print(f"[Rare Emerald V5] already fixed: {relpath} ({marker})")
        return
    if old not in text:
        raise SystemExit(f"[Rare Emerald V5] expected source anchor not found in {relpath}: {marker}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"[Rare Emerald V5] fixed: {relpath} ({marker})")


def set_gmm_english(relpath: str, row_id: str, english: str) -> None:
    path = ROOT / relpath
    text = path.read_text(encoding="utf-8")
    pat = re.compile(
        rf'(<row id="{re.escape(row_id)}"[^>]*>.*?<language name="English">)(.*?)(</language>)',
        re.S,
    )
    match = pat.search(text)
    if not match:
        raise SystemExit(f"[Rare Emerald V5] GMM row not found: {row_id}")
    if match.group(2) == english:
        print(f"[Rare Emerald V5] message already set: {row_id}")
        return
    text = text[:match.start(2)] + english + text[match.end(2):]
    path.write_text(text, encoding="utf-8")
    print(f"[Rare Emerald V5] message set: {row_id}")


# ---------------------------------------------------------------------------
# V4 save-state correction retained in V5
# ---------------------------------------------------------------------------
route101 = "files/fielddata/script/scr_seq/scr_seq_0225_R29.s"
route101_text = (ROOT / route101).read_text(encoding="utf-8")
if "RARE_EMERALD_ROUTE101_RESCUE_V3" not in route101_text:
    raise SystemExit("[Rare Emerald V5] Route 101 V3 patch must run before V5")
replace_once(
    route101,
    "\tSetVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001",
    "\tCopyVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001",
    "persist selected starter species",
)

# ---------------------------------------------------------------------------
# Route 103 rival trainers: Emerald's six first-rival combinations.
# HeartGold's Ethan/Lyra trainer classes are temporary DS-native stand-ins for
# Brendan/May battle art until their dedicated sprites are imported.
# ---------------------------------------------------------------------------
trainer_json_path = ROOT / "files/poketool/trainer/trainers.json"
trainer_data = json.loads(trainer_json_path.read_text(encoding="utf-8"))
trainers = trainer_data["trainers"]

starter_specs = [
    ("May", "TRAINERCLASS_PKMN_TRAINER_LYRA", "SPECIES_TREECKO"),
    ("May", "TRAINERCLASS_PKMN_TRAINER_LYRA", "SPECIES_TORCHIC"),
    ("May", "TRAINERCLASS_PKMN_TRAINER_LYRA", "SPECIES_MUDKIP"),
    ("Brendan", "TRAINERCLASS_PKMN_TRAINER_ETHAN", "SPECIES_TREECKO"),
    ("Brendan", "TRAINERCLASS_PKMN_TRAINER_ETHAN", "SPECIES_TORCHIC"),
    ("Brendan", "TRAINERCLASS_PKMN_TRAINER_ETHAN", "SPECIES_MUDKIP"),
]

if len(trainers) == 738:
    for rival_name, trainer_class, species in starter_specs:
        trainers.append({
            "type": "TRTYPE_MON",
            "class": trainer_class,
            "name": f"{{TRNAME}}{rival_name}",
            "items": [],
            "ai_flags": 1,
            "double": 0,
            "party": [{
                "difficulty": 0,
                "genderOverride": "TRPOKE_GENDER_OVERRIDE_OFF",
                "abilityOverride": "TRPOKE_ABILITY_OVERRIDE_OFF",
                "level": 5,
                "species": species,
                "capsule": 0,
            }],
            "messages": [],
        })
    trainer_json_path.write_text(json.dumps(trainer_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("[Rare Emerald V5] appended Route 103 May/Brendan trainer teams 738-743")
elif len(trainers) >= 744 and trainers[738].get("name") == "{TRNAME}May" and trainers[743].get("name") == "{TRNAME}Brendan":
    print("[Rare Emerald V5] Route 103 trainer teams already present")
else:
    raise SystemExit(f"[Rare Emerald V5] unexpected trainer table shape: {len(trainers)} entries")

trainer_constants = "include/constants/trainers.h"
trainer_constants_path = ROOT / trainer_constants
trainer_constants_text = trainer_constants_path.read_text(encoding="utf-8")
if "TRAINER_RARE_EMERALD_MAY_TREECKO" not in trainer_constants_text:
    old = "#define LAST_TRAINER_INDEX 740"
    new = """#define TRAINER_RARE_EMERALD_MAY_TREECKO      738
#define TRAINER_RARE_EMERALD_MAY_TORCHIC      739
#define TRAINER_RARE_EMERALD_MAY_MUDKIP       740
#define TRAINER_RARE_EMERALD_BRENDAN_TREECKO  741
#define TRAINER_RARE_EMERALD_BRENDAN_TORCHIC  742
#define TRAINER_RARE_EMERALD_BRENDAN_MUDKIP   743

#define LAST_TRAINER_INDEX 746"""
    if old not in trainer_constants_text:
        raise SystemExit("[Rare Emerald V5] LAST_TRAINER_INDEX anchor not found")
    trainer_constants_path.write_text(trainer_constants_text.replace(old, new, 1), encoding="utf-8")
    print("[Rare Emerald V5] added Route 103 trainer constants")
else:
    print("[Rare Emerald V5] Route 103 trainer constants already present")

# Arm the stock Route 30 coordinate event once Birch sends the player to the
# Route 103 research battle. This keeps the trigger one-shot: the rival script
# clears the scene var after a win.
birch_lab = "files/fielddata/script/scr_seq/scr_seq_0843_T20R0101.s"
replace_once(
    birch_lab,
    "\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_ROUTE_103\n\tReleaseAll",
    "\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_ROUTE_103\n\tSetVar VAR_SCENE_ROUTE_30_PHONE_CALL, 1\n\tReleaseAll",
    "arm Route 103 rival coordinate",
)

route103 = "files/fielddata/script/scr_seq/scr_seq_0227_R30.s"
replace_once(
    route103,
    '#include "constants/scrcmd.h"\n#include "fielddata/script/scr_seq/event_R30.h"',
    '#include "constants/scrcmd.h"\n#include "constants/rare_emerald.h"\n#include "fielddata/script/scr_seq/event_R30.h"',
    "constants/rare_emerald.h",
)

old_route103_event = """scr_seq_R30_004:
\tScrCmd_609
\tLockAll
\tPhoneCall PHONE_CONTACT_MOTHER, 2, 0
\tSetVar VAR_SCENE_ROUTE_30_PHONE_CALL, 0
\tSetFlag FLAG_TALKED_TO_MOM_AFTER_NAMING_RIVAL
\tReleaseAll
\tEnd

scr_seq_R30_005:"""

new_route103_event = """scr_seq_R30_004:
\tCompare VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_ROUTE_103
\tGoToIfEq _RareEmeraldRoute103Rival
\tScrCmd_609
\tLockAll
\tPhoneCall PHONE_CONTACT_MOTHER, 2, 0
\tSetVar VAR_SCENE_ROUTE_30_PHONE_CALL, 0
\tSetFlag FLAG_TALKED_TO_MOM_AFTER_NAMING_RIVAL
\tReleaseAll
\tEnd

_RareEmeraldRoute103Rival:
\t# RARE_EMERALD_ROUTE103_RIVAL_V1
\tScrCmd_609
\tLockAll
\tGetPlayerGender VAR_TEMP_x4000
\tCompare VAR_TEMP_x4000, 0
\tGoToIfEq _RareEmeraldRoute103MayIntro
\tNPCMsg msg_0375_R30_00005
\tCloseMsg
\tGoTo _RareEmeraldRoute103BrendanBattle

_RareEmeraldRoute103MayIntro:
\tNPCMsg msg_0375_R30_00000
\tCloseMsg
\tGoTo _RareEmeraldRoute103MayBattle

_RareEmeraldRoute103MayBattle:
\tCompare VAR_RARE_EMERALD_RIVAL_SPECIES, SPECIES_TREECKO
\tGoToIfEq _RareEmeraldRoute103MayTreecko
\tCompare VAR_RARE_EMERALD_RIVAL_SPECIES, SPECIES_TORCHIC
\tGoToIfEq _RareEmeraldRoute103MayTorchic
\tTrainerBattle TRAINER_RARE_EMERALD_MAY_MUDKIP, 0, 0, 0
\tGoTo _RareEmeraldRoute103BattleDone

_RareEmeraldRoute103MayTreecko:
\tTrainerBattle TRAINER_RARE_EMERALD_MAY_TREECKO, 0, 0, 0
\tGoTo _RareEmeraldRoute103BattleDone

_RareEmeraldRoute103MayTorchic:
\tTrainerBattle TRAINER_RARE_EMERALD_MAY_TORCHIC, 0, 0, 0
\tGoTo _RareEmeraldRoute103BattleDone

_RareEmeraldRoute103BrendanBattle:
\tCompare VAR_RARE_EMERALD_RIVAL_SPECIES, SPECIES_TREECKO
\tGoToIfEq _RareEmeraldRoute103BrendanTreecko
\tCompare VAR_RARE_EMERALD_RIVAL_SPECIES, SPECIES_TORCHIC
\tGoToIfEq _RareEmeraldRoute103BrendanTorchic
\tTrainerBattle TRAINER_RARE_EMERALD_BRENDAN_MUDKIP, 0, 0, 0
\tGoTo _RareEmeraldRoute103BattleDone

_RareEmeraldRoute103BrendanTreecko:
\tTrainerBattle TRAINER_RARE_EMERALD_BRENDAN_TREECKO, 0, 0, 0
\tGoTo _RareEmeraldRoute103BattleDone

_RareEmeraldRoute103BrendanTorchic:
\tTrainerBattle TRAINER_RARE_EMERALD_BRENDAN_TORCHIC, 0, 0, 0

_RareEmeraldRoute103BattleDone:
\tCheckBattleWon VAR_SPECIAL_RESULT
\tCompare VAR_SPECIAL_RESULT, 0
\tGoToIfEq _RareEmeraldRoute103WhiteOut
\tGetPlayerGender VAR_TEMP_x4000
\tCompare VAR_TEMP_x4000, 0
\tGoToIfEq _RareEmeraldRoute103MayOutro
\tNPCMsg msg_0375_R30_00006
\tCloseMsg
\tGoTo _RareEmeraldRoute103Rewards

_RareEmeraldRoute103MayOutro:
\tNPCMsg msg_0375_R30_00001
\tCloseMsg

_RareEmeraldRoute103Rewards:
\tHealParty
\tGivePokedex
\tSetFlag FLAG_GOT_POKEDEX
\tGiveItemNoCheck ITEM_POKE_BALL, 5
\tSetVar VAR_SCENE_ROUTE_30_PHONE_CALL, 0
\tSetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_OLDALE
\tReleaseAll
\tEnd

_RareEmeraldRoute103WhiteOut:
\tSetVar VAR_SCENE_ROUTE_30_PHONE_CALL, 1
\tWhiteOut
\tReleaseAll
\tEnd

scr_seq_R30_005:"""

replace_once(route103, old_route103_event, new_route103_event, "RARE_EMERALD_ROUTE103_RIVAL_V1")

route103_msg = "files/msgdata/msg/msg_0375_R30.gmm"
set_gmm_english(route103_msg, "msg_0375_R30_00000", "MAY: Oh, hi!\\rI was checking the Pokémon around here.\\rLet's have a quick battle!")
set_gmm_english(route103_msg, "msg_0375_R30_00001", "MAY: Wow! That's great!\\rYou're pretty good!")
set_gmm_english(route103_msg, "msg_0375_R30_00005", "BRENDAN: Hey!\\rI was checking the Pokémon around here.\\rLet's have a quick battle!")
set_gmm_english(route103_msg, "msg_0375_R30_00006", "BRENDAN: Wow! That's great!\\rYou're pretty good!")

print("[Rare Emerald V5] Route 103 rival vertical slice ready")
