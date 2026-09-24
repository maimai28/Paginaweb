// Generador de guías PDF · El Lab del Desierto
//
// Uso:
//   node construir.js                      construye todas las guías de contenido/
//   node construir.js contenido/x/y.html   construye solo esas
//
// Cada guía es un archivo HTML con un bloque de datos al inicio (ver plantilla/EJEMPLO.html).
// El generador agrega portada, "cómo usar", numeración de secciones, autoevaluación, contacto
// y pie de página, y se detiene si encuentra fórmulas mal escritas o contenido que se desborda.

const fs = require('node:fs');
const path = require('node:path');
const katex = require('katex');
const { chromium } = require('playwright-core');

const RAIZ = __dirname;
const CONFIG = JSON.parse(fs.readFileSync(path.join(RAIZ, 'config.json'), 'utf8'));

// ---------- Lectura del archivo de contenido ----------

function leerGuia(archivo) {
  const texto = fs.readFileSync(archivo, 'utf8');
  const m = texto.match(/^\s*<!--\s*guia([\s\S]*?)-->/);
  if (!m) throw new Error(`${archivo}: falta el bloque <!-- guia ... --> al inicio`);
  const meta = { objetivos: [], autoeval: [] };
  for (const linea of m[1].split('\n')) {
    const i = linea.indexOf(':');
    if (i < 0 || !linea.trim()) continue;
    const clave = linea.slice(0, i).trim();
    const valor = linea.slice(i + 1).trim();
    if (clave === 'objetivo') meta.objetivos.push(valor);
    else if (clave === 'autoeval') {
      const [txt, sec] = valor.split('|').map((s) => s.trim());
      meta.autoeval.push({ txt, sec });
    } else meta[clave] = valor;
  }
  for (const c of ['titulo', 'nivel', 'materia', 'rama', 'numero', 'entrada']) {
    if (!meta[c]) throw new Error(`${archivo}: falta "${c}" en el bloque de datos`);
  }
  return { meta, cuerpo: texto.slice(m[0].length) };
}

// ---------- Piezas automáticas ----------

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function paisaje(materia) {
  const fisica = /f[ií]sica/i.test(materia);
  // Matemáticas: marcas de eje. Física: trayectoria parabólica punteada.
  const extra = fisica
    ? '<path d="M210 122 Q420 -20 640 108" fill="none" stroke="#4b5d6b" stroke-width="1.6" stroke-dasharray="3 5"/><circle cx="640" cy="108" r="3.2" fill="#4b5d6b"/>'
    : '<g stroke="#2b241e" stroke-width="1">' + Array.from({ length: 9 }, (_, i) => `<line x1="${(i + 1) * 100}" y1="144" x2="${(i + 1) * 100}" y2="150"/>`).join('') + '</g>';
  return `<svg class="paisaje" viewBox="0 0 1000 150" aria-hidden="true">
    <circle cx="760" cy="78" r="34" fill="#c08a2e" opacity=".85"/>
    <path d="M0 96 L70 80 L118 88 L170 58 L214 74 L262 52 L318 78 L372 66 L430 84 L505 62 L560 70 L612 46 L668 72 L722 64 L790 88 L846 70 L905 82 L960 68 L1000 76 L1000 150 L0 150 Z" fill="#e4d2b4"/>
    <path d="M0 116 C90 98 150 104 230 110 S390 96 470 106 S640 118 720 104 S880 94 1000 108 L1000 150 L0 150 Z" fill="#d9b98c"/>
    <path d="M0 132 C120 118 210 122 300 130 S520 140 610 128 S820 116 1000 130 L1000 150 L0 150 Z" fill="#a8492a"/>
    <g stroke="#2b241e" stroke-width="2.2" stroke-linecap="round" fill="none">
      <path d="M120 128 C116 104 104 84 96 58"/><path d="M121 128 C121 100 118 76 120 46"/>
      <path d="M122 128 C128 104 138 86 148 64"/><path d="M120 128 C110 110 94 98 80 86"/>
      <path d="M123 128 C134 112 150 104 164 96"/>
    </g>
    <line x1="0" y1="149.5" x2="1000" y2="149.5" stroke="#2b241e" stroke-width="1"/>
    ${extra}
  </svg>`;
}

function portada(meta) {
  const titulo = esc(meta.titulo).replace(/ y /, ' <span class="y">y</span> ');
  return `<header class="portada">
  ${paisaje(meta.materia)}
  <div class="rotulo"><span>${esc(meta.nivel)}</span><span>${esc(meta.materia)}</span><span>${esc(meta.rama)}</span><span>Guía ${esc(meta.numero)}</span></div>
  <h1>${titulo}</h1>
  <p class="entrada">${meta.entrada}</p>
  <div class="objetivos">
    <h3>Al terminar vas a poder</h3>
    <ol>${meta.objetivos.map((o) => `<li>${o}</li>`).join('')}</ol>
  </div>
  <div class="uso">
    <div><b>1 · Lee en orden</b>Cada sección usa lo de la anterior. No te saltes ninguna aunque te parezca fácil.</div>
    <div><b>2 · Intenta antes de ver</b>En los ejemplos resueltos, tapa la solución y trata de hacerlo tú primero.</div>
    <div><b>3 · Practica</b>Haz los ejercicios en tu cuaderno. Al final vienen las respuestas y las soluciones paso a paso.</div>
    <div><b>4 · Si te atoras</b>Revisa la sección indicada en la autoevaluación. Si sigue sin salir, escríbeme (datos en la última página).</div>
  </div>
</header>`;
}

function cierre(meta) {
  const caja = '<td><span class="caja"></span></td>';
  const auto = meta.autoeval.length ? `
  <div class="autoeval">
    <h3>Autoevaluación</h3>
    <p class="paso">Marca con honestidad. Si algo quedó en “Todavía no”, vuelve a la sección que se indica y repite sus ejercicios.</p>
    <table>
      <thead><tr><th>Puedo…</th><th>Repasa</th><th>Todavía no</th><th>Más o menos</th><th>Lo domino</th></tr></thead>
      <tbody>${meta.autoeval.map((a) => `<tr><td>${a.txt}</td><td class="repasa">Sección ${esc(a.sec)}</td>${caja}${caja}${caja}</tr>`).join('')}</tbody>
    </table>
  </div>` : '';
  return `<div class="cierre-bloque">${auto}
  <div class="contacto">
    <div>
      <h3>¿Tienes una duda?</h3>
      <p>Si ya repasaste la sección y algo sigue sin salir, ${CONFIG.contacto}. Para ayudarte más rápido, mándame:</p>
      <ul>
        <li>el nombre de la guía y el número de ejercicio o ejemplo,</li>
        <li>una foto de tu procedimiento, aunque esté incompleto,</li>
        <li>en qué paso te atoraste.</li>
      </ul>
    </div>
    <div class="firma">${esc(CONFIG.marca)}<small>${esc(CONFIG.lugar)}</small></div>
  </div></div>`;
}

// ---------- Fórmulas y numeración ----------

function numerar(cuerpo) {
  // El título de "Ejercicios", su introducción y el primer bloque van juntos en la misma página.
  cuerpo = cuerpo.replace(
    /(<section class="ejercicios[^"]*">\s*)(<h2>[\s\S]*?<\/h2>\s*(?:<p>[\s\S]*?<\/p>\s*)?<div class="bloque-ej">[\s\S]*?<\/div>)/,
    '$1<div class="inicio-ej">$2</div>',
  );
  let n = 0;
  cuerpo = cuerpo.replace(/<h2>/g, () => `<h2><span class="num">${String(++n).padStart(2, '0')}</span>`);
  return { cuerpo, secciones: n };
}

function formulas(html, errores) {
  const tex = (src, display) => {
    if (src.includes('\u0000PESO')) {
      errores.push(`Fórmula: ${src.replace(/\u0000PESO\u0000/g, '\\$')}\n    No escribas \\$ dentro de una fórmula; ponlo en el texto.`);
      return '';
    }
    try {
      return katex.renderToString(src, { displayMode: display, throwOnError: true, strict: 'error' });
    } catch (e) {
      errores.push(`Fórmula: ${src}\n    ${e.message}`);
      return '';
    }
  };
  // \$ fuera de fórmulas es el signo de pesos, no un delimitador.
  html = html.replace(/\\\$/g, '\u0000PESO\u0000');
  html = html.replace(/\$\$([\s\S]+?)\$\$/g, (_, s) => tex(s.trim(), true));
  html = html.replace(/\$([^$\n]+?)\$/g, (_, s) => tex(s, false));
  return html.replace(/\u0000PESO\u0000/g, '$');
}

// ---------- Construcción ----------

function listarContenido(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = path.join(dir, e.name);
    return e.isDirectory() ? listarContenido(p) : e.name.endsWith('.html') ? [p] : [];
  }).sort();
}

async function construir(navegador, archivo) {
  const { meta, cuerpo: crudo } = leerGuia(archivo);
  const errores = [];
  const { cuerpo, secciones } = numerar(crudo);
  for (const a of meta.autoeval) {
    for (const s of a.sec.match(/\d+/g) || []) {
      if (Number(s) < 1 || Number(s) > secciones) errores.push(`Autoevaluación apunta a la sección ${s}, pero la guía tiene ${secciones}`);
    }
  }

  const html = `<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<title>${esc(CONFIG.marca)} · ${esc(meta.titulo)}</title>
<link rel="stylesheet" href="node_modules/katex/dist/katex.min.css">
<link rel="stylesheet" href="plantilla/estilos.css"></head>
<body>${formulas(portada(meta) + cuerpo.replace(/<\/section>\s*$/, `${cierre(meta)}\n</section>`), errores)}</body></html>`;
  if (!/<\/section>\s*$/.test(cuerpo)) errores.push('El contenido debe terminar con </section> (la sección de respuestas).');

  let relativo = path.relative(path.join(RAIZ, 'contenido'), archivo).replace(/\.html$/, '');
  if (relativo.startsWith('..')) relativo = path.basename(relativo); // archivos fuera de contenido/
  const salida = path.join(RAIZ, 'pdf', relativo.split(path.sep).join('-') + '.pdf');
  const tmp = path.join(RAIZ, `.render-${process.pid}.html`);
  fs.writeFileSync(tmp, html);

  const pagina = await navegador.newPage();
  const fallidos = [];
  pagina.on('requestfailed', (r) => fallidos.push(r.url()));
  await pagina.goto('file://' + tmp, { waitUntil: 'networkidle' });
  await pagina.evaluate(() => document.fonts.ready);
  await pagina.emulateMedia({ media: 'print' });
  const revision = await pagina.evaluate(() => {
    const ancho = document.body.getBoundingClientRect().right + 1;
    const bloques = new Set([...document.querySelectorAll('.katex-display, table, svg, img')]);
    const desbordes = [...document.querySelectorAll('.katex, .katex-display, table, .ejemplo, .nota, .definicion, .cuidado, .repaso, svg, img')]
      .filter((el) => el.getBoundingClientRect().right > ancho || (bloques.has(el) && el.scrollWidth > el.clientWidth + 2))
      .map((el) => (el.textContent || el.tagName).trim().slice(0, 60));
    const fuentes = [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family);
    return { desbordes: [...new Set(desbordes)], nunito: fuentes.includes('Nunito') };
  });
  if (fallidos.length) errores.push('Recursos que no cargaron: ' + fallidos.join(', '));
  if (!revision.nunito) errores.push('No cargó la fuente Nunito');
  if (revision.desbordes.length) errores.push('Contenido que se sale del margen: ' + revision.desbordes.join(' | '));

  if (errores.length) {
    await pagina.close();
    fs.rmSync(tmp, { force: true });
    return { archivo, errores };
  }

  fs.mkdirSync(path.dirname(salida), { recursive: true });
  await pagina.pdf({
    path: salida, format: 'Letter', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: `<div style="width:100%;font:8px Helvetica,Arial,sans-serif;color:#5f5448;padding:0 17mm;display:flex;justify-content:space-between;-webkit-print-color-adjust:exact">
      <span style="letter-spacing:.12em;text-transform:uppercase">${esc(CONFIG.marca)} · ${esc(meta.titulo)}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  });
  await pagina.close();
  fs.rmSync(tmp, { force: true });
  return { archivo, salida, errores };
}

// ---------- Manifiesto para la plataforma ----------
// La plataforma lee pdf/manifiesto.json al arrancar y carga descripción y PDF en cada tema.

const slugify = (t) => t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
  .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 80);

function escribirManifiesto() {
  const lista = [];
  for (const archivo of listarContenido(path.join(RAIZ, 'contenido'))) {
    const { meta } = leerGuia(archivo);
    const nombre = path.relative(path.join(RAIZ, 'contenido'), archivo).replace(/\.html$/, '').split(path.sep).join('-') + '.pdf';
    if (!fs.existsSync(path.join(RAIZ, 'pdf', nombre))) continue;
    lista.push({
      tema: meta.tema || `${slugify(meta.nivel)}-${slugify(meta.materia)}-${slugify(meta.titulo)}`,
      titulo: meta.titulo,
      descripcion: meta.descripcion || '',
      pdf: nombre,
    });
  }
  fs.writeFileSync(path.join(RAIZ, 'pdf', 'manifiesto.json'), JSON.stringify(lista, null, 2) + '\n');
  console.log(`Manifiesto: ${lista.length} guías.`);
}

(async () => {
  const archivos = process.argv.slice(2).length
    ? process.argv.slice(2).map((a) => path.resolve(a))
    : listarContenido(path.join(RAIZ, 'contenido'));
  const exe = process.env.CHROMIUM_PATH
    || ['/opt/pw-browsers'].filter(fs.existsSync).flatMap((d) => fs.readdirSync(d).map((s) => `${d}/${s}/chrome-linux/chrome`)).find(fs.existsSync);
  const navegador = await chromium.launch(exe ? { executablePath: exe } : { channel: 'chrome' }); // sin ruta: usa Google Chrome instalado
  let fallas = 0;
  for (const archivo of archivos) {
    const r = await construir(navegador, archivo);
    const nombre = path.relative(RAIZ, archivo);
    if (r.errores.length) {
      fallas++;
      console.error(`✗ ${nombre}\n  - ${r.errores.join('\n  - ')}`);
    } else {
      console.log(`✓ ${nombre} → ${path.relative(RAIZ, r.salida)}`);
    }
  }
  await navegador.close();
  escribirManifiesto();
  console.log(`\n${archivos.length - fallas} de ${archivos.length} guías construidas.`);
  process.exit(fallas ? 1 : 0);
})();
