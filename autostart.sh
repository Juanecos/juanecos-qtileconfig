#!/bin/bash

#configuracion de inicio para qtile



udiskie -t &
volumeicon &
cbatticon -u 5 &
nm-applet &
onboard &
#
#para que funcionen debe estar el widget de systray
picom &
# nitrogen
nitrogen --restore &

#mapeo de tecla p que no me sirve, mejor oner la tecla ¿¡ qie esta al lado del backspace y la del Escape
xmodmap -e "keycode 21=p"
xmodmap -e "keycode 49=Escape"

#redshift default color
redshift -P -O 4000
