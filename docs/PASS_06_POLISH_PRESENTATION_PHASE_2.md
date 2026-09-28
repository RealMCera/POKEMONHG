# Pass 06 — Presentation Polish, Phase 2

## Implemented
- Giovanni's temporary facility now uses the actual HGSS Giovanni overworld sprite (SPRITE_SAKAKI).
- Ash's handoff room now includes dedicated visual stand-ins for Misty and Brock:
  - Misty uses the HGSS Cerulean Gym leader sprite.
  - Brock uses the HGSS Pewter Gym leader sprite.
- Misty and Brock receive simple scripted reactions during the invitation handoff scene.
- These objects are now exposed through the event header so later cinematic passes can move them directly.

## Why this matters
The campaign previously relied almost entirely on narration while reusing unrelated HGSS NPCs. This phase starts replacing those placeholders with recognizable character presentation while keeping the proven map and script flow intact.

## Next presentation work
- Add Mewtwo field representation for scripted scenes.
- Add stronger Giovanni staging in the facility.
- Improve Grand Hall crowd composition using recognizable trainer sprites.
- Begin dedicated First Movie title graphic integration.
- Prepare dedicated New Island map replacement plan.
