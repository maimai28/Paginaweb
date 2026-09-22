const crypto = require('node:crypto');
const { db } = require('./db');

const COOKIE = 'sesion';
const DURACION_MS = 1000 * 60 * 60 * 24 * 14; // 14 días

function hashPassword(password) {
  const salt = crypto.randomBytes(16);
  const hash = crypto.scryptSync(password, salt, 64);
  return `scrypt$${salt.toString('hex')}$${hash.toString('hex')}`;
}

function verificarPassword(password, guardado) {
  const [alg, saltHex, hashHex] = String(guardado).split('$');
  if (alg !== 'scrypt' || !saltHex || !hashHex) return false;
  const esperado = Buffer.from(hashHex, 'hex');
  const hash = crypto.scryptSync(password, Buffer.from(saltHex, 'hex'), esperado.length);
  return crypto.timingSafeEqual(hash, esperado);
}

function compararSeguro(a, b) {
  const ha = crypto.createHash('sha256').update(String(a)).digest();
  const hb = crypto.createHash('sha256').update(String(b)).digest();
  return crypto.timingSafeEqual(ha, hb);
}

// Contraseña legible para dictar o mandar por WhatsApp: evita caracteres confusos (0/O, 1/l/I).
function generarPassword() {
  const letras = 'abcdefghjkmnpqrstuvwxyz';
  const digitos = '23456789';
  const bloque = (n, abc) => Array.from({ length: n }, () => abc[crypto.randomInt(abc.length)]).join('');
  return `${bloque(4, letras)}-${bloque(4, digitos)}-${bloque(4, letras)}`;
}

const hashToken = (t) => crypto.createHash('sha256').update(t).digest('hex');

function crearSesion(res, req, { alumnoId = null, esAdmin = false }) {
  const token = crypto.randomBytes(32).toString('base64url');
  // Un alumno solo puede tener una sesión abierta: si comparte su contraseña, la otra persona lo saca.
  if (alumnoId) db.prepare('DELETE FROM sesiones WHERE alumno_id = ?').run(alumnoId);
  db.prepare('INSERT INTO sesiones (token_hash, alumno_id, es_admin, expira) VALUES (?, ?, ?, ?)')
    .run(hashToken(token), alumnoId, esAdmin ? 1 : 0, Date.now() + DURACION_MS);
  res.cookie(COOKIE, token, {
    httpOnly: true, sameSite: 'lax', secure: req.secure, maxAge: DURACION_MS, path: '/',
  });
}

function cerrarSesion(req, res) {
  const token = leerCookie(req, COOKIE);
  if (token) db.prepare('DELETE FROM sesiones WHERE token_hash = ?').run(hashToken(token));
  res.clearCookie(COOKIE, { path: '/' });
}

function leerCookie(req, nombre) {
  const header = req.headers.cookie || '';
  for (const parte of header.split(';')) {
    const i = parte.indexOf('=');
    if (i > -1 && parte.slice(0, i).trim() === nombre) {
      try { return decodeURIComponent(parte.slice(i + 1).trim()); } catch { return null; }
    }
  }
  return null;
}

function alumnoVigente(alumno) {
  if (!alumno || alumno.estado !== 'activo') return false;
  if (alumno.expira && new Date(`${alumno.expira}T23:59:59`) < new Date()) return false;
  return true;
}

// Carga la sesión actual en req.usuario = { esAdmin, alumno }
function cargarSesion(req, res, next) {
  req.usuario = null;
  const token = leerCookie(req, COOKIE);
  if (token) {
    const s = db.prepare('SELECT * FROM sesiones WHERE token_hash = ?').get(hashToken(token));
    if (s && s.expira > Date.now()) {
      if (s.es_admin) {
        req.usuario = { esAdmin: true, alumno: null };
      } else {
        const alumno = db.prepare('SELECT * FROM alumnos WHERE id = ?').get(s.alumno_id);
        if (alumnoVigente(alumno)) req.usuario = { esAdmin: false, alumno };
      }
    }
    if (!req.usuario) res.clearCookie(COOKIE, { path: '/' });
  }
  res.locals.usuario = req.usuario;
  next();
}

function requiereAlumno(req, res, next) {
  if (req.usuario) return next();
  res.redirect(`/login?volver=${encodeURIComponent(req.originalUrl)}`);
}

function requiereAdmin(req, res, next) {
  if (req.usuario?.esAdmin) return next();
  res.redirect('/admin/login');
}

// Protección CSRF: todo POST debe venir de este mismo sitio.
function mismoOrigen(req, res, next) {
  if (req.method !== 'POST') return next();
  const origen = req.headers.origin || req.headers.referer;
  if (!origen) return next();
  try {
    if (new URL(origen).host === req.headers.host) return next();
  } catch { /* cae al rechazo */ }
  res.status(403).send('Solicitud rechazada.');
}

// Límite simple de intentos por IP: solo cuentan los que la ruta marca con req.registrarIntento().
const intentos = new Map();
function limiteIntentos(max = 10, ventanaMs = 15 * 60 * 1000) {
  return (req, res, next) => {
    const ahora = Date.now();
    const clave = `${req.baseUrl}${req.path}|${req.ip}`;
    let reg = intentos.get(clave);
    if (reg && reg.reinicio < ahora) { intentos.delete(clave); reg = null; }
    if (reg && reg.n >= max) {
      return res.status(429).send('Demasiados intentos. Espera un rato e inténtalo de nuevo.');
    }
    req.registrarIntento = () => {
      const r = intentos.get(clave) || { n: 0, reinicio: ahora + ventanaMs };
      r.n++;
      intentos.set(clave, r);
    };
    next();
  };
}
setInterval(() => {
  const ahora = Date.now();
  for (const [k, v] of intentos) if (v.reinicio < ahora) intentos.delete(k);
  db.prepare('DELETE FROM sesiones WHERE expira < ?').run(ahora);
}, 60 * 60 * 1000).unref();

module.exports = {
  hashPassword, verificarPassword, compararSeguro, generarPassword,
  crearSesion, cerrarSesion, cargarSesion, requiereAlumno, requiereAdmin,
  mismoOrigen, limiteIntentos, alumnoVigente,
};
