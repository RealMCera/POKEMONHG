# Pass 06 — Polish + Postgame, Phase 1

## Implemented
- Local bootstrap ROM workspace is now explicitly ignored by Git through .first_movie/.
- The existing HGSS title-screen renderer now uses Mewtwo's cry when the player starts the game.
- Added three stronger postgame clone rematch teams:
  - Clone Venusaur EX — level 50
  - Clone Blastoise EX — level 50
  - Clone Charizard EX — level 52
- The harbor seaman becomes a postgame ferry interaction after the main story.
- The ferry offers a return trip to New Island.
- Returning to the temporary clone arena starts a repeatable three-battle challenge.
- The party is healed between rematch rounds.
- Completing the postgame challenge returns the player to the harbor.

## Still to do in Pass 06
- Replace temporary HGSS stand-in maps with dedicated First Movie maps.
- Replace placeholder field sprites with Ash, Misty, Brock, Giovanni, Mewtwo and island-specific NPC presentation.
- Replace stock title visuals with the dedicated First Movie title artwork while retaining the proven title-screen state machine.
- Add more cinematic camera movement and sound timing.
- Compile/debug every changed script and trainer record.
- Validate in melonDS and then on real DS/R4 hardware.
