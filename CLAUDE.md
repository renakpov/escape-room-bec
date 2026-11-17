# CLAUDE.md: Operación Transferencia (Semana 13, replicar un artículo)

Contexto para Claude Code. Léelo antes de tocar cualquier archivo.

## Para quién es y para cuándo

- **Alumno:** Renato Apaza Raymundo. Universidad de Lima, Ingeniería de Sistemas, curso Proyecto de Investigación, 2026-2. Su cuenta de GitHub probablemente es `renakpov`.
- **Tesis:** *Gamificación y aprendizaje adaptativo para la mitigación de riesgos humanos frente a ataques de Business Email Compromise (BEC) en la ciberseguridad de PyMEs*.
- **Tarea de la Semana 13:** replicar el experimento de un artículo Scopus/WoS, de preferencia Q1/Q2 de SJR y de los últimos 5 años (mejor si es de los últimos 2). Se expone en formato pitch: **5 minutos, centrado en la experimentación, sin leer un libreto**, y luego 2 o 3 minutos de preguntas del jurado. El docente puede preguntar por cualquier parte del PPT, del código o del artículo original. Se puede usar IA generativa, siempre que el alumno valide el resultado.
- **PPT pedido:** portada, luego *Diapositiva 1: Workflow de la investigación* y *Diapositiva 2: Experimentación* (presentar el prototipo y agregar el enlace de GitHub).
- **Exposición:** martes 17 de noviembre de 2026.

## Artículo replicado

Keller, T. (2026). Effectiveness of a competence- and game-based learning environment using a digital educational escape room for promoting cybersecurity competence in apprentices. *Computers & Security, 171*, 105120. https://doi.org/10.1016/j.cose.2026.105120. La revista es Q1 en SJR (el alumno debe confirmarlo en scimagojr.com).

Si el PDF está disponible, se encuentra en `privado/articulos/`.

### Datos verificados del original (usa solo estos; no inventes otros)

- **Diseño:** ensayo controlado aleatorizado por conglomerados (aulas). El grupo de intervención jugó; el grupo de control solo respondió los tests (§4.1).
- **Muestra:** N = 154 aprendices de formación profesional comercial en 2 escuelas de Alemania; 79,9 % mujeres; edades de 15 a 37 años (M = 20,03) (§4.2).
- **Intervención:** lección de 90 minutos con briefing (15 min), juego (30 min) y debriefing (45 min). El escape room DEER 3 trata ingeniería social. Cada escape room tiene 5 misiones, un avatar que actúa como coach con pistas graduadas (de general a específica y luego combinada), retroalimentación inmediata (resultado, respuesta correcta y explicación) e insignias con una pregunta de reflexión (§3.2 y §3.3).
- **Medición:** test situacional (SJT) validado por Keller y Warwas (2026). Hay 7 dimensiones de competencia: conciencia de la amenaza, identificación, evaluación del impacto, elección de la táctica, justificación, ejecución, y revisión y seguimiento. Cada dimensión tiene un ítem que vale de 0 a 2 puntos, así que cada testlet vale 14 puntos. Hay 3 testlets por medición, para un máximo de 42 (§4.3).
- **Momentos:** pretest una semana antes, postest una semana después y seguimiento a las 8 semanas (§3.4 y §4.1).
- **Resultados** (modelo de cambio latente; resumen y §5.2):
  - El grupo de intervención empezó un poco más alto en el pretest (b = 0,71; p = 0,023).
  - Su ganancia del pretest al postest fue mucho mayor que la del control (b = 1,97; p < 0,001; β = 0,66).
  - Del postest al seguimiento, la ventaja bajó (b = −0,96; p = 0,028).
  - Diferencia total entre grupos en el postest: b = 2,77 (p < 0,001; β = 0,92). En el seguimiento: b = 1,03 (p = 0,009), es decir, la ventaja bajó pero siguió siendo significativa.
- **Escala:** la escala latente usa como referencia el primer testlet (0-14 puntos). Por eso b = 1,97 se puede leer, de forma aproximada y no exacta, como puntos de un testlet de 14. La réplica también usa formas de 14 puntos.

## Qué se replicó y qué se cambió

| | Keller (2026) | Esta réplica |
|---|---|---|
| Juego | DEER 3, ingeniería social | Escape room web sobre BEC (`index.html`), 5 misiones |
| Coach y ayudas | Avatar con pistas graduadas, feedback e insignias | Coach "Ada", 3 pistas por misión, feedback e insignias con reflexión |
| Test | SJT validado, 7 dimensiones × 3 testlets | 7 ítems por forma (uno por dimensión), 0-2 puntos, forma A (proveedor) y forma B (falso gerente). **Redacción propia, no validada** |
| Asignación | Por aulas | Por persona, bloques de 2 (lista `ASSIGN`, semilla 20261117) |
| Momentos | Pre, post (1 semana) y seguimiento (8 semanas) | Pre y post en la misma sesión |
| Análisis | Modelo de cambio latente | Ganancias, Mann-Whitney (unilateral), g de Hedges, ANCOVA y Wilcoxon |

## Estructura

```
index.html                 Prototipo completo en un solo archivo, sin dependencias
                           ?demo=1  → va directo al juego (para la exposición)
                           ?admin=1 → panel: pegar códigos, ver la tabla y descargar resultados.csv
analisis.py                Estadística (cargar, calcular, imprimir). Requiere pandas y scipy
resultados_plantilla.csv   Cabecera del CSV (24 columnas, en el orden que genera la app)
presentacion/
  build_ppt.py             Genera la PPT desde la plantilla; con --resultados llena la tabla
  plantilla_semana13.pptx  Plantilla oficial del curso
  capturas/                Capturas del juego que usa la PPT
  capturas.js              Regenera las capturas (Playwright)
  PI_2026-2_Semana13_RenatoApaza.pptx   PPT generada (resultados en blanco "__")
tests/prueba_e2e.js        Prueba de punta a punta del prototipo (Playwright)
docs/guion_pitch.md        Guion de 5 minutos y respuestas a preguntas probables
privado/                   Solo local, en .gitignore: documentos de la tesis y el PDF del artículo
```

Formato de cada código de resultados (una línea por participante):
`id,grupo,pre,post,ganancia,pre_d1..pre_d7,post_d1..post_d7,puntos,pistas,errores,t_juego_s,t_total_s`
El grupo es `J` (juego) o `C` (control). Las columnas del juego quedan vacías en el control.

## Comandos

```bash
pip install python-pptx pandas scipy
python analisis.py resultados.csv
python presentacion/build_ppt.py --github https://github.com/USUARIO/escape-room-bec --resultados resultados.csv

npm install --no-save playwright && npx playwright install chromium
node tests/prueba_e2e.js          # correr después de cualquier cambio en index.html
node presentacion/capturas.js     # si cambia el aspecto del juego, luego vuelve a generar la PPT
```

## Tareas pendientes (en orden)

1. **Publicar en GitHub.**
   - Si el repo `escape-room-bec` todavía no existe: `gh repo create escape-room-bec --public --source=. --push`.
   - Luego activa GitHub Pages, sea en *Settings → Pages → Branch main / root* o con `gh api -X POST repos/USUARIO/escape-room-bec/pages -f "source[branch]=main" -f "source[path]=/"`.
   - La URL del juego queda en `https://USUARIO.github.io/escape-room-bec/`.
2. **Poner el enlace en la PPT:** `python presentacion/build_ppt.py --github https://github.com/USUARIO/escape-room-bec`.
3. **Piloto con 10 a 20 compañeros.**
   - A cada uno se le da un número del 1 al 40 y el enlace de Pages.
   - Al terminar, cada uno envía su código de resultados.
4. **Resultados.**
   - Pega los códigos debajo de la cabecera de `resultados_plantilla.csv` y guárdalo como `resultados.csv`.
   - Corre `python analisis.py resultados.csv`.
   - Regenera la PPT con `--resultados resultados.csv`. Revisa que la frase "Réplica: …" diga lo que muestran los datos.
5. **Ensayo:** usa `docs/guion_pitch.md`. El alumno no puede leer en la exposición; ayúdalo a practicar con preguntas.

## Reglas de trabajo

- Responde en **español**, directo y sin relleno. Renato prefiere un lenguaje humano y poco técnico en lo que va a decir en voz alta.
- **No inventes datos ni resultados.** Los `__` de la PPT se llenan solo con datos reales del piloto. Si citas el artículo, usa los datos verificados de arriba.
- La empresa (Textiles Andinos SAC), las personas y los correos del juego son ficticios. Mantén que así sea y no uses marcas reales.
- `index.html` debe seguir siendo un solo archivo sin dependencias externas, para que funcione en GitHub Pages y también abierto como archivo local.
- **Nunca subas `privado/` a GitHub.** Ese contenido es su trabajo de tesis sin publicar.
- Los documentos de `privado/tesis` pueden estar desactualizados frente a las versiones que Renato editó después. Por ejemplo, él quitó "Lima Metropolitana" y no quiere citas de 2020 en la exposición. Pregúntale antes de usarlos como fuente final.
- Antes de dar por terminado un cambio en el juego, corre `node tests/prueba_e2e.js`.

## Limitaciones que hay que reconocer en la exposición

- Es un piloto con una muestra pequeña y de conveniencia, así que no es generalizable.
- No hay medición de seguimiento a las 8 semanas.
- El postest se aplica en la misma sesión, así que mide el efecto inmediato.
- El test es una adaptación propia y no está validado como el SJT de Keller y Warwas (2026).
- La asignación es individual, no por aulas.
