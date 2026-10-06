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

# Reuse the already-working First Movie Metrowerks toolchain when this fresh
# Rare Emerald checkout does not have it locally. This directory is intentionally
# not stored in git.
MWASM="$ROOT/tools/mwccarm/2.0/sp2p2/mwasmarm.exe"
FIRST_MOVIE="/c/Users/FrontDesk/Downloads/PokemonFirstMovieHGSS/tools/mwccarm"

if [ ! -f "$MWASM" ]; then
  echo "Metrowerks tools are missing from this checkout."
  if [ -d "$FIRST_MOVIE" ]; then
    echo "Reusing local First Movie toolchain..."
    mkdir -p "$ROOT/tools/mwccarm"
    cp -r "$FIRST_MOVIE"/* "$ROOT/tools/mwccarm/" || fail "Could not copy First Movie mwccarm tools"
  else
    fail "Missing tools/mwccarm and no First Movie toolchain found at $FIRST_MOVIE"
  fi
fi

[ -f "$MWASM" ] || fail "mwasmarm.exe is still missing after toolchain setup"

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
