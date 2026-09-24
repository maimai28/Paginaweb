// Importa las guías PDF del repositorio (guias/pdf/manifiesto.json) a sus temas.
//
// - Pone la descripción del tema si está vacía.
// - Agrega el PDF como primer material del tema.
// - Si el PDF cambió en el repositorio, reemplaza el archivo.
// - Si borraste la guía desde el panel, no la vuelve a subir.
// Se desactiva con IMPORTAR_GUIAS=0.
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const { db, UPLOAD_DIR } = require('./db');

const CARPETA = path.join(__dirname, '..', 'guias', 'pdf');

db.exec(`
CREATE TABLE IF NOT EXISTS guias_importadas (
  archivo TEXT PRIMARY KEY,
  tema_id INTEGER NOT NULL,
  recurso_id INTEGER,
  hash TEXT NOT NULL,
  fecha TEXT NOT NULL DEFAULT (datetime('now'))
);
`);

const hashDe = (ruta) => crypto.createHash('sha256').update(fs.readFileSync(ruta)).digest('hex');

function copiar(ruta) {
  const nombre = `${crypto.randomBytes(16).toString('hex')}.pdf`;
  fs.copyFileSync(ruta, path.join(UPLOAD_DIR, nombre));
  return { nombre, tamano: fs.statSync(ruta).size };
}

function importarGuias() {
  if (process.env.IMPORTAR_GUIAS === '0') return;
  const manifiesto = path.join(CARPETA, 'manifiesto.json');
  if (!fs.existsSync(manifiesto)) return;

  const lista = JSON.parse(fs.readFileSync(manifiesto, 'utf8'));
  const tema = db.prepare('SELECT id, descripcion FROM temas WHERE slug = ?');
  const registro = db.prepare('SELECT * FROM guias_importadas WHERE archivo = ?');
  const recurso = db.prepare('SELECT * FROM recursos WHERE id = ?');
  const resumen = { nuevas: 0, actualizadas: 0, descripciones: 0, sinTema: [] };

  for (const g of lista) {
    const ruta = path.join(CARPETA, path.basename(g.pdf));
    const t = tema.get(g.tema);
    if (!t) { resumen.sinTema.push(g.tema); continue; }
    if (!fs.existsSync(ruta)) continue;

    if (g.descripcion && !String(t.descripcion || '').trim()) {
      db.prepare('UPDATE temas SET descripcion = ? WHERE id = ?').run(g.descripcion, t.id);
      resumen.descripciones++;
    }

    const hash = hashDe(ruta);
    const previo = registro.get(g.pdf);
    if (!previo) {
      const { nombre, tamano } = copiar(ruta);
      const minimo = db.prepare('SELECT COALESCE(MIN(orden), 0) AS o FROM recursos WHERE tema_id = ?').get(t.id).o;
      const id = db.prepare(`INSERT INTO recursos (tema_id, tipo, titulo, archivo, nombre_original, tamano, orden)
        VALUES (?, 'pdf', ?, ?, ?, ?, ?)`).run(t.id, `Guía de estudio: ${g.titulo}`, nombre, g.pdf, tamano, minimo - 1).lastInsertRowid;
      db.prepare('INSERT INTO guias_importadas (archivo, tema_id, recurso_id, hash) VALUES (?, ?, ?, ?)').run(g.pdf, t.id, id, hash);
      resumen.nuevas++;
    } else if (previo.hash !== hash) {
      const r = previo.recurso_id ? recurso.get(previo.recurso_id) : null;
      if (r) {
        const { nombre, tamano } = copiar(ruta);
        fs.rmSync(path.join(UPLOAD_DIR, path.basename(r.archivo)), { force: true });
        db.prepare('UPDATE recursos SET archivo = ?, tamano = ? WHERE id = ?').run(nombre, tamano, r.id);
        resumen.actualizadas++;
      }
      db.prepare("UPDATE guias_importadas SET hash = ?, fecha = datetime('now') WHERE archivo = ?").run(hash, g.pdf);
    }
  }

  if (resumen.nuevas || resumen.actualizadas || resumen.descripciones) {
    console.log(`Guías: ${resumen.nuevas} nuevas, ${resumen.actualizadas} actualizadas, ${resumen.descripciones} descripciones.`);
  }
  if (resumen.sinTema.length) console.warn('Guías sin tema correspondiente:', resumen.sinTema.join(', '));
}

module.exports = { importarGuias };
