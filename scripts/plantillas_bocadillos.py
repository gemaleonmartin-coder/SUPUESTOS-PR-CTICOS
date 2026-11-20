# -*- coding: utf-8 -*-
"""Word de plantillas con bocadillos (fase 38): solo las plantillas amarillas de la Parte I de la libreta mágica
(7.1 a 7.8 y la frase que pasa al 7.9), con bocadillos dibujados al lado de cada párrafo.

Uso:  python3 scripts/plantillas_bocadillos.py   →   libreta-magica/Plantillas_con_bocadillos_v22.docx
Los textos están en textos_libreta_v22.py. Los bocadillos son formas de Word (llamada rectangular redondeada) en
línea, con el texto dentro; su alto se calcula midiendo el texto con Carlito (métrica de Calibri). Todas las medidas
de dibujo van en números enteros (Word no abre el archivo si llevan decimales).
"""
import os
import re
import sys
from xml.sax.saxutils import escape

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textos_libreta_v22 as T  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, 'libreta-magica', 'Plantillas_con_bocadillos_v22.docx')

# Colores de la libreta de Rafa
AZUL, VERDE_AZ, CREMA, NARANJA_BORDE, GRIS_TXT = '1F3A5F', '2A7F8E', 'FDF6E8', 'C98A1B', '595959'
BOC_FONDO, BOC_BORDE = 'E8F3F5', '2A7F8E'
FIJO_FONDO, FIJO_BORDE = 'FBEBCB', 'C98A1B'
NARANJA = 'FFC000'
FUENTE = 'Calibri'
EMU_CM = 360000

ANCHO_LADO, ANCHO_CENTRO = 8.6, 9.5       # cm (A4 apaisado con márgenes de 1,5 cm: 26,7 cm útiles)
BOC_ANCHO, COLA = 7.9, 0.35                # cm
UTIL = 26.7
INS_LR, INS_TB = 0.18, 0.12                # cm
TAM_BOC = 8                              # pt
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
      'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"')

_F = {b: ImageFont.truetype(f'/usr/share/fonts/truetype/crosextra/Carlito-{"Bold" if b else "Regular"}.ttf', 100)
      for b in (False, True)}


def _lineas(texto, ancho_cm, tam_pt, negrita=False):
    """Número de líneas que ocupa un texto en un ancho dado (ajuste por palabras)."""
    lim = ancho_cm / 2.54 * 72 / tam_pt * 100     # ancho en unidades de la fuente medida a 100 px = tam_pt
    f, n, linea = _F[negrita], 1, ''
    for pal in texto.split():
        prueba = (linea + ' ' + pal).strip()
        if f.getlength(prueba) <= lim:
            linea = prueba
        else:
            n, linea = n + 1, pal
    return n


def _rpr(color=None, negrita=False, tam=None, cursiva=False, versalitas=False, sup=False, fondo=None):
    x = f'<w:rPr><w:rFonts w:ascii="{FUENTE}" w:hAnsi="{FUENTE}" w:cs="{FUENTE}"/>'
    if negrita:
        x += '<w:b/>'
    if cursiva:
        x += '<w:i/>'
    if versalitas:
        x += '<w:caps/>'
    if color:
        x += f'<w:color w:val="{color}"/>'
    if versalitas:
        x += '<w:spacing w:val="20"/>'
    if tam:
        x += f'<w:sz w:val="{int(round(tam * 2))}"/>'
    if fondo:
        x += f'<w:shd w:val="clear" w:color="auto" w:fill="{fondo}"/>'
    if sup:
        x += '<w:vertAlign w:val="superscript"/>'
    return x + '</w:rPr>'


def _run(texto, **kw):
    return f'<w:r>{_rpr(**kw)}<w:t xml:space="preserve">{escape(texto)}</w:t></w:r>'


def alto_bocadillo(num, titulo, tipo, lineas):
    """Alto (cm) que necesita un bocadillo para su texto."""
    ancho_txt = BOC_ANCHO - 2 * INS_LR
    alto_linea = TAM_BOC * 1.31 / 72 * 2.54                       # cm
    n_lin = _lineas(f'{num}  {titulo}  {tipo}', ancho_txt - 0.2, TAM_BOC, True)
    n_lin += sum(_lineas('• ' + l, ancho_txt - 0.45, TAM_BOC) for l in lineas)
    alto = 2 * INS_TB + n_lin * alto_linea + (len(lineas) + 1) * 1.5 / 72 * 2.54
    return alto * 1.14 + 0.2


def bocadillo(n_id, num, titulo, tipo, lineas, lado='der'):
    """Run con una forma de llamada (bocadillo) en línea; la cola apunta a la plantilla (al centro)."""
    fijo = tipo == 'FIJO'
    alto = alto_bocadillo(num, titulo, tipo, lineas)
    cx, cy = round(BOC_ANCHO * EMU_CM), round(alto * EMU_CM)
    cola = round(COLA * EMU_CM)
    adj1 = round((0.5 + COLA / BOC_ANCHO) * 100000) * (1 if lado == 'izq' else -1)
    adj2 = round((min(0.32, alto / 2) / alto - 0.5) * 100000)
    fondo, borde = (FIJO_FONDO, FIJO_BORDE) if fijo else (BOC_FONDO, BOC_BORDE)
    sp = '<w:pPr><w:spacing w:before="0" w:after="30" w:line="240" w:lineRule="auto"/></w:pPr>'
    cab = (f'<w:p>{sp}{_run(str(num) + "  ", negrita=True, color=borde, tam=TAM_BOC)}'
           f'{_run(titulo, negrita=True, color=AZUL, tam=TAM_BOC)}'
           f'{_run("  " + tipo.lower(), versalitas=True, color=borde, tam=TAM_BOC - 1)}</w:p>')
    cuerpo = ''.join(
        f'<w:p><w:pPr><w:spacing w:before="0" w:after="30" w:line="240" w:lineRule="auto"/>'
        f'<w:ind w:left="142" w:hanging="142"/></w:pPr>{_run("• ", color=borde, tam=TAM_BOC)}'
        f'{_run(l, tam=TAM_BOC, color="262626")}</w:p>' for l in lineas)
    return (f'<w:r {NS}><mc:AlternateContent><mc:Choice Requires="wps"><w:drawing>'
            f'<wp:inline distT="0" distB="72000" distL="0" distR="0">'
            f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="{0 if lado == "izq" else cola}" t="0" '
            f'r="{cola if lado == "izq" else 0}" b="0"/>'
            f'<wp:docPr id="{n_id}" name="Bocadillo {n_id}"/><wp:cNvGraphicFramePr/>'
            f'<a:graphic><a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">'
            f'<wps:wsp><wps:cNvSpPr/><wps:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="wedgeRoundRectCallout"><a:avLst><a:gd name="adj1" fmla="val {adj1}"/>'
            f'<a:gd name="adj2" fmla="val {adj2}"/><a:gd name="adj3" fmla="val 16667"/></a:avLst></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{fondo}"/></a:solidFill><a:ln w="12700"><a:solidFill>'
            f'<a:srgbClr val="{borde}"/></a:solidFill></a:ln></wps:spPr>'
            f'<wps:txbx><w:txbxContent>{cab}{cuerpo}</w:txbxContent></wps:txbx>'
            f'<wps:bodyPr rot="0" vert="horz" wrap="square" lIns="{round(INS_LR * EMU_CM)}" '
            f'tIns="{round(INS_TB * EMU_CM)}" rIns="{round(INS_LR * EMU_CM)}" bIns="{round(INS_TB * EMU_CM)}" '
            f'anchor="t" anchorCtr="0"><a:noAutofit/></wps:bodyPr></wps:wsp></a:graphicData></a:graphic>'
            f'</wp:inline></w:drawing></mc:Choice></mc:AlternateContent></w:r>')


ORDEN_TCPR = ['cnfStyle', 'tcW', 'gridSpan', 'hMerge', 'vMerge', 'tcBorders', 'shd', 'noWrap', 'tcMar',
              'textDirection', 'tcFitText', 'vAlign', 'hideMark']
ORDEN_PPR = ['pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr', 'widowControl', 'numPr',
             'suppressLineNumbers', 'pBdr', 'shd', 'tabs', 'suppressAutoHyphens', 'kinsoku', 'wordWrap',
             'overflowPunct', 'topLinePunct', 'autoSpaceDE', 'autoSpaceDN', 'bidi', 'adjustRightInd', 'snapToGrid',
             'spacing', 'ind', 'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc', 'textDirection',
             'textAlignment', 'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr', 'sectPr', 'pPrChange']
ORDEN_TBLPR = ['tblStyle', 'tblpPr', 'tblOverlap', 'bidiVisual', 'tblStyleRowBandSize', 'tblStyleColBandSize', 'tblW',
               'jc', 'tblCellSpacing', 'tblInd', 'tblBorders', 'shd', 'tblLayout', 'tblCellMar', 'tblLook']


def ordena_esquema(body):
    """Pone los hijos de w:tcPr y w:tblPr en el orden del esquema (Word es estricto; LibreOffice, no)."""
    for etiqueta, orden in (('w:tcPr', ORDEN_TCPR), ('w:tblPr', ORDEN_TBLPR), ('w:pPr', ORDEN_PPR)):
        for el in body.iter(qn(etiqueta)):
            hijos = list(el)
            hijos.sort(key=lambda h: orden.index(h.tag.split('}')[1]) if h.tag.split('}')[1] in orden else 99)
            for h in hijos:
                el.remove(h)
            for h in hijos:
                el.append(h)


TROZO = re.compile(r'\[(\d+)\|([^\]]*)\]|\{(\d+)\|([^}]*)\}|\[([^\]]*)\]')


def runs_plantilla(texto, tam=10.5):
    """Runs de un párrafo de plantilla: huecos en verde azulado y en negrita, número del bocadillo en superíndice."""
    out, pos = [], 0
    for m in TROZO.finditer(texto):
        if m.start() > pos:
            out.append(_run(texto[pos:m.start()], tam=tam, color='262626'))
        if m.group(1):          # hueco con bocadillo
            out.append(_run('[' + m.group(2) + ']', negrita=True, color=VERDE_AZ, tam=tam))
            out.append(_run(m.group(1), negrita=True, color=NARANJA_BORDE, tam=tam, sup=True))
        elif m.group(3):        # texto fijo con bocadillo
            out.append(_run(m.group(4), tam=tam, color='262626'))
            out.append(_run(m.group(3), negrita=True, color=NARANJA_BORDE, tam=tam, sup=True))
        else:                   # hueco sin bocadillo
            out.append(_run('[' + m.group(5) + ']', negrita=True, color=VERDE_AZ, tam=tam))
        pos = m.end()
    if pos < len(texto):
        out.append(_run(texto[pos:], tam=tam, color='262626'))
    return ''.join(out)


def _bordes_celda(tc, izq=None, resto_nada=True):
    tcpr = tc.get_or_add_tcPr()
    b = OxmlElement('w:tcBorders')
    for lado in ('top', 'left', 'bottom', 'right'):
        e = OxmlElement(f'w:{lado}')
        if lado == 'left' and izq:
            e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '24'); e.set(qn('w:color'), izq)
        else:
            e.set(qn('w:val'), 'nil')
        b.append(e)
    tcpr.append(b)


def _fondo(tc, color):
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), color)
    tc.get_or_add_tcPr().append(shd)


def _margenes(tc, izq, der, arr=60, aba=60):
    m = OxmlElement('w:tcMar')
    for lado, v in (('top', arr), ('left', izq), ('bottom', aba), ('right', der)):
        e = OxmlElement(f'w:{lado}'); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa'); m.append(e)
    tc.get_or_add_tcPr().append(m)


def _parrafo_xml(contenido, antes=0, despues=80, ind=None, alin=None):
    ppr = f'<w:pPr><w:spacing w:before="{antes}" w:after="{despues}" w:line="259" w:lineRule="auto"/>'
    if ind:
        ppr += ind
    if alin:
        ppr += f'<w:jc w:val="{alin}"/>'
    ppr += '</w:pPr>'
    return parse_xml(f'<w:p {NS}>{ppr}{contenido}</w:p>')


def _limpia_celda(tc):
    for p in list(tc.findall(qn('w:p'))):
        tc.remove(p)


class Constructor:
    def __init__(self, apaisado=False):
        self.d = Document()
        self.n_id = 100
        self.uso = {'izq': 0.0, 'der': 0.0}
        s = self.d.sections[0]
        if apaisado:
            s.orientation = WD_ORIENT.LANDSCAPE
            s.page_width, s.page_height = Cm(29.7), Cm(21)
            s.left_margin = s.right_margin = Cm(1.5)
            s.top_margin, s.bottom_margin = Cm(1.6), Cm(1.4)
        else:
            s.page_width, s.page_height = Cm(21), Cm(29.7)
            s.orientation = WD_ORIENT.PORTRAIT
            s.left_margin = s.right_margin = Cm(1.8)
            s.top_margin, s.bottom_margin = Cm(2.0), Cm(1.8)
        st = self.d.styles['Normal']
        st.font.name, st.font.size = FUENTE, Pt(10.5)
        st.element.rPr.rFonts.set(qn('w:eastAsia'), FUENTE)
        st.paragraph_format.space_after = Pt(4)
        self._cabecera_pie()
        self.d.element.body.remove(self.d.paragraphs[0]._p) if self.d.paragraphs else None

    def _cabecera_pie(self):
        s = self.d.sections[0]
        h = s.header.paragraphs[0]
        h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        h._p.append(parse_xml(f'<w:r {NS}>{_rpr(negrita=True, color=AZUL, tam=8)}<w:t xml:space="preserve">'
                              f'Libreta mágica</w:t></w:r>'))
        h._p.append(parse_xml(f'<w:r {NS}>{_rpr(color=GRIS_TXT, tam=8)}<w:t xml:space="preserve">  ·  Plantillas '
                              f'con bocadillos · Educación Primaria · Andalucía 2027</w:t></w:r>'))
        f = s.footer.paragraphs[0]
        f.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f._p.append(parse_xml(f'<w:r {NS}>{_rpr(color=GRIS_TXT, tam=8)}<w:t xml:space="preserve">Página </w:t></w:r>'))
        for campo in ('PAGE', None, 'NUMPAGES'):
            if campo is None:
                f._p.append(parse_xml(f'<w:r {NS}>{_rpr(color=GRIS_TXT, tam=8)}<w:t xml:space="preserve"> de '
                                      f'</w:t></w:r>'))
                continue
            f._p.append(parse_xml(f'<w:fldSimple {NS} w:instr="{campo}"><w:r>{_rpr(color=GRIS_TXT, tam=8)}'
                                  f'<w:t>1</w:t></w:r></w:fldSimple>'))

    def _anade(self, el):
        """Añade al cuerpo justo antes de w:sectPr (después, Word no lo admite)."""
        self.d.element.body.find(qn('w:sectPr')).addprevious(el)

    def p(self, contenido, **kw):
        el = _parrafo_xml(contenido, **kw)
        self._anade(el)
        return el

    def portada(self):
        self.p(_run('SUPUESTOS PRÁCTICOS · PARTE A', versalitas=True, color=NARANJA_BORDE, tam=9, negrita=True),
               antes=600, despues=120)
        self.p(_run('Plantillas con bocadillos', negrita=True, color=AZUL, tam=26), despues=60)
        self.p(_run('Las plantillas de redacción de la Parte I de la libreta mágica (apartados 7.1 a 7.9), con el '
                    'contenido de cada hueco a los lados, para estudiar los supuestos desde aquí', color=VERDE_AZ, tam=12), despues=240)
        self.p(_run('Cómo se lee', negrita=True, color=AZUL, tam=12), despues=60)
        for texto in (
                'Cada plantilla va en el centro, en amarillo, igual que en la libreta. A los dos lados, los bocadillos '
                'del mismo párrafo, con la cola hacia la plantilla.',
                'El número naranja de un hueco es el número de su bocadillo.',
                'Bocadillo naranja, «fijo»: se memoriza y se escribe tal cual. Bocadillo verde, «ideas»: se elige o '
                'se adapta una. Los bocadillos traen el contenido para estudiar; solo los autores se concretarán con '
                'los temas.',
                'En el 4.1, los bloques «siempre» van en todos los supuestos; de los bloques «según el supuesto», '
                'solo uno o dos, los que pida el enunciado.'):
            self.p(_run('•  ', color=NARANJA_BORDE, tam=10.5) + _run(texto, tam=10.5, color='262626'),
                   ind='<w:ind w:left="284" w:hanging="284"/>', despues=60)
        self.p(_run('Versión 2.2 · 20 de noviembre de 2026 · Acompaña a la libreta mágica 2.2. Material de estudio '
                    'personal.', color=GRIS_TXT, tam=8.5, cursiva=True), antes=360)

    def titulo(self, texto, salto=True):
        el = self.p(_run(texto, negrita=True, color=VERDE_AZ, tam=14), antes=0, despues=120)
        if salto:
            el.find(qn('w:pPr')).insert(0, OxmlElement('w:pageBreakBefore'))
        return el

    def plantilla(self, clave):
        """Una fila por párrafo de la plantilla: el párrafo en el centro y sus bocadillos justo a sus lados, a
        izquierda y derecha, equilibrados dentro de la fila. Si un párrafo solo tiene un bocadillo y es mucho más alto
        que el párrafo, el bocadillo se parte en dos mitades, una a cada lado."""
        datos = T.PLANTILLAS[clave]
        boc = T.BOCADILLOS.get(clave, {})
        self.titulo(datos['titulo'])
        filas = datos['filas']
        anchos = (ANCHO_LADO, ANCHO_CENTRO, ANCHO_LADO)
        t = self.d.add_table(rows=len(filas), cols=3)
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        t.autofit = False
        tbl = t._tbl
        tblw = tbl.tblPr.find(qn('w:tblW'))
        tblw.set(qn('w:type'), 'dxa'); tblw.set(qn('w:w'), str(round(sum(anchos) / 2.54 * 1440)))
        for i, w in enumerate(anchos):
            tbl.tblGrid.gridCol_lst[i].w = Cm(w)
        for r_i, (row, fila) in enumerate(zip(t.rows, filas)):
            row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))   # cada párrafo con sus bocadillos, junto
            izq, cen, der = row.cells
            for c, w in zip(row.cells, anchos):
                c.width = Cm(w)
                _limpia_celda(c._tc)
            reubicar = fila.get('reubicar')
            _bordes_celda(izq._tc)
            _bordes_celda(der._tc)
            _bordes_celda(cen._tc, izq=('BFBFBF' if reubicar else NARANJA_BORDE))
            _fondo(cen._tc, 'EDEDED' if reubicar else CREMA)
            va = OxmlElement('w:vAlign'); va.set(qn('w:val'), 'center'); cen._tc.get_or_add_tcPr().append(va)
            ultima = r_i == len(filas) - 1
            _margenes(cen._tc, 220, 220, 90 if r_i == 0 else 20, 90 if ultima else 20)
            _margenes(izq._tc, 0, 120, 40, 60)
            _margenes(der._tc, 120, 0, 40, 60)
            if r_i == 0:
                cen._tc.append(_parrafo_xml(_run('Plantilla de redacción', versalitas=True, negrita=True,
                                                 color=NARANJA_BORDE, tam=8.5), despues=60))
            if fila.get('etiqueta'):
                color = '7F7F7F' if reubicar else AZUL
                txt = ('⚠ ' + fila['etiqueta']) if reubicar else fila['etiqueta']
                cen._tc.append(_parrafo_xml(_run(txt, negrita=True, versalitas=True, color=color, tam=8.5),
                                            antes=100, despues=40))
            cen._tc.append(_parrafo_xml(runs_plantilla(fila['texto'], tam=10.5), despues=100, alin='both'))
            if reubicar:
                cen._tc.append(_parrafo_xml(_run(T.NOTA_REUBICAR, cursiva=True, color='7F7F7F', tam=9.5),
                                            despues=60, alin='both'))
            # bocadillos de este párrafo
            nums = [int(m) for m in re.findall(r'[\[{](\d+)\|', fila['texto'])]
            texto_plano = re.sub(r'[\[\]{}|\d]', '', fila['texto'])
            alto_texto = _lineas(texto_plano, ANCHO_CENTRO - 0.8, 10.5) * 10.5 * 1.3 / 72 * 2.54 + 0.5
            piezas = [(n,) + tuple(boc[n]) for n in nums]
            if len(piezas) == 1:
                n, titulo, tipo, lineas = piezas[0]
                if len(lineas) >= 4 and alto_bocadillo(n, titulo, tipo, lineas) > 1.5 * alto_texto:
                    mitad = (len(lineas) + 1) // 2
                    piezas = [(n, titulo + ' (1/2)', tipo, lineas[:mitad]),
                              (n, titulo + ' (2/2)', tipo, lineas[mitad:])]
            lados = {'izq': [], 'der': []}
            if len(piezas) == 2 and piezas[0][0] == piezas[1][0]:          # bocadillo partido
                lados['izq'], lados['der'] = [piezas[0]], [piezas[1]]
            else:
                alto = {'izq': 0.0, 'der': 0.0}
                for pz in sorted(piezas, key=lambda q: -alto_bocadillo(*q)):
                    if abs(alto['izq'] - alto['der']) < 0.01:
                        lado = 'izq' if self.uso['izq'] <= self.uso['der'] else 'der'
                    else:
                        lado = 'izq' if alto['izq'] < alto['der'] else 'der'
                    alto[lado] += alto_bocadillo(*pz) + 0.2
                    self.uso[lado] += alto_bocadillo(*pz)
                    lados[lado].append(pz)
            for lado, celda in (('izq', izq), ('der', der)):
                for n, titulo, tipo, lineas in sorted(lados[lado], key=lambda q: (q[0], q[1])):
                    self.n_id += 1
                    par = _parrafo_xml('', despues=0, alin='right' if lado == 'izq' else None)
                    par.append(parse_xml(bocadillo(self.n_id, n, titulo, tipo, lineas, lado)))
                    celda._tc.append(par)
                if not lados[lado]:
                    celda._tc.append(_parrafo_xml('', despues=0))
        self._anade(tbl)

    def pendiente(self, texto):
        self.p(_run(texto, tam=10, fondo=NARANJA, color='262626'), antes=120, despues=120)

    def tabla(self, cabecera, filas, anchos, tam=8.5, negrita_col0=True):
        t = self.d.add_table(rows=len(filas) + 1, cols=len(cabecera))
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
                _limpia_celda(celda._tc)
                tcpr = celda._tc.get_or_add_tcPr()
                b = OxmlElement('w:tcBorders')
                for lado in ('top', 'left', 'bottom', 'right'):
                    e = OxmlElement(f'w:{lado}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4')
                    e.set(qn('w:color'), 'C9D6DF'); b.append(e)
                tcpr.append(b)
                _margenes(celda._tc, 80, 80, 30, 30)
                if r_i == 0:
                    _fondo(celda._tc, AZUL)
                    celda._tc.append(_parrafo_xml(_run(cabecera[c_i], negrita=True, color='FFFFFF', tam=tam),
                                                  despues=0))
                    continue
                if r_i % 2 == 0:
                    _fondo(celda._tc, 'F4F8FA')
                negrita = negrita_col0 and c_i == 0
                celda._tc.append(_parrafo_xml(_run(filas[r_i - 1][c_i], tam=tam, negrita=negrita,
                                                   color=AZUL if negrita else '222B33'), despues=0))
        self._anade(tbl)

    def elementos(self):
        el = self.p(_run('Tabla de elementos curriculares (recortada)', negrita=True, color=AZUL, tam=12), antes=0,
                    despues=60)
        el.find(qn('w:pPr')).insert(0, OxmlElement('w:pageBreakBefore'))
        self.p(_run('De la tabla de Gem: una competencia específica por fila, con su criterio de quinto, un saber '
                    'vinculado a ese criterio y dos descriptores. Códigos y vínculos comprobados en el BOJA; los '
                    'textos son resúmenes. La primera área se desarrolla entera; de la segunda, solo la competencia.',
                    tam=9.5, color=GRIS_TXT, cursiva=True), despues=100, alin='both')
        self.tabla(['Área', 'Competencia específica', 'Criterio de 5.º', 'Un saber básico', 'Descriptores'],
                   [list(f) for f in T.ELEMENTOS], [1.5, 7.6, 7.0, 7.6, 3.0])

    def orientaciones(self):
        el = self.p(_run('Orientaciones metodológicas de cada área', negrita=True, color=AZUL, tam=12), antes=0,
                    despues=60)
        el.find(qn('w:pPr')).insert(0, OxmlElement('w:pageBreakBefore'))
        self.p(_run('Anexo II de la Orden de 30 de mayo de 2023, introducción de cada área: una idea por frase, en '
                    'tres o cuatro palabras. Con ★, las más útiles para citar en el supuesto. Se omiten las frases que '
                    'solo enumeran los bloques de saberes.', tam=9.5, color=GRIS_TXT, cursiva=True), despues=100,
               alin='both')
        areas = list(T.ORIENTACIONES)
        n = max(len(v) for v in T.ORIENTACIONES.values())
        t = self.d.add_table(rows=n + 1, cols=len(areas))
        t.autofit = False
        tbl = t._tbl
        ancho = UTIL / len(areas)
        for i in range(len(areas)):
            tbl.tblGrid.gridCol_lst[i].w = Cm(ancho)
        for r_i, row in enumerate(t.rows):
            for c_i, celda in enumerate(row.cells):
                celda.width = Cm(ancho)
                _limpia_celda(celda._tc)
                tcpr = celda._tc.get_or_add_tcPr()
                b = OxmlElement('w:tcBorders')
                for lado in ('top', 'left', 'bottom', 'right'):
                    e = OxmlElement(f'w:{lado}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4')
                    e.set(qn('w:color'), 'D9D9D9'); b.append(e)
                tcpr.append(b)
                _margenes(celda._tc, 90, 90, 30, 30)
                if r_i == 0:
                    _fondo(celda._tc, AZUL)
                    celda._tc.append(_parrafo_xml(_run(areas[c_i], negrita=True, color='FFFFFF', tam=9),
                                                  despues=0))
                    continue
                ideas = T.ORIENTACIONES[areas[c_i]]
                if r_i - 1 < len(ideas):
                    idea, estrella = ideas[r_i - 1]
                    if r_i % 2 == 0:
                        _fondo(celda._tc, 'F3F8F9')
                    contenido = (_run('★ ', color=NARANJA_BORDE, tam=9, negrita=True) if estrella else '') + \
                        _run(idea, tam=9, negrita=estrella, color='262626')
                    celda._tc.append(_parrafo_xml(contenido, despues=0))
                else:
                    celda._tc.append(_parrafo_xml('', despues=0))
        self._anade(tbl)

    def guarda(self):
        ordena_esquema(self.d.element.body)
        zoom = self.d.settings.element.find(qn('w:zoom'))
        if zoom is not None and zoom.get(qn('w:percent')) is None:
            zoom.set(qn('w:percent'), '100')
        os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
        self.d.save(SALIDA)
        return SALIDA


def main():
    c = Constructor(apaisado=True)
    c.portada()
    for clave in ('7.1', '7.2', '7.3', '7.5', '7.6', '7.7', '7.8', '7.9'):
        c.plantilla(clave)
        if clave == '7.7':
            c.elementos()
        if clave == '7.8':
            c.orientaciones()
    print(c.guarda())


if __name__ == '__main__':
    main()
