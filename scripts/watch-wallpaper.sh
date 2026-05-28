#!/bin/bash
set -euo pipefail

CFG="$HOME/.config/nitrogen/bg-saved.cfg"
[ -f "$CFG" ] || exit 0

TIMER_PID=""

inotifywait -m -e modify,attrib,close_write,move_self --format '%e' "$CFG" |
while read -r _; do
    # cancela timer anterior si existe
    if [ -n "${TIMER_PID:-}" ] && kill -0 "$TIMER_PID" 2>/dev/null; then
        kill "$TIMER_PID" 2>/dev/null || true
    fi

    # programa ejecución única después de que se calme el file-write
    (
      sleep 0.7
      "$HOME/.config/qtile/scripts/wallpaper_event.sh"
    ) &
    TIMER_PID=$!
done
