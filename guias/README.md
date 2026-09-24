# Guías PDF · El Lab del Desierto

Generador de guías de estudio con el diseño aprobado (letra Nunito, tonos desérticos, tamaño carta),
pensadas para que el alumno estudie solo y te contacte si tiene dudas.

## Guías incluidas

`pdf/` tiene 92 guías listas; la plataforma las sube sola a su tema al arrancar (ver
`pdf/manifiesto.json`).

**Secundaria (35)**

- **Matemáticas (16):** enteros, fracciones y decimales, potencias y raíces, proporcionalidad y
  porcentajes, expresiones algebraicas, ecuaciones lineales, sistemas 2×2, productos notables y
  factorización, ecuaciones cuadráticas, ángulos y triángulos, Pitágoras, perímetros y áreas,
  volúmenes, tendencia central, gráficas, probabilidad.
- **Física (19):** posición y desplazamiento, MRU, MRUA, caída libre, leyes de Newton, masa y peso,
  presión, tipos de energía, conservación de la energía, calor y temperatura, carga eléctrica,
  circuitos, magnetismo, ondas, sonido, luz y colores, modelo cinético, estados de agregación,
  Sistema Solar y universo.

**Preparatoria (57)**

- **Matemáticas (32):** funciones, polinomios, desigualdades, exponentes y logaritmos; razones
  trigonométricas, leyes de senos y cosenos, círculo unitario, identidades; recta, circunferencia,
  parábola, elipse, hipérbola; límites, continuidad, definición de derivada, reglas de derivación,
  regla de la cadena, derivación implícita, máximos y mínimos, razones relacionadas; antiderivadas,
  integral definida y TFC, sustitución, partes, fracciones parciales, áreas entre curvas, volúmenes
  de revolución; estadística descriptiva, conteo, probabilidad condicional, binomial y normal.
- **Física (25):** vectores, cinemática 1D, tiro parabólico, movimiento circular, Newton y DCL,
  trabajo y energía, cantidad de movimiento, gravitación; densidad y presión, Pascal y Arquímedes,
  continuidad y Bernoulli; dilatación, calorimetría, leyes de la termodinámica; MAS, ondas
  mecánicas, reflexión y refracción, espejos y lentes; Coulomb, campo eléctrico, potencial, Ohm y
  circuitos, Kirchhoff, campo magnético, inducción.

Cada guía trae: objetivos, cómo usar la guía, teoría con ejemplos resueltos, errores comunes, hoja de
repaso recortable, ejercicios, respuestas, soluciones paso a paso, autoevaluación con la sección a
repasar y bloque de contacto.

## Crear una guía nueva

1. Copia `plantilla/EJEMPLO.html` a `contenido/<nivel>/<materia>/NN-nombre.html`.
2. Llena el bloque de datos (título, rama, objetivos, autoevaluación) y escribe las secciones.
   El ejemplo muestra todos los componentes: definición, nota, ejemplo resuelto, tablas, figuras,
   errores comunes, repaso, ejercicios y respuestas.
3. Construye:

```bash
cd guias
npm install          # solo la primera vez
node construir.js contenido/secundaria/fisica/20-mi-tema.html   # una guía
node construir.js                                                # todas
```

El PDF queda en `pdf/` y se actualiza `pdf/manifiesto.json`, que la plataforma usa para subir la
guía y la descripción del tema al arrancar. El tema se busca por el título (debe coincidir con el
del catálogo); si no coincide, agrega `tema: <slug-del-tema>` al bloque de datos. La descripción
va en `descripcion:`. El generador **se detiene** si una fórmula está mal escrita, si algo se sale
del margen, si falta una fuente o si la autoevaluación apunta a una sección que no existe.

Requiere Node.js 20+ y Chromium (en una computadora normal, instala Chrome y define
`CHROMIUM_PATH` con la ruta del ejecutable si no lo encuentra solo).

## Comprobar las respuestas

`verificar.py` recalcula con Python (fracciones exactas y `sympy`) todas las respuestas numéricas y
algebraicas de cada guía y las compara con lo que dice el PDF:

```bash
pip install sympy
python3 verificar.py
```

Cuando agregues una guía, agrega su bloque `@guia(...)` con sus comprobaciones.

## Personalizar

- `config.json`: nombre de la marca, ciudad y el texto de contacto (por ejemplo, un número de
  WhatsApp o correo).
- `plantilla/estilos.css`: colores y tipografía.
- `herramientas/graficas.py`: genera gráficas de barras, circulares y de líneas en SVG a partir de
  datos, para que queden exactas.
