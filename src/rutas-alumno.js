const path = require('node:path');
const fs = require('node:fs');
const express = require('express');
const { db, UPLOAD_DIR } = require('./db');
const { html, layout, aviso } = require('./html');
const auth = require('./auth');

const router = express.Router();

const MENSAJES = {
  enviado: ['ok', 'Solicitud enviada. En cuanto confirme tu pago te activo el acceso y podrás entrar con tu correo y contraseña.'],
  salir: ['ok', 'Sesión cerrada.'],
  credenciales: ['error', 'Correo o contraseña incorrectos.'],
  pendiente: ['info', 'Tu solicitud todavía no ha sido autorizada. Te aviso cuando esté lista.'],
  revocado: ['error', 'Tu acceso está desactivado. Escríbeme si crees que es un error.'],
  vencido: ['error', 'Tu periodo de acceso terminó. Escríbeme para renovarlo.'],
  existe: ['error', 'Ya existe una cuenta o solicitud con ese correo.'],
  datos: ['error', 'Revisa los datos: nombre, correo válido y contraseña de al menos 8 caracteres que coincida en ambos campos.'],
};
const mensaje = (clave) => (MENSAJES[clave] ? aviso(...MENSAJES[clave]) : '');

const volverSeguro = (v) => (typeof v === 'string' && /^\/(?![/\\])/.test(v) ? v : '/cursos');
const correoValido = (c) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(c) && c.length <= 200;

router.get('/', (req, res) => res.redirect(req.usuario ? (req.usuario.esAdmin ? '/admin' : '/cursos') : '/login'));

router.get('/login', (req, res) => {
  if (req.usuario) return res.redirect('/cursos');
  res.send(layout({
    titulo: 'Entrar',
    cuerpo: html`
      <section class="tarjeta angosta">
        <h1>Entrar a los cursos</h1>
        <p class="sub">Matemáticas, cálculo y física de secundaria, preparatoria y universidad.</p>
        ${mensaje(req.query.m)}
        <form method="post" action="/login" class="formulario">
          <input type="hidden" name="volver" value="${volverSeguro(req.query.volver)}">
          <label>Correo <input type="email" name="correo" required autocomplete="username"></label>
          <label>Contraseña <input type="password" name="password" required autocomplete="current-password"></label>
          <button class="boton">Entrar</button>
        </form>
        <p class="nota">¿Compraste una tutoría y aún no tienes acceso? <a href="/solicitar">Solicita tu acceso aquí</a>.</p>
      </section>`,
  }));
});

router.post('/login', auth.limiteIntentos(), (req, res) => {
  const correo = String(req.body.correo || '').trim().toLowerCase();
  const password = String(req.body.password || '');
  const alumno = db.prepare('SELECT * FROM alumnos WHERE correo = ?').get(correo);
  const volver = encodeURIComponent(volverSeguro(req.body.volver));
  if (!alumno || !auth.verificarPassword(password, alumno.pass_hash)) {
    req.registrarIntento();
    return res.redirect(`/login?m=credenciales&volver=${volver}`);
  }
  if (alumno.estado === 'pendiente') return res.redirect('/login?m=pendiente');
  if (alumno.estado === 'revocado') return res.redirect('/login?m=revocado');
  if (!auth.alumnoVigente(alumno)) return res.redirect('/login?m=vencido');
  auth.crearSesion(res, req, { alumnoId: alumno.id });
  db.prepare("UPDATE alumnos SET ultimo_acceso = datetime('now') WHERE id = ?").run(alumno.id);
  res.redirect(volverSeguro(req.body.volver));
});

router.post('/logout', (req, res) => {
  auth.cerrarSesion(req, res);
  res.redirect('/login?m=salir');
});

router.get('/solicitar', (req, res) => {
  res.send(layout({
    titulo: 'Solicitar acceso',
    cuerpo: html`
      <section class="tarjeta angosta">
        <h1>Solicitar acceso</h1>
        <p class="sub">Crea tu contraseña personal. No podrás entrar hasta que yo autorice tu cuenta después de confirmar tu compra.</p>
        ${mensaje(req.query.m)}
        <form method="post" action="/solicitar" class="formulario">
          <label>Nombre completo <input name="nombre" required maxlength="100" autocomplete="name"></label>
          <label>Correo <input type="email" name="correo" required maxlength="200" autocomplete="email"></label>
          <label>Contraseña (mínimo 8 caracteres) <input type="password" name="password" required minlength="8" autocomplete="new-password"></label>
          <label>Repite la contraseña <input type="password" name="password2" required minlength="8" autocomplete="new-password"></label>
          <label>¿Qué tutoría compraste? <textarea name="nota" maxlength="500" rows="3" placeholder="Ej. Paquete de 4 clases de cálculo diferencial, pagado el 20 de septiembre"></textarea></label>
          <button class="boton">Enviar solicitud</button>
        </form>
        <p class="nota">¿Ya tienes acceso? <a href="/login">Entra aquí</a>.</p>
      </section>`,
  }));
});

router.post('/solicitar', auth.limiteIntentos(5, 60 * 60 * 1000), (req, res) => {
  const nombre = String(req.body.nombre || '').trim().slice(0, 100);
  const correo = String(req.body.correo || '').trim().toLowerCase();
  const password = String(req.body.password || '');
  const nota = String(req.body.nota || '').trim().slice(0, 500);
  if (!nombre || !correoValido(correo) || password.length < 8 || password.length > 200 || password !== req.body.password2) {
    return res.redirect('/solicitar?m=datos');
  }
  if (db.prepare('SELECT 1 FROM alumnos WHERE correo = ?').get(correo)) return res.redirect('/solicitar?m=existe');
  db.prepare("INSERT INTO alumnos (nombre, correo, pass_hash, estado, nota) VALUES (?, ?, ?, 'pendiente', ?)")
    .run(nombre, correo, auth.hashPassword(password), nota);
  req.registrarIntento();
  res.redirect('/login?m=enviado');
});

// ---------- Contenido protegido ----------

router.get('/cursos', auth.requiereAlumno, (req, res) => {
  const niveles = db.prepare(`
    SELECT n.*,
      (SELECT COUNT(*) FROM temas t JOIN ramas r ON r.id = t.rama_id JOIN areas a ON a.id = r.area_id WHERE a.nivel_id = n.id) AS temas,
      (SELECT COUNT(*) FROM recursos x JOIN temas t ON t.id = x.tema_id JOIN ramas r ON r.id = t.rama_id JOIN areas a ON a.id = r.area_id WHERE a.nivel_id = n.id) AS recursos
    FROM niveles n ORDER BY n.orden`).all();
  const areas = db.prepare('SELECT * FROM areas ORDER BY orden').all();
  res.send(layout({
    titulo: 'Cursos',
    usuario: req.usuario,
    cuerpo: html`
      <h1>Cursos</h1>
      <p class="sub">Elige tu nivel. Cada tema se abre en su propia pestaña con videos, PDF descargables y enlaces.</p>
      <div class="rejilla">
        ${niveles.map((n) => html`
          <a class="tarjeta nivel" href="/cursos/${n.slug}">
            <h2>${n.nombre}</h2>
            <p>${n.descripcion}</p>
            <p class="chips">${areas.filter((a) => a.nivel_id === n.id).map((a) => html`<span class="chip">${a.nombre}</span>`)}</p>
            <p class="meta">${n.temas} temas · ${n.recursos} materiales</p>
          </a>`)}
      </div>`,
  }));
});

router.get('/cursos/:nivel', auth.requiereAlumno, (req, res, next) => {
  const nivel = db.prepare('SELECT * FROM niveles WHERE slug = ?').get(req.params.nivel);
  if (!nivel) return next();
  const areas = db.prepare('SELECT * FROM areas WHERE nivel_id = ? ORDER BY orden').all(nivel.id);
  const ramas = db.prepare('SELECT r.* FROM ramas r JOIN areas a ON a.id = r.area_id WHERE a.nivel_id = ? ORDER BY r.orden').all(nivel.id);
  const temas = db.prepare(`
    SELECT t.*, (SELECT COUNT(*) FROM recursos x WHERE x.tema_id = t.id) AS recursos
    FROM temas t JOIN ramas r ON r.id = t.rama_id JOIN areas a ON a.id = r.area_id
    WHERE a.nivel_id = ? ORDER BY t.orden, t.id`).all(nivel.id);
  res.send(layout({
    titulo: nivel.nombre,
    usuario: req.usuario,
    cuerpo: html`
      <p class="migas"><a href="/cursos">Cursos</a> › ${nivel.nombre}</p>
      <h1>${nivel.nombre}</h1>
      <input type="search" class="buscador" placeholder="Buscar tema…" data-filtro aria-label="Buscar tema">
      ${areas.map((a) => html`
        <section class="area">
          <h2>${a.nombre}</h2>
          <div class="rejilla ramas">
            ${ramas.filter((r) => r.area_id === a.id).map((r) => html`
              <div class="tarjeta rama" data-rama>
                <h3>${r.nombre}</h3>
                <ol class="temas">
                  ${temas.filter((t) => t.rama_id === r.id).map((t) => html`
                    <li data-tema="${t.titulo.toLowerCase()}">
                      <a href="/tema/${t.slug}" target="_blank" rel="noopener">${t.titulo}</a>
                      ${t.recursos ? html`<span class="contador" title="Materiales">${t.recursos}</span>` : html`<span class="contador vacio" title="Aún sin material">—</span>`}
                    </li>`)}
                </ol>
              </div>`)}
          </div>
        </section>`)}`,
  }));
});

function idYoutube(url) {
  const m = String(url).match(/(?:youtu\.be\/|[?&]v=|\/embed\/|\/shorts\/|\/live\/)([\w-]{11})/) || String(url).match(/^([\w-]{11})$/);
  return m ? m[1] : null;
}

function tamanoLegible(bytes) {
  if (!bytes) return '';
  return bytes > 1024 * 1024 ? `${(bytes / 1024 / 1024).toFixed(1)} MB` : `${Math.ceil(bytes / 1024)} KB`;
}

router.get('/tema/:slug', auth.requiereAlumno, (req, res, next) => {
  const tema = db.prepare(`
    SELECT t.*, r.nombre AS rama, a.nombre AS area, n.nombre AS nivel, n.slug AS nivel_slug
    FROM temas t JOIN ramas r ON r.id = t.rama_id JOIN areas a ON a.id = r.area_id JOIN niveles n ON n.id = a.nivel_id
    WHERE t.slug = ?`).get(req.params.slug);
  if (!tema) return next();
  const recursos = db.prepare('SELECT * FROM recursos WHERE tema_id = ? ORDER BY orden, id').all(tema.id);
  const videos = recursos.filter((r) => r.tipo === 'youtube');
  const pdfs = recursos.filter((r) => r.tipo === 'pdf');
  const enlaces = recursos.filter((r) => r.tipo === 'enlace');

  res.send(layout({
    titulo: tema.titulo,
    usuario: req.usuario,
    cuerpo: html`
      <p class="migas"><a href="/cursos">Cursos</a> › <a href="/cursos/${tema.nivel_slug}">${tema.nivel}</a> › ${tema.area} › ${tema.rama}</p>
      <h1>${tema.titulo}</h1>
      ${tema.descripcion ? html`<p class="sub">${tema.descripcion}</p>` : ''}
      ${req.usuario.esAdmin ? html`<p><a class="boton secundario" href="/admin/tema/${tema.id}">Editar material de este tema</a></p>` : ''}
      ${!recursos.length ? html`<p class="aviso info">Todavía no hay material en este tema. Pronto lo subiré.</p>` : ''}

      ${videos.length ? html`
        <section class="bloque">
          <h2>Videos</h2>
          <div class="rejilla videos">
            ${videos.map((v) => {
              const id = idYoutube(v.url);
              return id ? html`
                <figure class="video">
                  <button class="yt" data-yt="${id}" aria-label="Reproducir ${v.titulo}">
                    <img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">
                    <span class="play">▶</span>
                  </button>
                  <figcaption>${v.titulo}</figcaption>
                </figure>` : '';
            })}
          </div>
        </section>` : ''}

      ${pdfs.length ? html`
        <section class="bloque">
          <h2>Documentos PDF</h2>
          ${pdfs.map((p) => html`
            <div class="pdf tarjeta">
              <div class="pdf-cabecera">
                <div><strong>📄 ${p.titulo}</strong> <span class="meta">${tamanoLegible(p.tamano)}</span></div>
                <div class="acciones">
                  <button class="boton secundario" data-pdf="/archivos/${p.id}">Ver aquí</button>
                  <a class="boton secundario" href="/archivos/${p.id}" target="_blank" rel="noopener">Abrir en pestaña</a>
                  <a class="boton" href="/archivos/${p.id}/descargar">Descargar</a>
                </div>
              </div>
              <div class="visor" hidden></div>
            </div>`)}
        </section>` : ''}

      ${enlaces.length ? html`
        <section class="bloque">
          <h2>Enlaces</h2>
          <ul class="enlaces">
            ${enlaces.map((e) => html`<li><a href="${e.url}" target="_blank" rel="noopener noreferrer">🔗 ${e.titulo}</a> <span class="meta">${hostDe(e.url)}</span></li>`)}
          </ul>
        </section>` : ''}`,
  }));
});

function hostDe(url) {
  try { return new URL(url).hostname.replace(/^www\./, ''); } catch { return ''; }
}

function enviarPdf(req, res, next, descargar) {
  const r = db.prepare("SELECT * FROM recursos WHERE id = ? AND tipo = 'pdf'").get(Number(req.params.id));
  if (!r) return next();
  const ruta = path.join(UPLOAD_DIR, path.basename(r.archivo));
  if (!fs.existsSync(ruta)) return next();
  const nombre = (r.nombre_original || `${r.titulo}.pdf`).replace(/["\\\r\n]/g, '');
  res.removeHeader('Content-Security-Policy'); // algunos visores de PDF del navegador fallan con CSP
  res.setHeader('Content-Type', 'application/pdf');
  res.setHeader('Cache-Control', 'private, max-age=3600');
  res.setHeader('Content-Disposition', `${descargar ? 'attachment' : 'inline'}; filename*=UTF-8''${encodeURIComponent(nombre)}`);
  res.sendFile(ruta, { headers: { 'Content-Type': 'application/pdf' } });
}

router.get('/archivos/:id', auth.requiereAlumno, (req, res, next) => enviarPdf(req, res, next, false));
router.get('/archivos/:id/descargar', auth.requiereAlumno, (req, res, next) => enviarPdf(req, res, next, true));

module.exports = { router, idYoutube };
