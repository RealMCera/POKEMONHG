#include "constants/scrcmd.h"
#include "constants/rare_emerald.h"
#include "fielddata/script/scr_seq/event_T20.h"
#include "msgdata/msg/msg_0542_T20.h"
	.include "asm/macros/script.inc"

	.rodata

/*
 * Rare Emerald - Littleroot Town shell
 *
 * New Bark Town currently supplies the native HGSS map/field engine while the
 * Hoenn map assets are migrated. The stock New Bark story scripts are not
 * allowed to run on this branch: they are HeartGold progression and were
 * masking the Rare Emerald campaign during normal play.
 *
 * Script 002 is the existing west-exit coordinate event. During a new Rare
 * Emerald save it now acts as the first playable Emerald milestone: initialize
 * campaign state, present the native DS starter chooser, run Birch's Zigzagoon
 * rescue battle, register the starter with the native HGSS story state, and
 * move the player into Birch's Lab.
 */

	ScrDef scr_seq_T20_000
	ScrDef scr_seq_T20_001
	ScrDef scr_seq_T20_002
	ScrDef scr_seq_T20_003
	ScrDef scr_seq_T20_004
	ScrDef scr_seq_T20_005
	ScrDef scr_seq_T20_006
	ScrDef scr_seq_T20_007
	ScrDef scr_seq_T20_008
	ScrDef scr_seq_T20_009
	ScrDef scr_seq_T20_010
	ScrDef scr_seq_T20_011
	ScrDef scr_seq_T20_012
	ScrDef scr_seq_T20_013
	ScrDef scr_seq_T20_014
	ScrDef scr_seq_T20_015
	ScrDef scr_seq_T20_016
	ScrDef scr_seq_T20_017
	ScrDefEnd

/* Temporary NPC/object interactions are intentionally inert until their
 * Hoenn replacements are installed. Keeping all script slots defined keeps
 * the existing New Bark event table valid while preventing Johto story leaks.
 */
scr_seq_T20_000:
	End

scr_seq_T20_001:
	End

scr_seq_T20_002:
	Compare VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_INTRO
	GoToIfEq _RareEmeraldLittlerootExit
	Compare VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_LITTLEROOT
	GoToIfEq _RareEmeraldLittlerootExit
	End

_RareEmeraldLittlerootExit:
	LockAll
	SetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_RESCUE
	PlayCry RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, 0
	WaitCry
	ChooseStarter
	SetFlag FLAG_GOT_STARTER
	ScrCmd_605 3, 2
	GetPartyMonSpecies 0, VAR_TEMP_x4001
	SetStarterChoice VAR_TEMP_x4001
	SetVar VAR_RARE_EMERALD_STARTER, VAR_TEMP_x4001
	WildBattle RARE_EMERALD_BIRCH_ZIGZAGOON_SPECIES, RARE_EMERALD_BIRCH_ZIGZAGOON_LEVEL, 0
	SetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_FIRST_BATTLE
	SetVar VAR_SCENE_NEW_BARK_WEST_EXIT, 1
	SetFlag FLAG_HIDE_NEW_BARK_MOM
	SetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_BIRCH_LAB
	Warp MAP_RARE_EMERALD_BIRCH_LAB, 0, 4, 13, DIR_NORTH
	ReleaseAll
	End

scr_seq_T20_003:
	End

scr_seq_T20_004:
	End

scr_seq_T20_005:
	End

scr_seq_T20_006:
	Compare VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_INTRO
	GoToIfNe _RareEmeraldLittlerootInitDone
	SetVar VAR_RARE_EMERALD_CHAPTER, RARE_EMERALD_CHAPTER_LITTLEROOT
_RareEmeraldLittlerootInitDone:
	End

scr_seq_T20_007:
	End

scr_seq_T20_008:
	End

scr_seq_T20_009:
	End

scr_seq_T20_010:
	End

scr_seq_T20_011:
	End

scr_seq_T20_012:
	End

scr_seq_T20_013:
	End

scr_seq_T20_014:
	End

scr_seq_T20_015:
	End

scr_seq_T20_016:
	End

scr_seq_T20_017:
	End
