// Regenera las capturas del juego que usa la PPT (presentacion/capturas/).
// Uso (desde la raíz del repo): node presentacion/capturas.js
const path = require("path");
const { chromium } = require("playwright");

const URL = "file://" + path.resolve(__dirname, "..", "index.html");
const OUT = (n) => path.join(__dirname, "capturas", n);

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 760, height: 620 }, deviceScaleFactor: 2 });
  await p.goto(URL + "?demo=1");
  await p.screenshot({ path: OUT("ss_intro.png") });
  await p.click("#b");
  await p.click('label.opt:has-text("Transferencia urgente") input');
  await p.click("#hint");
  await p.screenshot({ path: OUT("ss_m1.png") });
  await p.click('label.opt:has-text("Actualizamos") input');
  await p.click("#check");
  await p.waitForTimeout(600);
  await p.screenshot({ path: OUT("ss_badge.png") });
  await b.close();
  console.log("Capturas actualizadas en presentacion/capturas/");
})();
