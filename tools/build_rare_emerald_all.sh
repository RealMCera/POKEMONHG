#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LOG_DIR="$ROOT/build_logs"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
LOG="$LOG_DIR/rare_emerald_build_$STAMP.log"

exec > >(tee "$LOG") 2>&1

echo "=== Rare Emerald full build ==="
echo "Root: $ROOT"
echo "Log:  $LOG"
echo

fail() {
  echo
  echo "BUILD STOPPED"
  echo "Reason: $1"
  echo "Full log: $LOG"
  exit 1
}

# Reuse the already-working First Movie proprietary/local build dependencies
# when this fresh Rare Emerald checkout does not have them. None of these files
# are committed to git.
FIRST_MOVIE_ROOT="/c/Users/FrontDesk/Downloads/PokemonFirstMovieHGSS"
MWASM="$ROOT/tools/mwccarm/2.0/sp2p2/mwasmarm.exe"
FIRST_MOVIE_MWCC="$FIRST_MOVIE_ROOT/tools/mwccarm"

if [ ! -f "$MWASM" ]; then
  echo "Metrowerks tools are missing from this checkout."
  if [ -d "$FIRST_MOVIE_MWCC" ]; then
    echo "Reusing local First Movie toolchain..."
    mkdir -p "$ROOT/tools/mwccarm"
    cp -r "$FIRST_MOVIE_MWCC"/* "$ROOT/tools/mwccarm/" || fail "Could not copy First Movie mwccarm tools"
  else
    fail "Missing tools/mwccarm and no First Movie toolchain found at $FIRST_MOVIE_MWCC"
  fi
fi

[ -f "$MWASM" ] || fail "mwasmarm.exe is still missing after toolchain setup"

# Reuse the Nintendo/NitroSDK command-line tools used by the linker/ROM packer.
# Copy the whole local bin directory so makelcf, makerom, makebanner, ntrcomp,
# and any related helpers are available together rather than failing one by one.
FIRST_MOVIE_BIN="$FIRST_MOVIE_ROOT/tools/bin"
if [ ! -f "$ROOT/tools/bin/makelcf.exe" ]; then
  if [ -d "$FIRST_MOVIE_BIN" ]; then
    echo "Reusing local First Movie NitroSDK tools/bin..."
    mkdir -p "$ROOT/tools/bin"
    cp -r "$FIRST_MOVIE_BIN"/* "$ROOT/tools/bin/" || fail "Could not copy First Movie tools/bin"
  else
    fail "Missing tools/bin/makelcf.exe and no First Movie tools/bin found at $FIRST_MOVIE_BIN"
  fi
fi

for sdktool in makelcf.exe makerom.exe makebanner.exe; do
  [ -f "$ROOT/tools/bin/$sdktool" ] || fail "tools/bin/$sdktool is missing after NitroSDK tool setup"
done

# NitroSDK linker templates are also local/proprietary build dependencies and
# are intentionally not tracked in git. Reuse the copies from the working
# First Movie checkout when they are absent here.
for template in ARM9-TS.lcf.template mwldarm.response.template; do
  if [ ! -f "$ROOT/$template" ] && [ -f "$FIRST_MOVIE_ROOT/$template" ]; then
    echo "Reusing local First Movie $template..."
    cp "$FIRST_MOVIE_ROOT/$template" "$ROOT/$template" || fail "Could not copy $template"
  fi
done

if [ ! -f "$ROOT/sub/ARM7-TS.lcf.template" ]; then
  if [ -f "$FIRST_MOVIE_ROOT/sub/ARM7-TS.lcf.template" ]; then
    echo "Reusing local First Movie ARM7-TS.lcf.template..."
    cp "$FIRST_MOVIE_ROOT/sub/ARM7-TS.lcf.template" "$ROOT/sub/ARM7-TS.lcf.template" || fail "Could not copy ARM7-TS.lcf.template"
  elif [ -f "$FIRST_MOVIE_ROOT/ARM7-TS.lcf.template" ]; then
    echo "Reusing local First Movie ARM7-TS.lcf.template..."
    cp "$FIRST_MOVIE_ROOT/ARM7-TS.lcf.template" "$ROOT/sub/ARM7-TS.lcf.template" || fail "Could not copy ARM7-TS.lcf.template"
  fi
fi

[ -f "$ROOT/ARM9-TS.lcf.template" ] || fail "ARM9-TS.lcf.template is missing; copy it from the working First Movie HGSS project"
[ -f "$ROOT/mwldarm.response.template" ] || fail "mwldarm.response.template is missing; copy it from the working First Movie HGSS project"
[ -f "$ROOT/sub/ARM7-TS.lcf.template" ] || fail "sub/ARM7-TS.lcf.template is missing; copy it from the working First Movie HGSS project"

echo "[1/5] Building host tools..."
make tools || fail "Host tools failed"

echo

echo "[2/5] Applying mwasmarm patch..."
make patch_mwasmarm || fail "mwasmarm patch step failed"

echo

echo "[3/5] Building Rare Emerald ROM..."
make COMPARE=0 || fail "Main ROM build failed"

echo

echo "[4/5] Locating final .nds..."
ROM=""
for candidate in \
  "$ROOT/build/heartgold.us/pokeheartgold.us.nds" \
  "$ROOT/pokeheartgold.us.nds" \
  "$ROOT/build/pokeheartgold.us.nds"; do
  if [ -f "$candidate" ]; then
    ROM="$candidate"
    break
  fi
done

if [ -z "$ROM" ]; then
  ROM="$(find "$ROOT" -maxdepth 4 -type f -name '*.nds' 2>/dev/null | head -n 1 || true)"
fi

[ -n "$ROM" ] && [ -f "$ROM" ] || fail "Build returned success but no .nds file was found"

echo "ROM found: $ROM"

echo

echo "[5/5] Copying release candidate..."
mkdir -p "$ROOT/dist"
OUT="$ROOT/dist/Rare_Emerald_DS.nds"
cp "$ROM" "$OUT" || fail "Could not copy ROM to dist"

if command -v sha1sum >/dev/null 2>&1; then
  sha1sum "$OUT" | tee "$ROOT/dist/Rare_Emerald_DS.sha1"
fi

echo

echo "========================================"
echo "RARE EMERALD BUILD COMPLETE"
echo "Final ROM: $OUT"
echo "Build log: $LOG"
echo "========================================"
