"""Genera index.html (la página publicada) a partir de rombos-de-propp.html, el código fuente del juego.
Agrega doctype, lang="en", viewport y descripción, y envuelve el contenido en <head>/<body>.
Uso (desde la carpeta CubeSwipe): python3 tools/mkindex.py
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, "rombos-de-propp.html"), encoding="utf-8").read()
head, body = s.split("</style>\n", 1)
head = head.replace('<meta charset="utf-8">\n', '', 1)
out = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       '<meta name="description" content="Cube Swipe: a relaxing cube puzzle by BluBer Games. Swipe groups of three tiles to put the cube back together.">\n'
       + head + "</style>\n</head>\n<body>\n" + body.rstrip() + "\n</body>\n</html>\n")
open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(out)
print("index.html", len(out) // 1024, "KB")
