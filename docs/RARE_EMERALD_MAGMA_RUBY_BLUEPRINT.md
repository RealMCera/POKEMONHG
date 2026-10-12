# Rare Emerald — Magma Ruby Blueprint

Magma Ruby is the primary presentation and map-design blueprint for Rare Emerald. Pokémon Emerald remains the canonical story/gameplay authority, while the HGSS codebase remains the native Nintendo DS engine foundation.

Reference walkthrough:
- https://www.youtube.com/watch?v=iYcOiyV5bvw

## Source hierarchy

When references disagree, use this order:

1. **Pokémon Emerald** — story order, Emerald-exclusive events, rival progression, Team Aqua/Magma structure, weather trio, Rayquaza, gyms, items, progression flags, and endgame.
2. **Pokémon Magma Ruby** — DS-era Hoenn presentation, map composition, visual pacing, scene staging, environmental scale, character placement, and the overall feeling of a Hoenn remake running on Nintendo DS hardware.
3. **Pokémon HeartGold/SoulSilver** — native engine systems: field engine, battles, menus, save data, scripts, movement, followers, text, audio, transitions, objects, and DS runtime behavior.
4. **Temporary HGSS shell maps** — only scaffolding until real Hoenn-style maps replace them.

## What to copy from Magma Ruby conceptually

Rare Emerald should feel visually and structurally close to Magma Ruby without becoming a Ruby-story game.

### World presentation
- Hoenn maps rebuilt at Nintendo DS scale rather than simply copying GBA tile-for-tile.
- Gen IV-style 3D/2.5D field presentation.
- Larger town and route compositions with DS-era depth, trees, elevation, shadows, cliffs, water, and building scale.
- Hoenn landmarks should remain immediately recognizable even when the map is redesigned for DS proportions.
- Indoor maps should preserve the identity of Emerald locations while using native DS camera, collision, and event behavior.

### Character presentation
- Brendan/May should use Hoenn-appropriate overworld, front, and back sprites.
- Professor Birch, Wally, Norman, Team Aqua, Team Magma, gym leaders, and major NPCs should not visibly reuse unrelated Johto/Sinnoh identities once replacement assets are available.
- Native HGSS follower support is a desirable Rare Emerald feature where technically stable.

### Event staging
- Use DS-native walk-ins, NPC movement, camera movement, pauses, facing changes, sound cues, fades, and battle transitions instead of recreating GBA scenes literally.
- Major Emerald moments should be staged like a commercial Gen IV DS event while preserving Emerald's actual story outcome.
- Avoid stock HGSS story scenes leaking into Rare Emerald (Lyra/Marill/Elm, Johto phone/tutorial scenes, etc.).

### Battles and systems
- Keep HGSS-native battle/runtime systems for stability and R4 compatibility.
- Hoenn starters: Treecko, Torchic, Mudkip.
- Preserve Gen IV physical/special mechanics and DS presentation.
- Rare Emerald may adopt Magma Ruby-style quality-of-life/presentation ideas when they do not conflict with Emerald progression.

## What NOT to copy from Magma Ruby

- Ruby-exclusive story sequencing when Emerald differs.
- Groudon as the sole central legendary plot.
- Ruby-only Team Magma/Aqua roles.
- Any Magma Ruby-specific trainer names, credits, branding, dialogue, or residual project text.
- Platinum-specific story logic simply because Magma Ruby uses a Platinum base.

Rare Emerald's late-game authority is Emerald: the Groudon/Kyogre crisis leads to Sky Pillar and Rayquaza, followed by the Emerald Sootopolis resolution.

## Opening target

The opening should visually feel like a DS Hoenn remake, following the same broad presentation philosophy seen in Magma Ruby, but the event state machine must be Emerald-correct:

1. New game / Hoenn intro
2. Player arrives in Littleroot
3. Player house / Mom sequence
4. Explore Littleroot
5. Birch is absent from the lab
6. Route 101 Birch rescue
7. Choose Treecko, Torchic, or Mudkip from Birch's bag
8. Wild rescue battle
9. Return to Birch's Lab
10. Starter ownership is confirmed
11. Travel through Oldale to Route 103
12. First May/Brendan rival battle with the correct counter-starter
13. Rival tells player to return to the lab
14. Return to Birch
15. Pokédex progression
16. Continue toward Oldale / Route 102 / Petalburg

Stock HGSS New Bark opening logic must be bypassed rather than cosmetically renamed.

## Map migration order

Build actual Hoenn-style maps in this order so the playable vertical slice expands cleanly:

1. Littleroot player house
2. Littleroot Town
3. Birch Lab
4. Route 101
5. Oldale Town
6. Route 103
7. Route 102
8. Petalburg City
9. Route 104
10. Petalburg Woods
11. Rustboro City

Each map should be visually compared against both Emerald and Magma Ruby: Emerald determines what the place is; Magma Ruby helps determine how that place should feel on Nintendo DS.

## Build rule

Do not promote a Rare Emerald pass merely because it compiles. Every pass must be tested for:
- emulator boot,
- title/menu,
- correct story state,
- no stock HGSS story leakage,
- movement/collision/warps,
- battles,
- save/reload,
- and eventual R4 hardware boot.
