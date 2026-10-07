# Rare Emerald — Full Game Build Plan

Rare Emerald is a Nintendo DS remake/remaster of Pokémon Emerald using the native Pokémon HeartGold/SoulSilver engine. Pokémon Emerald is the authority for story progression, major encounters, gyms, rival logic, Team Aqua/Magma sequencing, legendary events, and postgame progression. HGSS provides the DS runtime, save system, field engine, battle engine, menus, audio, sprites, transitions, and hardware compatibility.

## Non-negotiable goals

- Boot as a normal Nintendo DS ROM in DeSmuME and on an R4-class flashcart.
- Preserve native HGSS save/load, battle, menu, and field systems wherever possible.
- Rebuild Hoenn progressively rather than replacing the DS engine with a custom renderer.
- Follow Emerald story logic rather than Ruby/Sapphire logic when the games differ.
- Use Rayquaza as the central legendary resolution of the Groudon/Kyogre crisis.
- Remove stray HGSS, Platinum, Magma Ruby, or placeholder trainer names/dialogue.
- Keep each milestone bootable and save-compatible.

## Production milestones

### Milestone 1 — Opening vertical slice

- Rare Emerald title screen
- New game handoff
- Littleroot Town
- Player house and Mom sequence
- Rival house
- Route 101
- Professor Birch rescue
- Starter bag
- Treecko / Torchic / Mudkip choice
- Zigzagoon battle
- Birch Lab return
- Route 103 rival battle
- Pokédex handoff
- Oldale Town

### Milestone 2 — Petalburg to Rustboro

- Routes 102 and 104
- Petalburg City
- Norman introduction
- Wally catching tutorial
- Petalburg Woods
- Team Aqua encounter
- Rustboro City
- Rustboro Gym / Roxanne
- Stone Badge
- Devon Goods theft
- Route 116 / Rusturf Tunnel rescue

### Milestone 3 — Dewford and Slateport

- Mr. Briney travel flow
- Dewford Town
- Dewford Gym / Brawly
- Knuckle Badge
- Granite Cave / Steven
- Slateport City
- Stern's Shipyard
- Oceanic Museum Team Aqua event

### Milestone 4 — Mauville and central Hoenn

- Route 110 rival encounter
- Mauville City
- Mauville Gym / Wattson
- Dynamo Badge
- Verdanturf Town
- Rusturf Tunnel completion
- Route 111 / 112 progression
- Fiery Path
- Fallarbor Town
- Meteor Falls Team Aqua/Magma sequence

### Milestone 5 — Mt. Chimney and Lavaridge

- Cable Car
- Mt. Chimney conflict
- Team Magma boss sequence
- Jagged Pass
- Lavaridge Town
- Lavaridge Gym / Flannery
- Heat Badge
- Go-Goggles handoff

### Milestone 6 — Norman and Surf progression

- Return to Petalburg
- Petalburg Gym / Norman
- Balance Badge
- Surf unlock
- Routes 105–109 / water traversal
- Abandoned Ship content target
- New Mauville optional content target

### Milestone 7 — Weather Institute and Fortree

- Route 119
- Weather Institute takeover
- Castform reward
- Rival encounter
- Fortree City
- Devon Scope / invisible Kecleon progression
- Fortree Gym / Winona
- Feather Badge

### Milestone 8 — Lilycove, Mt. Pyre, and villain bases

- Routes 120–123
- Mt. Pyre
- Red Orb / Blue Orb story sequence as appropriate to Emerald
- Team Magma Hideout
- Groudon awakening sequence
- Lilycove City
- Rival encounter
- Team Aqua Hideout
- Wailmer blockade removal

### Milestone 9 — Mossdeep and ocean progression

- Routes 124–127
- Mossdeep City
- Mossdeep Gym / Tate & Liza
- Mind Badge
- Space Center Team Magma event
- Steven partner battle target
- Dive unlock

### Milestone 10 — Seafloor Cavern and Emerald climax

- Underwater routes
- Seafloor Cavern
- Team Aqua / Archie confrontation
- Kyogre awakening
- Groudon vs. Kyogre crisis
- Sootopolis lockdown
- Steven / Wallace guidance
- Sky Pillar
- Rayquaza awakening
- Rayquaza resolves the weather crisis

### Milestone 11 — Final badge and League

- Sootopolis Gym / Juan
- Rain Badge
- Waterfall unlock
- Ever Grande City
- Victory Road
- Wally final pre-League battle
- Elite Four
- Champion Wallace
- Hall of Fame
- Credits / postgame return

### Milestone 12 — Emerald postgame

- Battle Frontier foundation
- Scott progression
- Frontier facilities as practical within HGSS systems
- Fossil Maniac / Desert Underpass target
- Steven postgame battle target
- Legendary and optional encounter cleanup
- National Pokédex/postgame unlock logic as appropriate to Rare Emerald

## Content migration tracks

The project advances on parallel tracks, but no track may break the current playable build.

### Maps

1. Temporary HGSS shell maps
2. Hoenn collision and warp layout
3. Hoenn tilesets and map graphics
4. Object placement
5. Camera / matrix polish
6. Final visual pass

### Scripts and story

1. Chapter state
2. Warp gates
3. NPC dialogue
4. Trigger regions
5. Trainer battles
6. Gym progression
7. Villain-event choreography
8. Legendary sequences
9. Postgame flags

### Pokémon data

- Emerald encounter tables
- Trainer parties
- Gym and Elite Four parties
- Rival starter-dependent teams
- Static encounters
- Gift Pokémon
- Starter logic
- Evolution/move compatibility decisions documented separately if DS mechanics differ from Gen III

### Presentation

- Rare Emerald title screen
- Hoenn map naming
- Emerald-oriented intro presentation
- UI cleanup where HeartGold branding leaks through
- Rayquaza-focused title/legendary presentation
- Credits identifying Rare Emerald as a fan project

## Build validation

Every promoted build must pass:

1. ROM builds without a fatal error.
2. ROM boots in DeSmuME.
3. Title screen appears correctly.
4. New Game and Continue both work.
5. Player can enter the current campaign area.
6. Normal movement works.
7. Doors and warps work.
8. Required story triggers fire once and only when intended.
9. Battles return to the field correctly.
10. Save and reload preserve `VAR_RARE_EMERALD_CHAPTER`.
11. No unrelated trainer names or placeholder dialogue appear in completed areas.
12. Current checkpoint is tested on real DS/R4 before being treated as hardware-safe.

## Current coding rule

`VAR_RARE_EMERALD_CHAPTER` is the primary coarse campaign state. Existing chapter numbers must never be renumbered after a build has been distributed or used for saves. Fine-grained one-time events should use dedicated flags/variables only when needed rather than overloading the chapter value.

## Definition of “whole game complete”

Rare Emerald is considered feature-complete when a new save can progress from the opening sequence through Wallace and the Hall of Fame using Hoenn story/map content, all eight Emerald gyms work, the Team Aqua/Magma and Rayquaza climax matches Emerald's story flow, saving/loading works throughout, and the resulting `.nds` is stable in emulator and on the target R4 setup. Postgame/Frontier work can continue after the main-game completion gate if necessary.
