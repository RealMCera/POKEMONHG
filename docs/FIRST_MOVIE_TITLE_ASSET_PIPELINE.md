# First Movie Title Asset Pipeline

The HGSS title screen is already fully decompiled in `src/title_screen.c` and its graphics are packed into `files/demo/title/titledemo.narc`.

## Current First Movie changes
- Start-button cry is Mewtwo.
- The stock HGSS title renderer/state machine remains intact for stability.

## Confirmed title NARC roles from source
The title system loads these 2D resource groups:
- HeartGold version-specific SUB BG3 graphics: `titledemo_00000034.NCGR` + `titledemo_00000035.NSCR`
- HeartGold SUB BG2 graphics/palette: `titledemo_00000003.NCGR` + `titledemo_00000004.NCLR` + shared `titledemo_00000000.NSCR`
- Shared SUB BG1 graphics: `titledemo_00000015.NCGR` + `titledemo_00000017.NSCR`
- HeartGold 3D mascot/model set: files 25-29
- HeartGold sparkle set: files 38-40

## Safe replacement order
1. Replace the 2D logo/background layers first.
2. Rebuild and boot-test.
3. Only after 2D is stable, replace or disable the stock Ho-Oh 3D model.
4. Keep the existing input/fade/menu state machine.

Do not blindly replace an NCGR without a matching NSCR/palette layout. A mismatched tilemap is one of the easiest ways to get the sliced/corrupt title-screen effect seen in earlier DS tests.

## Target artwork
Final artwork should be authored for the Nintendo DS 256x192 screen and then converted into the matching NCGR/NSCR/NCLR resource set.

The project should use original First Movie-inspired fan-game artwork supplied/created for this project rather than redistributing ripped commercial title assets.
