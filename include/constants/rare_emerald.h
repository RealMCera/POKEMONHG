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
 *
 * Keep existing chapter IDs stable once used by save files. New chapters are
 * appended so old Rare Emerald saves continue to load with the same meaning.
 */

#define RARE_EMERALD_CHAPTER_INTRO                  0
#define RARE_EMERALD_CHAPTER_LITTLEROOT             1
#define RARE_EMERALD_CHAPTER_ROUTE_101              2
#define RARE_EMERALD_CHAPTER_BIRCH_RESCUE           3
#define RARE_EMERALD_CHAPTER_STARTER_SELECTED       4
#define RARE_EMERALD_CHAPTER_FIRST_BATTLE           5
#define RARE_EMERALD_CHAPTER_BIRCH_LAB              6
#define RARE_EMERALD_CHAPTER_ROUTE_103              7
#define RARE_EMERALD_CHAPTER_RIVAL_BATTLE           8
#define RARE_EMERALD_CHAPTER_POKEDEX                9
#define RARE_EMERALD_CHAPTER_OLDALE                10
#define RARE_EMERALD_CHAPTER_PETALBURG             11
#define RARE_EMERALD_CHAPTER_WALLY_TUTORIAL        12
#define RARE_EMERALD_CHAPTER_PETALBURG_WOODS       13
#define RARE_EMERALD_CHAPTER_RUSTBORO              14
#define RARE_EMERALD_CHAPTER_BADGE_STONE           15
#define RARE_EMERALD_CHAPTER_DEVON_GOODS           16
#define RARE_EMERALD_CHAPTER_DEWFORD               17
#define RARE_EMERALD_CHAPTER_BADGE_KNUCKLE         18
#define RARE_EMERALD_CHAPTER_GRANITE_CAVE          19
#define RARE_EMERALD_CHAPTER_SLATEPORT             20
#define RARE_EMERALD_CHAPTER_OCEANIC_MUSEUM        21
#define RARE_EMERALD_CHAPTER_MAUVILLE              22
#define RARE_EMERALD_CHAPTER_BADGE_DYNAMO          23
#define RARE_EMERALD_CHAPTER_VERDANTURF            24
#define RARE_EMERALD_CHAPTER_FALLARBOR             25
#define RARE_EMERALD_CHAPTER_METEOR_FALLS          26
#define RARE_EMERALD_CHAPTER_MT_CHIMNEY            27
#define RARE_EMERALD_CHAPTER_LAVARIDGE             28
#define RARE_EMERALD_CHAPTER_BADGE_HEAT            29
#define RARE_EMERALD_CHAPTER_PETALBURG_GYM         30
#define RARE_EMERALD_CHAPTER_BADGE_BALANCE         31
#define RARE_EMERALD_CHAPTER_SURF_UNLOCKED         32
#define RARE_EMERALD_CHAPTER_WEATHER_INSTITUTE     33
#define RARE_EMERALD_CHAPTER_FORTREE               34
#define RARE_EMERALD_CHAPTER_BADGE_FEATHER         35
#define RARE_EMERALD_CHAPTER_MT_PYRE               36
#define RARE_EMERALD_CHAPTER_MAGMA_HIDEOUT         37
#define RARE_EMERALD_CHAPTER_AQUA_HIDEOUT          38
#define RARE_EMERALD_CHAPTER_LILYCOVE              39
#define RARE_EMERALD_CHAPTER_MOSSDEEP              40
#define RARE_EMERALD_CHAPTER_BADGE_MIND            41
#define RARE_EMERALD_CHAPTER_SPACE_CENTER          42
#define RARE_EMERALD_CHAPTER_DIVE_UNLOCKED         43
#define RARE_EMERALD_CHAPTER_SEAFLOOR_CAVERN       44
#define RARE_EMERALD_CHAPTER_GROUDON_KYOGRE_CRISIS 45
#define RARE_EMERALD_CHAPTER_SOOTOPOLIS_CRISIS     46
#define RARE_EMERALD_CHAPTER_SKY_PILLAR            47
#define RARE_EMERALD_CHAPTER_RAYQUAZA_AWAKENED     48
#define RARE_EMERALD_CHAPTER_SOOTOPOLIS_RESOLVED   49
#define RARE_EMERALD_CHAPTER_BADGE_RAIN            50
#define RARE_EMERALD_CHAPTER_VICTORY_ROAD          51
#define RARE_EMERALD_CHAPTER_ELITE_FOUR            52
#define RARE_EMERALD_CHAPTER_CHAMPION_WALLACE      53
#define RARE_EMERALD_CHAPTER_HALL_OF_FAME          54
#define RARE_EMERALD_CHAPTER_POSTGAME              55
#define RARE_EMERALD_CHAPTER_BATTLE_FRONTIER       56
#define RARE_EMERALD_CHAPTER_COMPLETE              57

/* Temporary map aliases used while true Hoenn maps are migrated. */
#define MAP_RARE_EMERALD_LITTLEROOT_PLAYER_HOUSE MAP_NEW_BARK_PLAYER_HOUSE_1F
#define MAP_RARE_EMERALD_LITTLEROOT              MAP_NEW_BARK
#define MAP_RARE_EMERALD_BIRCH_LAB                MAP_NEW_BARK_ELMS_LAB_1F
#define MAP_RARE_EMERALD_ROUTE_101                 MAP_ROUTE_29
#define MAP_RARE_EMERALD_ROUTE_103                 MAP_ROUTE_30
#define MAP_RARE_EMERALD_OLDALE                    MAP_CHERRYGROVE

/*
 * Dedicated Rare Emerald story slot. Keep this separate from stock HGSS story
 * variables and from the First Movie campaign variable.
 */
#define VAR_RARE_EMERALD_CHAPTER 0x40FE

#endif // POKEHEARTGOLD_CONSTANTS_RARE_EMERALD_H
