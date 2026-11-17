# Operación Transferencia: escape room contra el fraude BEC

Prototipo web y experimento piloto que replican a pequeña escala el estudio de:

> Keller, T. (2026). Effectiveness of a competence- and game-based learning environment using a digital educational escape room for promoting cybersecurity competence in apprentices. *Computers & Security, 171*, 105120. https://doi.org/10.1016/j.cose.2026.105120

Este trabajo es parte de la propuesta de investigación *Gamificación y aprendizaje adaptativo para la mitigación de riesgos humanos frente a ataques de Business Email Compromise (BEC) en la ciberseguridad de PyMEs* (Universidad de Lima, Proyecto de Investigación 2026-2).

**Jugar:** `index.html?demo=1`, o la versión publicada en GitHub Pages.

## Qué se replica del artículo

| Elemento | Keller (2026) | Esta réplica |
|---|---|---|
| Intervención | Escape room digital (DEER 3: ingeniería social) | Escape room web sobre BEC, adaptado del DEER 3 |
| Estructura | 5 misiones con un avatar que hace de coach | 5 misiones con la coach "Ada" |
| Ayudas | Pistas graduadas: general, específica y combinada | 3 pistas graduadas por misión |
| Retroalimentación | Resultado, respuesta correcta y explicación | Igual: correcto o incorrecto, respuesta correcta tras 2 intentos y explicación |
| Motivación | Insignia y pregunta de reflexión por misión | Igual |
| Medición | Test situacional (SJT) validado de 7 dimensiones, 0-2 puntos por ítem | 7 ítems, uno por dimensión, 0-2 puntos, 14 por forma (redacción propia) |
| Formas paralelas | Testlets paralelos en cada medición | Forma A (cambio de cuenta del proveedor) y forma B (falso gerente) |
| Diseño | Ensayo aleatorizado por aulas, con grupo de control | Aleatorización individual por bloques de 2, con grupo de control |
| Momentos | Pretest, postest (1 semana) y seguimiento (8 semanas) | Pretest y postest en la misma sesión |
| Análisis | Modelo de cambio latente (n = 154) | Ganancias, Mann-Whitney, g de Hedges y ANCOVA |

Las 7 dimensiones del test son las de Keller (2026): conciencia de la amenaza, identificación, evaluación del impacto, elección de la táctica, justificación, ejecución, y revisión y seguimiento.

## Cómo usarlo

- **Participantes:** abren la página, escriben su número (1 a 40) y siguen los pasos. Al final copian su código de resultados y se lo envían al responsable.
- **Grupos:** los decide la lista `ASSIGN` de `index.html`, generada al azar por bloques de 2 (semilla 20261117).
- **Demo:** `?demo=1` va directo al escape room, sin tests.
- **Panel del responsable:** `?admin=1`. Pegas los códigos, ves la tabla por grupo y descargas `resultados.csv`.

## Análisis

```bash
pip install pandas scipy
python analisis.py resultados.csv
```

El script calcula los descriptivos por grupo, la prueba de Mann-Whitney y la t de Welch sobre las ganancias, la g de Hedges, una ANCOVA (test final según el test inicial y el grupo), la prueba de Wilcoxon dentro de cada grupo y la ganancia por dimensión.

## Prueba automática

```bash
npm install --no-save playwright && npx playwright install chromium
node tests/prueba_e2e.js
```

## Limitaciones

- Muestra pequeña y de conveniencia: es un piloto.
- No hay seguimiento a 8 semanas.
- El postest se aplica en la misma sesión, así que mide el efecto inmediato.
- El test es una adaptación propia y no está validado como el SJT de Keller y Warwas (2026).

La empresa (Textiles Andinos SAC), las personas y los correos del juego son ficticios.
