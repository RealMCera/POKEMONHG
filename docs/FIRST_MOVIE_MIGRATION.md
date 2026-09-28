# First Movie Content Migration Plan

The existing HGSS codebase supplies the engine. Movie-specific work should target content/data first and engine code only when necessary.

## Phase 1 — Preserve engine, replace entry flow
- New-game spawn moves to the Mewtwo prologue.
- Existing HGSS save, field, battle, menu, text, transition, and object systems stay intact.
- Title/intro flow will eventually be replaced with First Movie presentation.

## Phase 2 — Movie map set
Create/repurpose map headers, matrices, events, scripts, messages, and area data for:
- Mewtwo Laboratory
- Giovanni Training Facility
- Ash travel / invitation scene
- Old Shore Wharf
- Storm Crossing
- New Island Exterior
- New Island Entrance
- Grand Hall
- Stadium
- Clone Laboratory
- Final Arena

## Phase 3 — Characters
Use HGSS map-object and sprite infrastructure for:
- Ash
- Misty
- Brock
- Mewtwo
- Mew
- Nurse Joy / attendant
- invited trainers
- Giovanni
- scientists
- Team Rocket

## Phase 4 — Battles
Use the native HGSS battle engine. Movie encounters become scripted trainer/special battles instead of a custom battle implementation.

## Phase 5 — Script campaign
Field scripts become the campaign state machine. Each chapter ends by setting a story variable and warping/transitioning to the next map.

## Confirmed upstream systems
- `FieldSystem` owns map, camera, events, player avatar, map objects, field effects, and save access.
- map headers select matrix, script bank, script-header bank, message bank, events, weather, camera, and battle background.
- field scripts are assembled from `files/fielddata/script/scr_seq/`.
- the native battle system is already exposed through `include/battle/battle.h`.

## Build note
The upstream project currently requires Metrowerks tools and NitroSDK for a matching build; those proprietary tools are not included here.
