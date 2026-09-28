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

enum FirstMovieChapter {
    FIRST_MOVIE_CHAPTER_PROLOGUE = 0,
    FIRST_MOVIE_CHAPTER_GIOVANNI_FACILITY,
    FIRST_MOVIE_CHAPTER_INVITATION,
    FIRST_MOVIE_CHAPTER_HARBOR,
    FIRST_MOVIE_CHAPTER_STORM,
    FIRST_MOVIE_CHAPTER_NEW_ISLAND,
    FIRST_MOVIE_CHAPTER_MEWTWO_REVEAL,
    FIRST_MOVIE_CHAPTER_CLONE_TRIALS,
    FIRST_MOVIE_CHAPTER_CLONE_LAB,
    FIRST_MOVIE_CHAPTER_FINAL_BATTLE,
    FIRST_MOVIE_CHAPTER_EPILOGUE,
    FIRST_MOVIE_CHAPTER_POSTGAME
};

/*
 * Temporary map aliases for the first vertical slice.
 * These are deliberately aliases, not new map IDs. They will be replaced by
 * dedicated First Movie maps as those assets are introduced.
 */
#define MAP_FIRST_MOVIE_PROLOGUE_LAB MAP_NEW_BARK_ELMS_LAB_1F
#define MAP_FIRST_MOVIE_GIOVANNI_FACILITY MAP_NEW_BARK_ELMS_LAB_2F
#define MAP_FIRST_MOVIE_NEW_ISLAND_HALL MAP_NEW_BARK_PLAYER_HOUSE_1F

/*
 * Campaign state uses an otherwise-unassigned variable through an alias.
 * Keeping the alias here means scripts can use a descriptive name immediately
 * without changing SaveData layout.
 */
#define VAR_FIRST_MOVIE_CHAPTER 0x40FC

#endif // POKEHEARTGOLD_CONSTANTS_FIRST_MOVIE_H
