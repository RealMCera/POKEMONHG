#ifndef POKEHEARTGOLD_CONSTANTS_RARE_EMERALD_H
#define POKEHEARTGOLD_CONSTANTS_RARE_EMERALD_H

#include "constants/maps.h"

/*
 * Rare Emerald campaign state.
 *
 * Pokémon Emerald is the story/data authority. HGSS supplies the Nintendo DS
 * engine, field system, battle system, menus, saves, sprites, and scripting.
 * Temporary HGSS map aliases keep the project playable while Hoenn-native
 * matrices/events/graphics are migrated.
 */

#define RARE_EMERALD_CHAPTER_INTRO             0
#define RARE_EMERALD_CHAPTER_LITTLEROOT        1
#define RARE_EMERALD_CHAPTER_ROUTE_101         2
#define RARE_EMERALD_CHAPTER_BIRCH_RESCUE      3
#define RARE_EMERALD_CHAPTER_STARTER_SELECTED  4
#define RARE_EMERALD_CHAPTER_FIRST_BATTLE      5
#define RARE_EMERALD_CHAPTER_BIRCH_LAB         6
#define RARE_EMERALD_CHAPTER_ROUTE_103         7
#define RARE_EMERALD_CHAPTER_RIVAL_BATTLE      8
#define RARE_EMERALD_CHAPTER_POKEDEX            9
#define RARE_EMERALD_CHAPTER_OLDALE            10

/* Temporary map aliases for Build 0.1. */
#define MAP_RARE_EMERALD_LITTLEROOT_PLAYER_HOUSE MAP_NEW_BARK_PLAYER_HOUSE_1F
#define MAP_RARE_EMERALD_LITTLEROOT              MAP_NEW_BARK_TOWN
#define MAP_RARE_EMERALD_BIRCH_LAB                MAP_NEW_BARK_ELMS_LAB_1F
#define MAP_RARE_EMERALD_ROUTE_101                 MAP_ROUTE_29
#define MAP_RARE_EMERALD_ROUTE_103                 MAP_ROUTE_30
#define MAP_RARE_EMERALD_OLDALE                    MAP_CHERRYGROVE_CITY

/*
 * Dedicated Rare Emerald story slot. Keep this separate from stock HGSS story
 * variables and from the First Movie campaign variable.
 */
#define VAR_RARE_EMERALD_CHAPTER 0x40FE

#endif // POKEHEARTGOLD_CONSTANTS_RARE_EMERALD_H
