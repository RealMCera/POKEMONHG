# Pass 06 — Presentation Polish, Phase 4

## Implemented
- Male walking player avatar now uses HGSS Red as the temporary Ash stand-in.
- The player avatar is hidden during the Mewtwo awakening.
- The player avatar remains hidden during the Giovanni/Mewtwo facility segment.
- Mewtwo's field object is therefore the visible focal character during the facility sequence.
- The player avatar is explicitly restored when the story switches to Ash.
- Added a source-backed map of the HGSS title NARC resources so the final title art can be integrated without corrupting NCGR/NSCR/palette pairings.

## Result
The playable identity now changes visually with the story:
Mewtwo prologue -> visible Mewtwo field representation -> Ash campaign -> Kanto Red/Ash stand-in.

Dedicated Ash sprites can later replace the Red stand-in without changing the campaign scripts.
