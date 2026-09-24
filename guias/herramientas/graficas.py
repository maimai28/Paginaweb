"""Genera el SVG de gráficas simples a partir de datos, para pegarlo en una guía.

Así las barras, sectores y puntos quedan exactamente en su valor (no se dibujan a ojo).
Uso desde Python:  from graficas import barras, pastel, lineas
"""
import math

TINTA, SUAVE, ARENA = '#2b241e', '#5f5448', '#e4d2b4'
COLORES = ['#a8492a', '#c08a2e', '#6e7f62', '#4b5d6b', '#d9b98c', '#8a6f5a']
FUENTE = 'font-family="Nunito"'


def barras(etiquetas, valores, ymax, paso, ancho=300, alto=170, color='#a8492a', titulo_y='', ymin=0):
    x0, y0, arriba = 36, alto - 25, (22 if titulo_y else 12)
    esc = (y0 - arriba) / (ymax - ymin)
    n = len(valores)
    hueco = (ancho - x0 - 10) / n
    w = hueco * 0.62
    out = [f'<svg viewBox="0 0 {ancho} {alto}" width="{ancho * 0.26:.0f}mm">']
    for v in range(ymin, ymax + 1, paso):
        y = y0 - (v - ymin) * esc
        out.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{ancho - 6}" y2="{y:.1f}" stroke="{ARENA}" stroke-width="0.8"/>')
        out.append(f'<text x="{x0 - 5}" y="{y + 3.5:.1f}" {FUENTE} font-size="10" text-anchor="end" fill="{SUAVE}">{v}</text>')
    for i, (e, v) in enumerate(zip(etiquetas, valores)):
        x = x0 + i * hueco + (hueco - w) / 2
        out.append(f'<rect x="{x:.1f}" y="{y0 - (v - ymin) * esc:.1f}" width="{w:.1f}" height="{(v - ymin) * esc:.1f}" fill="{color}"/>')
        out.append(f'<text x="{x + w / 2:.1f}" y="{y0 + 14}" {FUENTE} font-size="10" text-anchor="middle" fill="{TINTA}">{e}</text>')
    out.append(f'<line x1="{x0}" y1="{y0}" x2="{ancho - 6}" y2="{y0}" stroke="{TINTA}"/>')
    if titulo_y:
        out.append(f'<text x="4" y="8" {FUENTE} font-size="9" fill="{SUAVE}">{titulo_y}</text>')
    out.append('</svg>')
    return '\n'.join(out)


def pastel(etiquetas, valores, r=62, cx=75, cy=75):
    total = sum(valores)
    out = [f'<svg viewBox="0 0 290 150" width="78mm">']
    ang = -90.0
    for i, (e, v) in enumerate(zip(etiquetas, valores)):
        a2 = ang + 360 * v / total
        p1 = (cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang)))
        p2 = (cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2)))
        grande = 1 if a2 - ang > 180 else 0
        out.append(f'<path d="M{cx} {cy} L{p1[0]:.2f} {p1[1]:.2f} A{r} {r} 0 {grande} 1 {p2[0]:.2f} {p2[1]:.2f} Z" fill="{COLORES[i % 6]}" stroke="#fff" stroke-width="1.5"/>')
        ly = 22 + i * 22
        out.append(f'<rect x="160" y="{ly - 9}" width="11" height="11" fill="{COLORES[i % 6]}"/>')
        out.append(f'<text x="177" y="{ly}" {FUENTE} font-size="11" fill="{TINTA}">{e}</text>')
        ang = a2
    out.append('</svg>')
    return '\n'.join(out)


def lineas(xs, ys, xmin, xmax, ymin, ymax, paso_y, ancho=300, alto=170, sufijo_x='', color='#a8492a'):
    x0, y0, der, arriba = 36, alto - 25, ancho - 12, 12
    fx = lambda v: x0 + (v - xmin) * (der - x0) / (xmax - xmin)
    fy = lambda v: y0 - (v - ymin) * (y0 - arriba) / (ymax - ymin)
    out = [f'<svg viewBox="0 0 {ancho} {alto}" width="{ancho * 0.26:.0f}mm">']
    for v in range(ymin, ymax + 1, paso_y):
        out.append(f'<line x1="{x0}" y1="{fy(v):.1f}" x2="{der}" y2="{fy(v):.1f}" stroke="{ARENA}" stroke-width="0.8"/>')
        out.append(f'<text x="{x0 - 5}" y="{fy(v) + 3.5:.1f}" {FUENTE} font-size="10" text-anchor="end" fill="{SUAVE}">{v}</text>')
    for v in xs:
        out.append(f'<text x="{fx(v):.1f}" y="{y0 + 14}" {FUENTE} font-size="10" text-anchor="middle" fill="{TINTA}">{v}{sufijo_x}</text>')
    out.append(f'<line x1="{x0}" y1="{y0}" x2="{der}" y2="{y0}" stroke="{TINTA}"/>')
    pts = ' '.join(f'{fx(a):.1f},{fy(b):.1f}' for a, b in zip(xs, ys))
    out.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2.2"/>')
    for a, b in zip(xs, ys):
        out.append(f'<circle cx="{fx(a):.1f}" cy="{fy(b):.1f}" r="3.2" fill="{color}"/>')
    out.append('</svg>')
    return '\n'.join(out)
