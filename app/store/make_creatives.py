"""Imágenes "Header" y "Search Results" de la App Store para Cube Swipe.

Tamaños dedicados (no el universal, que Apple recorta muchísimo):
- Header:         3840 x 1646 (21:9). Zona segura 1646 x 661 en (1097, 493), centrada.
                  Las esquinas de arriba quedan libres (ahí van los botones de regresar y compartir).
- Search Results: 3840 x 2560 (3:2). Zona segura 2168 x 1030 en (836, 765), centrada.
Lo importante (tablero, nombre y frase) va dentro de la zona segura; el fondo y los rombos
decorativos llegan hasta las orillas. PNG sin transparencia.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "node_modules", "@fontsource", "nunito", "files")
INK = (0xEE, 0xF1, 0xF6)
SOFT = (0xA9, 0xB6, 0xCC)
TOP, LEFT, RIGHT = (0xFF, 0xC9, 0x4F), (0xFF, 0x7B, 0x63), (0x6F, 0x8E, 0xF7)
GRAD = {  # degradados de los rombos, como en el juego (modo oscuro)
    "t": ((0xFF, 0xDB, 0x7E), (0xF5, 0xB1, 0x2C)),
    "l": ((0xFF, 0x98, 0x84), (0xEC, 0x5F, 0x48)),
    "r": ((0x8F, 0xA9, 0xFF), (0x53, 0x71, 0xE6)),
}
TEXT = {
    "en": {"header": "Swipe. Turn. Relax.", "search": "Swipe to rebuild the cube"},
    "es": {"header": "Desliza. Gira. Relájate.", "search": "Desliza y arma el cubo"},
}


def font(weight, size):
    return ImageFont.truetype(os.path.join(FONTS, f"nunito-latin-{weight}-normal.woff"), size)


def background(W, H, glow_xy):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.clip((xx / W * 0.35 + yy / H) / 1.35, 0, 1)[..., None]
    rgb = np.array([0x2C, 0x39, 0x54]) * (1 - t) + np.array([0x12, 0x19, 0x27]) * t
    gx, gy = glow_xy
    d = np.sqrt((xx - gx) ** 2 + (yy - gy) ** 2) / (H * 0.75)
    a = np.clip(1 - d, 0, 1)[..., None] ** 1.6 * 0.42
    rgb = rgb * (1 - a) + np.array([0x6F, 0x8E, 0xF7]) * a
    return Image.fromarray(rgb.astype("uint8"), "RGB").convert("RGBA")


def board(src, height):
    """Tablero 3x3x3 del juego en alta resolución (renderizado del SVG real del juego con Chrome,
    sin puntos de giro ni pistas, fondo transparente) escalado a la altura pedida."""
    im = Image.open(os.path.join(HERE, "raw", src)).convert("RGBA")
    k = height / im.height
    return im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)


def rhombus(kind, size, angle):
    """Un rombo del juego (degradado y esquinas redondeadas), para decorar."""
    ss = 3
    n = size * ss
    g1, g2 = GRAD[kind]
    yy, xx = np.mgrid[0:n, 0:n] / max(1, n - 1)
    t = np.clip(0.2 * xx + 0.8 * yy, 0, 1)[..., None]
    rgb = np.array(g1) * (1 - t) + np.array(g2) * t
    tile = Image.fromarray(rgb.astype("uint8"), "RGB").convert("RGBA")
    m = Image.new("L", (n, n), 0)
    c = n / 2
    rx, ry = n * 0.47, n * 0.27  # rombo "acostado" como la cara de arriba del cubo
    ImageDraw.Draw(m).polygon([(c, c - ry), (c + rx, c), (c, c + ry), (c - rx, c)], fill=255)
    m = m.filter(ImageFilter.GaussianBlur(n * 0.02)).point(lambda v: 255 if v > 140 else int(v * 1.8))
    tile.putalpha(m)
    tile = tile.resize((size, size), Image.LANCZOS)
    return tile.rotate(angle, resample=Image.BICUBIC, expand=True)


def scatter(img, safe, count, seed, size_range):
    """Rombos flotando alrededor, fuera de la zona segura (algunos desenfocados para dar profundidad)."""
    W, H = img.size
    rnd = random.Random(seed)
    sx0, sy0, sx1, sy1 = safe
    placed = 0
    tries = 0
    while placed < count and tries < 4000:
        tries += 1
        s = rnd.randint(*size_range)
        x, y = rnd.randint(-s // 3, W - s // 2), rnd.randint(-s // 3, H - s // 2)
        # fuera de la zona segura (con margen) y fuera de las esquinas de arriba muy pegadas
        if x + s > sx0 - 80 and x < sx1 + 80 and y + s > sy0 - 80 and y < sy1 + 80:
            continue
        kind = rnd.choice("tlr")
        r = rhombus(kind, s, rnd.choice([0, 60, 120]) + rnd.uniform(-8, 8))
        depth = rnd.random()
        if depth < 0.45:
            r = r.filter(ImageFilter.GaussianBlur(s * 0.05))
            a = r.getchannel("A").point(lambda v: int(v * 0.45))
            r.putalpha(a)
        else:
            a = r.getchannel("A").point(lambda v: int(v * 0.85))
            r.putalpha(a)
        img.alpha_composite(r, (x, y))
        placed += 1


def shadow_under(img, piece, xy, spread):
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    a = piece.getchannel("A").point(lambda v: int(v * 0.55))
    blk = Image.new("RGBA", piece.size, (4, 7, 14, 255))
    blk.putalpha(a)
    sh.alpha_composite(blk, (xy[0], xy[1] + spread // 2))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(spread)))


def wordmark(img, x, y, size, tagline, tag_size):
    """'Cube Swipe' como en el inicio del juego, con la franja de tres colores bajo 'Swipe'."""
    d = ImageDraw.Draw(img)
    f = font(900, size)
    cube = "Cube "
    d.text((x, y), "Cube Swipe", font=f, fill=INK)
    w_cube = d.textlength(cube, font=f)
    w_swipe = d.textlength("Swipe", font=f)
    by = y + size * 1.36  # debajo de la colita de la "p"
    bh = max(6, round(size * 0.075))
    for i, c in enumerate((TOP, LEFT, RIGHT)):
        x0 = x + w_cube + w_swipe * i / 3
        d.rounded_rectangle([x0, by, x0 + w_swipe / 3, by + bh], radius=bh // 2, fill=c)
    ft = font(700, tag_size)
    d.text((x + size * 0.04, by + bh + tag_size * 0.9), tagline, font=ft, fill=SOFT)
    total_w = max(d.textlength("Cube Swipe", font=f), d.textlength(tagline, font=ft))
    return total_w


def block_height(size, tag_size):
    return size * 1.36 + max(6, round(size * 0.075)) + tag_size * 0.9 + tag_size * 1.25


def compose(W, H, safe, board_src, board_h, title_size, tag_size, tagline, seed, rh_range, out):
    sx0, sy0, sx1, sy1 = safe
    cy = (sy0 + sy1) / 2
    b = board(board_src, board_h)
    gap = round(title_size * 0.55)
    # medir el texto para centrar el conjunto (tablero + texto) dentro de la zona segura
    probe = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(probe)
    text_w = max(d.textlength("Cube Swipe", font=font(900, title_size)), d.textlength(tagline, font=font(700, tag_size)))
    total = b.width + gap + text_w
    x0 = round((sx0 + sx1) / 2 - total / 2)
    img = background(W, H, (x0 + b.width / 2, cy))
    scatter(img, safe, count=16, seed=seed, size_range=rh_range)
    bx, by = x0, round(cy - b.height / 2)
    shadow_under(img, b, (bx, by), spread=round(board_h * 0.05))
    img.alpha_composite(b, (bx, by))
    th = block_height(title_size, tag_size)
    wordmark(img, x0 + b.width + gap, round(cy - th / 2 - title_size * 0.08), title_size, tagline, tag_size)
    assert x0 >= sx0 and x0 + total <= sx1 + 2, (out, x0, total, sx0, sx1)
    img.convert("RGB").save(out)
    print(out, img.size)


os.makedirs(os.path.join(HERE, "creatives"), exist_ok=True)
for lang, t in TEXT.items():
    # Header 3840 x 1646 · zona segura 1646 x 661 en (1097, 493)
    compose(3840, 1646, (1097, 493, 1097 + 1646, 493 + 661), "board-hd-2.png", 660, 150, 62, t["header"],
            seed=7, rh_range=(150, 300), out=os.path.join(HERE, "creatives", f"header-3840x1646-{lang}.png"))
    # Search Results 3840 x 2560 · zona segura 2168 x 1030 en (836, 765)
    compose(3840, 2560, (836, 765, 836 + 2168, 765 + 1030), "board-hd-1.png", 1030, 196, 84, t["search"],
            seed=11, rh_range=(200, 380), out=os.path.join(HERE, "creatives", f"search-3840x2560-{lang}.png"))
