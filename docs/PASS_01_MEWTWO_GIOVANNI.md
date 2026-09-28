# Pass 01 — Mewtwo Prologue + Giovanni Facility

## Implemented
- New saves enter the real HGSS field engine through the temporary Mewtwo laboratory.
- Original Mewtwo awakening dialogue.
- Transition to the temporary Giovanni training facility.
- Temporary playable Level 30 Mewtwo.
- Two dedicated First Movie evaluation trainer records:
  - Test Unit A: Machamp + Alakazam
  - Test Unit B: Golem + Arcanine
- Native HGSS trainer battle flow for both evaluations.
- Giovanni control dialogue and Mewtwo breakaway beat.
- Mewtwo is removed from the temporary player party at the end of the sequence.
- Story transitions to the Ash campaign.
- Ash receives a temporary movie-era party: Pikachu, Bulbasaur, Squirtle, Charizard.
- Original Ash/Misty/Brock invitation scene.
- Campaign state advances to the harbor chapter.

## Still placeholder in Pass 01
- Laboratory and facility geometry currently reuse HGSS interiors.
- Player/NPC character graphics have not yet been replaced with Ash/Misty/Brock/Giovanni/Mewtwo-specific field sprites.
- Cinematic camera/effects are intentionally minimal until the branch builds and boots cleanly.

## Test checkpoint
The intended path is:
New Game -> Mewtwo Lab -> Giovanni Facility -> Evaluation Battle A -> Evaluation Battle B -> Breakaway -> Ash/Misty/Brock invitation -> Harbor-ready state.

This checkpoint should be compiled and boot-tested before Pass 02 expands the harbor/storm/New Island path.
