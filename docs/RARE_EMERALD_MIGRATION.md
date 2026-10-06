# Rare Emerald — HGSS Native DS Migration

Rare Emerald remains a Nintendo DS `.nds` project. Pokémon Emerald is the story and gameplay authority; the HGSS codebase supplies the native DS engine.

## Core rule
Do not recreate Pokémon Emerald in a separate custom renderer unless a system is genuinely unavailable in HGSS. Reuse the native HGSS field, battle, save, menu, text, sprite, transition, audio, and object systems, and replace content/data progressively.

## Build 0.1 vertical slice
The first playable target is:

1. New game / intro handoff
2. Littleroot Town
3. Route 101
4. Professor Birch chased by Zigzagoon
5. Bag interaction
6. Choose Treecko, Torchic, or Mudkip
7. Starter battle against Zigzagoon
8. Return to Birch's Lab
9. Starter ownership/state persists correctly

Temporary HGSS maps are used as shells while Hoenn maps are migrated:
- Littleroot player house -> New Bark player house 1F
- Littleroot -> New Bark Town
- Birch Lab -> Elm's Lab 1F
- Route 101 -> Route 29
- Route 103 -> Route 30
- Oldale -> Cherrygrove City

## Engine strategy
- Field scripts are the story state machine.
- `VAR_RARE_EMERALD_CHAPTER` tracks Rare Emerald campaign progress.
- Native HGSS Pokémon party creation and battle launch commands are used.
- Native save handling remains intact.
- Native title/menu/battle code remains intact unless Rare Emerald presentation requires a targeted patch.

## Emerald alignment requirements
- Story progression follows Pokémon Emerald, not Ruby.
- Rayquaza is the principal legendary/endgame story target where Emerald differs from Ruby.
- Rival, gym, Team Aqua/Magma, weather-trio, and event sequencing should match Emerald behavior unless explicitly redesigned.
- Character names and messages must not leak unrelated HGSS/Platinum/Magma Ruby trainer names.

## Build order
### Pass A — Boot and state
- Keep the game bootable as a normal HGSS-native ROM.
- Add Rare Emerald campaign constants.
- Redirect new-game progression into the temporary Littleroot shell.

### Pass B — Littleroot / Route 101
- Replace the temporary scripts/messages/events with Emerald's opening sequence.
- Add Birch rescue trigger and Zigzagoon encounter.

### Pass C — Starter selection
- Present Treecko, Torchic, and Mudkip.
- Give the selected starter through HGSS-native party code.
- Persist the selected species and story chapter.

### Pass D — Birch Lab return
- Warp/return to Birch Lab after the rescue battle.
- Replace Elm-specific dialogue/flags with Birch-specific Rare Emerald state.
- Confirm the player can enter/exit the lab normally.

### Pass E — Route 103 / rival
- Implement the first rival encounter using Emerald species/level logic.
- Return to Birch for Pokédex progression.

## Known historical problems this architecture is intended to avoid
- White-screen boot failures from custom DS builds.
- R4 incompatibility caused by non-native or fragile boot/runtime code.
- Proxy/custom graphics systems diverging from commercial DS behavior.
- Broken house/lab transitions from incomplete custom map collision/warp logic.
- Incorrect Ruby/Magma Ruby story details in an Emerald-target project.

## Validation gate for every build
A build is not promoted unless it:
- boots in a DS emulator,
- reaches the title/menu,
- starts a new game,
- loads the current Rare Emerald test map,
- allows normal movement and warps,
- can save/reload without corrupting story state.
