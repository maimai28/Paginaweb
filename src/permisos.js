const { db } = require('./db');
const { html } = require('./html');

// Todas las áreas con su nivel, en el orden del temario.
function listaAreas() {
  return db.prepare(`SELECT a.id, a.nombre, n.id AS nivel_id, n.nombre AS nivel FROM areas a
    JOIN niveles n ON n.id = a.nivel_id ORDER BY n.orden, a.orden`).all();
}

function areasDe(alumnoId) {
  return new Set(db.prepare('SELECT area_id FROM permisos WHERE alumno_id = ?').all(alumnoId).map((p) => p.area_id));
}

// Lee las casillas marcadas de un formulario (name="areas") y descarta ids que no existan.
function idsDelFormulario(body) {
  const validos = new Set(listaAreas().map((a) => a.id));
  return [...new Set([].concat(body.areas ?? []).map(Number))].filter((id) => validos.has(id));
}

function guardar(alumnoId, ids) {
  db.exec('BEGIN');
  try {
    db.prepare('DELETE FROM permisos WHERE alumno_id = ?').run(alumnoId);
    const ins = db.prepare('INSERT INTO permisos (alumno_id, area_id) VALUES (?, ?)');
    ids.forEach((id) => ins.run(alumnoId, id));
    db.exec('COMMIT');
  } catch (err) {
    db.exec('ROLLBACK');
    throw err;
  }
}

// Casillas agrupadas por nivel: Secundaria [ ] Matemáticas [ ] Física, etc.
function casillas(marcadas = new Set()) {
  const areas = listaAreas();
  const niveles = [...new Map(areas.map((a) => [a.nivel_id, a.nivel])).entries()];
  return html`
    <div class="casillas">
      ${niveles.map(([nivelId, nivel]) => html`
        <fieldset>
          <legend>${nivel}</legend>
          ${areas.filter((a) => a.nivel_id === nivelId).map((a) => html`
            <label class="casilla"><input type="checkbox" name="areas" value="${a.id}" ${marcadas.has(a.id) ? 'checked' : ''}> ${a.nombre}</label>`)}
        </fieldset>`)}
    </div>`;
}

function resumen(marcadas) {
  const areas = listaAreas().filter((a) => marcadas.has(a.id));
  if (!areas.length) return html`<span class="etiqueta error">Sin áreas</span>`;
  if (areas.length === listaAreas().length) return html`<span class="chip">Todo</span>`;
  return areas.map((a) => html`<span class="chip">${a.nivel} · ${a.nombre}</span> `);
}

module.exports = { listaAreas, areasDe, idsDelFormulario, guardar, casillas, resumen };
