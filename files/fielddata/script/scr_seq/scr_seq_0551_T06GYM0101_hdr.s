#include "constants/scrcmd.h"
#include "constants/first_movie.h"
#include "fielddata/script/scr_seq/event_T06GYM0101.h"
#include "constants/init_script_types.h"
	.include "asm/macros/script.inc"

	.rodata
	.option alignment off

	InitScriptEntry_OnTransition _EV_scr_seq_T06GYM0101_021 + 1
	InitScriptEntry_OnResume _EV_scr_seq_T06GYM0101_022 + 1
	InitScriptEntry_OnFrameTable scr_seq_T06GYM0101_first_movie_scripts
	InitScriptEntryEnd

scr_seq_T06GYM0101_first_movie_scripts:
	InitScriptGoToIfEqual VAR_FIRST_MOVIE_CHAPTER, FIRST_MOVIE_CHAPTER_CLONE_TRIALS, _EV_scr_seq_T06GYM0101_026 + 1
	InitScriptFrameTableEnd

	InitScriptEnd
