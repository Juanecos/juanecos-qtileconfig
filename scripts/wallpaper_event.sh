#!/bin/bash
set -euo pipefail

LOCKFILE="/tmp/qtile_wallpaper.lock"
NITROGEN_CFG="$HOME/.config/nitrogen/bg-saved.cfg"
SCRIPT_DIR="$HOME/.config/qtile/scripts"

exec 9>"$LOCKFILE"
flock -n 9 || exit 0

# debounce: esperar que nitrogen termine
# sleep 0.35

# obtener SOLO el último wallpaper
WP=$(awk -F= '/^file=/ {print $2}' "$NITROGEN_CFG" | tail -n 1)
[ -z "$WP" ] && exit 0
[ ! -f "$WP" ] && exit 0


# generar paleta
/usr/bin/python3 "$SCRIPT_DIR/extract_colors.py" "$WP"

for i in 1 2 3 4 5; do
  if qtile cmd-obj -o cmd -f restart; then
    exit 0
  fi
  sleep 0.4
done
exit 0
