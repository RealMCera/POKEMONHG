# Pass 02 — Harbor, Storm Crossing, New Island Arrival

## Implemented
- Ash/Misty/Brock invitation sequence now warps directly into the harbor chapter.
- Temporary harbor map uses the HGSS Olivine port exterior so the scene runs on a real dock environment.
- Harbor sequence includes:
  - storm warning
  - Misty objecting to the crossing
  - Ash choosing to continue
  - Pikachu response
  - departure into the storm
- Temporary storm crossing uses the S.S. Aqua 1F map.
- Native HGSS field effects provide repeated screen shake during the crossing.
- Storm dialogue leads into the first view of New Island.
- Temporary New Island arrival uses the Whirl Islands Lugia cave because it already supplies a dramatic stone-and-water environment.
- Arrival sequence advances the campaign to the Mewtwo reveal chapter.

## Current campaign path
New Game
-> Mewtwo Laboratory
-> Giovanni Facility
-> Evaluation Test A
-> Evaluation Test B
-> Mewtwo Breakaway
-> Ash / Misty / Brock Invitation
-> Old Shore Wharf
-> Storm Crossing
-> New Island Arrival
-> Mewtwo Reveal chapter

## Temporary assets
The three Pass 02 locations currently reuse HGSS maps while dedicated First Movie geometry is authored:
- Harbor: Olivine port exterior
- Storm: S.S. Aqua 1F
- New Island arrival: Whirl Islands Lugia cave

The scripting, state changes, warps, party, and effects are already running through HGSS systems; these locations can later be replaced without rebuilding the campaign logic.
