# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess
from libqtile import hook

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy


mod = "mod4"
terminal = "alacritty"
web_browser = "brave"
editor = "code"
explorer = "thunar"
# blue = "#1DA1F2"
blue = "#7F8CAA"
ars = "#8C426B"


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "j", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "k", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "i", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "j", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "i", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "j", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "k", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "i", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes

    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod,"shift"], "q", lazy.shutdown(), desc="Spawn a command using a prompt widget"),


    # Captura de pantalla
    Key([], "Print", lazy.spawn("scrot /home/juanecos/Imágenes/Screenshots/screenshot_%Y-%m-%d_%H-%M-%S.png"), desc="Captura toda la pantalla"),
    Key([mod, "Shift"], "s", lazy.spawn("scrot -s /home/juanecos/Imágenes/Screenshots/screenshot_%Y-%m-%d_%H-%M-%S.png"), desc="Captura seleccion"),
    Key([mod, "Control"], "Print", lazy.spawn("scrot -u /home/juanecos/Imágenes/Screenshots/screenshot_%Y-%m-%d_%H-%M-%S.png"), desc="Captura seleccion"),
    
    # scrot -u para la ventana  actual
    #como hacerlo al portapapeles?
    #quiero subirlelacalidadi} tambien
    #
    
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "r", lazy.spawn("qtile cmd-obj -o cmd -f restart"), desc="Restart Qtile"),
        
    # Menu de rofi
    Key([mod], "m", lazy.spawn("zsh /home/juanecos/.config/rofi/launchers/type-2/launcher.sh"), desc="Rofi menu"),
    
    # Menu de apagado 
    Key([mod, "control"], "delete", lazy.spawn("zsh /home/juanecos/.config/rofi/powermenu/type-2/powermenu.sh"), desc="Rofi menu"),
    
    # Teclas personalizadas

    # Abrir thunar
    Key([mod], "e", lazy.spawn(explorer), desc="Open en thunar"),
    # Abrir brave
    Key([mod], "w", lazy.spawn(web_browser), desc="Open brave"),
    # Visual Studio Code
    Key([mod], "c", lazy.spawn(editor), desc="Open Code"),

    # Subir y bajar el brillo
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10-"), desc="Lower Brightness by 10"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10"), desc="Raise Brightness by 10"),

    Key([mod], "left", lazy.spawn("brightnessctl set 10-"), desc="Lower Brightness by 10"),
    Key([mod], "right", lazy.spawn("brightnessctl set +10"), desc="Raise Brightness by 10"),

    # Sound
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5")),

    Key([mod], "Down", lazy.spawn("pamixer -d 5")),
    Key([mod], "Up", lazy.spawn("pamixer -i 5")),

    
]
# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

#defino el label que tendran los escritorios

desk = ["󰣇","","","󰨞","","","󰖹","󰌔",""]
# olddesk = ["󰣇","󰈹","","󰨞","","󰝚","","󰡨",""]


"""
listado de nerdfonts
1 󰣇, nf-md-arch 
2 , nf-md-chrome
3 , nf-cod-terminal_bash
4 󰨞, nf-md-microsoft_visual_studio_code
5 , nf-fa-folder_open
6 , nf-dev-android
7 󰖹, nf-md-microsoft_xbox
8 󰌔, nf-md-kodi
9 , nf-seti-config
"""


#inicializo un array donde quedaran almacendos los objetos Group
groups = []

# relleno la informacin de cada grupo  iterando el array principal
for idx, label in enumerate(desk):
    team = Group(str(idx + 1), label=label)
    groups.append(team)

# Define los nombres de las teclas del teclado numérico
keypad_mapping = {
    "1": "KP_End",
    "2": "KP_Down",
    "3": "KP_Next",
    "4": "KP_Left",
    "5": "KP_Begin",
    "6": "KP_Right",
    "7": "KP_Home",
    "8": "KP_Up",
    "9": "KP_Prior",

}
for i in groups:
    alias= f"KP_{i.name}"
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            Key(
                [mod],
                keypad_mapping[i.name],  # Usa el mapeo para teclas del teclado numérico
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name} (keypad)",
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            Key(
                [mod, "shift"],
                keypad_mapping[i.name],  # Usa el mapeo para teclas del teclado numérico
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name} (keypad)",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
borderfocus = "#3C5875"
bordernormal= "#000000"

layouts = [
    layout.Columns(margin=4, border_width=2, border_focus=borderfocus,border_normal=bordernormal),
    layout.Max(margin=0),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    #layout.Bsp(),
    layout.Matrix(margin=4, border_width=2, border_focus=borderfocus,border_normal=bordernormal),
    #layout.MonadTall(),
    #layout.MonadWide(),
    #layout.RatioTile(),
    layout.Tile(margin=4, border_width=2, border_focus=borderfocus,border_normal=bordernormal),
    layout.TreeTab(margin=4, border_width=2, border_focus=borderfocus,border_normal=bordernormal),
    layout.Floating(border_width=2, border_focus=borderfocus,border_normal=bordernormal),
    
    #layout.VerticalTile(),
    #layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# colorv1="#101426"
colorv1="#333446"




fontsize1 = 30 #iconos bara
fontsize2 = 35 #iconos escritorio
fontsize3 = 14 #textos

sep = 14

top_bar =[

    # widget.Chord(background=blue),
    widget.Sep(linewidth=0,padding=10),
    widget.CurrentLayoutIcon(fontsize=3),

    widget.Sep(linewidth=0,padding=sep),
    widget.TextBox(text="", fontsize=fontsize1, foreground="#fff", background=colorv1),
    widget.ThermalSensor(background=colorv1, fontsize=fontsize3),
    widget.Sep(linewidth=0,padding=sep),
    widget.TextBox(text="", fontsize=fontsize1, foreground="#fff", background=colorv1),
    widget.Memory(background=colorv1, format="{MemUsed: .2f}{mm}/{MemTotal: .2f}{mm}", measure_mem="G"),
    # widget.Sep(linewidth=0,padding=sep),
    # widget.TextBox(text="", fontsize=fontsize1, foreground="#fff", background=colorv1),
    # widget.CPU(background=colorv1, format="{freq_current}GHz {load_percent}%",width=80),


# groupbox
    widget.Spacer(length=bar.STRETCH), 
    widget.GroupBox(
        fontsize=fontsize2,
        highlight_method='block',  # Opcional, para resaltar grupos activos
        active="#FFFFFF",            # Color de los grupos activos
        inactive="#9EAFAE",          # Color de los grupos inactivos
        this_current_screen_border=blue,  # Borde del grupo activo
        padding=7,
        ),
    widget.Spacer(length=bar.STRETCH), 




#widgets sistema
    widget.Chord(background=blue),
    widget.Sep(linewidth=0,padding=sep),
    widget.Systray(background=colorv1),
    widget.TextBox(text="", fontsize=fontsize1, foreground="#fff", background=colorv1),
    widget.Clock(format='%d/%m/%y %H:%M',background=colorv1),
    widget.Sep(linewidth=0,padding=sep),



]

# max_width=1366
# max_height=768
top_bar_height=40
# top_bar_width=320


screens = [
    Screen(
        top=bar.Bar(top_bar,top_bar_height,background = colorv1,border_color= colorv1,),

    )
]
#? descomentar este fake screen si quiero probarlas
# fake_screens = [
#     Screen(
#         # Puedes definir el tamaño y la posición de la pantalla falsa aquí
#         top=bar.Bar(top_bar,top_bar_height,background = colorv1,border_color= colorv1,),
#             x=523,  # Posición X (desde la izquierda)
#             y=0,    # Posición Y (desde arriba)
#             width=top_bar_width, # Ancho deseado para la barra (y para esta "pantalla falsa")
#             height=top_bar_height, # Altura deseada para la barra
#     ),
#     Screen(
#         bottom = bar.Bar(bottom_bar,24,background = colorv1,border_color= colorv1,),
#         x=0,
#         y=top_bar_height,
#         width= max_width,
#         height=max_height-top_bar_height
#     )
# ]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    Click([mod], "Button5", lazy.screen.next_group()),
    Click([mod], "Button4", lazy.screen.prev_group()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    script = os.path.expanduser("/home/juanecos/.config/qtile/autostart.sh")
    subprocess.run([script])
