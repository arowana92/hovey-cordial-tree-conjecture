#!/bin/sh
# Replay the eight-label theorem from the published archive in a fresh module path.
set -eu
repo=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
build=$(mktemp -d)
trap 'rm -rf "$build"' EXIT
lean_bin=${LEAN:-lean}
export LEAN_PATH="$build"
cd "$repo"
python3 -B research/eight/lean_tables.py "$build/research/eight"
python3 -B -m research.eight.kernel_base "$build/research/eight"
"$lean_bin" -o "$build/research/Reduction.olean" research/Reduction.lean
"$lean_bin" -o "$build/research/eight/Base.olean" research/eight/Base.lean
"$lean_bin" -o "$build/research/eight/BaseCheck.olean" research/eight/BaseCheck.lean
(cd "$build" && "$lean_bin" -j 2 -o research/eight/BaseRows.olean research/eight/BaseRows.lean)
"$lean_bin" -o "$build/research/eight/Representation.olean" research/eight/Representation.lean
"$lean_bin" -o "$build/research/eight/Tree.olean" research/eight/Tree.lean
(cd "$build" && "$lean_bin" -o research/eight/Data.olean research/eight/Data.lean)
"$lean_bin" research/eight/Certificate.lean
