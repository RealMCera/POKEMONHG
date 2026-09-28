#include "constants/scrcmd.h"
#include "constants/first_movie.h"
#include "fielddata/script/scr_seq/event_D40R0107.h"
#include "constants/init_script_types.h"
	.include "asm/macros/script.inc"

	.rodata
	.option alignment off

	InitScriptEntry_OnLoad _EV_scr_seq_D40R0107_002 + 1
	InitScriptEntry_OnResume _EV_scr_seq_D40R0107_004 + 1
	InitScriptEntry_OnTransition _EV_scr_seq_D40R0107_006 + 1
	InitScriptEntry_OnFrameTable scr_seq_D40R0107_first_movie_scripts
	InitScriptEntryEnd

scr_seq_D40R0107_first_movie_scripts:
	InitScriptGoToIfEqual VAR_FIRST_MOVIE_CHAPTER, FIRST_MOVIE_CHAPTER_NEW_ISLAND, _EV_scr_seq_D40R0107_007 + 1
	InitScriptFrameTableEnd

	InitScriptEnd
