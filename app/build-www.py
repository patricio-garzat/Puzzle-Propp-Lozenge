"""Arma la carpeta www/ de la app de iOS a partir del juego web (../index.html).

Diferencias con la versión web:
- La fuente Plus Jakarta Sans va incluida en la app (sin internet no carga Google Fonts).
- Se quitan el manifest y los íconos web: en la app no sirven.

Uso: python3 build-www.py   (o npm run build, que además copia www/ al proyecto de Xcode)
"""
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "index.html")
WWW = os.path.join(HERE, "www")
FONTS = os.path.join(HERE, "node_modules", "@fontsource", "plus-jakarta-sans", "files")
WEIGHTS = (500, 600, 700, 800)

html = open(SRC, encoding="utf-8").read()

# Fuente local en lugar de Google Fonts
font_css = "\n".join(
    f'@font-face {{ font-family: "Plus Jakarta Sans"; font-style: normal; font-weight: {w}; font-display: block; '
    f'src: url("fonts/plus-jakarta-sans-latin-{w}-normal.woff2") format("woff2"); }}'
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

# Sin zoom en la app: ni pellizco ni doble toque
vp_old = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
assert vp_old in html, "no encontré el viewport"
html = html.replace(vp_old, '<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">')
no_zoom = """<style>html, body { touch-action: manipulation; -webkit-text-size-adjust: 100%; }</style>
<script>
  // Bloquea el pellizco (gestos de Safari/WebKit) y el doble toque para hacer zoom
  ["gesturestart", "gesturechange", "gestureend"].forEach((ev) => document.addEventListener(ev, (e) => e.preventDefault(), { passive: false }));
  document.addEventListener("touchmove", (e) => { if (e.touches.length > 1) e.preventDefault(); }, { passive: false });
  let lastTouchEnd = 0;
  document.addEventListener("touchend", (e) => { const now = Date.now(); if (now - lastTouchEnd < 300 && !e.target.closest("#board, .ill-swipe")) e.preventDefault(); lastTouchEnd = now; }, { passive: false });
</script>
"""
html = html.replace("</head>", no_zoom + "</head>", 1)

# Versión de la app (Ajustes → Acerca de): la misma del proyecto de Xcode que sube release.sh
pbx = open(os.path.join(HERE, "ios", "App", "App.xcodeproj", "project.pbxproj"), encoding="utf-8").read()
version = re.search(r"MARKETING_VERSION = ([0-9.]+);", pbx).group(1)
build = re.search(r"CURRENT_PROJECT_VERSION = (\d+);", pbx).group(1)
html, n = re.subn(r'(id="app-version">)Web(<)', rf"\g<1>{version} ({build})\2", html)
assert n == 1, "no encontré la versión en Ajustes"

shutil.rmtree(WWW, ignore_errors=True)
os.makedirs(os.path.join(WWW, "fonts"))
for w in WEIGHTS:
    shutil.copy(os.path.join(FONTS, f"plus-jakarta-sans-latin-{w}-normal.woff2"), os.path.join(WWW, "fonts"))
open(os.path.join(WWW, "index.html"), "w", encoding="utf-8").write(html)
print("www/ listo:", len(html) // 1024, "KB · versión", version, f"({build})")
