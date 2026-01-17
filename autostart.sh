#!/bin/bash

#configuracion de inicio para bspwm
#

#udiskie -t &
nm-applet &
#onboard
#onboard &

#sxhkd &
#para que funcionen debe estar el widget de systray
picom &
# nitrogen
nitrogen --restore &
#mpd
#mpd ~/.config/mpd/mpd.conf &
#mpc update &

#polkit de kde
if ! pgrep -x polkit-kde-authentication-agent-1 > /dev/null; then
    /usr/lib/polkit-kde-authentication-agent-1 &
fi


#layout teclado internacional con altgr
#setxkbmap -layout us -variant intl
#setxkbmap latam

#redshift default color
redshift -P -O 5000


