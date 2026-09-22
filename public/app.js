// JS mínimo: nada se carga hasta que el alumno lo pide, para que las páginas abran rápido.
document.addEventListener('click', (e) => {
  // Video de YouTube: se muestra la miniatura y el reproductor solo se carga al hacer clic.
  const yt = e.target.closest('[data-yt]');
  if (yt) {
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube-nocookie.com/embed/${yt.dataset.yt}?autoplay=1&rel=0`;
    iframe.title = yt.getAttribute('aria-label') || 'Video';
    iframe.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; fullscreen';
    iframe.allowFullscreen = true;
    iframe.className = 'yt-frame';
    yt.replaceWith(iframe);
    return;
  }

  // Visor de PDF: se inserta al pedirlo y se quita al cerrarlo (libera memoria).
  const pdf = e.target.closest('[data-pdf]');
  if (pdf) {
    const visor = pdf.closest('.pdf').querySelector('.visor');
    if (visor.hidden) {
      visor.innerHTML = '';
      const iframe = document.createElement('iframe');
      iframe.src = pdf.dataset.pdf;
      iframe.title = 'Visor de PDF';
      iframe.className = 'pdf-frame';
      visor.appendChild(iframe);
      const nota = document.createElement('p');
      nota.className = 'meta';
      nota.textContent = '¿No se ve en tu celular? Usa “Abrir en pestaña” o “Descargar”.';
      visor.appendChild(nota);
      visor.hidden = false;
      pdf.textContent = 'Cerrar visor';
    } else {
      visor.hidden = true;
      visor.innerHTML = '';
      pdf.textContent = 'Ver aquí';
    }
    return;
  }

  const copiar = e.target.closest('[data-copiar]');
  if (copiar) {
    const campo = document.querySelector(copiar.dataset.copiar);
    navigator.clipboard.writeText(campo.value).then(
      () => { copiar.textContent = '¡Copiado!'; },
      () => { campo.select(); document.execCommand('copy'); copiar.textContent = '¡Copiado!'; },
    );
  }
});

// Confirmación antes de acciones destructivas en el panel.
document.addEventListener('submit', (e) => {
  const msg = e.target.dataset.confirmar;
  if (msg && !confirm(msg)) e.preventDefault();
});

// Buscador de temas dentro de un nivel.
const filtro = document.querySelector('[data-filtro]');
if (filtro) {
  const quitarAcentos = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  filtro.addEventListener('input', () => {
    const q = quitarAcentos(filtro.value.trim());
    document.querySelectorAll('[data-rama]').forEach((rama) => {
      let visibles = 0;
      rama.querySelectorAll('[data-tema]').forEach((li) => {
        const ok = !q || quitarAcentos(li.dataset.tema).includes(q);
        li.hidden = !ok;
        if (ok) visibles++;
      });
      rama.hidden = visibles === 0;
    });
  });
}
