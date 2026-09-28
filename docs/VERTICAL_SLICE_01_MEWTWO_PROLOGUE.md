# Vertical Slice 01 — Mewtwo Prologue

The first playable integration target is intentionally small: boot through the real HGSS new-game/field stack and land in a temporary map that represents Mewtwo's laboratory.

## What is live now
- HGSS new-game initialization
- HGSS save structures
- HGSS FieldSystem
- HGSS player/map object rendering
- HGSS collision and map loading
- HGSS script/event infrastructure
- native HGSS battle framework remains untouched

## Current temporary mapping
`MAP_FIRST_MOVIE_PROLOGUE_LAB` aliases `MAP_NEW_BARK_ELMS_LAB_1F`.

This is temporary. It gives us a known-good HGSS interior while we build the movie-specific lab map, scripts, sprites, and messages.

## Next implementation
1. Add a dedicated First Movie prologue script.
2. Replace the lab's object/event set with scientists + Mewtwo.
3. Add campaign variable `VAR_FIRST_MOVIE_CHAPTER`.
4. Redirect map transition scripts into the Giovanni facility.
5. Replace temporary map assets with the movie-faithful lab.
