from hsl_helper import hex_to_hsl, hsl_to_hex

def is_conflicting(bg_hex, fg_hex,
                   min_hue_diff=0.08,
                   min_lum_diff=0.18):
    bg_h, bg_s, bg_l = hex_to_hsl(bg_hex)
    fg_h, fg_s, fg_l = hex_to_hsl(fg_hex)

    hue_diff = abs(bg_h - fg_h)
    hue_diff = min(hue_diff, 1 - hue_diff)

    lum_diff = abs(bg_l - fg_l)

    return hue_diff < min_hue_diff and lum_diff < min_lum_diff

def resolve_contrast(bg_hex, fg_hex, role):
    bg_h, bg_s, bg_l = hex_to_hsl(bg_hex)
    h, s, l = hex_to_hsl(fg_hex)

    # estrategia según rol
    if role in ("yellow", "peach", "launcher", "power"):
        # mover el tono lejos del background
        h = (bg_h + 0.25) % 1.0
        l = max(l, 0.55)
        s = max(s, 0.6)

    elif role in ("mauve", "blue"):
        # variar luminosidad más que tono
        l = 0.7 if bg_l < 0.5 else 0.3
        s = max(s, 0.55)

    elif role == "foreground":
        l = 0.9 if bg_l < 0.5 else 0.15
        s = min(s, 0.3)

    return hsl_to_hex(h, s, l)
