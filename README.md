# Rombos de Propp

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="brand/logo-dark.png">
  <img alt="Rombos de Propp" src="brand/logo-light.png" width="560">
</picture>

Versión web del puzzle magnético **Propp Lozenge**: 27 rombos de tres colores dentro de un hexágono que forman la ilusión de un cubo. Levanta grupos de tres rombos, gíralos y vuelve a dejar el cubo armado.

**Jugar:** https://patricio-garzat.github.io/Puzzle-Propp-Lozenge/

## Qué incluye

- Tableros de 2×2×2, 3×3×3 (el original) y 4×4×4.
- **Mezclar al azar:** revuelve colores y orientaciones por todo el tablero, con la dificultad que elijas.
- **Arma tu mezcla:** el cubo empieza en blanco; pintas cada color con su cupo exacto (9 en 3×3×3), acomodas con giros y juegas desde ahí.
- Tres niveles de dificultad: Fácil (6–9 movimientos), Intermedio (15–20) y Difícil (30–35); en 4×4×4, Fácil 9–15, Intermedio 21–35 y Difícil 40–60. Se ajustan a lo que permite cada tamaño.
- Cada mezcla indica en cuántos movimientos se resuelve (el mínimo exacto cuando se puede calcular).
- Pistas que siguen el camino más corto, deshacer, récords por tamaño y atajos de teclado.
- Sonidos generados con Web Audio y animaciones; tema claro y oscuro.

## Logo e íconos

- `brand/logo-light.png` y `brand/logo-dark.png`: logo horizontal para fondos claros y oscuros.
- `brand/logo-mark.svg` y `brand/logo-mark.png`: solo el cubo, sin fondo.
- `icons/`: ícono de la app (SVG y PNG de 192 y 512, versión *maskable*) y favicon.
- `manifest.webmanifest` y `apple-touch-icon.png`: para instalarla en la pantalla de inicio del celular.

## Cómo funciona

Todo es un solo archivo, `index.html`, sin dependencias ni compilación. Para jugar sin internet, descárgalo y ábrelo en el navegador.

- Las posiciones se modelan como teselados por rombos de un hexágono en una red triangular.
- El mínimo se calcula con una búsqueda bidireccional exacta (hasta 14 movimientos en 2×2×2 y 8 en los demás). Más allá de eso, cada mezcla trae una meta segura: se sabe que se resuelve en ese número.

## Créditos

Puzzle original inventado por James Propp y diseñado por Oskar van Deventer. Esta es una versión web no oficial; el puzzle físico se vende en [Puzzle Guy Store](https://puzzleguy.store/products/propp-lozenge).
