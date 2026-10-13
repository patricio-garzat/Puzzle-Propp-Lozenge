// Renderiza el tablero 3x3x3 del juego en alta resolución (PNG con fondo transparente),
// sin los puntos de giro ni la pista. Uso: node render-board.js <salida-dir>
const puppeteer = require("puppeteer-core");
const path = require("path");
const out = process.argv[2];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    headless: true,
  });
  const page = await browser.newPage();
  await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "dark" }]);
  await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 7, isMobile: true, hasTouch: true });
  await page.evaluateOnNewDocument(() => {
    try { sessionStorage.setItem("propp-skip-intro", "home"); } catch (e) {}
    try { localStorage.setItem("propp-settings-v1", JSON.stringify({ lang: "en", theme: "dark", vibe: true, intro: false })); } catch (e) {}
  });
  await page.goto("http://localhost:8792/index.html", { waitUntil: "load" });
  await new Promise((r) => setTimeout(r, 1500));

  const clickText = (re) => page.evaluate((src) => {
    const rx = new RegExp(src);
    const b = [...document.querySelectorAll("button")].find((x) => rx.test(x.textContent) && x.offsetParent !== null);
    if (b) b.click();
    return !!b;
  }, re.source);

  for (let i = 0; i < 2; i++) {
    if (i === 0) {
      console.log("free play", await clickText(/^\s*Free play/));
      await new Promise((r) => setTimeout(r, 700));
      console.log("3x3", await clickText(/^\s*3×3×3\s*$/));
      await new Promise((r) => setTimeout(r, 300));
      console.log("medium", await clickText(/^\s*Medium/));
    } else {
      console.log("new", await clickText(/^\s*\+?\s*New\s*$/));
      await new Promise((r) => setTimeout(r, 700));
      const again = await clickText(/^\s*Medium/);
      console.log("medium again", again);
    }
    await new Promise((r) => setTimeout(r, 3500));
    const ok = await page.evaluate(() => {
      const b = document.getElementById("board");
      if (!b) return "no board";
      ["dots", "hits", "hint", "hlg", "lift"].forEach((id) => { const g = b.querySelector("#" + id); if (g) g.style.display = "none"; });
      document.documentElement.style.background = "transparent";
      document.body.style.background = "transparent";
      document.querySelectorAll("body *").forEach((n) => { if (!n.contains(b) && !b.contains(n)) n.style.visibility = "hidden"; });
      let p = b; while (p) { if (p.style) { p.style.background = "transparent"; p.style.visibility = "visible"; } p = p.parentElement; }
      b.querySelectorAll("*").forEach((n) => (n.style.visibility = "visible"));
      return b.querySelectorAll("#tiles > *").length;
    });
    console.log("tiles", ok);
    const el = await page.$("#board");
    await el.screenshot({ path: path.join(out, `board-${i + 1}.png`), omitBackground: true });
    // regresar la interfaz a visible para el siguiente
    await page.evaluate(() => {
      const b = document.getElementById("board");
      document.querySelectorAll("body *").forEach((n) => (n.style.visibility = ""));
      ["dots", "hits", "hint", "hlg", "lift"].forEach((id) => { const g = b.querySelector("#" + id); if (g) g.style.display = ""; });
    });
  }
  await browser.close();
})();
