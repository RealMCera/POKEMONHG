# Pass 03 — Grand Hall, Mewtwo Reveal, Clone Trials

## Implemented
- New Island arrival now enters a temporary Grand Hall map using the Pokémon League Champion room.
- The Grand Hall runs a First Movie-specific sequence:
  - gathered Trainers
  - Misty and Ash dialogue
  - Mewtwo voice/cry reveal
  - Mewtwo's challenge
- Campaign advances into the clone trial chapter.
- Clone arena temporarily uses Vermilion Gym.
- Added three dedicated battle records:
  - Clone Venusaur — level 36
  - Clone Blastoise — level 36
  - Clone Charizard — level 38
- All three battles use the native HGSS trainer battle engine.
- Party is healed between trial battles so the sequence can be tested as a continuous set piece.
- Completing all three battles advances the campaign to the cloning-lab chapter.

## Current playable spine
New Game
-> Mewtwo Laboratory
-> Giovanni Facility
-> Evaluation Battles
-> Mewtwo Breakaway
-> Ash / Misty / Brock
-> Invitation
-> Harbor
-> Storm Crossing
-> New Island Arrival
-> Grand Hall
-> Mewtwo Reveal
-> Clone Venusaur
-> Clone Blastoise
-> Clone Charizard
-> Clone Lab ready

## Placeholder presentation
The Champion room and Vermilion Gym are temporary layout stand-ins. Their scripts and battle progression can later be connected to dedicated New Island geometry without replacing the campaign-state logic.
