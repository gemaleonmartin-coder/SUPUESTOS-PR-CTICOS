# -*- coding: utf-8 -*-
"""Word de plantillas por importancia, segunda versión (fase 38, quinta vuelta).

Cambios pedidos por Gem sobre la primera versión: sin saltos de página entre apartados; lo fijo, dentro del cuadro
y sin nada debajo; muchos más ejemplos y comodines (con ◆ los diferenciadores); el texto de la norma, literal, con su
etiqueta; y la tabla de elementos curriculares con los colores de las áreas de la programación.

Uso:  python3 scripts/plantillas_por_importancia_2.py   →   libreta-magica/Plantillas_por_importancia_v22_5.docx
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

SALIDA = os.path.join(PB.RAIZ, 'libreta-magica', 'Plantillas_por_importancia_v22_5.docx')   # v22_4: la anterior
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

    # ------------------------------------------------------------------------------------------- portada
    # Distinta de la de la libreta (allí, un bloque azul marino arriba): una banda vertical verde petróleo a la
    # izquierda, el título en serif, el índice con sus páginas y la leyenda en un recuadro; mismo tono académico.
    PETROLEO, CREMA_BANDA, TINTA = '1D4E59', 'F3E9D2', '1F2D33'
    INDICE = [('7.1. Introducción', '7.1. Introducción'),
              ('7.2. Contexto: entorno, centro y alumnado', '7.2. Contexto'),
              ('7.3. Justificación normativa y epistemológica', '7.3. Justificación'),
              ('7.5. Intervención a nivel de centro', '7.5. Intervención'),
              ('7.6. Intervención a nivel de aula: datos identificativos', '7.6. Intervención'),
              ('7.7. Concreción curricular y tabla de elementos', '7.7. Concreción'),
              ('7.8. Metodología y orientaciones de cada área', '7.8. Metodología'),
              ('7.9. Secuencia didáctica', '7.9. Secuencia')]

    @staticmethod
    def _r(t, fuente='Calibri', tam=10.5, color='1F2D33', b=False, i=False, esp=None):
        t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        return (f'<w:r><w:rPr><w:rFonts w:ascii="{fuente}" w:hAnsi="{fuente}" w:cs="{fuente}"/>' + ('<w:b/>' if b else '')
                + ('<w:i/>' if i else '') + f'<w:color w:val="{color}"/>' + (f'<w:spacing w:val="{esp}"/>' if esp else '')
                + f'<w:sz w:val="{int(tam * 2)}"/></w:rPr><w:t xml:space="preserve">{t}</w:t></w:r>')

    @staticmethod
    def _pp(runs, antes=0, despues=0, linea=259, jc='left', extra=''):
        return (f'<w:p><w:pPr>{extra}<w:spacing w:before="{antes}" w:after="{despues}" w:line="{linea}" '
                f'w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>{runs}</w:p>')

    def portada(self, paginas=None):
        paginas = paginas or {}
        r, pp = self._r, self._pp
        ancho_total = int(ANCHO * 567)
        banda, cuerpo = 794, ancho_total - 794
        tab = cuerpo - 567 - 120
        indice = ''.join(
            pp(r(t, tam=10.5, color=self.TINTA) + '<w:r><w:tab/></w:r>'
               + r(str(paginas.get(t, '')), tam=10.5, color=self.PETROLEO, b=True), despues=70,
               extra=f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{tab}"/></w:tabs>')
            for t, _ in self.INDICE)
        leyenda = ''
        for nivel, texto in (('1', 'la más importante; si depende del área, una por área.'),
                             ('C', 'por si no encaja la primera, en orden de utilidad.'),
                             ('D', 'el comodín diferenciador, el que sorprende al tribunal.'),
                             ('N', 'el texto de la norma, copiado tal cual, para estudiarlo.')):
            etq, color = INSIGNIA[nivel]
            leyenda += pp(PB._run(etq.format(n=1), negrita=True, color='FFFFFF', tam=8, fondo=color)
                          + r('  ' + texto, tam=10), despues=50)
        leyenda += pp(r('El número naranja de cada hueco lleva a sus opciones, justo debajo del cuadro. Lo fijo va en el '
                        'cuadro y no lleva nada debajo. En gris, de dónde sale cada ejemplo o cómo se usa. En el 4.1, los '
                        'bloques «según el supuesto» van del más frecuente al menos. Los autores se concretarán con los '
                        'temas.', tam=9.5, color='4A5A60'), antes=60, jc='both')
        caja = (f'<w:tbl><w:tblPr><w:tblW w:w="{cuerpo - 567}" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
                f'<w:tblCellMar><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar></w:tblPr>'
                f'<w:tblGrid><w:gridCol w:w="{cuerpo - 567}"/></w:tblGrid><w:tr><w:trPr><w:cantSplit/></w:trPr><w:tc>'
                f'<w:tcPr><w:tcW w:w="{cuerpo - 567}" w:type="dxa"/><w:tcBorders><w:top w:val="single" w:sz="4" '
                f'w:space="0" w:color="{self.PETROLEO}"/><w:left w:val="single" w:sz="4" w:space="0" '
                f'w:color="{self.PETROLEO}"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="{self.PETROLEO}"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{self.PETROLEO}"/></w:tcBorders>'
                f'<w:shd w:val="clear" w:color="auto" w:fill="F4F8F8"/><w:tcMar><w:top w:w="160" w:type="dxa"/>'
                f'<w:left w:w="220" w:type="dxa"/><w:bottom w:w="140" w:type="dxa"/><w:right w:w="220" w:type="dxa"/>'
                f'</w:tcMar></w:tcPr>'
                + pp(r('CÓMO SE LEE', tam=9, color=self.PETROLEO, b=True, esp=40), despues=100) + leyenda
                + '</w:tc></w:tr></w:tbl>')
        raya = (f'<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="1" w:color="{self.PETROLEO}"/></w:pBdr>'
                f'<w:ind w:right="3400"/>')
        contenido = (pp(r('MATERIAL DE ESTUDIO · SUPUESTOS PRÁCTICOS', tam=9, color=PB.NARANJA_BORDE, b=True,
                          esp=40), antes=600)
                     + pp(r('Plantillas', fuente='Cambria', tam=44, color=self.PETROLEO, b=True), antes=260, linea=240)
                     + pp(r('por importancia', fuente='Cambria', tam=44, color=self.PETROLEO, b=True), linea=240)
                     + pp(r(' ', tam=4), antes=0, linea=240, despues=0, extra=raya)
                     + pp(r('La plantilla de cada apartado de la libreta mágica y, para cada hueco, las opciones ordenadas '
                            'de lo esencial a lo complementario, con la norma copiada tal cual', fuente='Cambria',
                            tam=14, color='4A5A60', i=True), antes=300, despues=0, extra='<w:ind w:right="900"/>')
                     + pp(r('CONTENIDO', tam=9, color=self.PETROLEO, b=True, esp=40), antes=800, despues=140)
                     + indice
                     + pp('', antes=500) + caja
                     + pp(r('Educación Primaria · Andalucía · Convocatoria de 2027', tam=10.5, color=self.PETROLEO,
                            b=True), antes=700)
                     + pp(r('Versión 2.2, quinta edición de las plantillas · 20 de noviembre de 2026 · Acompaña a la '
                            'libreta mágica 2.2. Material de estudio personal.', tam=8.5, color='5B6770', i=True),
                          antes=60))
        texto_banda = pp(r('SUPUESTOS PRÁCTICOS  ·  EDUCACIÓN PRIMARIA  ·  ANDALUCÍA 2027', tam=9, color=self.CREMA_BANDA,
                           b=True, esp=60), jc='center')
        tabla = (f'<w:tbl {PB.NS}><w:tblPr><w:tblW w:w="{ancho_total}" w:type="dxa"/><w:tblLayout w:type="fixed"/>'
                 f'<w:tblCellMar><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>'
                 f'</w:tblPr><w:tblGrid><w:gridCol w:w="{banda}"/><w:gridCol w:w="{cuerpo}"/></w:tblGrid>'
                 f'<w:tr><w:trPr><w:cantSplit/><w:trHeight w:val="14300" w:hRule="exact"/></w:trPr>'
                 f'<w:tc><w:tcPr><w:tcW w:w="{banda}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" '
                 f'w:fill="{self.PETROLEO}"/><w:textDirection w:val="btLr"/><w:vAlign w:val="center"/></w:tcPr>'
                 f'{texto_banda}</w:tc>'
                 f'<w:tc><w:tcPr><w:tcW w:w="{cuerpo}" w:type="dxa"/><w:tcMar><w:top w:w="0" w:type="dxa"/>'
                 f'<w:left w:w="567" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/>'
                 f'</w:tcMar></w:tcPr>{contenido}</w:tc></w:tr></w:tbl>')
        self._anade(parse_xml(tabla))
        self.d.sections[0].different_first_page_header_footer = True     # sin cabecera ni pie en la portada

    def titulo(self, texto, salto=False):
        el = self.p(PB._run(texto, negrita=True, color=PB.VERDE_AZ, tam=14), antes=0 if salto else 160, despues=80)
        if salto:
            _keep(el, 'w:pageBreakBefore')
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

    def apartado(self, clave, salto=False):
        datos = O.PLANTILLAS[clave]
        self.titulo(datos['titulo'], salto)
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


def construye(paginas=None):
    PB.UTIL = ANCHO                       # la tabla de orientaciones, al ancho de la página vertical
    c = Plantillas()
    c.portada(paginas)
    for clave in ('7.1', '7.2', '7.3', '7.5', '7.6', '7.7', '7.8', '7.9'):
        c.apartado(clave, salto=clave == '7.1')
        if clave == '7.7':
            c.tabla_elementos()
        if clave == '7.8':
            c.orientaciones()
    PB.ordena_esquema(c.d.element.body)
    # sin párrafos vacíos al final, para que no salga una página en blanco detrás de la última
    cuerpo = c.d.element.body
    hijos = [h for h in cuerpo if h.tag != qn('w:sectPr')]
    while (len(hijos) > 1 and hijos[-1].tag == qn('w:p') and hijos[-2].tag == qn('w:p')
           and not ''.join(t.text or '' for t in hijos[-1].iter(qn('w:t')))
           and hijos[-1].find('.//' + qn('w:drawing')) is None and hijos[-1].find('.//' + qn('w:sectPr')) is None):
        cuerpo.remove(hijos.pop())
    zoom = c.d.settings.element.find(qn('w:zoom'))
    if zoom is not None and zoom.get(qn('w:percent')) is None:
        zoom.set(qn('w:percent'), '100')
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    c.d.save(SALIDA)


def paginas_del_indice():
    """Página de cada apartado, con LibreOffice (la portada es la página 1)."""
    import subprocess
    import tempfile
    tmp = tempfile.mkdtemp()
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, SALIDA], capture_output=True)
    pdf = os.path.join(tmp, os.path.basename(SALIDA).replace('.docx', '.pdf'))
    pags = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
    res = {}
    for texto, busca in Plantillas.INDICE:
        for k, pagina in enumerate(pags[1:], start=2):
            if any(l.strip().startswith(busca) for l in pagina.split('\n')):
                res[texto] = k
                break
    return res


def main():
    construye()
    paginas = paginas_del_indice()
    construye(paginas)
    print(SALIDA, paginas)


if __name__ == '__main__':
    main()
