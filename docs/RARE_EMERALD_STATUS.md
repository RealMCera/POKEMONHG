# Rare Emerald — Persistent Project Status

This file is the permanent checkpoint for Rare Emerald. Update it whenever meaningful work is completed, a blocker is found, or the beta scope changes.

## Source of truth

- Engine/base: `pret/pokeheartgold` on branch `rare-emerald`
- Canonical game behavior/story/maps: Pokémon Emerald decomp
- DS-era reference when useful: Pokémon Platinum decomp
- Magma Ruby: donor/reference/correlation material only; **not** the runtime base

## Available local reference archives

The working sessions have access to user-provided source archives for:

- `pokeemerald-master(2).zip`
- `pokeplatinum-main(1).zip`
- `POKEMONHG-cicd-calcrom-2(1).zip`

These are reference inputs. Important findings and implemented changes must be committed to GitHub so progress does not depend on a temporary chat/container session.

## Current branch

- Repository: `RealMCera/POKEMONHG`
- Branch: `rare-emerald`
- Last verified head before this status file: `c149484a5c022144005493569ab072e201ecf1bb`
- Last verified commit message: `Ignore local Rare Emerald ROM-derived cache`

## Current build blocker

Latest verified GitHub Actions run:

- Workflow: `Rare Emerald build`
- Run ID: `37984384462`
- Job ID: `114002650653`
- Failed step: `Build Rare Emerald (HeartGold base)`
- Setup, checkout, repo setup, swap setup, and source normalization all completed successfully.
- ROM artifact upload was skipped because the build step failed.
- Failure archive upload succeeded.

The next engineering task is to extract the exact compiler/link/ROM-assembly error from the failed job/failure artifact, patch the source, and rerun CI until the build is green.

## Beta acceptance target

Rare Emerald is not considered Beta until the project can satisfy all of the following:

1. Boots reliably in an emulator.
2. Starts in Littleroot.
3. Correct Brendan/May handling.
4. Player house and Mom sequence work.
5. Professor Birch/lab sequence works.
6. Route 101 works.
7. Starter selection works.
8. First rival battle works.
9. Oldale works.
10. Route 102 works.
11. Petalburg progression works.
12. Pokémon Center, Mart, houses, and doors work.
13. Saving/loading works.
14. Wild encounters work.
15. Trainer battles work.
16. Important Emerald flags/events do not softlock progression.
17. HGSS-style UI/assets are stable.
18. Rare Emerald branding/title screen works.
19. A clean reproducible `.nds` build is produced.
20. Release is distributed as `Rare_Emerald_Beta.xdelta`, not as a Nintendo ROM.

## Branding direction

- Title: Rare Emerald
- Legendary focus: Rayquaza
- Copyright year: 2026
- Credit: `RealMCera`
- Remove `www.pokehacking.com`
- DS top/bottom title-screen layout

## Release direction

Preferred release flow:

```text
clean HeartGold base ROM
        ↓ hash verification
Rare Emerald HGSS-native build
        ↓ xdelta3 encode
Rare_Emerald_Beta.xdelta
        ↓ test apply
reconstructed test ROM
        ↓ SHA-256 compare against built ROM
PASS
```

The clean Nintendo base ROM must not be committed or distributed.

## Persistence rule

From this point forward:

- Significant code/data fixes go directly onto `rare-emerald` in GitHub.
- Build/beta milestones are recorded in this file.
- Temporary generated files are not treated as completed work until the relevant source/configuration is committed.
- Do not claim a feature or beta milestone is complete unless build/test evidence supports it.
