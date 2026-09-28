#include "location_backup.h"

#include "global.h"

#include "constants/maps.h"
#include "constants/first_movie.h"

#include "field_system.h"
#include "save_local_field_data.h"

/*
 * First Movie vertical slice:
 * A new save now enters the HGSS field engine through the temporary
 * Mewtwo-lab map alias. Using warp 0 keeps coordinates tied to the map's
 * existing event data while we replace the map with the dedicated lab.
 */
static const Location sLocation_PlayerRoom = {
    .mapId = MAP_FIRST_MOVIE_PROLOGUE_LAB,
    .warpId = 0,
    .x = 0,
    .y = 0,
    .direction = 0x00000001,
};

static const Location sLocation_OutsidePlayerHome = {
    .mapId = MAP_NEW_BARK,
    .warpId = 0xFFFFFFFF,
    .x = 0x000002B7,
    .y = 0x0000018D,
    .direction = 0x00000001,
};

void Location_SetToPlayerRoom(Location *dest) {
    const Location *src = &sLocation_PlayerRoom;
    *dest = *src;
}

void Location_SetToOutsidePlayerHome(Location *dest) {
    const Location *src = &sLocation_OutsidePlayerHome;
    *dest = *src;
}

void Save_SetPositionToPlayerRoom(SaveData *saveData) {
    Location *position = LocalFieldData_GetCurrentPosition(Save_LocalFieldData_Get(saveData));
    Location_SetToPlayerRoom(position);
}
