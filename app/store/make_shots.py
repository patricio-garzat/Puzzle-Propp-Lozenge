"""Imágenes para la App Store (iPhone 6.9": 1290x2796) a partir de las capturas del simulador (raw/)."""
import os
from PIL import Image, ImageDraw, ImageFont
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
    try: f.set_variation_by_axes([weight])
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
    img = background()
    d = ImageDraw.Draw(img)
    f = font(104, 800)
    lines = caption.split('\n')
    y = 190
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2, y), ln, font=f, fill=(0xEE, 0xF1, 0xF6))
        y += 128
    # franja de tres colores bajo el título
    bw, by = 240, y + 34
    for i, c in enumerate([(0xFF, 0xC9, 0x4F), (0xFF, 0x7B, 0x63), (0x6F, 0x8E, 0xF7)]):
        d.rounded_rectangle([W / 2 - bw / 2 + i * bw / 3, by, W / 2 - bw / 2 + (i + 1) * bw / 3, by + 12], radius=6, fill=c)
    # captura con esquinas redondeadas y sombra
    shot = Image.open(raw).convert('RGB')
    sw = 1010
    sh = round(shot.height * sw / shot.width)
    shot = shot.resize((sw, sh), Image.LANCZOS)
    top = H - sh - 150 if H - sh - 150 > by + 120 else by + 120
    mask = Image.new('L', (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw - 1, sh - 1], radius=86, fill=255)
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([(W - sw) / 2 - 10, top - 10, (W + sw) / 2 + 10, top + sh + 10], radius=96, fill=(255, 255, 255, 40))
    img.paste(shadow, (0, 0), shadow)
    img.paste(shot, ((W - sw) // 2, top), mask)
    img.save(out)

here = os.path.dirname(os.path.abspath(__file__))
for lang, items in SHOTS.items():
    os.makedirs(os.path.join(here, 'appstore-6.9', lang), exist_ok=True)
    for i, (name, cap) in enumerate(items, 1):
        make(os.path.join(here, 'raw', name + '.png'), cap, os.path.join(here, 'appstore-6.9', lang, f'{i}-{name}.png'))
print('ok')
