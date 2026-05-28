#!/usr/bin/env python3
import sys
import os
from colorthief import ColorThief
from PIL import Image
import colorsys

from conflict_helper import is_conflicting, resolve_contrast

CONFIG_DIR = os.path.expanduser("~/.config/qtile")
OUTPUT_FILE = os.path.join(CONFIG_DIR, "generated_colors.py")


def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


def luminance(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def get_image_luminance(path):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    # muestreamos una versión reducida para eficiencia
    img = img.resize((64, 64))
    pixels = list(img.getdata())
    return sum(luminance(p) for p in pixels) / len(pixels)


def classify_mode(avg_lum):
    # lum en [0,1]
    if avg_lum < 0.35:
        return "dark", 1.0
    elif avg_lum < 0.65:
        return "hybrid", 0.8
    else:
        return "pseudo_light", 0.7


def build_palette_from_wallpaper(wall_path):
    thief = ColorThief(wall_path)
    raw_palette = thief.get_palette(color_count=8)

    # ordenamos la paleta por luminancia
    sorted_by_lum = sorted(raw_palette, key=luminance)

    darkest = sorted_by_lum[0]
    lightest = sorted_by_lum[-1]

    # separamos colores cálidos y fríos
    warm = []
    cold = []
    for c in raw_palette:
        r, g, b = c
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        h_deg = h * 360
        if s < 0.15:
            # casi gris, lo ignoramos para warm/cold
            continue
        if 30 <= h_deg <= 210:
            # range más frío: verdes-azules
            cold.append((c, s, v, h_deg))
        else:
            warm.append((c, s, v, h_deg))

    # si no hay suficiente datos, usamos todo como cold
    if not warm and not cold:
        cold = [(c, 0.5, 0.5, 0) for c in raw_palette]

    # helper para tomar el más saturado/brillante
    def pick_most_saturated(lst):
        if not lst:
            return None
        return max(lst, key=lambda x: (x[1], x[2]))[0]

    def pick_darker(lst):
        if not lst:
            return None
        return min(lst, key=lambda x: luminance(x[0]))[0]

    # colores base
    background = darkest
    foreground = lightest

    # acentos fríos
    primary_rgb = pick_most_saturated(cold) or lightest
    secondary_rgb = None
    if cold and len(cold) > 1:
        # tomamos otro distinto al primary
        candidates = [c[0] for c in cold if c[0] != primary_rgb]
        secondary_rgb = candidates[0] if candidates else primary_rgb
    else:
        secondary_rgb = primary_rgb

    # acentos cálidos
    warm_primary = pick_most_saturated(warm) if warm else None
    warm_darker = pick_darker(warm) if warm else None

    # si no hay cálidos, generamos complementarios sintéticos
    if not warm:
        # generamos un peach y un yellow sintéticos
        warm_primary = (255, 136, 105)   # peach
        warm_darker = (223, 161, 87)     # yellow-ish

    # demás acentos
    green_rgb = (106, 214, 154)     # valor por defecto razonable
    blue_rgb = primary_rgb
    darkblue_rgb = pick_darker(cold) or (27, 42, 72)
    yellow_rgb = warm_darker
    peach_rgb = warm_primary
    mauve_rgb = secondary_rgb
    red_rgb = (255, 83, 112)        # por defecto, luego podrías mejorar

    palette = {
        "background": rgb_to_hex(background),
        "foreground": rgb_to_hex(foreground),
        "primary":    rgb_to_hex(primary_rgb),
        "secondary":  rgb_to_hex(secondary_rgb),
        "yellow":     rgb_to_hex(yellow_rgb),
        "green":      rgb_to_hex(green_rgb),
        "peach":      rgb_to_hex(peach_rgb),
        "mauve":      rgb_to_hex(mauve_rgb),
        "blue":       rgb_to_hex(blue_rgb),
        "darkblue":   rgb_to_hex(darkblue_rgb),
        "red":        rgb_to_hex(red_rgb),
    }

    return palette


def main():
    if len(sys.argv) < 2:
        print("Uso: extract_colors.py /ruta/al/wallpaper")
        sys.exit(1)

    wall_path = sys.argv[1]
    if not os.path.isfile(wall_path):
        print(f"Wallpaper no encontrado: {wall_path}")
        sys.exit(1)

    # 1) luminancia promedio → modo + opacidad
    avg_lum = get_image_luminance(wall_path)
    mode, opacity = classify_mode(avg_lum)

    # 2) paleta base desde el wallpaper
    palette = build_palette_from_wallpaper(wall_path)

    # 3) si el modo es pseudo_light, ajustamos un poco background/foreground
    bg = palette["background"]
    ROLE_MAP = {
			"yellow": "launcher",
			"peach": "power",
			"mauve": "mauve",
			"blue": "blue",
			"foreground": "foreground",
		}
    for key, role in ROLE_MAP.items():
        if key not in palette:
            continue
        if is_conflicting(bg, palette[key]):
            palette[key] = resolve_contrast(bg, palette[key], role)
            
    fg = palette["foreground"]

    if mode == "pseudo_light":
        # fondo más claro y texto oscuro
        bg = "#EDEFF2"
        fg = "#1D1F23"
    elif mode == "hybrid":
        # fondo oscuro pero mantenemos texto claro
        # dejamos los que vinieron de la paleta
        pass
    else:  # dark
        # si el fondo no es muy oscuro, lo forzamos
        # (esto puede afinarse más adelante)
        pass

    palette["background"] = bg
    palette["foreground"] = fg

    # 4) escribir archivo generated_colors.py
    with open(OUTPUT_FILE, "w") as f:
        f.write("# Archivo generado automáticamente a partir del wallpaper\n")
        f.write("colors = {\n")
        for k, v in palette.items():
            f.write(f'    "{k}": "{v}",\n')
        f.write("}\n\n")
        f.write(f"BAR_OPACITY = {opacity}\n")

    print("Paleta generada en:", OUTPUT_FILE)
    print("Modo:", mode, "   Opacidad:", opacity)


if __name__ == "__main__":
    main()
