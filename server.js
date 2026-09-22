const path = require('node:path');
const express = require('express');
require('./src/db');
const auth = require('./src/auth');
const { layout, html } = require('./src/html');
const alumno = require('./src/rutas-alumno');
const admin = require('./src/rutas-admin');

const app = express();
app.disable('x-powered-by');
app.set('trust proxy', 1); // detrás del proxy HTTPS del hosting (Render, Railway, etc.)

app.use((req, res, next) => {
  res.setHeader('Content-Security-Policy', [
    "default-src 'self'",
    "img-src 'self' data: https://i.ytimg.com",
    "frame-src 'self' https://www.youtube-nocookie.com",
    "script-src 'self'",
    "style-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'self'",
  ].join('; '));
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('X-Robots-Tag', 'noindex, nofollow');
  next();
});

app.use('/static', express.static(path.join(__dirname, 'public'), { maxAge: '7d' }));
app.use(express.urlencoded({ extended: false, limit: '100kb' }));
app.use(auth.mismoOrigen);
app.use(auth.cargarSesion);
app.use((req, res, next) => {
  // Las páginas protegidas no deben quedar en la caché compartida.
  res.setHeader('Cache-Control', 'private, no-store');
  next();
});

app.get('/robots.txt', (req, res) => res.type('text/plain').send('User-agent: *\nDisallow: /\n'));
app.use('/admin', admin.router);
app.use('/', alumno.router);

app.use((req, res) => {
  res.status(404).send(layout({
    titulo: 'No encontrado',
    usuario: req.usuario,
    cuerpo: html`<section class="tarjeta angosta"><h1>Página no encontrada</h1><p><a href="/">Volver al inicio</a></p></section>`,
  }));
});

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).send('Ocurrió un error en el servidor.');
});

const PORT = Number(process.env.PORT) || 3000;
app.listen(PORT, () => {
  console.log(`Plataforma de cursos en http://localhost:${PORT}`);
  if (!process.env.ADMIN_PASSWORD) console.warn('AVISO: define ADMIN_PASSWORD para poder entrar a /admin');
});
