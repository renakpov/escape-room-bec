// Prueba de punta a punta del prototipo (index.html).
// Uso (desde la raíz del repo):
//   npm install --no-save playwright && npx playwright install chromium
//   node tests/prueba_e2e.js
// Simula un participante del grupo control (#1) y uno del grupo juego (#2),
// revisa el código de resultados, el panel ?admin=1 y el modo ?demo=1.
const path = require("path");
const assert = require("assert");
const { chromium } = require("playwright");

const URL = "file://" + path.resolve(__dirname, "..", "index.html");

async function responderTest(p, valor) {
  for (let i = 0; i < 7; i++) await p.check(`input[name="q${i}"][value="${valor}"]`);
  await p.click("#send");
}

async function jugar(p) {
  await p.click("#b");
  for (const t of ["Transferencia urgente", "Actualizamos nuestra"]) await p.click(`label.opt:has-text("${t}") input`);
  await p.click("#check"); await p.click("#b");
  await p.click("#hint");
  await p.click('.clue:has-text("Dirección:")'); await p.click('.clue:has-text("Responder a")');
  await p.click("#check"); await p.click("#b");
  for (const t of ["Autoridad", "Urgencia", "Secreto"]) await p.click(`label.opt:has-text("${t}") input`);
  await p.click("#check"); await p.click("#b");
  await p.click('label.opt:has-text("Llamo al gerente") input'); await p.click("#check"); await p.click("#b");
  const pasos = ["No pagar ni responder", "Confirmar por teléfono", "Reportar el correo", "Avisar al equipo"];
  for (let k = 0; k < 4; k++) await p.selectOption(`label.opt:has-text("${pasos[k]}") select`, String(k + 1));
  await p.click("#check"); await p.click("#b");
  await p.fill("#code", "47295"); await p.click("#b");
  assert.ok((await p.textContent("#app")).includes("Transferencia bloqueada"), "No se llegó al final del escape room");
  await p.click("#b");
}

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 420, height: 900 } });
  const errores = [];
  p.on("pageerror", (e) => errores.push(e.message));
  const filas = [];

  for (const [id, pre, post] of [[1, "1", "1"], [2, "1", "2"]]) {
    await p.goto(URL);
    await p.fill("#pid", String(id)); await p.click("#b");
    await responderTest(p, pre);
    if ((await p.textContent("#app")).includes("Grupo de comparación")) await p.click("#b");
    else await jugar(p);
    await responderTest(p, post);
    filas.push((await p.textContent("#code")).trim());
  }

  assert.match(filas[0], /^1,C,7,7,0,/, "Fila del control incorrecta: " + filas[0]);
  assert.match(filas[1], /^2,J,7,14,7,/, "Fila del juego incorrecta: " + filas[1]);
  assert.strictEqual(filas[1].split(",").length, 24, "La fila debe tener 24 columnas");

  await p.goto(URL + "?admin=1");
  await p.fill("#raw", filas.join("\n")); await p.click("#calc");
  const panel = await p.textContent("#out");
  assert.ok(panel.includes("Juego") && panel.includes("Control"), "El panel no calculó la tabla");

  await p.goto(URL + "?demo=1");
  assert.ok((await p.textContent("#app")).includes("Bloquea el pago falso"), "El modo demo no abre el juego");

  assert.deepStrictEqual(errores, [], "Errores de JavaScript: " + errores.join(" | "));
  await b.close();
  console.log("OK: prueba de punta a punta superada\n" + filas.join("\n"));
})().catch((e) => { console.error("FALLÓ:", e.message); process.exit(1); });
