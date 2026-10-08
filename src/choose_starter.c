#include "choose_starter.h"

#include "constants/balls.h"
#include "constants/items.h"
#include "constants/rare_emerald.h"
#include "constants/species.h"

#include "field_system.h"
#include "launch_application.h"
#include "map_header.h"
#include "pokedex.h"
#include "save_vars_flags.h"
#include "screen_fade.h"
#include "task.h"
#include "update_dex_received.h"

struct ChooseStarterTaskData {
    int state;
    struct ChooseStarterArgs *args;
};

static BOOL CreateStarter(TaskManager *taskManager);

void LaunchStarterChoiceScene(FieldSystem *fieldSystem) {
    struct ChooseStarterTaskData *env = Heap_AllocAtEnd(HEAP_ID_FIELD2, sizeof(struct ChooseStarterTaskData));
    env->state = 0;
    TaskManager_Call(fieldSystem->taskman, CreateStarter, env);
}

static BOOL CreateStarter(TaskManager *taskManager) {
    FieldSystem *fieldSystem = TaskManager_GetFieldSystem(taskManager);
    struct ChooseStarterTaskData *env = TaskManager_GetEnvironment(taskManager);
    int i;
    u32 mapsec;
    Party *party;

    switch (env->state) {
    case 0:
        BeginNormalPaletteFade(FADE_BOTH_SCREENS, FADE_TYPE_BRIGHTNESS_OUT, FADE_TYPE_BRIGHTNESS_OUT, RGB_BLACK, 6, 1, HEAP_ID_FIELD1);
        env->state = 1;
        break;
    case 1:
        if (!IsPaletteFadeFinished()) {
            break;
        }
        {
            // Rare Emerald keeps the native HGSS starter-selection overlay,
            // but swaps Johto's trio for Emerald's Treecko/Torchic/Mudkip trio.
            const int species[] = {
                SPECIES_TREECKO,
                SPECIES_TORCHIC,
                SPECIES_MUDKIP,
            };
            mapsec = MapHeader_GetMapSec(fieldSystem->location->mapId); // sp14

            env->args = Heap_AllocAtEnd(HEAP_ID_FIELD2, sizeof(struct ChooseStarterArgs));
            env->args->cursorPos = 0;
            env->args->options = Save_PlayerData_GetOptionsAddr(fieldSystem->saveData);
            for (i = 0; i < (int)NELEMS(species); i++) {
                Pokemon *mon = &env->args->starters[i];
                PlayerProfile *profile = Save_PlayerData_GetProfile(fieldSystem->saveData);
                ZeroMonData(mon);
                CreateMon(mon, species[i], RARE_EMERALD_STARTER_LEVEL, 32, FALSE, 0, OT_ID_PLAYER_ID, 0);
                sub_020720FC(mon, profile, BALL_POKE, mapsec, 12, HEAP_ID_FIELD2);
                {
                    int item = ITEM_NONE;
                    SetMonData(mon, MON_DATA_HELD_ITEM, &item);
                }
            }
        }
        ChooseStarter_LaunchApp(fieldSystem, env->args);
        sub_0203E30C();
        env->state = 2;
        break;
    case 2:
        if (FieldSystem_ApplicationIsRunning(fieldSystem)) {
            break;
        }
        env->state = 3;
        break;
    case 3: {
        Pokedex *pokedex = Save_Pokedex_Get(fieldSystem->saveData);
        SaveVarsFlags *varsFlags = Save_VarsFlags_Get(fieldSystem->saveData);
        party = SaveArray_Party_Get(fieldSystem->saveData);
        Pokemon *myChoice = &env->args->starters[env->args->cursorPos];
        u16 starterSpecies = GetMonData(myChoice, MON_DATA_SPECIES, NULL);
        u16 rivalSpecies = RARE_EMERALD_STARTER_NONE;

        if (Party_AddMon(party, myChoice)) {
            UpdatePokedexWithReceivedSpecies(fieldSystem->saveData, myChoice);
        }
        Pokedex_SetMonCaughtFlag(pokedex, Party_GetMonByIndex(party, 0));

        switch (starterSpecies) {
        case RARE_EMERALD_STARTER_TREECKO:
            rivalSpecies = RARE_EMERALD_RIVAL_FOR_TREECKO;
            break;
        case RARE_EMERALD_STARTER_TORCHIC:
            rivalSpecies = RARE_EMERALD_RIVAL_FOR_TORCHIC;
            break;
        case RARE_EMERALD_STARTER_MUDKIP:
            rivalSpecies = RARE_EMERALD_RIVAL_FOR_MUDKIP;
            break;
        }

        // Persist the actual chosen Hoenn starter and Emerald's counter-pick so
        // Route 103 and later rival battles do not depend on HGSS scene state.
        *Save_VarsFlags_GetVarAddr(varsFlags, VAR_RARE_EMERALD_STARTER) = starterSpecies;
        *Save_VarsFlags_GetVarAddr(varsFlags, VAR_RARE_EMERALD_RIVAL_SPECIES) = rivalSpecies;
        *Save_VarsFlags_GetVarAddr(varsFlags, VAR_RARE_EMERALD_CHAPTER) = RARE_EMERALD_CHAPTER_STARTER_SELECTED;

        env->state = 4;
        FieldSystem_LoadFieldOverlay(fieldSystem);
        break;
    }
    case 4:
        if (!sub_020505C8(fieldSystem)) {
            break;
        }
        BeginNormalPaletteFade(FADE_BOTH_SCREENS, FADE_TYPE_BRIGHTNESS_IN, FADE_TYPE_BRIGHTNESS_IN, RGB_BLACK, 6, 1, HEAP_ID_FIELD1);
        env->state = 5;
        break;
    case 5:
        if (!IsPaletteFadeFinished()) {
            break;
        }
        Heap_Free(env->args);
        Heap_Free(env);
        return TRUE;
    }

    return FALSE;
}
