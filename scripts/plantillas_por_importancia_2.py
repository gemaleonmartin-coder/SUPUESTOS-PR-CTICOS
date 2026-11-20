# -*- coding: utf-8 -*-
"""Word de plantillas por importancia, segunda versión (fase 38, quinta vuelta).

Cambios pedidos por Gem sobre la primera versión: sin saltos de página entre apartados; lo fijo, dentro del cuadro
y sin nada debajo; muchos más ejemplos y comodines (con ◆ los diferenciadores); el texto de la norma, literal, con su
etiqueta; y la tabla de elementos curriculares con los colores de las áreas de la programación.

Uso:  python3 scripts/plantillas_por_importancia_2.py   →   libreta-magica/Plantillas_por_importancia_v22_3.docx
Textos: opciones_plantillas_2.py (plantillas y opciones) y textos_libreta_v22.py (elementos y orientaciones).
"""
import os
import re
import sys

from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Cm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opciones_plantillas_2 as O  # noqa: E402
import plantillas_bocadillos as PB  # noqa: E402
import textos_libreta_v22 as T  # noqa: E402

SALIDA = os.path.join(PB.RAIZ, 'libreta-magica', 'Plantillas_por_importancia_v22_3.docx')   # v22_2: la anterior
ANCHO = 17.4
GRIS_C = '8C8C8C'
INSIGNIA = {'1': (' 1.ª OPCIÓN ', PB.VERDE_AZ), 'C': (' COMODÍN {n} ', GRIS_C),
            'D': (' COMODÍN {n} ◆ ', PB.NARANJA_BORDE), 'N': (' NORMA ', PB.AZUL)}
# Colores de las áreas en la programación de Gem (build_tabla_udi.py y apartado_4.py): fuerte, suave y texto
AREA = {'CMN': ('E2F0DC', 'F2F8EF', '2E6B34'), 'LCL': ('F8DEDD', 'FCF1F0', '8B2E3C'),
        'MAT': ('DCE9F5', 'F1F6FB', '1F4E79'), 'EAR': ('FBE5CC', 'FDF4EA', '9A5410')}


def _apretado(el, linea=246):
    """Interlineado algo más justo en las opciones (todo cabe sin páginas casi vacías)."""
    el.find(qn('w:pPr')).find(qn('w:spacing')).set(qn('w:line'), str(linea))
    return el


def _keep(el, *etiquetas):
    ppr = el.find(qn('w:pPr'))
    for e in etiquetas:
        ppr.insert(0, OxmlElement(e))
    return el


def rico(texto, tam=9.5, color='262626'):
    """Runs de un texto con **negrita**, una nota tras « § » (en gris) y lo pendiente [POR COMPROBAR…] en naranja."""
    nota = None
    if ' § ' in texto:
        texto, nota = texto.split(' § ', 1)
    # tras una etiqueta en negrita que acaba en punto, la primera letra, en mayúscula
    texto = re.sub(r'^(\*\*[^*]+\.\*\* )([a-záéíóúñ])', lambda m: m.group(1) + m.group(2).upper(), texto)
    out = []
    for trozo in re.split(r'(\*\*[^*]+\*\*|\[POR COMPROBAR[^\]]*\])', texto):
        if not trozo:
            continue
        if trozo.startswith('**'):
            out.append(PB._run(trozo[2:-2], negrita=True, color=PB.AZUL, tam=tam))
        elif trozo.startswith('[POR COMPROBAR'):
            out.append(PB._run(trozo, tam=tam, color='262626', fondo=PB.NARANJA))
        else:
            out.append(PB._run(trozo, tam=tam, color=color))
    if nota:
        out.append(PB._run('  ·  ' + nota, tam=tam - 1, color=PB.GRIS_TXT, cursiva=True))
    return ''.join(out)


def _trozos(texto):
    """Analiza una plantilla con huecos anidados: [n|hueco], [hueco] y {n|fijo}."""
    out, i, txt = [], 0, ''
    while i < len(texto):
        c = texto[i]
        if c in '[{':
            cierre, prof, j = (']' if c == '[' else '}'), 0, i
            while j < len(texto):
                if texto[j] == c:
                    prof += 1
                elif texto[j] == cierre:
                    prof -= 1
                    if prof == 0:
                        break
                j += 1
            dentro = texto[i + 1:j]
            m = re.match(r'(\d+)\|', dentro)
            num = m.group(1) if m else None
            if m:
                dentro = dentro[m.end():]
            if txt:
                out.append(('txt', txt))
                txt = ''
            out.append(('hueco', _trozos(dentro), num) if c == '[' else ('fijo', dentro, num))
            i = j + 1
            continue
        txt += c
        i += 1
    if txt:
        out.append(('txt', txt))
    return out


def runs_plantilla(texto, tam=10.5):
    def pinta(trozos, en_hueco=False):
        r = []
        for t in trozos:
            if t[0] == 'txt':
                r.append(PB._run(t[1], tam=tam, color=PB.VERDE_AZ if en_hueco else '262626', negrita=en_hueco))
            elif t[0] == 'hueco':
                r.append(PB._run('[', negrita=True, color=PB.VERDE_AZ, tam=tam))
                r.extend(pinta(t[1], True))
                r.append(PB._run(']', negrita=True, color=PB.VERDE_AZ, tam=tam))
                if t[2]:
                    r.append(PB._run(t[2], negrita=True, color=PB.NARANJA_BORDE, tam=tam, sup=True))
            else:
                if t[1]:
                    r.append(PB._run(t[1], tam=tam, color='262626'))
                if t[2]:
                    r.append(PB._run(t[2], negrita=True, color=PB.NARANJA_BORDE, tam=tam, sup=True))
        return r
    return ''.join(pinta(_trozos(texto)))


def etiqueta_hueco(texto, n):
    """Texto del hueco n en la plantilla (con huecos anidados)."""
    def busca(trozos):
        for t in trozos:
            if t[0] == 'hueco':
                if t[2] == str(n):
                    return ''.join(x[1] if x[0] == 'txt' else '[…]' for x in t[1])
                r = busca(t[1])
                if r:
                    return r
        return None
    return busca(_trozos(texto))


class Plantillas(PB.Constructor):
    def __init__(self):
        super().__init__(apaisado=False)
        h = self.d.sections[0].header.paragraphs[0]
        for r in list(h._p.findall(qn('w:r'))):
            h._p.remove(r)
        h._p.append(parse_xml(f'<w:r {PB.NS}>{PB._rpr(negrita=True, color=PB.AZUL, tam=8)}<w:t xml:space="preserve">'
                              f'Libreta mágica</w:t></w:r>'))
        h._p.append(parse_xml(f'<w:r {PB.NS}>{PB._rpr(color=PB.GRIS_TXT, tam=8)}<w:t xml:space="preserve">  ·  '
                              f'Plantillas por importancia · Educación Primaria · Andalucía 2027</w:t></w:r>'))

    def portada(self):
        self.p(PB._run('SUPUESTOS PRÁCTICOS · PARTE A', versalitas=True, color=PB.NARANJA_BORDE, tam=9, negrita=True),
               antes=0, despues=60)
        self.p(PB._run('Plantillas por importancia', negrita=True, color=PB.AZUL, tam=24), despues=40)
        self.p(PB._run('Las plantillas de redacción de la libreta mágica (7.1 a 7.9) y, debajo de cada párrafo, con qué '
                       'se completa cada hueco, de lo más importante a lo menos, con muchos ejemplos para elegir según el '
                       'proyecto', color=PB.VERDE_AZ, tam=11.5), despues=120)
        for nivel, texto in (('1', 'la más importante; si depende del área, una por área.'),
                             ('C', 'por si no encaja la primera, en orden de utilidad.'),
                             ('D', 'el comodín diferenciador, el que sorprende al tribunal.'),
                             ('N', 'el texto de la norma, copiado tal cual, para estudiarlo.')):
            etq, color = INSIGNIA[nivel]
            self.p(PB._run(etq.format(n=1), negrita=True, color='FFFFFF', tam=8, fondo=color)
                   + PB._run('  ' + texto, tam=10, color='262626'), despues=40)
        self.p(PB._run('El número naranja de cada hueco lleva a sus opciones, justo debajo del cuadro. Lo fijo va en el '
                       'cuadro y no lleva nada debajo. En gris, de dónde sale el ejemplo (Rafa, tu manual, tu '
                       'programación o tu libreta definitiva) o cómo se usa. En el 4.1, los bloques «según el supuesto» '
                       'van del más frecuente al menos. Los autores se concretarán con los temas.', tam=10,
                       color='262626'), antes=80, despues=40, alin='both')
        self.p(PB._run('Versión 2.2, tercera edición de las plantillas · 20 de noviembre de 2026 · Acompaña a la libreta '
                       'mágica 2.2. Material de estudio personal.', color=PB.GRIS_TXT, tam=8.5, cursiva=True),
               despues=100)

    def titulo(self, texto, salto=False):
        el = self.p(PB._run(texto, negrita=True, color=PB.VERDE_AZ, tam=14), antes=160, despues=80)
        return _keep(el, 'w:keepNext')

    def cuadro(self, contenido_xml, etiqueta_caja=None):
        t = self.d.add_table(rows=1, cols=1)
        t.autofit = False
        t._tbl.tblGrid.gridCol_lst[0].w = Cm(ANCHO)
        c = t.rows[0].cells[0]
        c.width = Cm(ANCHO)
        PB._limpia_celda(c._tc)
        PB._bordes_celda(c._tc, izq=PB.NARANJA_BORDE)
        PB._fondo(c._tc, PB.CREMA)
        PB._margenes(c._tc, 220, 200, 70, 60)
        if etiqueta_caja:
            c._tc.append(PB._parrafo_xml(PB._run(etiqueta_caja, versalitas=True, negrita=True, color=PB.NARANJA_BORDE,
                                                 tam=8.5), despues=40))
        c._tc.append(PB._parrafo_xml(contenido_xml, despues=40, alin='both'))
        for par in c._tc.findall(qn('w:p')):        # el cuadro, en la misma página que sus opciones
            _keep(par, 'w:keepNext')
        t._tbl.find(qn('w:tr')).get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        self._anade(t._tbl)

    def insignia(self, nivel, k=None):
        etq, color = INSIGNIA[nivel]
        return PB._run(etq.format(n=k), negrita=True, color='FFFFFF', tam=7.5, fondo=color)

    def opciones(self, clave, n, fila_texto):
        datos = O.OPCIONES[clave][n]
        titulo = datos.get('titulo') or '[' + (etiqueta_hueco(fila_texto, n) or '') + ']'
        _keep(self.p(PB._run(f'{n}  ', negrita=True, color=PB.NARANJA_BORDE, tam=10)
                     + PB._run(titulo, negrita=True, color=PB.VERDE_AZ, tam=10), antes=100, despues=40,
                     ind='<w:ind w:left="120"/>'), 'w:keepNext')
        for cita, fuente in datos.get('norma', []):
            _keep(self.p(self.insignia('N') + PB._run('  ' + cita, tam=9.5, color=PB.AZUL, cursiva=True)
                         + PB._run('  (' + fuente + ')', tam=8.5, color=PB.GRIS_TXT), despues=50, alin='both',
                         ind='<w:ind w:left="440"/>'), 'w:keepNext', 'w:keepLines')
        k = 0
        for op in datos['ops']:
            nivel, texto = op[0], op[1]
            elementos = op[2] if len(op) > 2 else []
            if nivel in 'CD':
                k += 1
            el = self.p(self.insignia(nivel, k) + PB._run('  ', tam=9.5) + rico(texto), despues=20 if elementos else 40,
                        alin='both', ind='<w:ind w:left="440"/>')
            _keep(_apretado(el), 'w:keepLines', *(('w:keepNext',) if elementos else ()))
            for i, e in enumerate(elementos):
                el = self.p(PB._run('•', color=PB.NARANJA_BORDE, tam=9.5) + '<w:r><w:tab/></w:r>' + rico(e),
                            despues=8 if i + 1 < len(elementos) else 50, alin='both',
                            ind='<w:ind w:left="760" w:hanging="220"/>')
                _keep(_apretado(el), 'w:keepLines')
        if datos.get('nota'):
            self.p(rico(datos['nota'], tam=9), despues=60, ind='<w:ind w:left="440"/>')

    def apartado(self, clave):
        datos = O.PLANTILLAS[clave]
        self.titulo(datos['titulo'])
        for i, fila in enumerate(datos['filas']):
            if fila.get('etiqueta'):
                _keep(self.p(PB._run(fila['etiqueta'], negrita=True, versalitas=True, color=PB.AZUL, tam=8.5),
                             antes=140, despues=40), 'w:keepNext')
            self.cuadro(runs_plantilla(fila['texto'], tam=10.5), 'Plantilla de redacción' if i == 0 else None)
            vistos = []
            for m in re.finditer(r'[\[{](\d+)\|', fila['texto']):
                n = int(m.group(1))
                if n not in vistos:
                    vistos.append(n)
                    self.opciones(clave, n, fila['texto'])
            self.p('', despues=30)

    def tabla_elementos(self):
        _keep(self.p(PB._run('Tabla de elementos curriculares de quinto', negrita=True, color=PB.AZUL, tam=12),
                     antes=160, despues=40), 'w:keepNext')
        leyenda = PB._run('Con los colores de las áreas de la programación: ', tam=9, color=PB.GRIS_TXT, cursiva=True)
        for area, nombre in (('CMN', 'Conocimiento del Medio'), ('LCL', 'Lengua'), ('MAT', 'Matemáticas'),
                             ('EAR', 'Educación Artística')):
            fuerte, _, texto = AREA[area]
            leyenda += PB._run(f' {nombre} ', tam=8.5, negrita=True, color=texto, fondo=fuerte) + PB._run(' ', tam=9)
        _keep(self.p(leyenda, despues=40), 'w:keepNext')
        _keep(self.p(PB._run('Una competencia por fila, con su criterio de quinto, un saber vinculado a ese criterio y dos '
                             'descriptores, comprobados en el BOJA; los textos son resúmenes. El área eje, entera; la '
                             'segunda, solo la competencia.', tam=9, color=PB.GRIS_TXT, cursiva=True), despues=80,
                     alin='both'), 'w:keepNext')
        cab = ['Área', 'Competencia específica', 'Criterio de 5.º', 'Un saber básico', 'Descriptores']
        anchos = [1.2, 5.0, 4.4, 4.6, 2.2]
        filas = [list(f) for f in T.ELEMENTOS]
        t = self.d.add_table(rows=len(filas) + 1, cols=len(cab))
        t.autofit = False
        tbl = t._tbl
        for i, w in enumerate(anchos):
            tbl.tblGrid.gridCol_lst[i].w = Cm(w)
        for r_i, row in enumerate(t.rows):
            row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
            if r_i == 0:
                row._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
            for c_i, celda in enumerate(row.cells):
                celda.width = Cm(anchos[c_i])
                PB._limpia_celda(celda._tc)
                tcpr = celda._tc.get_or_add_tcPr()
                b = OxmlElement('w:tcBorders')
                for lado in ('top', 'left', 'bottom', 'right'):
                    e = OxmlElement(f'w:{lado}')
                    e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:color'), 'FFFFFF')
                    b.append(e)
                tcpr.append(b)
                PB._margenes(celda._tc, 80, 80, 30, 30)
                if r_i == 0:
                    PB._fondo(celda._tc, PB.AZUL)
                    celda._tc.append(PB._parrafo_xml(PB._run(cab[c_i], negrita=True, color='FFFFFF', tam=8.5),
                                                     despues=0))
                    continue
                area = filas[r_i - 1][0]
                fuerte, suave, texto = AREA[area]
                PB._fondo(celda._tc, fuerte if c_i == 0 else suave)
                celda._tc.append(PB._parrafo_xml(
                    PB._run(filas[r_i - 1][c_i], tam=8.5, negrita=c_i == 0, color=texto if c_i == 0 else '222B33'),
                    despues=0))
        self._anade(tbl)
        self.p('', despues=60)

    def orientaciones(self):
        """La tabla de orientaciones de la primera versión, sin salto de página."""
        n_antes = len(self.d.element.body.findall(qn('w:p')))
        super().orientaciones()
        for par in self.d.element.body.findall(qn('w:p'))[n_antes:]:
            ppr = par.find(qn('w:pPr'))
            if ppr is not None:
                for pb in ppr.findall(qn('w:pageBreakBefore')):
                    ppr.remove(pb)
        self.p('', despues=60)


def main():
    PB.UTIL = ANCHO                       # la tabla de orientaciones, al ancho de la página vertical
    c = Plantillas()
    c.portada()
    for clave in ('7.1', '7.2', '7.3', '7.5', '7.6', '7.7', '7.8', '7.9'):
        c.apartado(clave)
        if clave == '7.7':
            c.tabla_elementos()
        if clave == '7.8':
            c.orientaciones()
    PB.ordena_esquema(c.d.element.body)
    zoom = c.d.settings.element.find(qn('w:zoom'))
    if zoom is not None and zoom.get(qn('w:percent')) is None:
        zoom.set(qn('w:percent'), '100')
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    c.d.save(SALIDA)
    print(SALIDA)


if __name__ == '__main__':
    main()
