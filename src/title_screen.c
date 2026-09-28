#include "title_screen.h"

#include "global.h"

#include "constants/sndseq.h"
#include "constants/species.h"

#include "application/check_savedata.h"
#include "application/delete_savedata.h"
#include "demo/title/titledemo.naix"
#include "msgdata/msg.naix"
#include "msgdata/msg/msg_0719.h"

#include "brightness.h"
#include "camera.h"
#include "font.h"
#include "gf_3d_render.h"
#include "gf_gfx_loader.h"
#include "gf_gfx_planes.h"
#include "intro_movie.h"
#include "main.h"
#include "math_util.h"
#include "msgdata.h"
#include "overlay_62.h"
#include "overlay_manager.h"
#include "screen_fade.h"
#include "sound.h"
#include "sound_02004A44.h"
#include "system.h"
#include "text.h"
#include "unk_02005D10.h"
#include "unk_02020B8C.h"
#include "unk_02026E30.h"

/*
 * First Movie build: keep the proven HGSS title-screen renderer for now,
 * but make its interactive audio identity match the project.
 * Dedicated 2D/3D title assets can replace the stock resources later.
 */
#define TITLE_SCREEN_SPECIES SPECIES_MEWTWO

#define CLEAR_SAVE_KEY_COMBO  (PAD_BUTTON_B | PAD_BUTTON_SELECT | PAD_KEY_UP)
#define MIC_TEST_KEY_COMBO    (PAD_BUTTON_X | PAD_BUTTON_Y | PAD_KEY_DOWN)
#define TITLE_SCREEN_DURATION 2340

enum TitleScreenMainState {
    TITLESCREEN_MAIN_WAIT_FADE,
    TITLESCREEN_MAIN_START_MUSIC,
    TITLESCREEN_MAIN_PLAY,
    TITLESCREEN_MAIN_PROCEED_FLASH,
    TITLESCREEN_MAIN_PROCEED_FLASH_2,
    TITLESCREEN_MAIN_PROCEED_NOFLASH,
    TITLESCREEN_MAIN_FADEOUT,
};

enum TitleScreenModelState {
    TITLESCREEN_MODEL_OFF,
    TITLESCREEN_MODEL_STOP,
    TITLESCREEN_MODEL_RUN,
};

enum TitleScreenModelSubState {
    TITLESCREEN_MODELSUB_STOP,
    TITLESCREEN_MODELSUB_WAIT_STOP,
    TITLESCREEN_MODELSUB_RUN,
};

enum TitleScreenAnimState {
    TITLESCREEN_ANIM_SETUP,
    TITLESCREEN_ANIM_RUN,
};

enum TitleScreenTopScreenGlowState {
    TITLESCREEN_GLOW_SETUP,
    TITLESCREEN_GLOW_IN,
    TITLESCREEN_GLOW_OUT,
    TITLESCREEN_GLOW_PAUSE,
};

struct CameraScript {
    VecFx32 pos;
    int duration;
};

static BOOL TitleScreen_Init(OverlayManager *man, int *state);
static BOOL TitleScreen_Main(OverlayManager *man, int *state);
static BOOL TitleScreen_Exit(OverlayManager *man, int *state);
static void TitleScreen_VBlankCB(void *pVoid);
static void TitleScreen_SetGfxBanks(void);
static void TitleScreen_Create3DVramMan(TitleScreenOverlayData *data);
static void TitleScreen_Delete3DVramMan(TitleScreenOverlayData *data);
static void TitleScreen_Load3DObjects(TitleScreenAnimObject *animObj, int texFileId, int anim1Id, int anim2Id, int anim3Id, int anim4Id, enum HeapID heapID);
static void TitleScreen_Unload3DObjects(TitleScreenAnimObject *animObj);
static void TitleScreen_AdvanceAnimObjsFrame(NNSG3dAnmObj **ppAnmObj, fx32 a1);
static void TitleScreenAnimObjs_Run(TitleScreenAnimObject *animObj);
static void TitleScreen_InitBgs(TitleScreenOverlayData *data);
static void TitleScreen_ReleaseBgs(TitleScreenOverlayData *data);
static BOOL TitleScreenAnim_InitObjectsAndCamera(TitleScreenAnimData *animData, BgConfig *bgConfig, enum HeapID heapID);
static BOOL TitleScreenAnim_Run(TitleScreenAnimData *animData, BgConfig *bgConfig, enum HeapID heapID);
static BOOL TitleScreenAnim_UnloadAndRemoveTopScreenResources(TitleScreenAnimData *animData, BgConfig *bgConfig, enum HeapID heapID);
static void TitleScreenAnim_Load2dBgGfx(BgConfig *bgConfig, enum HeapID heapID, TitleScreenAnimData *animData) {
    (void)animData;

    // Physical top screen (SUB engine after display swap).
    GfGfxLoader_LoadCharData(NARC_demo_title_titledemo, NARC_titledemo_titledemo_00000044_NCGR, bgConfig, GF_BG_LYR_SUB_3, 0, 0, FALSE, heapID);
    GfGfxLoader_LoadScrnData(NARC_demo_title_titledemo, NARC_titledemo_titledemo_00000045_NSCR, bgConfig, GF_BG_LYR_SUB_3, 0, 0, FALSE, heapID);
    GfGfxLoader_GXLoadPal(NARC_demo_title_titledemo, NARC_titledemo_titledemo_00000046_NCLR, GF_PAL_LOCATION_SUB_BG, GF_PAL_SLOT_0_OFFSET, 0, heapID);

    // Physical bottom screen (MAIN engine after display swap).
    GfGfxLoader_LoadCharData(NARC_demo_title_titledemo, NARC_titledemo_titledemo_00000047_NCGR, bgConfig, GF_BG_LYR_MAIN_2, 0, 0, FALSE, heapID);
    GfGfxLoader_LoadScrnData(NARC_demo_title_titledemo, NARC_titledemo_titledemo_00000048_NSCR, bgConfig, GF_BG_LYR_MAIN_2, 0, 0, FALSE, heapID);
    GfGfxLoader_GXLoadPal(NARC_demo_title_titledemo, NARC_titledemo_titledemo_00000049_NCLR, GF_PAL_LOCATION_MAIN_BG, GF_PAL_SLOT_0_OFFSET, 0, heapID);
}
static void TitleScreenAnim_RunTopScreenGlow(TitleScreenAnimData *animData) {
    (void)animData;
}
static void TitleScreen_RemoveTouchToStartWindow(BgConfig *bgConfig, enum HeapID heapID, TitleScreenAnimData *animData) {
    (void)bgConfig;
    (void)heapID;
    (void)animData;
}
static void TitleScreenAnim_SetCameraInitialPos(TitleScreenAnimData *animData) {
    if (animData->gameVersion == VERSION_HEARTGOLD) {
        SetVec(animData->cameraPosStart, FX32_CONST(0), FX32_CONST(65), FX32_CONST(72));
        SetVec(animData->cameraPosEnd, FX32_CONST(625), FX32_CONST(152), FX32_CONST(256));
        SetVec(animData->cameraTargetStart, FX32_CONST(0), FX32_CONST(90), FX32_CONST(0));
        SetVec(animData->cameraTargetEnd, FX32_CONST(-2), FX32_CONST(124), FX32_CONST(-38));
        SetVec(animData->light0Vec, FX16_CONST(0), FX16_CONST(0.635498), FX16_CONST(0));
        SetVec(animData->light1Vec, FX16_CONST(0), FX16_CONST(0.476807), FX16_CONST(0));
        animData->cameraSpeed = FX32_CONST(3);
    } else {
        SetVec(animData->cameraPosStart, FX32_CONST(0), FX32_CONST(65), FX32_CONST(72));
        SetVec(animData->cameraPosEnd, FX32_CONST(420), FX32_CONST(87), FX32_CONST(331));
        SetVec(animData->cameraTargetStart, FX32_CONST(0), FX32_CONST(90), FX32_CONST(0));
        SetVec(animData->cameraTargetEnd, FX32_CONST(-2), FX32_CONST(124), FX32_CONST(-38));
        SetVec(animData->light0Vec, FX16_CONST(0), FX16_CONST(0.635498), FX16_CONST(0));
        SetVec(animData->light1Vec, FX16_CONST(0), FX16_CONST(0.476807), FX16_CONST(0));
        animData->cameraSpeed = FX32_CONST(3);
    }

    {
        VecFx32 light0vec;
        VecFx32 light0vecNorm;

        SetVec(light0vec, FX32_CONST(0), FX32_CONST(0.635498), FX32_CONST(0));
        VEC_Normalize(&light0vec, &light0vecNorm);
        animData->light0Vec.x = light0vecNorm.x;
        animData->light0Vec.y = light0vecNorm.y;
        animData->light0Vec.z = light0vecNorm.z;
    }
}

static const struct CameraScript sCameraScript_HG[5] = {
    {
     .pos = {
            .x = FX32_CONST(180),
            .y = FX32_CONST(177),
            .z = FX32_CONST(301),
        },
     .duration = 10,
     },
    {
     .pos = {
            .x = FX32_CONST(335),
            .y = FX32_CONST(-293),
            .z = FX32_CONST(296),
        },
     .duration = 5,
     },
    {
     .pos = {
            .x = FX32_CONST(180),
            .y = FX32_CONST(177),
            .z = FX32_CONST(301),
        },
     .duration = 5,
     },
    {
     .pos = {
            .x = FX32_CONST(625),
            .y = FX32_CONST(152),
            .z = FX32_CONST(256),
        },
     .duration = 10,
     },
    {
     .pos = {
            .x = FX32_CONST(0),
            .y = FX32_CONST(0),
            .z = FX32_CONST(0),
        },
     .duration = 0,
     },
};

static const struct CameraScript sCameraScript_SS[5] = {
    {
     .pos = {
            .x = FX32_CONST(105),
            .y = FX32_CONST(162),
            .z = FX32_CONST(291),
        },
     .duration = 10,
     },
    {
     .pos = {
            .x = FX32_CONST(395),
            .y = FX32_CONST(432),
            .z = FX32_CONST(191),
        },
     .duration = 5,
     },
    {
     .pos = {
            .x = FX32_CONST(105),
            .y = FX32_CONST(162),
            .z = FX32_CONST(291),
        },
     .duration = 5,
     },
    {
     .pos = {
            .x = FX32_CONST(420),
            .y = FX32_CONST(87),
            .z = FX32_CONST(331),
        },
     .duration = 10,
     },
    {
     .pos = {
            .x = FX32_CONST(0),
            .y = FX32_CONST(0),
            .z = FX32_CONST(0),
        },
     .duration = 0,
     },
};

static fx32 fx32_abs(fx32 x) {
    return x < 0 ? -x : x;
}

#if 0
// Maybe originally intended, but never used
#define CAMERA_SPEED (animData->cameraSpeed)
#else
#define CAMERA_SPEED (5 * FX32_ONE)
#endif

static void TitleScreenAnim_GetCameraNextPosition(TitleScreenAnimData *animData) {
    const struct CameraScript *cameraScript = animData->gameVersion == VERSION_HEARTGOLD ? sCameraScript_HG : sCameraScript_SS;
    ++animData->cameraSceneTimer;
    if (animData->cameraSceneTimer > cameraScript[animData->cameraScene].duration * 30) {
        VecFx32 pos;
        VEC_Subtract(&cameraScript[animData->cameraScene].pos, &animData->cameraPosEnd, &pos);
        if (pos.x > FX32_ONE) {
            animData->cameraPosEnd.x += CAMERA_SPEED;
        }
        if (pos.x < -FX32_ONE) {
            animData->cameraPosEnd.x -= CAMERA_SPEED;
        }
        if (pos.y > FX32_ONE) {
            animData->cameraPosEnd.y += CAMERA_SPEED;
        }
        if (pos.y < -FX32_ONE) {
            animData->cameraPosEnd.y -= CAMERA_SPEED;
        }
        if (pos.z > FX32_ONE) {
            animData->cameraPosEnd.z += CAMERA_SPEED;
        }
        if (pos.z < -FX32_ONE) {
            animData->cameraPosEnd.z -= CAMERA_SPEED;
        }
        Camera_SetLookAtCamPos(&animData->cameraPosEnd, animData->hooh_lugia.camera);
        if (fx32_abs(pos.x) <= FX32_ONE && fx32_abs(pos.y) <= FX32_ONE && fx32_abs(pos.z) <= FX32_ONE) {
            animData->cameraSceneTimer = 0;
            ++animData->cameraScene;
            if (cameraScript[animData->cameraScene].pos.x == 0) {
                animData->cameraScene = 0;
            }
        }
    }
}

static void TitleScreenAnim_FadeInGameTitleLayer(TitleScreenAnimData *animData) {
    (void)animData;
}
