#include "constants/scrcmd.h"
#include "constants/first_movie.h"
#include "fielddata/script/scr_seq/event_T20R0102.h"
#include "msgdata/msg/msg_0544_T20R0102.h"
	.include "asm/macros/script.inc"

	.rodata

	ScrDef scr_seq_T20R0102_000
	ScrDef scr_seq_T20R0102_001
	ScrDef scr_seq_T20R0102_002
	ScrDefEnd

scr_seq_T20R0102_000:
	PlaySE SEQ_SE_DP_SELECT
	LockAll
	FacePlayer
	BufferPlayersName 0
	GenderMsgBox msg_0544_T20R0102_00000, msg_0544_T20R0102_00001
	WaitButton
	CloseMsg
	ReleaseAll
	End

scr_seq_T20R0102_001:
	SimpleNPCMsg msg_0544_T20R0102_00002
	End
	.balign 4, 0


scr_seq_T20R0102_002:
	LockAll
	NPCMsg msg_0544_T20R0102_00000
	WaitButton
	CloseMsg
	GetPartyCount VAR_TEMP_x4000
	Compare VAR_TEMP_x4000, 0
	GoToIfNe _FM_GIOVANNI_TEST_1
	GiveMon SPECIES_MEWTWO, 30, 0, 0, 0, VAR_SPECIAL_RESULT
_FM_GIOVANNI_TEST_1:
	NPCMsg msg_0544_T20R0102_00001
	WaitButton
	CloseMsg
	TrainerBattle TRAINER_TEAM_ROCKET_GRUNT_20, 0, 0, 0
	CheckBattleWon VAR_SPECIAL_RESULT
	Compare VAR_SPECIAL_RESULT, 0
	GoToIfEq _FM_GIOVANNI_RECOVER
	NPCMsg msg_0544_T20R0102_00002
	WaitButton
	CloseMsg
	TrainerBattle TRAINER_BLACK_BELT_KIYO, 0, 0, 0
	CheckBattleWon VAR_SPECIAL_RESULT
	Compare VAR_SPECIAL_RESULT, 0
	GoToIfEq _FM_GIOVANNI_RECOVER
	NPCMsg msg_0544_T20R0102_00003
	WaitButton
	CloseMsg
	SetVar VAR_FIRST_MOVIE_CHAPTER, FIRST_MOVIE_CHAPTER_INVITATION
	ReleaseAll
	End

_FM_GIOVANNI_RECOVER:
	NPCMsg msg_0544_T20R0102_00003
	WaitButton
	CloseMsg
	ReleaseAll
	End

	.balign 4, 0
