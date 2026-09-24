const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const express = require('express');
const multer = require('multer');
const { db, UPLOAD_DIR, slugify, slugUnico } = require('./db');
const { html, layout, aviso } = require('./html');
const auth = require('./auth');
const permisos = require('./permisos');
const { idYoutube } = require('./rutas-alumno');

const router = express.Router();
const MAX_PDF_MB = Number(process.env.MAX_PDF_MB) || 50;

const subida = multer({
  storage: multer.diskStorage({
    destination: UPLOAD_DIR,
    filename: (req, file, cb) => cb(null, `${crypto.randomBytes(16).toString('hex')}.pdf`),
  }),
  limits: { fileSize: MAX_PDF_MB * 1024 * 1024, files: 1 },
  fileFilter: (req, file, cb) => cb(null, file.mimetype === 'application/pdf' || /\.pdf$/i.test(file.originalname)),
});

const pagina = (req, titulo, cuerpo) => layout({ titulo, usuario: req.usuario, cuerpo, admin: true });
const fechaValida = (f) => (/^\d{4}-\d{2}-\d{2}$/.test(f || '') ? f : null);
const urlValida = (u) => { try { return ['http:', 'https:'].includes(new URL(u).protocol); } catch { return false; } };

// ---------- Acceso de administrador ----------

router.get('/login', (req, res) => {
  if (req.usuario?.esAdmin) return res.redirect('/admin');
  const sinPassword = !process.env.ADMIN_PASSWORD;
  res.send(layout({
    titulo: 'Administración',
    cuerpo: html`
      <section class="tarjeta angosta">
        <h1>Panel de administración</h1>
        ${sinPassword ? aviso('error', 'Falta configurar la variable ADMIN_PASSWORD en el servidor. El panel está deshabilitado hasta entonces.') : ''}
        ${req.query.m === 'error' ? aviso('error', 'Contraseña incorrecta.') : ''}
        <form method="post" action="/admin/login" class="formulario">
          <label>Contraseña de administrador <input type="password" name="password" required autocomplete="current-password"></label>
          <button class="boton" ${sinPassword ? 'disabled' : ''}>Entrar</button>
        </form>
      </section>`,
  }));
});

router.post('/login', auth.limiteIntentos(5), (req, res) => {
  const esperado = process.env.ADMIN_PASSWORD;
  if (!esperado || !auth.compararSeguro(String(req.body.password || ''), esperado)) {
    req.registrarIntento();
    return res.redirect('/admin/login?m=error');
  }
  auth.crearSesion(res, req, { esAdmin: true });
  res.redirect('/admin');
});

router.post('/logout', (req, res) => {
  auth.cerrarSesion(req, res);
  res.redirect('/admin/login');
});

router.use(auth.requiereAdmin);

// ---------- Alumnos ----------

function filaAlumno(a, areas) {
  const vencido = a.estado === 'activo' && !auth.alumnoVigente(a);
  return html`
    <tr>
      <td><strong>${a.nombre}</strong><br><span class="meta">${a.correo}</span>
        ${a.nota ? html`<br><span class="nota-alumno">“${a.nota}”</span>` : ''}</td>
      <td class="meta">Alta: ${a.creado.slice(0, 10)}<br>Último acceso: ${a.ultimo_acceso ? a.ultimo_acceso.slice(0, 16) : 'nunca'}</td>
      <td>
        <div class="chips">${permisos.resumen(areas)}</div>
        <details class="editar-permisos" ${a.estado === 'pendiente' ? 'open' : ''}>
          <summary>Editar materias</summary>
          <form method="post" action="/admin/alumnos/${a.id}/permisos">
            ${permisos.casillas(areas)}
            <div class="acciones">
              <button class="boton mini secundario">Guardar materias</button>
              ${a.estado === 'pendiente' ? html`<button class="boton mini" name="autorizar" value="1">Guardar y autorizar</button>` : ''}
            </div>
          </form>
        </details>
      </td>
      <td>
        <form method="post" action="/admin/alumnos/${a.id}/vigencia" class="en-linea">
          <input type="date" name="expira" value="${a.expira || ''}" aria-label="Acceso hasta">
          <button class="boton mini secundario">Guardar</button>
        </form>
        ${vencido ? html`<span class="etiqueta error">Vencido</span>` : ''}
      </td>
      <td><div class="acciones">
        ${a.estado === 'pendiente' ? html`
          <form method="post" action="/admin/alumnos/${a.id}/estado"><input type="hidden" name="estado" value="activo"><button class="boton mini">Autorizar</button></form>
          <form method="post" action="/admin/alumnos/${a.id}/eliminar" data-confirmar="¿Rechazar y borrar la solicitud de ${a.nombre}?"><button class="boton mini peligro">Rechazar</button></form>` : ''}
        ${a.estado === 'activo' ? html`
          <form method="post" action="/admin/alumnos/${a.id}/password" data-confirmar="¿Generar una contraseña nueva para ${a.nombre}? La anterior dejará de funcionar."><button class="boton mini secundario">Nueva contraseña</button></form>
          <form method="post" action="/admin/alumnos/${a.id}/estado"><input type="hidden" name="estado" value="revocado"><button class="boton mini peligro">Revocar</button></form>` : ''}
        ${a.estado === 'revocado' ? html`
          <form method="post" action="/admin/alumnos/${a.id}/estado"><input type="hidden" name="estado" value="activo"><button class="boton mini">Reactivar</button></form>
          <form method="post" action="/admin/alumnos/${a.id}/eliminar" data-confirmar="¿Borrar definitivamente a ${a.nombre}?"><button class="boton mini peligro">Eliminar</button></form>` : ''}
      </div></td>
    </tr>`;
}

function tablaAlumnos(titulo, lista, vacio, areasPorAlumno) {
  return html`
    <section class="bloque">
      <h2>${titulo} <span class="contador">${lista.length}</span></h2>
      ${lista.length ? html`
        <div class="tabla-scroll"><table class="tabla">
          <thead><tr><th>Alumno</th><th>Actividad</th><th>Materias</th><th>Acceso hasta</th><th>Acciones</th></tr></thead>
          <tbody>${lista.map((a) => filaAlumno(a, areasPorAlumno.get(a.id) || new Set()))}</tbody>
        </table></div>` : html`<p class="meta">${vacio}</p>`}
    </section>`;
}

router.get('/', (req, res) => {
  const alumnos = db.prepare('SELECT * FROM alumnos ORDER BY creado DESC').all();
  const de = (estado) => alumnos.filter((a) => a.estado === estado);
  const areasPorAlumno = new Map();
  for (const p of db.prepare('SELECT alumno_id, area_id FROM permisos').all()) {
    if (!areasPorAlumno.has(p.alumno_id)) areasPorAlumno.set(p.alumno_id, new Set());
    areasPorAlumno.get(p.alumno_id).add(p.area_id);
  }
  const avisos = {
    areas: aviso('error', 'Marca al menos una materia para el alumno.'),
    existe: aviso('error', 'Ya existe un alumno con ese correo.'),
    datos: aviso('error', 'Nombre y correo válido son obligatorios.'),
    ok: aviso('ok', 'Cambios guardados.'),
  };
  res.send(pagina(req, 'Alumnos', html`
    <h1>Alumnos</h1>
    ${avisos[req.query.m] || ''}
    <section class="tarjeta">
      <h2>Dar de alta a un alumno</h2>
      <p class="meta">Se genera una contraseña única para esa persona. Solo se muestra una vez: cópiala y mándasela.</p>
      <form method="post" action="/admin/alumnos" class="formulario">
        <div class="formulario fila">
          <label>Nombre <input name="nombre" required maxlength="100"></label>
          <label>Correo <input type="email" name="correo" required maxlength="200"></label>
          <label>Acceso hasta (opcional) <input type="date" name="expira"></label>
          <label>Nota (opcional) <input name="nota" maxlength="500" placeholder="Ej. 4 clases de física"></label>
        </div>
        <p class="etiqueta-campo">Materias a las que tendrá acceso</p>
        ${permisos.casillas()}
        <div><button class="boton">Crear alumno</button></div>
      </form>
    </section>
    ${tablaAlumnos('Solicitudes pendientes de autorizar', de('pendiente'), 'No hay solicitudes pendientes.', areasPorAlumno)}
    ${tablaAlumnos('Alumnos con acceso', de('activo'), 'Aún no hay alumnos activos.', areasPorAlumno)}
    ${tablaAlumnos('Acceso revocado', de('revocado'), 'Ninguno.', areasPorAlumno)}
  `));
});

function mostrarCredenciales(req, res, alumno, password) {
  const url = `${req.protocol}://${req.get('host')}/login`;
  const texto = `Hola ${alumno.nombre}, este es tu acceso a los cursos de El Lab del Desierto:\n${url}\nCorreo: ${alumno.correo}\nContraseña: ${password}\nEs personal, no la compartas: si alguien más entra con ella, tu sesión se cierra.`;
  res.send(pagina(req, 'Credenciales', html`
    <section class="tarjeta angosta">
      <h1>Acceso listo</h1>
      ${aviso('info', 'Esta contraseña solo se muestra ahora. Cópiala antes de salir de esta página.')}
      <dl class="credenciales">
        <dt>Alumno</dt><dd>${alumno.nombre}</dd>
        <dt>Correo</dt><dd>${alumno.correo}</dd>
        <dt>Contraseña</dt><dd><code class="grande">${password}</code></dd>
      </dl>
      <label>Mensaje para enviar
        <textarea id="mensaje-acceso" rows="6" readonly>${texto}</textarea>
      </label>
      <p class="acciones">
        <button class="boton" data-copiar="#mensaje-acceso">Copiar mensaje</button>
        <a class="boton secundario" href="https://wa.me/?text=${encodeURIComponent(texto)}" target="_blank" rel="noopener">Enviar por WhatsApp</a>
        <a class="boton secundario" href="/admin">Volver a alumnos</a>
      </p>
    </section>`));
}

router.post('/alumnos', (req, res) => {
  const nombre = String(req.body.nombre || '').trim().slice(0, 100);
  const correo = String(req.body.correo || '').trim().toLowerCase();
  if (!nombre || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo)) return res.redirect('/admin?m=datos');
  const areas = permisos.idsDelFormulario(req.body);
  if (!areas.length) return res.redirect('/admin?m=areas');
  if (db.prepare('SELECT 1 FROM alumnos WHERE correo = ?').get(correo)) return res.redirect('/admin?m=existe');
  const password = auth.generarPassword();
  const id = db.prepare("INSERT INTO alumnos (nombre, correo, pass_hash, estado, nota, expira) VALUES (?, ?, ?, 'activo', ?, ?)")
    .run(nombre, correo, auth.hashPassword(password), String(req.body.nota || '').slice(0, 500), fechaValida(req.body.expira)).lastInsertRowid;
  permisos.guardar(id, areas);
  mostrarCredenciales(req, res, db.prepare('SELECT * FROM alumnos WHERE id = ?').get(id), password);
});

router.post('/alumnos/:id/estado', (req, res) => {
  const estado = ['activo', 'revocado'].includes(req.body.estado) ? req.body.estado : null;
  if (estado) {
    db.prepare('UPDATE alumnos SET estado = ? WHERE id = ?').run(estado, Number(req.params.id));
    if (estado === 'revocado') db.prepare('DELETE FROM sesiones WHERE alumno_id = ?').run(Number(req.params.id));
  }
  res.redirect('/admin?m=ok');
});

router.post('/alumnos/:id/permisos', (req, res) => {
  const alumno = db.prepare('SELECT * FROM alumnos WHERE id = ?').get(Number(req.params.id));
  if (!alumno) return res.redirect('/admin');
  permisos.guardar(alumno.id, permisos.idsDelFormulario(req.body));
  if (req.body.autorizar && alumno.estado === 'pendiente') {
    db.prepare("UPDATE alumnos SET estado = 'activo' WHERE id = ?").run(alumno.id);
  }
  res.redirect('/admin?m=ok');
});

router.post('/alumnos/:id/vigencia', (req, res) => {
  db.prepare('UPDATE alumnos SET expira = ? WHERE id = ?').run(fechaValida(req.body.expira), Number(req.params.id));
  res.redirect('/admin?m=ok');
});

router.post('/alumnos/:id/password', (req, res) => {
  const alumno = db.prepare('SELECT * FROM alumnos WHERE id = ?').get(Number(req.params.id));
  if (!alumno) return res.redirect('/admin');
  const password = auth.generarPassword();
  db.prepare('UPDATE alumnos SET pass_hash = ? WHERE id = ?').run(auth.hashPassword(password), alumno.id);
  db.prepare('DELETE FROM sesiones WHERE alumno_id = ?').run(alumno.id);
  mostrarCredenciales(req, res, alumno, password);
});

router.post('/alumnos/:id/eliminar', (req, res) => {
  db.prepare('DELETE FROM alumnos WHERE id = ?').run(Number(req.params.id));
  res.redirect('/admin?m=ok');
});

// ---------- Contenido ----------

router.get('/contenido', (req, res) => {
  const niveles = db.prepare('SELECT * FROM niveles ORDER BY orden').all();
  const areas = db.prepare('SELECT * FROM areas ORDER BY orden').all();
  const ramas = db.prepare('SELECT * FROM ramas ORDER BY orden, id').all();
  const temas = db.prepare('SELECT t.*, (SELECT COUNT(*) FROM recursos x WHERE x.tema_id = t.id) AS recursos FROM temas t ORDER BY t.orden, t.id').all();
  res.send(pagina(req, 'Contenido', html`
    <h1>Contenido</h1>
    <p class="sub">Entra a cualquier tema para subirle videos, PDF o enlaces. También puedes agregar temas y ramas nuevas.</p>
    ${req.query.m === 'ok' ? aviso('ok', 'Cambios guardados.') : ''}
    ${niveles.map((n) => html`
      <details class="tarjeta nivel-admin" open>
        <summary><h2>${n.nombre}</h2></summary>
        ${areas.filter((a) => a.nivel_id === n.id).map((a) => html`
          <section class="area">
            <h3>${a.nombre}</h3>
            <div class="rejilla ramas">
              ${ramas.filter((r) => r.area_id === a.id).map((r) => html`
                <div class="tarjeta rama">
                  <h4>${r.nombre}</h4>
                  <ol class="temas">
                    ${temas.filter((t) => t.rama_id === r.id).map((t) => html`
                      <li><a href="/admin/tema/${t.id}">${t.titulo}</a>
                        <span class="contador ${t.recursos ? '' : 'vacio'}">${t.recursos || '—'}</span></li>`)}
                  </ol>
                  <form method="post" action="/admin/ramas/${r.id}/temas" class="en-linea">
                    <input name="titulo" required maxlength="120" placeholder="Nuevo tema" aria-label="Nuevo tema en ${r.nombre}">
                    <button class="boton mini">Agregar</button>
                  </form>
                </div>`)}
            </div>
            <form method="post" action="/admin/areas/${a.id}/ramas" class="en-linea">
              <input name="nombre" required maxlength="100" placeholder="Nueva rama en ${a.nombre}" aria-label="Nueva rama">
              <button class="boton mini secundario">Agregar rama</button>
            </form>
          </section>`)}
      </details>`)}
  `));
});

router.post('/ramas/:id/temas', (req, res) => {
  const rama = db.prepare(`SELECT r.id, a.slug AS area, n.slug AS nivel FROM ramas r
    JOIN areas a ON a.id = r.area_id JOIN niveles n ON n.id = a.nivel_id WHERE r.id = ?`).get(Number(req.params.id));
  const titulo = String(req.body.titulo || '').trim().slice(0, 120);
  if (rama && titulo) {
    const orden = db.prepare('SELECT COALESCE(MAX(orden), -1) + 1 AS o FROM temas WHERE rama_id = ?').get(rama.id).o;
    db.prepare('INSERT INTO temas (rama_id, slug, titulo, orden) VALUES (?, ?, ?, ?)')
      .run(rama.id, slugUnico(`${rama.nivel}-${rama.area}-${slugify(titulo)}`), titulo, orden);
  }
  res.redirect('/admin/contenido?m=ok');
});

router.post('/areas/:id/ramas', (req, res) => {
  const area = db.prepare('SELECT id FROM areas WHERE id = ?').get(Number(req.params.id));
  const nombre = String(req.body.nombre || '').trim().slice(0, 100);
  if (area && nombre) {
    const orden = db.prepare('SELECT COALESCE(MAX(orden), -1) + 1 AS o FROM ramas WHERE area_id = ?').get(area.id).o;
    db.prepare('INSERT INTO ramas (area_id, nombre, orden) VALUES (?, ?, ?)').run(area.id, nombre, orden);
  }
  res.redirect('/admin/contenido?m=ok');
});

function temaCompleto(id) {
  return db.prepare(`SELECT t.*, r.nombre AS rama, a.nombre AS area, n.nombre AS nivel FROM temas t
    JOIN ramas r ON r.id = t.rama_id JOIN areas a ON a.id = r.area_id JOIN niveles n ON n.id = a.nivel_id
    WHERE t.id = ?`).get(id);
}

const ICONOS = { youtube: '▶️', pdf: '📄', enlace: '🔗' };

router.get('/tema/:id', (req, res, next) => {
  const tema = temaCompleto(Number(req.params.id));
  if (!tema) return next();
  const recursos = db.prepare('SELECT * FROM recursos WHERE tema_id = ? ORDER BY orden, id').all(tema.id);
  const avisos = {
    ok: aviso('ok', 'Cambios guardados.'),
    youtube: aviso('error', 'No reconocí el enlace de YouTube. Pega la URL completa del video.'),
    url: aviso('error', 'El enlace debe empezar con http:// o https://'),
    pdf: aviso('error', `Sube un archivo PDF válido de máximo ${MAX_PDF_MB} MB.`),
  };
  res.send(pagina(req, tema.titulo, html`
    <p class="migas"><a href="/admin/contenido">Contenido</a> › ${tema.nivel} › ${tema.area} › ${tema.rama}</p>
    <h1>${tema.titulo}</h1>
    <p><a class="boton secundario" href="/tema/${tema.slug}" target="_blank" rel="noopener">Ver como alumno</a></p>
    ${avisos[req.query.m] || ''}

    <section class="tarjeta">
      <h2>Material del tema</h2>
      ${recursos.length ? html`
        <ul class="lista-recursos">
          ${recursos.map((r, i) => html`
            <li>
              <span>${ICONOS[r.tipo]} <strong>${r.titulo}</strong>
                <span class="meta">${r.tipo === 'pdf' ? r.nombre_original : r.url}</span></span>
              <span class="acciones">
                <form method="post" action="/admin/recursos/${r.id}/mover"><input type="hidden" name="dir" value="-1"><button class="boton mini secundario" ${i === 0 ? 'disabled' : ''} aria-label="Subir">↑</button></form>
                <form method="post" action="/admin/recursos/${r.id}/mover"><input type="hidden" name="dir" value="1"><button class="boton mini secundario" ${i === recursos.length - 1 ? 'disabled' : ''} aria-label="Bajar">↓</button></form>
                <form method="post" action="/admin/recursos/${r.id}/eliminar" data-confirmar="¿Eliminar “${r.titulo}”?"><button class="boton mini peligro">Eliminar</button></form>
              </span>
            </li>`)}
        </ul>` : html`<p class="meta">Este tema aún no tiene material.</p>`}
    </section>

    <div class="rejilla">
      <section class="tarjeta">
        <h2>▶️ Video de YouTube</h2>
        <p class="meta">Tip: sube los videos como “No listado” para que solo los vean tus alumnos desde aquí.</p>
        <form method="post" action="/admin/tema/${tema.id}/youtube" class="formulario">
          <label>Título <input name="titulo" required maxlength="150"></label>
          <label>URL del video <input name="url" required placeholder="https://youtu.be/…"></label>
          <button class="boton">Agregar video</button>
        </form>
      </section>
      <section class="tarjeta">
        <h2>📄 Archivo PDF</h2>
        <p class="meta">Los alumnos podrán verlo en la página y descargarlo. Máximo ${MAX_PDF_MB} MB.</p>
        <form method="post" action="/admin/tema/${tema.id}/pdf" enctype="multipart/form-data" class="formulario">
          <label>Título <input name="titulo" maxlength="150" placeholder="Si lo dejas vacío uso el nombre del archivo"></label>
          <label>Archivo <input type="file" name="archivo" accept="application/pdf,.pdf" required></label>
          <button class="boton">Subir PDF</button>
        </form>
      </section>
      <section class="tarjeta">
        <h2>🔗 Enlace</h2>
        <p class="meta">Simuladores (PhET, GeoGebra, Desmos), artículos, Drive, formularios…</p>
        <form method="post" action="/admin/tema/${tema.id}/enlace" class="formulario">
          <label>Título <input name="titulo" required maxlength="150"></label>
          <label>URL <input type="url" name="url" required placeholder="https://"></label>
          <button class="boton">Agregar enlace</button>
        </form>
      </section>
    </div>

    <section class="tarjeta">
      <h2>Datos del tema</h2>
      <form method="post" action="/admin/tema/${tema.id}/editar" class="formulario">
        <label>Título <input name="titulo" required maxlength="120" value="${tema.titulo}"></label>
        <label>Descripción (se muestra a los alumnos) <textarea name="descripcion" rows="3" maxlength="1000">${tema.descripcion}</textarea></label>
        <button class="boton secundario">Guardar</button>
      </form>
      <form method="post" action="/admin/tema/${tema.id}/eliminar" data-confirmar="¿Eliminar el tema “${tema.titulo}” y todo su material?" class="derecha">
        <button class="boton peligro">Eliminar tema</button>
      </form>
    </section>
  `));
});

function siguienteOrden(temaId) {
  return db.prepare('SELECT COALESCE(MAX(orden), -1) + 1 AS o FROM recursos WHERE tema_id = ?').get(temaId).o;
}

router.post('/tema/:id/youtube', (req, res) => {
  const id = Number(req.params.id);
  const titulo = String(req.body.titulo || '').trim().slice(0, 150);
  const vid = idYoutube(String(req.body.url || '').trim());
  if (!temaCompleto(id) || !titulo || !vid) return res.redirect(`/admin/tema/${id}?m=youtube`);
  db.prepare("INSERT INTO recursos (tema_id, tipo, titulo, url, orden) VALUES (?, 'youtube', ?, ?, ?)")
    .run(id, titulo, `https://www.youtube.com/watch?v=${vid}`, siguienteOrden(id));
  res.redirect(`/admin/tema/${id}?m=ok`);
});

router.post('/tema/:id/enlace', (req, res) => {
  const id = Number(req.params.id);
  const titulo = String(req.body.titulo || '').trim().slice(0, 150);
  const url = String(req.body.url || '').trim().slice(0, 2000);
  if (!temaCompleto(id) || !titulo || !urlValida(url)) return res.redirect(`/admin/tema/${id}?m=url`);
  db.prepare("INSERT INTO recursos (tema_id, tipo, titulo, url, orden) VALUES (?, 'enlace', ?, ?, ?)")
    .run(id, titulo, url, siguienteOrden(id));
  res.redirect(`/admin/tema/${id}?m=ok`);
});

router.post('/tema/:id/pdf', (req, res) => {
  const id = Number(req.params.id);
  subida.single('archivo')(req, res, (err) => {
    const borrar = () => req.file && fs.rm(req.file.path, { force: true }, () => {});
    if (err || !req.file || !temaCompleto(id)) { borrar(); return res.redirect(`/admin/tema/${id}?m=pdf`); }
    // Verifica que realmente sea un PDF (firma %PDF- al inicio).
    const cabecera = Buffer.alloc(5);
    const fd = fs.openSync(req.file.path, 'r');
    fs.readSync(fd, cabecera, 0, 5, 0);
    fs.closeSync(fd);
    if (cabecera.toString('latin1') !== '%PDF-') { borrar(); return res.redirect(`/admin/tema/${id}?m=pdf`); }
    // multer entrega el nombre original en latin1; lo pasamos a UTF-8 para conservar acentos.
    const original = Buffer.from(req.file.originalname, 'latin1').toString('utf8').slice(0, 200);
    const titulo = String(req.body.titulo || '').trim().slice(0, 150) || original.replace(/\.pdf$/i, '');
    db.prepare("INSERT INTO recursos (tema_id, tipo, titulo, archivo, nombre_original, tamano, orden) VALUES (?, 'pdf', ?, ?, ?, ?, ?)")
      .run(id, titulo, req.file.filename, original, req.file.size, siguienteOrden(id));
    res.redirect(`/admin/tema/${id}?m=ok`);
  });
});

router.post('/tema/:id/editar', (req, res) => {
  const id = Number(req.params.id);
  const titulo = String(req.body.titulo || '').trim().slice(0, 120);
  if (titulo) {
    db.prepare('UPDATE temas SET titulo = ?, descripcion = ? WHERE id = ?')
      .run(titulo, String(req.body.descripcion || '').trim().slice(0, 1000), id);
  }
  res.redirect(`/admin/tema/${id}?m=ok`);
});

function borrarArchivos(recursos) {
  for (const r of recursos) if (r.archivo) fs.rm(path.join(UPLOAD_DIR, path.basename(r.archivo)), { force: true }, () => {});
}

router.post('/tema/:id/eliminar', (req, res) => {
  const id = Number(req.params.id);
  borrarArchivos(db.prepare('SELECT archivo FROM recursos WHERE tema_id = ?').all(id));
  db.prepare('DELETE FROM temas WHERE id = ?').run(id);
  res.redirect('/admin/contenido?m=ok');
});

router.post('/recursos/:id/eliminar', (req, res) => {
  const r = db.prepare('SELECT * FROM recursos WHERE id = ?').get(Number(req.params.id));
  if (!r) return res.redirect('/admin/contenido');
  borrarArchivos([r]);
  db.prepare('DELETE FROM recursos WHERE id = ?').run(r.id);
  res.redirect(`/admin/tema/${r.tema_id}?m=ok`);
});

router.post('/recursos/:id/mover', (req, res) => {
  const r = db.prepare('SELECT * FROM recursos WHERE id = ?').get(Number(req.params.id));
  if (!r) return res.redirect('/admin/contenido');
  const lista = db.prepare('SELECT id FROM recursos WHERE tema_id = ? ORDER BY orden, id').all(r.tema_id).map((x) => x.id);
  const i = lista.indexOf(r.id);
  const j = i + (Number(req.body.dir) < 0 ? -1 : 1);
  if (j >= 0 && j < lista.length) {
    [lista[i], lista[j]] = [lista[j], lista[i]];
    const upd = db.prepare('UPDATE recursos SET orden = ? WHERE id = ?');
    lista.forEach((rid, k) => upd.run(k, rid));
  }
  res.redirect(`/admin/tema/${r.tema_id}`);
});

module.exports = { router };
