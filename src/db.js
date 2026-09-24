const fs = require('node:fs');
const path = require('node:path');
const { DatabaseSync } = require('node:sqlite');
const catalogo = require('./catalogo');

// En Railway se usa el volumen montado automáticamente (RAILWAY_VOLUME_MOUNT_PATH).
const DATA_DIR = path.resolve(
  process.env.DATA_DIR || process.env.RAILWAY_VOLUME_MOUNT_PATH || path.join(__dirname, '..', 'data'),
);
const UPLOAD_DIR = path.join(DATA_DIR, 'archivos');
fs.mkdirSync(UPLOAD_DIR, { recursive: true });

const db = new DatabaseSync(path.join(DATA_DIR, 'cursos.db'));
db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON;');

db.exec(`
CREATE TABLE IF NOT EXISTS alumnos (
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL,
  correo TEXT NOT NULL UNIQUE,
  pass_hash TEXT NOT NULL,
  estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente','activo','revocado')),
  nota TEXT NOT NULL DEFAULT '',
  expira TEXT,
  creado TEXT NOT NULL DEFAULT (datetime('now')),
  ultimo_acceso TEXT
);
CREATE TABLE IF NOT EXISTS sesiones (
  token_hash TEXT PRIMARY KEY,
  alumno_id INTEGER REFERENCES alumnos(id) ON DELETE CASCADE,
  es_admin INTEGER NOT NULL DEFAULT 0,
  expira INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS niveles (
  id INTEGER PRIMARY KEY, slug TEXT NOT NULL UNIQUE, nombre TEXT NOT NULL,
  descripcion TEXT NOT NULL DEFAULT '', orden INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS areas (
  id INTEGER PRIMARY KEY, nivel_id INTEGER NOT NULL REFERENCES niveles(id) ON DELETE CASCADE,
  slug TEXT NOT NULL, nombre TEXT NOT NULL, orden INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS ramas (
  id INTEGER PRIMARY KEY, area_id INTEGER NOT NULL REFERENCES areas(id) ON DELETE CASCADE,
  nombre TEXT NOT NULL, orden INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS temas (
  id INTEGER PRIMARY KEY, rama_id INTEGER NOT NULL REFERENCES ramas(id) ON DELETE CASCADE,
  slug TEXT NOT NULL UNIQUE, titulo TEXT NOT NULL, descripcion TEXT NOT NULL DEFAULT '',
  orden INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS recursos (
  id INTEGER PRIMARY KEY, tema_id INTEGER NOT NULL REFERENCES temas(id) ON DELETE CASCADE,
  tipo TEXT NOT NULL CHECK (tipo IN ('enlace','youtube','pdf')),
  titulo TEXT NOT NULL, url TEXT, archivo TEXT, nombre_original TEXT, tamano INTEGER,
  orden INTEGER NOT NULL DEFAULT 0, creado TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_temas_rama ON temas(rama_id);
CREATE INDEX IF NOT EXISTS idx_recursos_tema ON recursos(tema_id);
CREATE INDEX IF NOT EXISTS idx_sesiones_alumno ON sesiones(alumno_id);
`);

function slugify(texto) {
  return texto
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
    .slice(0, 80) || 'tema';
}

function slugUnico(base) {
  let slug = base;
  for (let i = 2; db.prepare('SELECT 1 FROM temas WHERE slug = ?').get(slug); i++) slug = `${base}-${i}`;
  return slug;
}

function sembrarCatalogo() {
  if (db.prepare('SELECT COUNT(*) AS n FROM niveles').get().n > 0) return;
  const insNivel = db.prepare('INSERT INTO niveles (slug, nombre, descripcion, orden) VALUES (?, ?, ?, ?)');
  const insArea = db.prepare('INSERT INTO areas (nivel_id, slug, nombre, orden) VALUES (?, ?, ?, ?)');
  const insRama = db.prepare('INSERT INTO ramas (area_id, nombre, orden) VALUES (?, ?, ?)');
  const insTema = db.prepare('INSERT INTO temas (rama_id, slug, titulo, orden) VALUES (?, ?, ?, ?)');
  db.exec('BEGIN');
  try {
    catalogo.forEach((nivel, i) => {
      const nivelId = insNivel.run(nivel.slug, nivel.nombre, nivel.descripcion, i).lastInsertRowid;
      nivel.areas.forEach((area, j) => {
        const areaId = insArea.run(nivelId, area.slug, area.nombre, j).lastInsertRowid;
        area.ramas.forEach((rama, k) => {
          const ramaId = insRama.run(areaId, rama.nombre, k).lastInsertRowid;
          rama.temas.forEach((titulo, l) => {
            insTema.run(ramaId, slugUnico(`${nivel.slug}-${area.slug}-${slugify(titulo)}`), titulo, l);
          });
        });
      });
    });
    db.exec('COMMIT');
  } catch (err) {
    db.exec('ROLLBACK');
    throw err;
  }
}

sembrarCatalogo();

module.exports = { db, DATA_DIR, UPLOAD_DIR, slugify, slugUnico };
