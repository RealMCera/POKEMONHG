#include "constants/scrcmd.h"
#include "constants/first_movie.h"
#include "fielddata/script/scr_seq/event_T20R0101.h"
#include "constants/init_script_types.h"
	.include "asm/macros/script.inc"

	.rodata
	.option alignment off

	InitScriptEntry_OnFrameTable scr_seq_T20R0101_first_movie_scripts
	InitScriptEntryEnd

scr_seq_T20R0101_first_movie_scripts:
	InitScriptGoToIfEqual VAR_FIRST_MOVIE_CHAPTER, FIRST_MOVIE_CHAPTER_PROLOGUE, _EV_scr_seq_T20R0101_015 + 1
	InitScriptFrameTableEnd

	InitScriptEnd
