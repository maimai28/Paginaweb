# Tarea 2 · Demo de producto B (negocio ficticio)

`index.html` = página completa en un solo archivo (CSS y JS dentro). Negocio inventado: **Fisio Ocotillo**. Lo verifiqué el 6 nov 2026: no encontré ningún negocio real con ese nombre.

Qué trae: aviso fijo "EJEMPLO — NEGOCIO FICTICIO", servicios con precios, cómo agendar, fotos, ubicación con mapa, horario, botón de WhatsApp flotante. **No trae reseñas ni testimonios.**

Por qué fisioterapia: 16 de los 25 prospectos son de salud (fisio, nutrición, psicología, dental). Para uñas/pestañas cambias textos, fotos y colores (ver abajo).

## Publicarla en Cloudflare Pages (sin Git, 5 min)

1. [ ] Descarga la carpeta `servicios/demo/` (con `index.html` dentro).
2. [ ] Cloudflare → **Workers & Pages** → **Create application** → **Get started** → **Drag and drop your files** (pasos de la doc oficial de Direct Upload, actualizada el 21 abr 2026).
3. [ ] Nombre del proyecto: algo como `demo-pagina-agenda` → la URL queda `demo-pagina-agenda.pages.dev`.
4. [ ] Arrastra la carpeta (o un .zip) → **Deploy site**.
5. [ ] Abre la URL en tu celular y revisa: aviso amarillo visible, fotos cargan, mapa carga, botones abren el aviso de demo.

Notas verificadas (ver `../FUENTES.md`):
- Un proyecto con Direct Upload **no se puede pasar a Git después**. Para la demo no importa.
- Cloudflare recomienda **Workers** para proyectos nuevos; Pages sigue funcionando en el plan gratis. Si en el panel ya no ves la opción de Pages, crea un Worker con "static assets" y sube la misma carpeta.
- La demo tiene `noindex`: no aparece en Google. Así nadie la confunde con un negocio real.

## Modo demo vs. página real

Al final del HTML hay un bloque `CONFIG`:

```js
const CONFIG = {
  whatsapp: "",   // 10 dígitos: "6561234567"
  mensaje: "Hola, vi su página y quiero información para agendar una cita.",
  agendaUrl: ""   // link de "Copiar vínculo" de la página de reservas de Google Calendar
};
```

- Vacío → los botones muestran "Esto es una demo" y no abren nada.
- Lleno → "WhatsApp" abre `https://wa.me/52<10 dígitos>?text=...` (formato oficial: número internacional sin +, espacios ni guiones) y "Agendar cita" abre la página de reservas.

## Adaptarla para un cliente real (solo con su permiso)

1. [ ] **Antes del permiso**: si haces una maqueta con su nombre, se la enseñas en tu laptop/celular (abres el archivo local). **No la subas.**
2. [ ] Con permiso y anticipo: copia la carpeta, renómbrala con el negocio.
3. [ ] Quita el `<div class="aviso">`, la etiqueta `DEMO`, la línea `<meta name="robots" content="noindex, nofollow">` y el texto del pie.
4. [ ] Cambia nombre, textos, servicios y precios **que te dé el cliente por escrito** (WhatsApp sirve).
5. [ ] Fotos: las del cliente (pídelas en buena luz, horizontales). Si usa de stock, que diga "foto ilustrativa".
6. [ ] Mapa: Google Maps → menú → **Compartir o incorporar mapa** → **Incorporar un mapa** → **Copiar HTML** → reemplaza el `<iframe>` de OpenStreetMap.
7. [ ] Llena `CONFIG` con su WhatsApp y su link de reservas. Prueba los dos botones desde tu celular.
8. [ ] Colores: cambia las variables `--terracota`, `--salvia`, `--fondo` al inicio del `<style>`. Verifica contraste texto/fondo ≥ 4.5:1.
9. [ ] Publica en la cuenta de Cloudflare **del cliente** (o en la tuya y le transfieres). Dominio propio: lo compra y paga él.

## Créditos

- Fotos: Unsplash (licencia Unsplash, uso comercial permitido, crédito opcional). Se eligieron fotos **sin caras reconocibles** porque la licencia no cubre la imagen de personas.
- Mapa: © colaboradores de OpenStreetMap (la atribución es obligatoria si usas su mapa).
