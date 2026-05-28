import colorsys

def hex_to_rgb01(hexcolor):
    hexcolor = hexcolor.lstrip("#")
    r, g, b = (int(hexcolor[i:i+2], 16) for i in (0, 2, 4))
    return r/255, g/255, b/255


def rgb01_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(
        int(rgb[0]*255),
        int(rgb[1]*255),
        int(rgb[2]*255),
    )


def hex_to_hsl(hexcolor):
    r, g, b = hex_to_rgb01(hexcolor)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l


def hsl_to_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return rgb01_to_hex((r, g, b))
