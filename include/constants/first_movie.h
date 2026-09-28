#ifndef POKEHEARTGOLD_CONSTANTS_FIRST_MOVIE_H
#define POKEHEARTGOLD_CONSTANTS_FIRST_MOVIE_H

#include "constants/maps.h"

/*
 * First Movie campaign constants.
 *
 * During the migration phase we intentionally reuse proven HGSS map headers
 * while the movie-specific map matrices/events are authored. This lets the
 * actual HGSS field, sprite, script, save, menu, and battle systems remain
 * live from the beginning of development.
 */

#define FIRST_MOVIE_CHAPTER_PROLOGUE          0
#define FIRST_MOVIE_CHAPTER_GIOVANNI_FACILITY 1
#define FIRST_MOVIE_CHAPTER_INVITATION        2
#define FIRST_MOVIE_CHAPTER_HARBOR            3
#define FIRST_MOVIE_CHAPTER_STORM             4
#define FIRST_MOVIE_CHAPTER_NEW_ISLAND        5
#define FIRST_MOVIE_CHAPTER_MEWTWO_REVEAL     6
#define FIRST_MOVIE_CHAPTER_CLONE_TRIALS      7
#define FIRST_MOVIE_CHAPTER_CLONE_LAB         8
#define FIRST_MOVIE_CHAPTER_FINAL_BATTLE      9
#define FIRST_MOVIE_CHAPTER_EPILOGUE          10
#define FIRST_MOVIE_CHAPTER_POSTGAME          11

/*
 * Temporary map aliases for the first vertical slice.
 * These are deliberately aliases, not new map IDs. They will be replaced by
 * dedicated First Movie maps as those assets are introduced.
 */
#define MAP_FIRST_MOVIE_PROLOGUE_LAB MAP_NEW_BARK_ELMS_LAB_1F
#define MAP_FIRST_MOVIE_GIOVANNI_FACILITY MAP_NEW_BARK_ELMS_LAB_2F
#define MAP_FIRST_MOVIE_ASH_HANDOFF MAP_NEW_BARK_PLAYER_HOUSE_1F
#define MAP_FIRST_MOVIE_HARBOR MAP_SS_AQUA_OLIVINE_PORT_EXTERIOR
#define MAP_FIRST_MOVIE_STORM_CROSSING MAP_SS_AQUA_1F
#define MAP_FIRST_MOVIE_NEW_ISLAND_ARRIVAL MAP_WHIRL_ISLANDS_B3F_LUGIA_CAVE
#define MAP_FIRST_MOVIE_GRAND_HALL MAP_POKEMON_LEAGUE_LANCE_ROOM
#define MAP_FIRST_MOVIE_CLONE_ARENA MAP_VERMILION_GYM

/*
 * Campaign state uses an otherwise-unassigned variable through an alias.
 * Keeping the alias here means scripts can use a descriptive name immediately
 * without changing SaveData layout.
 */
#define VAR_FIRST_MOVIE_CHAPTER 0x40FC

#endif // POKEHEARTGOLD_CONSTANTS_FIRST_MOVIE_H
