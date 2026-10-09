# Magma Ruby source manifest for Rare Emerald

The uploaded `POKEMON_MAGMA_RUBY_decomp` is a Platinum-family Nintendo DS decomp/NitroFS extraction. Rare Emerald remains an HGSS-engine project; these resources are migration/reference inputs, not drop-in HGSS archives.

## Verified source

- ROM title: `POKEMON MR`
- Game code: `PMRE`
- ROM SHA-256: `69be21a3f1003a5649e27cacdb3cbd7923f5f7c4992ce2dc56dcf81c0cbbc46e`
- NitroFS files: 462
- ARM9 overlays: 122

## High-value resources

| Resource | Members | Size | SHA-256 | Rare Emerald treatment |
| --- | ---: | ---: | --- | --- |
| `fielddata/script/scr_seq.narc` | 1125 | 310460 | `8872fd996e159982379914e467c102701913b50c1425b599a61b517bdb986662` | Translate Platinum script commands/IDs to HGSS |
| `fielddata/eventdata/zone_event.narc` | 534 | 157092 | `502410f7d024167f1ff694b39dd6c7d07aea2050a15a3d8e1fd90c953ae8582a` | Translate object/warp/trigger records |
| `fielddata/land_data/land_data.narc` | 666 | 16420542 | `a7b7ed98c89f953daa5988b06e06876ca6a271e281f7ba8ade41304bf4300f58` | Convert map geometry/model dependencies to HGSS field format |
| `fielddata/mapmatrix/map_matrix.narc` | 289 | 13049 | `252460865c7fb6e3220aef96f8b8a2255e00da726e4ddcbe6cf594a9209ffbbc` | Translate matrices and map-header links |
| `fielddata/encountdata/pl_enc_data.narc` | 183 | 79108 | `c4fedca8f0864b9a40ea68cfba6f6ea3fd46c92f7a8c7effab9a01f5b3e9e219` | Convert encounter slots/species to HGSS encounter data |
| `poketool/trainer/trdata.narc` | 928 | 26036 | `f7f1756250101b4f5a0460ed523084c68e350b7eeb44846671811e4dab015da3` | Translate trainer metadata to HGSS trainer JSON/data |
| `poketool/trainer/trpoke.narc` | 928 | 28624 | `81ed62c42d7ca22a7edc98479632ee78aa7b958700cd9152b85185008d9f4315` | Translate parties, moves, items and forms |
| `demo/title/titledemo.narc` | 29 | 251640 | `e56eb73f22814b4afa1dbd63ce129d329d5711d4762a38c7fe59add2c58e7022` | Reference/extract compatible title presentation pieces |

## Migration rule

Never overwrite an HGSS NARC with the Platinum-family NARC directly. The importer must decode the Magma Ruby member, map Platinum IDs/commands/header fields to HGSS equivalents, then emit the native HGSS source representation used by `pokeheartgold`.

## Priority order

1. Resolve map/script/event member relationships and identify Magma Ruby's Hoenn locations.
2. Convert Littleroot, Route 101, Birch Lab, Oldale and Route 103 as the first contiguous slice.
3. Convert Emerald trainer/encounter data and use HGSS-native battle/event systems.
4. Expand through Petalburg/Rustboro, then the remaining badge path.
5. Convert Aqua/Magma, weather-trio/Rayquaza, Pokémon League and postgame content.
6. Replace temporary HGSS map aliases only after each converted Hoenn map passes boot, warp, collision, save/reload and R4 tests.

Use `tools/rare_emerald/magma_ruby_manifest.py` to fingerprint another extraction before importing from it.
