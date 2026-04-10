#!/bin/bash
# build.sh — reproducible build script for mypsx

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

SRC_DIR="$PROJECT_ROOT/src"
BIN_DIR="$PROJECT_ROOT/bin"

CC=gcc
CFLAGS="-std=gnu99 -Wall -Wextra -Werror -O2"
INCLUDES="-I$SRC_DIR/core -I$SRC_DIR/cli -I$SRC_DIR/util"

SOURCES=(
    "$SRC_DIR/cli/main.c"
    "$SRC_DIR/core/maps.c"
    "$SRC_DIR/core/proc_enum.c"
    "$SRC_DIR/core/proc_info.c"
)

echo "[*] Building mypsx..."
mkdir -p "$BIN_DIR"

$CC $CFLAGS $INCLUDES "${SOURCES[@]}" -o "$BIN_DIR/mypsx"

echo "[✓] Build complete: bin/mypsx"
