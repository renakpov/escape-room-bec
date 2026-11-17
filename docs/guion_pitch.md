# Guion del pitch (5 minutos, sin leer)

No es para memorizar palabra por palabra. Quédate con la idea de cada bloque.

## 1. El artículo (30 s), en la portada
"Repliqué el estudio de Thomas Keller, publicado este año en *Computers & Security*, una revista Q1. Keller probó un escape room digital con 154 aprendices en Alemania. Los que jugaron mejoraron bastante más que el grupo de control, y la ventaja se mantuvo ocho semanas después, aunque más baja."

## 2. El workflow (1 min), en la diapositiva 1
"Lo adapté a mi tesis, que trata del fraude BEC. Mantuve lo que hace funcionar el juego de Keller: cinco misiones, una coach que da pistas de lo más general a lo más específico, retroalimentación al instante e insignias. Para medir usé sus siete dimensiones: reconocer el ataque, identificarlo, ver el impacto, elegir la defensa, justificarla, aplicarla y hacer el seguimiento. Cada pregunta vale de 0 a 2 puntos, hasta 14."

Señala la tabla de abajo: "Cambié el tema a BEC, asigné al azar persona por persona y no por aula, y medí antes y después en la misma sesión."

## 3. Demo (2 min), en la diapositiva 2 con el enlace `?demo=1`
- Misión 1: "Llegan cuatro correos. Dos son BEC: piden dinero y vienen de dominios parecidos, pero no iguales." Pide una pista para que vean a la coach.
- Misión 2: "El nombre se puede falsificar. Lo que delata el engaño es el dominio con guion y el 'Responder a' que manda la respuesta a un Gmail."
- Termina la misión y muestra la insignia: "Cada misión da un dígito. Con los cinco se bloquea el pago."

## 4. Resultados (1 min 30 s)
"En mi piloto participaron __ compañeros. El grupo que jugó subió __ puntos y el control __." Luego di qué significa: si fue significativo o no, y cómo se compara con Keller.

Cierra con las limitaciones: "Es una muestra pequeña, no hice la medición a las ocho semanas y mi test no está validado. El siguiente paso es probarlo en PyMEs reales y medir otra vez semanas después."

## Preguntas probables del jurado

- **¿Por qué este artículo?** Es Q1, es de 2026 y trata la gamificación, que es la base de mi tesis. Además describe el juego con suficiente detalle para replicarlo.
- **¿Qué es un escape room educativo?** Un juego en el que resuelves retos para "escapar". Aquí, para bloquear un pago falso antes de que cierre el sistema.
- **¿Cómo asignaste los grupos?** Al azar, por bloques de dos: a cada número le toca juego o control según una lista generada con una semilla fija, para que se pueda reproducir.
- **¿Por qué Mann-Whitney y no el modelo de Keller?** El modelo de cambio latente necesita muestras grandes. Con un piloto pequeño se usa una prueba no paramétrica y una ANCOVA para controlar el punto de partida.
- **¿Qué es la g de Hedges?** El tamaño del efecto: cuánto más mejoró el grupo que jugó, en unidades de desviación estándar. Está corregida para muestras pequeñas.
- **¿Qué cambiarías?** Validar el test con expertos, hacerlo en una PyME real, medir a las 8 semanas y agregar la parte adaptativa de mi tesis.
- **¿Dónde está el código?** En GitHub, en el enlace de la diapositiva: el juego, el análisis y el README.
