// Plantillas HTML con escape automático: todo lo interpolado se escapa salvo que venga de raw() o de otro html``.
class Raw {
  constructor(s) { this.s = s; }
  toString() { return this.s; }
}
const raw = (s) => new Raw(String(s));

const esc = (v) => String(v)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

function valor(v) {
  if (v == null || v === false) return '';
  if (v instanceof Raw) return v.s;
  if (Array.isArray(v)) return v.map(valor).join('');
  return esc(v);
}

function html(strings, ...vals) {
  let out = strings[0];
  vals.forEach((v, i) => { out += valor(v) + strings[i + 1]; });
  return new Raw(out);
}

function layout({ titulo, usuario, cuerpo, admin = false }) {
  const nav = usuario
    ? html`<nav class="nav">
        ${usuario.esAdmin
          ? html`<a href="/admin">Alumnos</a><a href="/admin/contenido">Contenido</a><a href="/cursos">Ver cursos</a>`
          : html`<a href="/cursos">Mis cursos</a><span class="quien">${usuario.alumno.nombre}</span>`}
        <form method="post" action="${usuario.esAdmin ? '/admin/logout' : '/logout'}"><button class="link">Salir</button></form>
      </nav>`
    : '';
  return `<!doctype html>${html`<html lang="es-MX">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>${titulo} · El Lab del Desierto</title>
<link rel="stylesheet" href="/static/estilos.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%E2%9A%9B%3C/text%3E%3C/svg%3E">
<script src="/static/app.js" defer></script>
</head>
<body class="${admin ? 'admin' : ''}">
<header class="barra">
  <a class="marca" href="${usuario ? (usuario.esAdmin ? '/admin' : '/cursos') : '/'}"><span class="logo">⚛</span> El Lab del Desierto <small>Cursos</small></a>
  ${nav}
</header>
<main class="contenedor">${cuerpo}</main>
<footer class="pie">© ${new Date().getFullYear()} El Lab del Desierto · Material exclusivo para alumnos. No compartas tu contraseña.</footer>
</body>
</html>`}`;
}

const aviso = (tipo, texto) => (texto ? html`<p class="aviso ${tipo}">${texto}</p>` : '');

module.exports = { html, raw, esc, layout, aviso };
