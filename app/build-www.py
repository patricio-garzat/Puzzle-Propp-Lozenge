"""Arma la carpeta www/ de la app de iOS a partir del juego web (../index.html).

Diferencias con la versión web:
- La fuente Nunito va incluida en la app (sin internet no carga Google Fonts).
- Se quitan el manifest y los íconos web: en la app no sirven.

Uso: python3 build-www.py   (o npm run build, que además copia www/ al proyecto de Xcode)
"""
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "index.html")
WWW = os.path.join(HERE, "www")
FONTS = os.path.join(HERE, "node_modules", "@fontsource", "nunito", "files")
WEIGHTS = (500, 600, 700, 800, 900)

html = open(SRC, encoding="utf-8").read()

# Fuente local en lugar de Google Fonts
font_css = "\n".join(
    f'@font-face {{ font-family: "Nunito"; font-style: normal; font-weight: {w}; font-display: block; '
    f'src: url("fonts/nunito-latin-{w}-normal.woff2") format("woff2"); }}'
    for w in WEIGHTS
)
html, n = re.subn(
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n'
    r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]*">\n',
    "<style>\n" + font_css + "\n</style>\n",
    html,
)
assert n == 1, "no encontré el link de Google Fonts en index.html"

# Cosas solo de la web
for tag in (
    '<link rel="icon" href="favicon.ico" sizes="32x32">\n',
    '<link rel="icon" href="icons/favicon.svg" type="image/svg+xml">\n',
    '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n',
    '<link rel="manifest" href="manifest.webmanifest">\n',
):
    assert tag in html, tag
    html = html.replace(tag, "")

shutil.rmtree(WWW, ignore_errors=True)
os.makedirs(os.path.join(WWW, "fonts"))
for w in WEIGHTS:
    shutil.copy(os.path.join(FONTS, f"nunito-latin-{w}-normal.woff2"), os.path.join(WWW, "fonts"))
open(os.path.join(WWW, "index.html"), "w", encoding="utf-8").write(html)
print("www/ listo:", len(html) // 1024, "KB")
