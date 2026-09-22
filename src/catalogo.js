// Temario inicial. Se carga en la base de datos solo la primera vez que arranca el servidor.
// Después puedes agregar o borrar temas desde el panel de administración.
// Estructura: nivel -> área -> rama -> temas

module.exports = [
  {
    slug: 'secundaria',
    nombre: 'Secundaria',
    descripcion: 'Bases sólidas de matemáticas y física para 1°, 2° y 3° de secundaria.',
    areas: [
      {
        slug: 'matematicas',
        nombre: 'Matemáticas',
        ramas: [
          { nombre: 'Aritmética', temas: ['Números enteros y operaciones', 'Fracciones y decimales', 'Potencias y raíces', 'Proporcionalidad y porcentajes'] },
          { nombre: 'Álgebra', temas: ['Expresiones algebraicas', 'Ecuaciones lineales', 'Sistemas de ecuaciones 2×2', 'Productos notables y factorización', 'Ecuaciones cuadráticas'] },
          { nombre: 'Geometría', temas: ['Ángulos y triángulos', 'Teorema de Pitágoras', 'Perímetros y áreas', 'Volúmenes de cuerpos geométricos'] },
          { nombre: 'Probabilidad y estadística', temas: ['Medidas de tendencia central', 'Gráficas e interpretación de datos', 'Probabilidad básica'] },
        ],
      },
      {
        slug: 'fisica',
        nombre: 'Física',
        ramas: [
          { nombre: 'Movimiento', temas: ['Posición, distancia y desplazamiento', 'Velocidad y rapidez (MRU)', 'Aceleración (MRUA)', 'Caída libre'] },
          { nombre: 'Fuerzas', temas: ['Leyes de Newton', 'Masa y peso', 'Presión'] },
          { nombre: 'Energía', temas: ['Tipos de energía', 'Conservación de la energía', 'Calor y temperatura'] },
          { nombre: 'Electricidad y magnetismo', temas: ['Carga eléctrica', 'Circuitos eléctricos simples', 'Magnetismo e imanes'] },
          { nombre: 'Ondas, sonido y luz', temas: ['Ondas y sus características', 'El sonido', 'La luz y los colores'] },
          { nombre: 'Materia y universo', temas: ['Modelo cinético de partículas', 'Estados de agregación', 'El Sistema Solar y el universo'] },
        ],
      },
    ],
  },
  {
    slug: 'preparatoria',
    nombre: 'Preparatoria',
    descripcion: 'Del álgebra al cálculo y la física clásica de bachillerato.',
    areas: [
      {
        slug: 'matematicas',
        nombre: 'Matemáticas y cálculo',
        ramas: [
          { nombre: 'Álgebra y funciones', temas: ['Funciones y sus gráficas', 'Polinomios', 'Desigualdades', 'Exponentes y logaritmos'] },
          { nombre: 'Trigonometría', temas: ['Razones trigonométricas', 'Ley de senos y ley de cosenos', 'Círculo unitario y funciones trigonométricas', 'Identidades trigonométricas'] },
          { nombre: 'Geometría analítica', temas: ['La recta', 'La circunferencia', 'La parábola', 'La elipse', 'La hipérbola'] },
          { nombre: 'Cálculo diferencial', temas: ['Límites', 'Continuidad', 'Definición de derivada', 'Reglas de derivación', 'Regla de la cadena', 'Derivación implícita', 'Máximos y mínimos', 'Razones de cambio relacionadas'] },
          { nombre: 'Cálculo integral', temas: ['Antiderivadas', 'Integral definida y Teorema Fundamental del Cálculo', 'Integración por sustitución', 'Integración por partes', 'Fracciones parciales', 'Áreas entre curvas', 'Volúmenes de revolución'] },
          { nombre: 'Probabilidad y estadística', temas: ['Estadística descriptiva', 'Técnicas de conteo', 'Probabilidad condicional', 'Distribución binomial y normal'] },
        ],
      },
      {
        slug: 'fisica',
        nombre: 'Física',
        ramas: [
          { nombre: 'Mecánica', temas: ['Vectores', 'Cinemática en una dimensión', 'Tiro parabólico', 'Movimiento circular', 'Leyes de Newton y diagramas de cuerpo libre', 'Trabajo, energía y potencia', 'Cantidad de movimiento y choques', 'Gravitación universal'] },
          { nombre: 'Fluidos', temas: ['Densidad y presión hidrostática', 'Principios de Pascal y Arquímedes', 'Ecuación de continuidad y Bernoulli'] },
          { nombre: 'Termodinámica', temas: ['Temperatura y dilatación térmica', 'Calorimetría y cambios de fase', 'Leyes de la termodinámica'] },
          { nombre: 'Ondas y óptica', temas: ['Movimiento armónico simple', 'Ondas mecánicas', 'Reflexión y refracción', 'Espejos y lentes'] },
          { nombre: 'Electricidad y magnetismo', temas: ['Ley de Coulomb', 'Campo eléctrico', 'Potencial eléctrico', 'Ley de Ohm y circuitos', 'Leyes de Kirchhoff', 'Campo magnético', 'Inducción electromagnética'] },
        ],
      },
    ],
  },
  {
    slug: 'universidad',
    nombre: 'Universidad básica',
    descripcion: 'Cálculo, álgebra lineal, ecuaciones diferenciales y física universitaria de primeros semestres.',
    areas: [
      {
        slug: 'matematicas',
        nombre: 'Matemáticas y cálculo',
        ramas: [
          { nombre: 'Cálculo diferencial', temas: ['Límites y definición ε-δ', 'Derivadas y sus aplicaciones', "Regla de L'Hôpital", 'Aproximaciones lineales y diferenciales'] },
          { nombre: 'Cálculo integral', temas: ['Técnicas de integración', 'Sustitución trigonométrica', 'Integrales impropias', 'Aplicaciones de la integral'] },
          { nombre: 'Sucesiones y series', temas: ['Sucesiones', 'Criterios de convergencia', 'Series de potencias', 'Series de Taylor y Maclaurin'] },
          { nombre: 'Cálculo multivariable', temas: ['Vectores y geometría del espacio', 'Funciones de varias variables', 'Derivadas parciales y gradiente', 'Multiplicadores de Lagrange', 'Integrales dobles y triples', 'Integrales de línea y de superficie', 'Teoremas de Green, Stokes y divergencia'] },
          { nombre: 'Álgebra lineal', temas: ['Sistemas de ecuaciones y eliminación gaussiana', 'Matrices y determinantes', 'Espacios vectoriales', 'Transformaciones lineales', 'Valores y vectores propios'] },
          { nombre: 'Ecuaciones diferenciales', temas: ['EDO de primer orden', 'EDO lineales de orden superior', 'Transformada de Laplace', 'Sistemas de ecuaciones diferenciales'] },
        ],
      },
      {
        slug: 'fisica',
        nombre: 'Física',
        ramas: [
          { nombre: 'Mecánica clásica', temas: ['Cinemática en 2D y 3D', 'Dinámica de partículas', 'Trabajo y energía', 'Momento lineal y colisiones', 'Rotación y torca', 'Momento angular', 'Oscilaciones', 'Gravitación'] },
          { nombre: 'Termodinámica', temas: ['Gas ideal y teoría cinética', 'Primera ley de la termodinámica', 'Segunda ley y entropía', 'Máquinas térmicas'] },
          { nombre: 'Electromagnetismo', temas: ['Ley de Gauss', 'Potencial eléctrico y capacitancia', 'Corriente, resistencia y circuitos RC', 'Ley de Biot-Savart y ley de Ampère', 'Ley de Faraday e inductancia', 'Ecuaciones de Maxwell'] },
          { nombre: 'Ondas y óptica', temas: ['Ondas mecánicas y sonido', 'Interferencia', 'Difracción', 'Polarización'] },
          { nombre: 'Física moderna', temas: ['Relatividad especial', 'Efecto fotoeléctrico', 'Modelo atómico de Bohr', 'Dualidad onda-partícula'] },
        ],
      },
    ],
  },
];
