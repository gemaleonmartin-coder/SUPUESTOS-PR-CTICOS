# -*- coding: utf-8 -*-
"""Libreta mágica 2.2, segunda edición (fase 38, sexta vuelta, 20 de noviembre de 2026).

Parte de libreta-magica/Libreta_magica_v22.docx (no se toca) y da Libreta_magica_v22_2.docx con lo que pidió Gem:
  1. la portada de Rafa, calcada del PDF de la versión 2.1 (bloque azul entero con su barra naranja, rótulo
     espaciado, tabla de contenido con sus columnas y sin cabecera ni pie), con «2.600 palabras» y la versión 2.2;
  2. la chuleta, con «Palabras (2.600)» y el reparto nuevo;
  3. fuera el bocadillo de ideas de la plantilla del 7.2 y el recuadro «Clave» del 7.3;
  4. las páginas que vienen del PDF, arregladas: los cuadros (plantilla, atención, clave) y las bandas de las partes,
     que pdf2docx había partido en una tabla por renglón (unas con fondo y otras sin él), vuelven a ser un recuadro
     continuo con sus colores y su barra; los rótulos espaciados («P L A N T I L L A …») recuperan sus palabras; las
     viñetas y los números de las listas recuperan su hueco; las columnas de las tablas, sus anchos (la rejilla estaba
     repartida a partes iguales); y fuera los decimales en las medidas.
También: «[curso][elabora…]» con sus espacios, «minientrevista» (prefijo junto, como pide la RAE) y el índice con
las páginas nuevas.
"""
import copy
import os
import re
import subprocess
import sys
import tempfile

from docx import Document
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libreta_v22_final as F  # noqa: E402
import plantillas_bocadillos as PB  # noqa: E402

RAIZ = F.RAIZ
ENTRADA = os.path.join(RAIZ, 'libreta-magica', 'Libreta_magica_v22.docx')
SALIDA = os.path.join(RAIZ, 'libreta-magica', 'Libreta_magica_v22_2.docx')
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
NS = PB.NS

# Colores de Rafa (los del PDF)
AZUL, ORO, NARANJA, VERDE_AZ, GRIS, TXT, CELESTE = '1F3A5F', 'F2C46D', 'C98A1B', '2A7F8E', '5B6770', '222B33', 'D6E4EE'
CAJAS = {  # tipo: (fondo, color de la barra izquierda o None, barra inferior o None)
    'plantilla': ('FCF6E8', NARANJA, None),
    'atencion': ('FAEAE7', 'B5473A', None),
    'clave': ('E8F3F5', VERDE_AZ, None),
    'banda': (AZUL, None, NARANJA),
}
ROTULOS = {'PLANTILLADEREDACCIÓN': ('PLANTILLA DE REDACCIÓN', 'plantilla'), 'ATENCIÓN': ('ATENCIÓN', 'atencion'),
           'CLAVE': ('CLAVE', 'clave'), 'PRESENTACIÓN': ('PRESENTACIÓN', 'banda'), 'PARTEI': ('PARTE I', 'banda'),
           'PARTEII': ('PARTE II', 'banda'), 'PARTEIII': ('PARTE III', 'banda'), 'PARTEIV': ('PARTE IV', 'banda'),
           'PARTEV': ('PARTE V', 'banda'), 'ANEXO': ('ANEXO', 'banda'), 'CONTENIDO': ('CONTENIDO', None),
           'SUPUESTOSPRÁCTICOS·PARTEA': ('SUPUESTOS PRÁCTICOS · PARTE A', None)}
ESPACIADO = re.compile(r'^\s*(?:\S ){2,}\S\s*$')


def texto(el):
    return ''.join(t.text or '' for t in el.iter(qn('w:t')))


def rotulo(t):
    """Si un texto es un rótulo espaciado de Rafa, (texto bueno, tipo de caja); si no, None."""
    if not ESPACIADO.match(t or ''):
        return None
    return ROTULOS.get(re.sub(r'\s', '', t))


# --------------------------------------------------------------------------------------------- XML pequeño
def run(t, fuente='Calibri', sz=20, color=TXT, b=False, i=False, esp=None):
    rpr = (f'<w:rPr><w:rFonts w:ascii="{fuente}" w:hAnsi="{fuente}" w:eastAsia="{fuente}" w:cs="{fuente}"/>'
           + ('<w:b/>' if b else '') + ('<w:i/>' if i else '') + f'<w:color w:val="{color}"/>'
           + (f'<w:spacing w:val="{esp}"/>' if esp else '') + f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>')
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return f'<w:r>{rpr}<w:t xml:space="preserve">{t}</w:t></w:r>'


def par(runs, antes=0, despues=0, linea=240, jc='left', izq=0):
    return (f'<w:p><w:pPr><w:spacing w:before="{antes}" w:after="{despues}" w:line="{linea}" w:lineRule="auto"/>'
            f'<w:ind w:left="{izq}" w:right="0"/><w:jc w:val="{jc}"/></w:pPr>{runs}</w:p>')


def tabla(anchos, filas_xml, sin_bordes=True):
    grid = ''.join(f'<w:gridCol w:w="{a}"/>' for a in anchos)
    bordes = ('<w:tblBorders>' + ''.join(f'<w:{l} w:val="nil"/>' for l in ('top', 'left', 'bottom', 'right',
                                                                           'insideH', 'insideV')) + '</w:tblBorders>'
              if sin_bordes else '')
    return parse_xml(f'<w:tbl {NS}><w:tblPr><w:tblW w:w="{sum(anchos)}" w:type="dxa"/><w:tblInd w:w="0" w:type="dxa"/>'
                     f'{bordes}<w:tblLayout w:type="fixed"/><w:tblCellMar><w:left w:w="0" w:type="dxa"/>'
                     f'<w:right w:w="0" w:type="dxa"/></w:tblCellMar><w:tblLook w:val="0000" w:firstRow="0" '
                     f'w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="1" w:noVBand="1"/></w:tblPr>'
                     f'<w:tblGrid>{grid}</w:tblGrid>{filas_xml}</w:tbl>')


def celda(ancho, contenido, fondo=None, izq=None, abajo=None, mar=(0, 0, 0, 0), valign=None, borde_inf_fino=None):
    b = '<w:tcBorders>'
    b += '<w:top w:val="nil"/>'
    b += (f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{izq}"/>' if izq else '<w:left w:val="nil"/>')
    if abajo:
        b += f'<w:bottom w:val="single" w:sz="40" w:space="0" w:color="{abajo}"/>'
    elif borde_inf_fino:
        b += f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{borde_inf_fino}"/>'
    else:
        b += '<w:bottom w:val="nil"/>'
    b += '<w:right w:val="nil"/></w:tcBorders>'
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fondo}"/>' if fondo else ''
    a, i, ab, d = mar
    tcmar = (f'<w:tcMar><w:top w:w="{a}" w:type="dxa"/><w:left w:w="{i}" w:type="dxa"/>'
             f'<w:bottom w:w="{ab}" w:type="dxa"/><w:right w:w="{d}" w:type="dxa"/></w:tcMar>')
    va = f'<w:vAlign w:val="{valign}"/>' if valign else ''
    return f'<w:tc><w:tcPr><w:tcW w:w="{ancho}" w:type="dxa"/>{b}{shd}{tcmar}{va}</w:tcPr>{contenido}</w:tc>'


# --------------------------------------------------------------------------------------------- 1. portada
CONTENIDO = [('I', 'Método', 'Examen en cifras, criterios, reparto de las 2.600 palabras, coherencia y manual de cada '
                             'apartado'),
             ('II', 'Banco de recursos por apartado', 'Normas, autores, elementos curriculares, actividades, medidas, '
                                                      'instrumentos y frases verificados'),
             ('III', 'Fichas por tipo de supuesto', 'Clasificación de los oficiales, 31 subtipos, formatos y qué poner '
                                                   'en cada apartado'),
             ('IV', 'Lista de verificación final', 'Revisión apartado por apartado antes de entregar'),
             ('V', 'Currículo de referencia', 'Competencias, criterios por curso y saberes de las áreas de la '
                                             'especialidad; descriptores por ciclo'),
             ('—', 'Anexo', 'Recursos pendientes de verificar (no se usan en el examen)')]
ALTOS = [852, 918, 836, 708, 838, 694]          # alto de cada fila (medido en el PDF de Rafa)
VERSION = ('Versión 2.2 · 20 de noviembre de 2026 · Revisión de Gem · Correcciones de la Parte I llevadas a toda la '
           'libreta')
AVISO = ('Material de estudio personal. Incluye ideas procedentes de materiales con derechos de autor: no se publica ni '
         'se redistribuye.')


def portada(ancho):
    """La portada de la versión 2.1 de Rafa, con sus medidas (en puntos del PDF, pasadas a twips)."""
    bloque = (par(run('SUPUESTOS PRÁCTICOS · PARTE A', sz=22, color=ORO, b=True, esp=60), antes=1800)
              + par(run('Libreta mágica', fuente='Cambria', sz=84, color='FFFFFF', b=True), antes=260)
              + par(run('Método, recursos verificados y fichas para resolver el supuesto práctico', fuente='Cambria',
                        sz=28, color=CELESTE, i=True), antes=60)
              + par(run('Cuerpo de Maestros · Especialidad de Educación Primaria', sz=24, color='FFFFFF'), antes=400)
              + par(run('Andalucía · Convocatoria de 2027', sz=24, color='FFFFFF', b=True), antes=80, despues=1700))
    azul = tabla([ancho], '<w:tr><w:trPr><w:cantSplit/></w:trPr>'
                 + celda(ancho, bloque, fondo=AZUL, abajo=NARANJA, mar=(0, 600, 0, 400)) + '</w:tr>')
    anchos = [960, 2904, ancho - 960 - 2904]
    filas = ''
    for (num, titulo, desc), alto in zip(CONTENIDO, ALTOS):
        filas += (f'<w:tr><w:trPr><w:cantSplit/><w:trHeight w:val="{alto}" w:hRule="atLeast"/></w:trPr>'
                  + celda(anchos[0], par(run(num, fuente='Cambria', sz=30, color=NARANJA, b=True)), mar=(40, 60, 40, 60),
                          valign='center', borde_inf_fino='C8D5DF')
                  + celda(anchos[1], par(run(titulo, sz=22, color=AZUL, b=True), linea=259), mar=(40, 60, 40, 120),
                          valign='center', borde_inf_fino='C8D5DF')
                  + celda(anchos[2], par(run(desc, sz=19, color=GRIS), linea=259), mar=(40, 60, 40, 60),
                          valign='center', borde_inf_fino='C8D5DF') + '</w:tr>')
    contenido = tabla(anchos, filas)
    hueco = parse_xml(f'<w:p {NS}><w:pPr><w:spacing w:before="0" w:after="0" w:line="1016" w:lineRule="exact"/>'
                      f'</w:pPr></w:p>')       # el bloque empieza a 3,58 cm del borde, como en el PDF
    return [hueco, azul,
            parse_xml(f'<w:p {NS}>' + par(run('CONTENIDO', sz=18, color=VERDE_AZ, b=True, esp=37), antes=480,
                                            despues=200)[5:]),
            contenido,
            parse_xml(f'<w:p {NS}>' + par(run(VERSION, sz=18, color=GRIS, b=True), antes=560)[5:]),
            parse_xml(f'<w:p {NS}>' + par(run(AVISO, sz=16, color=GRIS, i=True), antes=60)[5:])]


def pon_portada(d):
    body = d.element.body
    hijos = list(body)
    corte = next(i for i, e in enumerate(hijos) if e.tag == qn('w:p') and any(
        b.get(qn('w:type')) == 'page' for b in e.iter(qn('w:br'))))
    for e in hijos[:corte]:
        body.remove(e)
    sp = body.find(qn('w:sectPr'))
    ancho = int(sp.find(qn('w:pgSz')).get(qn('w:w'))) - int(sp.find(qn('w:pgMar')).get(qn('w:left'))) - int(
        sp.find(qn('w:pgMar')).get(qn('w:right')))
    primero = body[0]
    for el in portada(ancho):
        primero.addprevious(el)
    # sin cabecera ni pie en la portada, como en la de Rafa
    if sp.find(qn('w:titlePg')) is None:
        tp = OxmlElement('w:titlePg')
        ancla = sp.find(qn('w:docGrid'))
        if ancla is not None:
            ancla.addprevious(tp)
        else:
            sp.append(tp)
    return ancho


# --------------------------------------------------------------------------------------------- 2 y 3. contenido
def chuleta(d):
    for tr in d.element.body.iter(qn('w:tr')):
        tcs = tr.findall(qn('w:tc'))
        if len(tcs) == 2 and texto(tcs[0]).strip() == 'Palabras (2.500)':
            negrita = any(b.get(qn('w:val')) not in ('0', 'false') for b in tcs[0].iter(qn('w:b')))
            F.pon_celda(tcs[0], '**Palabras (2.600)**' if negrita else 'Palabras (2.600)')
            F.pon_celda(tcs[1], '1: 165 · 2: 180 · 3: 190 · 4.1: 275 · datos 4.2: 105 · 4.2.1: 220 · 4.2.2: 280 · '
                                '4.2.3: 450 · 4.2.4: 290 · 4.2.5: 240 · 5: 90 · 6: 110')
            return True
    raise SystemExit('No encuentro la fila de las palabras en la chuleta')


def quita_bocadillos(d):
    body = d.element.body
    hecho = 0
    for p in list(body.iter(qn('w:p'))):
        if p.find('.//' + qn('w:drawing')) is not None and 'Ideas: biblioteca municipal' in texto(p):
            p.getparent().remove(p)
            hecho += 1
            break
    for e in list(body):
        if e.tag == qn('w:tbl') and texto(e).startswith('ClaveLa normativa de este apartado es prácticamente la misma'):
            sig = e.getnext()
            body.remove(e)
            if sig is not None and sig.tag == qn('w:p') and not texto(sig).strip():
                body.remove(sig)
            hecho += 1
            break
    assert hecho == 2, hecho


# --------------------------------------------------------------------------------------------- 4. cuadros
def es_pieza(e):
    return (e.tag == qn('w:tbl') and len(e.findall(qn('w:tr'))) == 1 and len(e.find(qn('w:tr')).findall(qn('w:tc'))) == 1
            and e.find('.//' + qn('w:tbl')) is None)


def alto_separador(e):
    """Alto (twips) de un párrafo separador de pdf2docx, o None si no lo es."""
    if e is None or e.tag != qn('w:p') or texto(e).strip() or e.find('.//' + qn('w:drawing')) is not None:
        return None
    sp = e.find('.//' + qn('w:spacing'))
    if sp is None or sp.get(qn('w:lineRule')) != 'exact':
        return None
    v = int(float(sp.get(qn('w:line'), '999')))
    return v if v <= 60 else None


def saca_rotulos(body):
    """Los rótulos que pdf2docx metió dentro de otra tabla salen a una pieza propia, justo después."""
    for p in list(body.iter(qn('w:p'))):
        r = rotulo(texto(p))
        if not r or r[1] in (None,):
            continue
        cont = p
        while cont.getparent() is not body:
            cont = cont.getparent()
        if es_pieza(cont) and texto(cont).strip() == texto(p).strip():
            continue
        p.getparent().remove(p)
        pieza = parse_xml(f'<w:tbl {NS}><w:tblPr><w:tblW w:w="0" w:type="auto"/></w:tblPr><w:tblGrid>'
                          f'<w:gridCol w:w="9548"/></w:tblGrid><w:tr><w:tc><w:tcPr><w:tcW w:w="9548" w:type="dxa"/>'
                          f'</w:tcPr></w:tc></w:tr></w:tbl>')
        pieza.find('.//' + qn('w:tc')).append(p)
        cont.addnext(pieza)


def _pdf_vocabulario():
    pdf = os.path.join(RAIZ, [f for f in os.listdir(RAIZ) if f.startswith('Libreta') and f.endswith('.pdf')][0])
    t = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
    return set(re.findall(r'\w+(?:-\w+)+', t))


def _primer_t(p):
    return next(iter(p.iter(qn('w:t'))), None)


def _ultimo_t(p):
    ts = list(p.iter(qn('w:t')))
    return ts[-1] if ts else None


def _une(destino, origen, compuestos):
    """Añade al párrafo destino los runs del renglón origen, con el espacio (o sin guion de corte) que toque."""
    ult, pri = _ultimo_t(destino), _primer_t(origen)
    if ult is not None and pri is not None:
        a, b = ult.text or '', pri.text or ''
        if a.endswith('-') and len(a) > 1 and a[-2].isalpha() and b[:1].islower():
            izq = re.findall(r'\w+-$', a)[0][:-1]
            der = re.findall(r'^\w+', b)[0]
            if f'{izq}-{der}' not in compuestos:
                ult.text = a[:-1]
        elif not a.endswith((' ', ' ')) and not b.startswith(' '):
            pri.text = ' ' + b
            pri.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    for r in list(origen):
        if r.tag in (qn('w:r'), qn('w:hyperlink')):
            destino.append(r)


def _ppr_caja(p, despues=80):
    ppr = p.find(qn('w:pPr'))
    if ppr is not None:
        p.remove(ppr)
    p.insert(0, parse_xml(f'<w:pPr {NS}><w:spacing w:before="0" w:after="{despues}" w:line="259" w:lineRule="auto"/>'
                          f'<w:ind w:left="0" w:right="0" w:firstLine="0"/><w:jc w:val="left"/></w:pPr>'))


def _parrafo_rotulo(p_rotulo, bueno):
    """El rótulo con sus palabras, en mayúsculas espaciadas (como en Rafa)."""
    r0 = p_rotulo.find('.//' + qn('w:r'))
    rpr = copy.deepcopy(r0.find(qn('w:rPr'))) if r0 is not None and r0.find(qn('w:rPr')) is not None else None
    p = parse_xml(f'<w:p {NS}><w:r><w:t xml:space="preserve">{bueno}</w:t></w:r></w:p>')
    if rpr is not None:
        for e in rpr.findall(qn('w:spacing')):
            rpr.remove(e)
        esp = OxmlElement('w:spacing')
        esp.set(qn('w:val'), '40')
        sz = rpr.find(qn('w:sz'))
        (sz.addprevious(esp) if sz is not None else rpr.append(esp))
        p.find(qn('w:r')).insert(0, rpr)
    return p


def rehace_cajas(body, ancho):
    compuestos = _pdf_vocabulario()
    hechas = {'plantilla': 0, 'atencion': 0, 'clave': 0, 'banda': 0}
    i = 0
    while True:
        hijos = list(body)
        if i >= len(hijos):
            break
        e = hijos[i]
        r = rotulo(texto(e)) if es_pieza(e) else None
        if not r or r[1] is None:
            i += 1
            continue
        bueno, tipo = r
        piezas, seps = [e], [None]
        j = i + 1
        while j + 1 < len(hijos) and alto_separador(hijos[j]) is not None and es_pieza(hijos[j + 1]):
            if tipo == 'banda' and len(piezas) == 2:
                break
            if rotulo(texto(hijos[j + 1])):
                break
            seps.append(alto_separador(hijos[j]))
            piezas.append(hijos[j + 1])
            j += 2
        fondo, barra, inferior = CAJAS[tipo]
        p_rot = next(p for p in e.iter(qn('w:p')) if rotulo(texto(p)))
        contenido = [_parrafo_rotulo(p_rot, bueno)]
        actual = None
        for pieza, sep in zip(piezas[1:], seps[1:]):
            for k, q in enumerate([q for q in pieza.find('.//' + qn('w:tc')).findall(qn('w:p'))]):
                if not texto(q).strip():
                    continue
                if actual is None or (k == 0 and sep >= 28) or tipo == 'banda':
                    actual = copy.deepcopy(q)
                    _ppr_caja(actual, 0 if tipo == 'banda' else 80)
                    contenido.append(actual)
                else:
                    _une(actual, copy.deepcopy(q), compuestos)
        _ppr_caja(contenido[0], 40 if tipo != 'banda' else 20)
        if tipo == 'banda':
            for q in contenido[1:]:
                for t in q.iter(qn('w:t')):
                    t.text = (t.text or '').strip()
        caja = tabla([ancho], '<w:tr><w:trPr><w:cantSplit/></w:trPr>' + celda(
            ancho, '', fondo=fondo, izq=barra, abajo=inferior,
            mar=(100, 220, 120, 220) if tipo != 'banda' else (140, 240, 140, 240)) + '</w:tr>')
        tc = caja.find('.//' + qn('w:tc'))
        for q in contenido:
            tc.append(q)
        e.addprevious(caja)
        for pieza in piezas:
            body.remove(pieza)
        for k in range(i + 1, j, 2):      # separadores entre piezas
            if hijos[k].getparent() is body:
                body.remove(hijos[k])
        hechas[tipo] += 1
        separa_de_tablas(caja)
        i = list(body).index(caja) + 1
    return hechas


def _hueco(alto=220):
    return parse_xml(f'<w:p {NS}><w:pPr><w:spacing w:before="0" w:after="0" w:line="{alto}" w:lineRule="exact"/>'
                     f'</w:pPr></w:p>')


def separa_de_tablas(t):
    """Dos tablas seguidas se funden en una al abrir el documento: entre el cuadro y una tabla vecina, un párrafo."""
    if t.getprevious() is not None and t.getprevious().tag == qn('w:tbl'):
        t.addprevious(_hueco())
    if t.getnext() is not None and t.getnext().tag == qn('w:tbl'):
        t.addnext(_hueco())


def _vacio(e):
    return (e is not None and e.tag == qn('w:p') and not texto(e).strip() and e.find('.//' + qn('w:drawing')) is None
            and not any(b.get(qn('w:type')) == 'page' for b in e.iter(qn('w:br'))))


def _fila_oscura(tr):
    return any((s.get(qn('w:fill')) or '').lower() in ('1f395f', '1f3a5f') for s in tr.iter(qn('w:shd')))


def une_tablas_partidas(body):
    """Las tablas que en el PDF de Rafa pasaban de una página a otra salieron en dos trozos, con un hueco y, a veces,
    la cabecera repetida: se quitan los envoltorios de una celda, se juntan los trozos y la cabecera se repite sola."""
    quitados = unidas = 0
    for t in list(body):
        if t.tag != qn('w:tbl') or not es_pieza(t) and not (len(t.findall(qn('w:tr'))) == 1 and len(
                t.find(qn('w:tr')).findall(qn('w:tc'))) == 1):
            continue
        tc = t.find(qn('w:tr')).find(qn('w:tc'))
        dentro = [x for x in tc if x.tag != qn('w:tcPr')]
        tablas = [x for x in dentro if x.tag == qn('w:tbl')]
        if len(tablas) == 1 and all(x.tag == qn('w:tbl') or _vacio(x) for x in dentro):
            t.addprevious(tablas[0])
            body.remove(t)
            quitados += 1
    hijos = list(body)
    k = 0
    while k < len(hijos):
        t1 = hijos[k]
        if t1.tag != qn('w:tbl') or t1.getparent() is not body:
            k += 1
            continue
        j = k + 1
        while j < len(hijos) and _vacio(hijos[j]):
            j += 1
        if j >= len(hijos) or hijos[j].tag != qn('w:tbl') or j == k + 1 and False:
            k += 1
            continue
        t2 = hijos[j]
        g1 = [int(g.get(qn('w:w'))) for g in t1.find(qn('w:tblGrid'))]
        g2 = [int(g.get(qn('w:w'))) for g in t2.find(qn('w:tblGrid'))]
        f1, f2 = t1.findall(qn('w:tr')), t2.findall(qn('w:tr'))
        if len(g1) != len(g2) or len(g1) < 2 or not f1 or not f2 or not _fila_oscura(f1[0]):
            k += 1
            continue
        misma_cabecera = texto(f2[0]) == texto(f1[0])
        sigue = not _fila_oscura(f2[0]) and all(abs(a - b) <= max(a, b) * 0.1 for a, b in zip(g1, g2))
        if not (misma_cabecera or sigue):
            k += 1
            continue
        for tr in f2[1:] if misma_cabecera else f2:
            t1.append(tr)
        for x in hijos[k + 1:j + 1]:
            if x.getparent() is body:
                body.remove(x)
        trpr = f1[0].find(qn('w:trPr'))
        if trpr is None:
            trpr = OxmlElement('w:trPr'); f1[0].insert(0, trpr)
        if trpr.find(qn('w:tblHeader')) is None:
            trpr.append(OxmlElement('w:tblHeader'))
        unidas += 1
        hijos = list(body)
    return quitados, unidas


def rotulos_sueltos(body):
    n = 0
    for t in body.iter(qn('w:t')):
        r = rotulo(t.text)
        if r:
            t.text = r[0]
            rpr = t.getparent().find(qn('w:rPr'))
            if rpr is not None and rpr.find(qn('w:spacing')) is None:
                esp = OxmlElement('w:spacing'); esp.set(qn('w:val'), '40'); rpr.append(esp)
            n += 1
    return n


# --------------------------------------------------------------------------------------------- 5. listas y texto
def vinetas(body):
    n = 0
    for p in body.iter(qn('w:p')):
        rs = [r for r in p.findall(qn('w:r')) if r.find(qn('w:t')) is not None or r.find(qn('w:tab')) is not None]
        if not rs or rs[0].find(qn('w:t')) is None:
            continue
        t0 = rs[0].find(qn('w:t'))
        txt = t0.text or ''
        m = re.match(r'^(•|\d+\.)(\S.*)?$', txt)
        if not m:
            continue
        if m.group(2) and not re.match(r'[A-Za-zÁÉÍÓÚÑáéíóúñ¿«(★]', m.group(2)):
            continue                        # «4.2.1. …» es un número de apartado, no una lista
        if m.group(2):                      # viñeta y texto en el mismo run
            nuevo = copy.deepcopy(rs[0])
            nuevo.find(qn('w:t')).text = m.group(2)
            nuevo.find(qn('w:t')).set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            t0.text = m.group(1)
            rs[0].addnext(nuevo)
            rs.insert(1, nuevo)
        if len(rs) < 2 or rs[1].find(qn('w:tab')) is not None:
            continue
        t1 = rs[1].find(qn('w:t'))
        if t1 is None or not (t1.text or '') or (t1.text or '')[0].isspace():
            continue
        if m.group(1) != '•' and not re.match(r'[A-Za-zÁÉÍÓÚÑáéíóúñ¿«(\d★]', t1.text[0]):
            continue
        tab = parse_xml(f'<w:r {NS}><w:tab/></w:r>')
        if rs[0].find(qn('w:rPr')) is not None:
            tab.insert(0, copy.deepcopy(rs[0].find(qn('w:rPr'))))
        rs[0].addnext(tab)
        ppr = p.find(qn('w:pPr'))
        if ppr is None:
            ppr = OxmlElement('w:pPr'); p.insert(0, ppr)
        ind = ppr.find(qn('w:ind'))
        if ind is None:
            ind = OxmlElement('w:ind'); ppr.append(ind)
        if ind.get(qn('w:hanging')) is None:
            izq = int(float(ind.get(qn('w:left'), '0')))
            ind.set(qn('w:left'), str(izq + 284))
            ind.set(qn('w:hanging'), '284')
            if ind.get(qn('w:firstLine')) is not None:
                del ind.attrib[qn('w:firstLine')]
        n += 1
    return n


def _es_lista(p):
    rs = p.findall(qn('w:r'))
    return (len(rs) > 1 and rs[1].find(qn('w:tab')) is not None and rs[0].find(qn('w:t')) is not None
            and re.fullmatch(r'•|\d+\.', rs[0].find(qn('w:t')).text or '') is not None)


def _negrita(r):
    b = r.find(qn('w:rPr')).find(qn('w:b')) if r.find(qn('w:rPr')) is not None else None
    return b is not None and b.get(qn('w:val')) not in ('0', 'false')


def parte_listas(body):
    """pdf2docx juntó en un párrafo dos puntos de una lista («… se invalida. 2. El índice…») o un punto y el bloque
    siguiente («… evidencias. Recomendable: …»), y en un caso dos viñetas con un salto de línea: se separan."""
    n = 0
    cambiado = True
    while cambiado:
        cambiado = False
        for p in list(body.iter(qn('w:p'))):
            if not _es_lista(p):
                continue
            rs = p.findall(qn('w:r'))
            antes = ''.join(texto(r) for r in rs[:2])
            corte = None
            for k, r in enumerate(rs[2:], start=2):
                t = texto(r)
                if r.find(qn('w:br')) is not None and k + 1 < len(rs) and texto(rs[k + 1]).startswith('•'):
                    corte = ('salto', k)
                    break
                fin_frase = antes.rstrip().endswith(('.', ')', '»'))
                if fin_frase and re.fullmatch(r'\d+\.\s*', t):
                    corte = ('numero', k)
                    break
                if fin_frase and _negrita(r) and re.match(r'^(Recomendable|Estructura interna|Contenido obligatorio)', t):
                    corte = ('bloque', k)
                    break
                antes += t
            if not corte:
                continue
            tipo, k = corte
            nuevo = parse_xml(f'<w:p {NS}/>')
            ppr = copy.deepcopy(p.find(qn('w:pPr')))
            nuevo.append(ppr)
            mover = rs[k + 1:] if tipo == 'salto' else rs[k:]
            if tipo == 'salto':
                p.remove(rs[k])
            for r in mover:
                nuevo.append(r)
            # el párrafo de arriba, sin espacios finales sobrantes
            ult = _ultimo_t(p)
            if ult is not None and ult.text:
                ult.text = ult.text.rstrip()
            # el de abajo: viñeta o número con su tabulador; o bloque normal, sin sangría francesa
            pri = nuevo.findall(qn('w:r'))
            if tipo in ('salto', 'numero'):
                t0 = pri[0].find(qn('w:t'))
                m = re.match(r'^(•|\d+\.)\s*(.*)$', t0.text or '')
                t0.text = m.group(1)
                if m.group(2):
                    resto = copy.deepcopy(pri[0]); resto.find(qn('w:t')).text = m.group(2)
                    pri[0].addnext(resto)
                siguiente = pri[0].getnext()
                if siguiente is not None and siguiente.find(qn('w:t')) is not None:
                    siguiente.find(qn('w:t')).text = (siguiente.find(qn('w:t')).text or '').lstrip()
                tab = parse_xml(f'<w:r {NS}><w:tab/></w:r>')
                if pri[0].find(qn('w:rPr')) is not None:
                    tab.insert(0, copy.deepcopy(pri[0].find(qn('w:rPr'))))
                pri[0].addnext(tab)
            else:
                ind = nuevo.find(qn('w:pPr')).find(qn('w:ind'))
                if ind is not None and ind.get(qn('w:hanging')) is not None:
                    ind.set(qn('w:left'), str(max(0, int(ind.get(qn('w:left'))) - int(ind.get(qn('w:hanging'))))))
                    del ind.attrib[qn('w:hanging')]
                sp = nuevo.find(qn('w:pPr')).find(qn('w:spacing'))
                if sp is not None:
                    sp.set(qn('w:before'), '120')
                t0 = pri[0].find(qn('w:t'))
                if t0 is not None:
                    t0.text = (t0.text or '').lstrip()
            p.addnext(nuevo)
            n += 1
            cambiado = True
            break
    return n


def saltos(body):
    """Un párrafo que solo lleva un salto de página deja una página en blanco si la anterior acaba justo al pie: se
    cambia por un párrafo mínimo con «salto de página anterior» y se quitan los párrafos vacíos que lo preceden."""
    n = 0
    for p in list(body):
        if p.tag != qn('w:p') or texto(p).strip():
            continue
        brs = [b for b in p.iter(qn('w:br')) if b.get(qn('w:type')) == 'page']
        if not brs or p.find('.//' + qn('w:drawing')) is not None:
            continue
        ant = p.getprevious()
        while _vacio(ant):
            quitar, ant = ant, ant.getprevious()
            body.remove(quitar)
        nuevo = parse_xml(f'<w:p {NS}><w:pPr><w:pageBreakBefore/><w:spacing w:before="0" w:after="0" w:line="20" '
                          f'w:lineRule="exact"/></w:pPr></w:p>')
        p.addprevious(nuevo)
        body.remove(p)
        n += 1
    return n


def bandas_en_pagina_nueva(body):
    """Cada parte (y el anexo) empieza en página nueva, como en Rafa."""
    n = 0
    for t in list(body):
        if t.tag != qn('w:tbl') or not re.match(r'^(PARTE [IV]+|PRESENTACIÓN|ANEXO)', texto(t)):
            continue
        ant = t.getprevious()
        if ant is not None and ant.find('.//' + qn('w:pageBreakBefore')) is not None and not texto(ant).strip():
            continue
        while _vacio(ant):
            quitar, ant = ant, ant.getprevious()
            body.remove(quitar)
        t.addprevious(parse_xml(f'<w:p {NS}><w:pPr><w:pageBreakBefore/><w:spacing w:before="0" w:after="0" '
                                f'w:line="20" w:lineRule="exact"/></w:pPr></w:p>'))
        n += 1
    return n


def mantener_titulos(body):
    """Los títulos no se quedan solos al pie de la página: «conservar con el siguiente»."""
    n = 0
    for p in body.iter(qn('w:p')):
        t = texto(p).strip()
        if not t or len(t) > 150 or p.find('.//' + qn('w:drawing')) is not None:
            continue
        rs = [r for r in p.findall(qn('w:r')) if (texto(r) or '').strip()]
        if not rs or not all(_negrita(r) for r in rs):
            continue
        cont = p.getparent()
        en_tabla = cont.tag == qn('w:tc')
        if en_tabla:
            # solo las cabeceras de una celda con fondo (las de las fichas), no las celdas de las tablas
            tbl = cont.getparent().getparent()
            if not es_pieza(tbl) or len(tbl.findall(qn('w:tr'))) != 1:
                continue
        tam = [int(float(r.find(qn('w:rPr')).find(qn('w:sz')).get(qn('w:val')))) for r in rs
               if r.find(qn('w:rPr')) is not None and r.find(qn('w:rPr')).find(qn('w:sz')) is not None]
        colores = {(r.find(qn('w:rPr')).find(qn('w:color')).get(qn('w:val')) or '').upper() for r in rs
                   if r.find(qn('w:rPr')) is not None and r.find(qn('w:rPr')).find(qn('w:color')) is not None}
        if not (tam and max(tam) >= 21) and not (colores & {'1F3A5F', '2A7F8E'}):
            continue
        ppr = p.find(qn('w:pPr'))
        if ppr is None:
            ppr = OxmlElement('w:pPr'); p.insert(0, ppr)
        if ppr.find(qn('w:keepNext')) is None:
            ppr.insert(0, OxmlElement('w:keepNext'))
            n += 1
    return n


def textos(body):
    cambios = 0
    for p in body.iter(qn('w:p')):
        ts = list(p.iter(qn('w:t')))
        for a, b in zip(ts, ts[1:]):
            if (a.text or '').endswith(']') and (b.text or '').startswith('['):
                b.text = ' ' + b.text
                b.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                cambios += 1
    for t in body.iter(qn('w:t')):
        if t.text and 'mini entrevista' in t.text:
            t.text = t.text.replace('mini entrevista', 'minientrevista')
            cambios += 1
    return cambios


# --------------------------------------------------------------------------------------------- 6. tablas y medidas
def rejillas(body):
    n = 0
    for t in body.iter(qn('w:tbl')):
        grid = t.find(qn('w:tblGrid'))
        if grid is None:
            continue
        cols = grid.findall(qn('w:gridCol'))
        if len(cols) == 1:                   # una sola columna: la celda, al ancho de la rejilla
            for tc in t.iter(qn('w:tc')):
                if tc.getparent().getparent() is not t:
                    continue
                tcw = tc.find(qn('w:tcPr')).find(qn('w:tcW')) if tc.find(qn('w:tcPr')) is not None else None
                if tcw is not None:
                    tcw.set(qn('w:w'), str(int(float(cols[0].get(qn('w:w'))))))
                    tcw.set(qn('w:type'), 'dxa')
            continue
        for tr in t.findall(qn('w:tr')):
            tcs = tr.findall(qn('w:tc'))
            if len(tcs) != len(cols):
                continue
            ws = []
            for tc in tcs:
                pr = tc.find(qn('w:tcPr'))
                sp = pr.find(qn('w:gridSpan')) if pr is not None else None
                w = pr.find(qn('w:tcW')) if pr is not None else None
                if (sp is not None and sp.get(qn('w:val')) != '1') or w is None or not w.get(qn('w:w')):
                    ws = None
                    break
                ws.append(int(float(w.get(qn('w:w')))))
            if ws:
                for c, w in zip(cols, ws):
                    c.set(qn('w:w'), str(w))
                n += 1
                break
    return n


def sin_decimales(body):
    n = 0
    for el in body.iter():
        for k, v in list(el.attrib.items()):
            if k.startswith(W) and re.fullmatch(r'-?\d+\.\d+', v or ''):
                el.set(k, str(int(round(float(v)))))
                n += 1
    return n


# --------------------------------------------------------------------------------------------- 7. índice
def actualiza_indice(d, paginas):
    b = d.element.body
    dentro = False
    n = 0
    for p in list(b):
        if p.tag != qn('w:p'):
            if dentro:
                break
            continue
        t = texto(p).strip()
        if t == 'Índice':
            dentro = True
            continue
        if not dentro:
            continue
        if any(x.get(qn('w:type')) == 'page' for x in p.iter(qn('w:br'))):
            break
        rs = p.findall(qn('w:r'))
        k = next((i for i, r in enumerate(rs) if r.find(qn('w:tab')) is not None), None)
        if k is None:
            continue
        titulo = ''.join(texto(r) for r in rs[:k]).strip()
        if titulo in paginas and rs[-1].find(qn('w:t')) is not None:
            rs[-1].find(qn('w:t')).text = str(paginas[titulo])
            n += 1
    return n


def guarda(d, ruta):
    F.ids_unicos(d)
    F.repara_esquema(d.element.body)
    zoom = d.settings.element.find(qn('w:zoom'))
    if zoom is not None and zoom.get(qn('w:percent')) is None:
        zoom.set(qn('w:percent'), '100')
    d.save(ruta)


def main():
    d = Document(ENTRADA)
    body = d.element.body
    quita_bocadillos(d)
    chuleta(d)
    ancho = pon_portada(d)
    saca_rotulos(body)
    hechas = rehace_cajas(body, ancho)
    n_env, n_uni = une_tablas_partidas(body)
    n_rot = rotulos_sueltos(body)
    n_vin = vinetas(body)
    n_par = parte_listas(body)
    n_sal = saltos(body) + bandas_en_pagina_nueva(body)
    n_tit = mantener_titulos(body)
    n_txt = textos(body)
    n_rej = rejillas(body)
    n_dec = sin_decimales(body)
    guarda(d, SALIDA)
    pags, total = F.paginas_de(SALIDA)
    d = Document(SALIDA)
    n_ind = actualiza_indice(d, pags)
    guarda(d, SALIDA)
    print('envoltorios quitados:', n_env, '| tablas partidas unidas:', n_uni, '| párrafos de lista separados:', n_par,
          '| saltos de página:', n_sal, '| títulos con el siguiente:', n_tit)
    print('cajas rehechas:', hechas, '| rótulos sueltos:', n_rot, '| viñetas y números:', n_vin, '| textos:', n_txt,
          '| tablas con columnas:', n_rej, '| medidas sin decimales:', n_dec, '| índice:', n_ind, 'páginas;',
          total, 'páginas en LibreOffice')
    print(SALIDA)


if __name__ == '__main__':
    main()
