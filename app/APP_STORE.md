# Cube Swipe: cómo publicarlo en la App Store

Esta guía va paso a paso, desde que el build está listo hasta mandarlo a revisión. Los textos para la ficha de la App Store (en inglés y en español) están al final y se pueden copiar y pegar tal cual.

## Datos de la app

| Dato | Valor |
|---|---|
| Nombre en la App Store | **Cube Swipe: Calm Puzzle** (debajo del ícono en el iPhone dice "Cube Swipe") |
| Bundle ID | `com.blubergames.cubeswipe` |
| Equipo | Patricio Garza T (Team ID `CGW77RJS5Q`) |
| Versión / build | 1.0 (1) |
| Dispositivos | Solo iPhone, en vertical |
| iOS mínimo | 15.0 (desde la versión 1.0.1; el build 1.0 (1) se subió con 14.0) |
| Encriptación | No usa (ya está declarado en el `Info.plist`, así que Apple no pregunta) |
| Archive | En Xcode → Window → Organizer → Archives → **Cube Swipe 1.0 (1)** |

---

## Paso 0. Registrar el Bundle ID (una sola vez)

App Store Connect solo muestra los Bundle ID que ya están registrados en tu cuenta.

1. Entra a <https://developer.apple.com/account/resources/identifiers/list> con la cuenta del equipo **Patricio Garza T**.
2. Haz clic en **+** → **App IDs** → **App** → **Continue**.
3. Llena el formulario:
   - **Description:** `Cube Swipe`
   - **Bundle ID:** elige **Explicit** y escribe `com.blubergames.cubeswipe`
   - No marques ninguna capacidad.
4. Haz clic en **Continue** y luego en **Register**.

## Paso 1. Crear la app en App Store Connect

1. Entra a <https://appstoreconnect.apple.com> → **Apps** → botón **+** → **New App**.
2. Llena los datos:
   - **Platforms:** iOS
   - **Name:** `Cube Swipe`. El nombre debe ser único en toda la App Store; si ya está ocupado, usa `Cube Swipe: Calm Puzzle`.
   - **Primary Language:** English (U.S.)
   - **Bundle ID:** `com.blubergames.cubeswipe` (el que registraste en el paso 0)
   - **SKU:** `cubeswipe-ios-001`. Es solo un código interno tuyo.
   - **User Access:** Full Access
3. Haz clic en **Create**.

## Paso 2. Subir el build desde Xcode

1. Abre Xcode → **Window → Organizer** → pestaña **Archives**.
2. Selecciona **Cube Swipe 1.0 (1)** y haz clic en **Distribute App**.
3. Elige **App Store Connect** → **Distribute**.
   - En versiones anteriores de Xcode los pasos son **Upload** → **Next**, con la firma **Automatically manage signing**.
4. Xcode crea solo el certificado de distribución y el perfil, y sube la app.
5. Espera el correo de Apple que dice que el build terminó de procesarse. Normalmente tarda entre 5 y 30 minutos.

> **Recomendado antes de mandarla a revisión: pruébala en tu iPhone con TestFlight.**
> 1. En App Store Connect → tu app → **TestFlight** → **Internal Testing**, haz clic en **+**, crea un grupo y agrégate.
> 2. Instala la app **TestFlight** en tu iPhone y abre Cube Swipe desde ahí.
> 3. Revisa sobre todo cuatro cosas: el sonido, la vibración, el modo oscuro y el modo claro, y la intro.

## Paso 3. App Information (menú izquierdo)

| Campo | Qué poner |
|---|---|
| **Subtitle** | `A relaxing cube puzzle` |
| **Category** | Primary: **Games → Puzzle** · Secondary: **Games → Casual** |
| **Content Rights** | "No, it does not contain, show, or access third-party content" |
| **Age Rating** | Contesta **None / No** a todo, y la app queda como **4+**. No tiene compras, anuncios, chat ni navegador web abierto. |
| **Privacy Policy URL** | `https://blubergames.com/privacy/` |

## Paso 4. Pricing and Availability

- **Price:** Free (USD 0), o el precio que decidas.
- **Availability:** todos los países.

## Paso 5. App Privacy

1. Haz clic en **Get Started**.
2. Contesta **"No, we do not collect data from this app"**.
3. Haz clic en **Save** y luego en **Publish**.

La respuesta es correcta porque el juego no tiene cuentas, analítica ni anuncios. El avance se guarda solo en el iPhone.

## Paso 6. La versión 1.0 (iOS App → 1.0 Prepare for Submission)

1. **Previews and Screenshots**
   - En la pestaña **iPhone with Dynamic Island (medium display)** (6.1"/6.3", 1206 × 2622), arrastra las 5 imágenes de `app/store/appstore-6.3/en/` en orden (1 a 5).
   - Si también aparece una pestaña de **6.9"**, usa las de `app/store/appstore-6.9/en/`.
   - Las pestañas de iPad y Apple Watch no aplican: la app es solo para iPhone.
2. **Promotional Text, Description y Keywords:** cópialos del final de esta guía.
3. **URLs:**
   - **Support URL:** `https://blubergames.com/support/`
   - **Marketing URL:** `https://blubergames.com`
4. **Version:** `1.0`
5. **Copyright:** `2026 BluBer Games`. Si la cuenta es personal, puedes usar tu nombre legal.
6. **Build:** haz clic en **+** y elige el build **1.0 (1)**. Aparece cuando termina de procesarse.
7. **App Review Information:**
   - Sign-in required: **No**
   - **Contact:** tu nombre, teléfono y correo. Solo los ve Apple.
   - **Notes:** `No account or sign-in needed. The game works fully offline. Tap "Levels" to start; the light bulb shows a hint.`
8. **Version Release:** elige **Manually release this version** si quieres decidir tú el día del lanzamiento, o **Automatically** para que salga en cuanto la aprueben.

## Paso 7. Ficha en español (opcional, recomendado)

1. Arriba a la derecha, en el selector de idioma (dice **English (U.S.)**), elige **Add Language → Spanish (Mexico)**. Si quieres, también **Spanish (Spain)**.
2. Llena el nombre, el subtítulo, el texto promocional, la descripción y las palabras clave en español (están abajo).
3. En las capturas, sube las de `app/store/appstore-6.3/es/` (y `appstore-6.9/es/` si te pide 6.9").

## Paso 8. Mandar a revisión

1. Haz clic en **Add for Review** → **Submit to App Review**.
2. La revisión suele tardar entre 24 y 48 horas. Te llega un correo cuando la aprueban o si piden algún cambio.

---

## Antes de mandar a revisión: activa el formulario de soporte (Netlify)

La página `https://blubergames.com/support/` tiene un formulario de contacto. Para que funcione:

1. En Netlify, abre el sitio **blubergames** → **Site configuration → Forms** → **Enable form detection**.
2. Ve a **Deploys** → **Trigger deploy** → **Deploy site**, para que Netlify detecte el formulario.
3. En **Forms → Form notifications** → **Add notification → Email notification**, pon tu correo.
   - Así te llegan los mensajes, y tu correo nunca aparece en la página.

---

## Textos para la ficha

### English (U.S.)

**Name:** Cube Swipe: Calm Puzzle

**Subtitle:** A relaxing cube puzzle

**Promotional Text:**
50 handcrafted levels, from a gentle 2×2×2 to a brain-bending 4×4×4. Swipe, turn and rebuild the cube. No ads, no pressure, just calm.

**Description:**
```
Cube Swipe is a calm, beautiful puzzle about putting a cube back together.

The board looks like a 3D cube, but it's all flat: tiles in three colors that you turn in groups of three. Swipe in a circle over a group to turn it, and rebuild the cube with yellow on top, red on the left and blue on the right. It's easy to learn and hard to put down.

• 50 levels that grow with you, from 2×2×2 to 4×4×4 (and a little secret at the end)
• Earn up to 3 stars per level by solving in fewer moves
• Stuck? A hint shows exactly where to swipe, and unused hints are saved for later
• Free play: pick a size and difficulty for endless shuffles
• Build your own: paint the tiles and create your own challenge
• Soft, relaxing sounds and gentle haptics
• Light and dark themes
• Works fully offline. No ads, no accounts, no tracking
• English and Spanish

Inspired by the Propp Lozenge, the magnetic puzzle invented by James Propp and designed by Oskar van Deventer.

Made with care by BluBer Games.
```

**Keywords:**
```
puzzle,cube,relax,brain,logic,tiles,swipe,calm,zen,mind,offline,levels,isometric,rhombus,teaser
```

### Spanish (Mexico)

**Nombre:** Cube Swipe: Calm Puzzle

**Subtítulo:** Un puzzle de cubo relajante

**Texto promocional:**
50 niveles, de un tranquilo 2×2×2 a un desafiante 4×4×4. Desliza, gira y vuelve a armar el cubo: sin anuncios ni presiones, solo calma.

**Descripción:**
```
Cube Swipe es un rompecabezas tranquilo y bonito: tu meta es volver a armar un cubo.

El tablero parece un cubo en 3D, pero todo es plano: rombos de tres colores que giras en grupos de tres. Desliza el dedo en círculo sobre un grupo para girarlo y vuelve a armar el cubo con amarillo arriba, rojo a la izquierda y azul a la derecha. Es fácil de aprender y difícil de soltar.

• 50 niveles que crecen contigo, de 2×2×2 a 4×4×4 (y un pequeño secreto al final)
• Gana hasta 3 estrellas por nivel resolviéndolo en menos movimientos
• ¿Te atoraste? Una pista te muestra exactamente dónde deslizar, y las pistas que no uses se guardan
• Juego libre: elige tamaño y dificultad para mezclas sin fin
• Arma tu mezcla: pinta los rombos y crea tu propio reto
• Sonidos suaves y relajantes, y vibración ligera
• Tema claro y oscuro
• Funciona sin internet. Sin anuncios, sin cuentas, sin rastreo
• En español e inglés

Inspirado en el Propp Lozenge, el puzzle magnético inventado por James Propp y diseñado por Oskar van Deventer.

Hecho con cariño por BluBer Games.
```

**Palabras clave:**
```
puzzle,cubo,relajante,mente,lógica,rombos,deslizar,calma,zen,niveles,sin internet,acertijo,reto
```

---

## Para sacar una actualización más adelante

1. Haz los cambios en el juego y vuelve a generar `index.html`, igual que con la versión web.
2. En la carpeta `app/`, ejecuta:
   - `./release.sh` para subir solo un build nuevo (por ejemplo 1.0 (3)), o
   - `./release.sh 1.1` para además cambiar la versión.

   El script sube el número de build, copia el juego al proyecto de Xcode, hace el archive y lo sube a App Store Connect con la clave de API. No hace falta abrir Xcode.
   - La clave es Admin y vive solo en tu Mac, en `~/.appstoreconnect/` (`cubeswipe.env` y `private_keys/`). No se sube a git.
3. En App Store Connect, crea la versión nueva con **+ Version**, elige el build, escribe **What's New** y mándala a revisión.
