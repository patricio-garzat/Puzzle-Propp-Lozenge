"""Imágenes para la App Store a partir de las capturas del simulador (raw/).
Tamaños: iPhone 6.3" (1206x2622, el que pide App Store Connect primero) y 6.9" (1290x2796)."""
import os
from PIL import Image, ImageDraw, ImageFont
SIZES = {'appstore-6.3': (1206, 2622), 'appstore-6.9': (1290, 2796)}
W, H = 1290, 2796
FONT = '/System/Library/Fonts/SFNSRounded.ttf'
SHOTS = {
    'en': [
        ('01-home-dark', 'A calm puzzle\nfor your mind'),
        ('02-play-dark', 'Swipe to turn\nthree tiles at once'),
        ('03-hint-dark', 'Stuck? A hint\nshows the way'),
        ('05-levels-light', '50 levels, from easy\nto brain-bending'),
        ('04-play-light', 'Light or dark,\nalways relaxing'),
    ],
    'es': [
        ('01-home-dark', 'Un puzzle tranquilo\npara tu mente'),
        ('02-play-dark', 'Desliza y gira\ntres rombos a la vez'),
        ('03-hint-dark', '¿Atorado? Una pista\nte muestra el camino'),
        ('05-levels-light', '50 niveles, de fácil\na rompecabezas'),
        ('04-play-light', 'Claro u oscuro,\nsiempre relajante'),
    ],
}

def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    try: f.set_variation_by_axes([400, weight])  # ejes: GRAD (grosor sin ensanchar) y Weight
    except Exception: pass
    return f

def background():
    top, bot = (0x2C, 0x39, 0x54), (0x12, 0x19, 0x27)
    bg = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(round(a * (1 - t) + b * t) for a, b in zip(top, bot)))
    return bg

def make(raw, caption, out):
    k = W / 1290
    img = background()
    d = ImageDraw.Draw(img)
    f = font(round(104 * k), 800)
    lines = caption.split('\n')
    y = round(190 * k)
    track = 0.005 * f.size  # apenas un poco de aire entre letras
    for ln in lines:
        w = sum(d.textlength(ch, font=f) for ch in ln) + track * (len(ln) - 1)
        x = (W - w) / 2
        for ch in ln:
            d.text((x, y), ch, font=f, fill=(0xEE, 0xF1, 0xF6))
            x += d.textlength(ch, font=f) + track
        y += round(128 * k)
    # franja de tres colores bajo el título
    bw, by = 240 * k, y + 34 * k
    for i, c in enumerate([(0xFF, 0xC9, 0x4F), (0xFF, 0x7B, 0x63), (0x6F, 0x8E, 0xF7)]):
        d.rounded_rectangle([W / 2 - bw / 2 + i * bw / 3, by, W / 2 - bw / 2 + (i + 1) * bw / 3, by + 12 * k], radius=6 * k, fill=c)
    # captura con esquinas redondeadas y sombra
    shot = Image.open(raw).convert('RGB')
    # la captura entera, sin cortarse abajo
    top = round(by + 110 * k)
    sh = H - top - round(90 * k)
    sw = round(shot.width * sh / shot.height)
    shot = shot.resize((sw, sh), Image.LANCZOS)
    mask = Image.new('L', (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw - 1, sh - 1], radius=round(86 * k), fill=255)
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([(W - sw) / 2 - 10 * k, top - 10 * k, (W + sw) / 2 + 10 * k, top + sh + 10 * k], radius=96 * k, fill=(255, 255, 255, 40))
    img.paste(shadow, (0, 0), shadow)
    img.paste(shot, ((W - sw) // 2, top), mask)
    img.save(out)

here = os.path.dirname(os.path.abspath(__file__))
for folder, (W, H) in SIZES.items():
    for lang, items in SHOTS.items():
        os.makedirs(os.path.join(here, folder, lang), exist_ok=True)
        for i, (name, cap) in enumerate(items, 1):
            make(os.path.join(here, 'raw', name + '.png'), cap, os.path.join(here, folder, lang, f'{i}-{name}.png'))
print('ok')
