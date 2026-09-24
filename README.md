# El Lab del Desierto · Plataforma de cursos

Sitio privado para las tutorías de matemáticas, cálculo y física (secundaria, preparatoria y universidad básica).
Solo entran los alumnos que tú autorizas. Cada alumno tiene **su propia contraseña**.

## Qué incluye

- **Temario precargado**: 3 niveles → Matemáticas / Física → ramas principales → 146 temas (editable desde el panel).
- **Una página por tema** (se abre en pestaña nueva) con:
  - Videos de YouTube: se muestra solo la miniatura; el reproductor se carga al darle clic.
  - PDF: visor dentro de la página (se carga al pulsar “Ver aquí”), abrir en pestaña y **descargar**.
  - Enlaces externos (GeoGebra, PhET, Desmos, Drive…).
- **Control de acceso**:
  - El alumno pide acceso en `/solicitar` y crea su contraseña → queda **pendiente** hasta que tú la autorizas.
  - O tú lo das de alta en `/admin` y el sistema genera una contraseña única (con botón para copiarla o mandarla por WhatsApp).
  - Fecha de vencimiento opcional por alumno, revocar/reactivar, generar contraseña nueva.
  - **Permisos por materia**: cada alumno ve solo los niveles y áreas que le marques (ej. Preparatoria · Física). Se bloquea también el acceso directo por enlace a temas y PDF.
  - **Una sesión por alumno**: si comparte su contraseña y otra persona entra, a él se le cierra la sesión.
  - Los PDF solo se descargan con sesión iniciada; el sitio no se indexa en buscadores.

## Correr en tu computadora

Requiere Node.js 22.13 o superior.

```bash
npm install
cp .env.example .env     # edita ADMIN_PASSWORD
npm start                # http://localhost:3000
```

- Alumnos: `http://localhost:3000/login`
- Administración: `http://localhost:3000/admin`

## Uso diario

1. Alguien te compra una tutoría → le mandas el enlace `/solicitar` **o** lo das de alta tú en `/admin`.
2. En `/admin` → “Solicitudes pendientes”: revisa las materias que marcó el alumno, corrígelas si hace falta y pulsa **Guardar y autorizar**.
3. Para subir material: `/admin/contenido` → clic en el tema → agrega video, PDF o enlace.
4. Si un alumno compra otra materia: “Editar materias” en su fila y marca la nueva.
5. Si un alumno deja de pagar: **Revocar** (o ponle fecha en “Acceso hasta”).

Recomendación: sube tus videos a YouTube como **No listado**. Si los pones públicos, cualquiera los puede ver fuera de la plataforma.

## Publicarlo en internet

Es una app de Node con base de datos SQLite y archivos en disco (carpeta `DATA_DIR`).
**El servidor necesita disco persistente**, si no, se borran alumnos y PDF en cada reinicio.

Opciones que funcionan:

- **Railway**: crea el proyecto desde este repositorio, agrega un *Volume* montado en `/data` y define `ADMIN_PASSWORD`. La app detecta el volumen sola (`RAILWAY_VOLUME_MOUNT_PATH`), no hace falta `DATA_DIR`.
- **Render**: Web Service con *Persistent Disk* montado en `/data` (requiere plan de pago), mismas variables.
- **VPS** (DigitalOcean, Hetzner, etc.): `npm install && npm start` detrás de Nginx/Caddy con HTTPS.

Comando de inicio: `npm start`. Usa siempre HTTPS en producción.

### Variables de entorno

| Variable | Para qué |
|---|---|
| `ADMIN_PASSWORD` | Contraseña del panel `/admin` (obligatoria, larga y única). |
| `DATA_DIR` | Carpeta de la base de datos y los PDF. |
| `PORT` | Puerto (el hosting normalmente lo pone solo). |
| `MAX_PDF_MB` | Tamaño máximo por PDF (50 por defecto). |
| `IMPORTAR_GUIAS` | Pon `0` para no cargar automáticamente las guías de `guias/pdf/`. |

### Respaldos

Todo vive en `DATA_DIR`: `cursos.db` (alumnos, temas, recursos) y `archivos/` (PDF). Copia esa carpeta para respaldar.

## Guías PDF

La carpeta `guias/` tiene el generador de guías de estudio con el diseño de la marca y 92 guías (35 de secundaria y 57 de preparatoria, matemáticas y física) listas en `guias/pdf/`. Ver `guias/README.md`.

**Se cargan solas.** Al arrancar, el servidor lee `guias/pdf/manifiesto.json` y, para cada guía:

- pone la descripción del tema si está vacía (no toca las que escribiste tú);
- sube el PDF como primer material del tema, con el título «Guía de estudio: …»;
- si la guía cambió en el repositorio, reemplaza el archivo;
- si la borraste desde el panel, no la vuelve a subir.

Para publicar guías nuevas: haz push y en Railway pulsa **Check for updates** (o *Redeploy*).

## Estructura

```
server.js              arranque, cabeceras de seguridad
src/catalogo.js        temario inicial (solo se usa la primera vez)
src/db.js              esquema SQLite
src/permisos.js        materias (nivel + área) que puede ver cada alumno
src/auth.js            contraseñas (scrypt), sesiones, límites de intentos
src/rutas-alumno.js    login, solicitud de acceso, cursos, página de tema, PDF
src/rutas-admin.js     panel: alumnos y contenido
public/                CSS y JS del navegador
```
