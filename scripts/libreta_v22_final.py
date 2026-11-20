# -*- coding: utf-8 -*-
"""Libreta mágica 2.2 completa y limpia (fase 38): el PDF de Rafa (versión 2.1) convertido a Word con pdf2docx y, dentro,
todos los apartados corregidos con Gem, sustituidos por los bloques rehechos (libreta_v22_parte1.py y libreta_v22_resto.py).

Uso:  python3 scripts/libreta_v22_final.py
Salida: libreta-magica/Libreta_magica_v22.docx (solo la versión limpia, como pidió Gem).

Pasos: (1) convertir el PDF (si no está ya convertido en la carpeta temporal); (2) quitar las cabeceras y los pies que
pdf2docx deja en cada página y las secciones por página (el texto pasa a fluir), poner una cabecera y un pie reales y
cambiar las alturas de fila exactas por mínimas (para que no se corte texto); (3) sustituir cada apartado corregido,
entre su título y el siguiente; (4) cambiar celdas y párrafos sueltos; (5) saltos de página antes de cada parte; (6)
índice con las páginas recalculadas en LibreOffice (segunda pasada).
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
from docx.shared import Cm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libreta_v22_completa as C  # noqa: E402
import libreta_v22_parte1 as L  # noqa: E402
import libreta_v22_resto as R  # noqa: E402
import plantillas_bocadillos as PB  # noqa: E402

RAIZ = L.RAIZ
PDF = os.path.join(RAIZ, 'Libreta mágica.pdf')
if not os.path.exists(PDF):
    PDF = os.path.join(RAIZ, [f for f in os.listdir(RAIZ) if f.lower().startswith('libreta m') and f.endswith('.pdf')][0])
TMP = os.path.join(tempfile.gettempdir(), 'libreta_v22_final')
CONV = os.path.join(TMP, 'rafa_convertida.docx')
SALIDA = os.path.join(RAIZ, 'libreta-magica', 'Libreta_magica_v22.docx')


# ---------------------------------------------------------------------------------------------------------------
def texto(el):
    return ''.join(x.text or '' for x in el.iter(qn('w:t')))


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def sin_espacios(s):
    return re.sub(r'\s+', '', s)


def convierte():
    if os.path.exists(CONV):
        return
    os.makedirs(TMP, exist_ok=True)
    from pdf2docx import Converter
    c = Converter(PDF)
    c.convert(CONV)
    c.close()


# ---------------------------------------------------------------------------------------------------------------
# Bloques finales (limpios y completos) para cada apartado que se sustituye
def tramo(titulo, hasta=None, sin=('nota',)):
    """Bloques de R.B desde el h2 que empieza por «titulo» hasta el siguiente h2/h1 (o hasta «hasta»)."""
    ini = next(i for i, b in enumerate(R.B) if b[0] in ('h2', 'h1') and b[1].replace('<<', '').startswith(titulo))
    fin = ini + 1
    while fin < len(R.B) and R.B[fin][0] not in ('h1', 'h2', 'apartados_6_a_79'):
        if hasta and R.B[fin][0] in ('sub',) and R.B[fin][1].replace('<<', '').startswith(hasta):
            break
        fin += 1
    return [b for b in R.B[ini:fin] if b[0] not in sin]


def desde_sub(bloques, sub):
    i = next(k for k, b in enumerate(bloques) if b[0] == 'sub' and b[1].replace('<<', '').startswith(sub))
    return bloques[i:]


VARIANTES = [['1', '165', '165', '165', '165', '165'], ['2', '180', '210', '200', '190', '170'],
             ['3', '190', '180', '200', '180', '180'], ['4.1', '275', '305', '365', '405', '265'],
             ['4.2 (datos)', '105', '95', '95', '105', '105'], ['4.2.1', '220', '190', '180', '200', '210'],
             ['4.2.2', '280', '240', '260', '250', '350'], ['4.2.3', '450', '400', '420', '420', '470'],
             ['4.2.4', '290', '390', '260', '250', '260'], ['4.2.5', '240', '230', '250', '230', '220'],
             ['5', '90', '90', '90', '90', '90'], ['6', '110', '100', '110', '110', '110'],
             ['Total', '2.595', '2.595', '2.595', '2.595', '2.595']]

OTRAS_NORMAS_33 = [
    ['Real Decreto 157/2022', '5.4: medidas regidas por los principios del Diseño Universal para el Aprendizaje · 6: '
                              'principios pedagógicos (se citan en 4.2.2, no aquí) · anexo III: orientaciones para las '
                              'situaciones de aprendizaje', 'Todos'],
    ['Real Decreto 157/2022', '8: áreas de la etapa (Conocimiento del Medio Natural, Social y Cultural, desdoblable en '
                              'Ciencias de la Naturaleza y Ciencias Sociales; Educación Artística, desdoblable en Educación '
                              'Plástica y Visual y Música y Danza; Educación Física; Lengua Castellana y Literatura; Lengua '
                              'Extranjera; Matemáticas; Educación en Valores Cívicos y Éticos en un curso del tercer ciclo)',
     'Enunciados que citan áreas antiguas'],
    ['Decreto 101/2023', '4: principios generales (globalidad, atención a la diversidad, equidad e inclusión, aprendizaje '
                         'significativo, excelencia)', 'Todos'],
    ['LOE modificada por LOMLOE', '19.1-19.3: inclusión, atención personalizada, prevención; comprensión lectora y '
                                  'aprendizajes transversales en todas las áreas; tiempo diario de lectura', 'T2, T3'],
    ['LOE modificada por LOMLOE', '71-74, 76, 79 bis: alumnado con necesidad específica de apoyo educativo; altas '
                                  'capacidades; dificultades específicas de aprendizaje', 'T3'],
    ['Ley 17/2007', '39: educación en valores como elemento transversal · 46-48: atención a la diversidad, áreas '
                    'instrumentales, refuerzo de comunicación lingüística y razonamiento matemático · 113-114: equidad, '
                    'detección y atención temprana', 'T1, T2, T3, T4'],
]

CHECK_424 = ['Diseño universal con dos o tres aplicaciones concretas de la secuencia.',
             'Dos medidas generales del artículo 27.4 con su actividad.',
             'Medida específica del artículo 33.3 para cada perfil del contexto, con ajuste y profesional.',
             'Ningún perfil sin medida y ninguna medida sin perfil.',
             'Adaptación curricular significativa solo con necesidades educativas especiales y desfase de dos cursos.',
             'Apoyo preferentemente dentro del aula.', 'Diferencias individuales (tareas graduadas, ampliación).',
             'Remisión a la coordinación de 4.1.']


def bloques_finales():
    F = {}
    t12 = tramo('1.2. Tiempo')
    F['1.2'] = [t12[0], ('p', 'La convocatoria de 2025 fijó cuatro horas y treinta minutos para el tema y el supuesto, sin '
                               'interrupción; con un reparto equilibrado, el supuesto dispone de 135 minutos. La '
                               'convocatoria de 2027 puede cambiarlo.')] + t12[1:]
    F['3'] = [('h1', '3. Reparto de las palabras (unas 2.600)')] + tramo('3.1. Reparto estándar')
    F['3.3'] = [('h2', '3.3. Variantes según el tipo de supuesto'),
                ('tabla', ['Apartado', 'Estándar', 'V1 Diversidad (T3)', 'V2 Convivencia (T4)', 'V3 Centro (T5)',
                           'V4 Metodología impuesta (T6)'], VARIANTES, [2.6, 2.2, 3.0, 3.2, 2.8, 3.6]),
                ('p', 'Reglas: la secuencia didáctica nunca baja de 400 palabras; ningún apartado desaparece; las '
                      'variantes se combinan (un proyecto de centro con alumnado con necesidades toma 4.1 de V3 y 4.2.4 '
                      'de V1, y recorta en 4.2.1 y 4.2.2). T2 usa el reparto estándar con el 4.1 de V3 si el tiempo lo '
                      'permite; T5e (salida) usa V3; T1 con proyecto de centro (T5b) toma el 4.1 de V3.')]
    F['4.1-4.2'] = tramo('4.1. Orden de planificación') + tramo('4.2. Cadena de dependencias')
    F['7.13'] = tramo('7.13. Referencias')
    F['II-1.6'] = [('h2', '1.6. Antesalas (cierre de la introducción) ★')] + tramo('1.6. Antesalas')[1:]
    F['II-2.1-2.2'] = tramo('2.1. Frases base') + tramo('2.2. Líneas generales')
    F['II-3.1-3.3'] = (tramo('3.1. Normativa fija') + tramo('3.2. Instrucción según el área')
                       + [('h2', '3.3. Otras normas útiles en la justificación'),
                          ('tabla', ['Norma', 'Artículo y contenido', 'Tipos'], OTRAS_NORMAS_33, [3.4, 11.6, 2.4])])
    F['II-4.1e'] = desde_sub(tramo('4.1. Intervención a nivel de centro'), 'e) Frases de 4.1')
    F['II-4.2a'] = [('sub', 'a) Base y frases')] + tramo('4.2. Datos identificativos')[1:]
    t421 = tramo('4.2.1. Concreción curricular')
    F['II-4.2.1'] = [('sub', 'Tabla de elementos curriculares de quinto (comprobada en el BOJA)')] + t421[1:]
    t422 = tramo('4.2.2. Metodología', sin=('nota',))
    i_f = next(k for k, b in enumerate(t422) if b[0] == 'sub' and b[1].startswith('4.2.2. f)'))
    i_h = next(k for k, b in enumerate(t422) if b[0] == 'sub' and b[1].startswith('4.2.2. h)'))
    F['II-4.2.2a'] = [('sub', 'a) Marco normativo')] + t422[1:i_f]
    F['II-4.2.2h'] = [('sub', 'h) Frases de metodología')] + t422[i_h + 1:]
    F['II-4.2.3e'] = [('sub', 'e) Frase de cierre de las actividades')] + tramo('4.2.3. Secuencia didáctica')[1:]
    t425 = desde_sub(tramo('4.2.5. Evaluación'), 'b) La tríada')
    F['II-4.2.5'] = [(('p', 'No se usan la diana de autoevaluación ni la diana cooperativa: son propias de infantil.')
                      if b[0] == 'p' and 'Fuera' in b[1] else b) for b in t425]
    F['III-nota'] = [b for b in R.B if b[0] == 'clave' and 'Lo que cambia en todas las fichas' in b[1]]
    F['III-nota'] = [('clave', F['III-nota'][0][1].replace('**Lo que cambia en todas las fichas.**',
                                                           '**En todas las fichas.**'))]
    F['IV-1'] = tramo('1. Antes de redactar')
    iv = tramo('3. Apartados 1 a 3') + tramo('4. Apartado 4.1') + tramo('5. Apartado 4.2')
    k = next(i for i, b in enumerate(iv) if b[0] == 'sub' and b[1].startswith('4.2.5'))
    F['IV-3-5'] = iv[:k] + [('sub', '4.2.4. Atención a la diversidad'), ('check', CHECK_424)] + iv[k:]
    return F


class Final(C.Completa):
    """Construye bloques limpios en un documento auxiliar para copiarlos después."""
    def parte(self, t):
        self.h1(t)


def elementos(bloques):
    lib = Final(False)
    cuerpo = lib.d.element.body
    for el in list(cuerpo):
        if el.tag != qn('w:sectPr'):
            cuerpo.remove(el)
    for b in bloques:
        if b[0] == 'apartados_6_a_79':
            continue
        lib.bloque(b)
    PB.ordena_esquema(cuerpo)
    return [copy.deepcopy(el) for el in cuerpo if el.tag != qn('w:sectPr')]


def elementos_6_a_79():
    lib = Final(False)
    cuerpo = lib.d.element.body
    for el in list(cuerpo):
        if el.tag != qn('w:sectPr'):
            cuerpo.remove(el)
    for b in L.B:
        if b[0] == 'h1':
            lib.h1(b[1])
        else:
            lib.bloque(b)
    PB.ordena_esquema(cuerpo)
    return [copy.deepcopy(el) for el in cuerpo if el.tag != qn('w:sectPr')]


# ---------------------------------------------------------------------------------------------------------------
# Ediciones en celdas y párrafos convertidos
NEG = re.compile(r'\*\*(.*?)\*\*')


def pon_texto(contenedor_p, texto_nuevo, conserva_primero=False):
    """Deja el párrafo con el texto nuevo en el formato del primer run (o del segundo, si el primero es una viñeta
    que se conserva); **negrita** si se marca."""
    runs = contenedor_p.findall(qn('w:r'))
    if conserva_primero and len(runs) > 1:
        guardado, runs = runs[0], runs[1:]
    else:
        guardado = None
    molde = copy.deepcopy(runs[0].find(qn('w:rPr'))) if runs and runs[0].find(qn('w:rPr')) is not None else None
    for r in contenedor_p.findall(qn('w:r')) + contenedor_p.findall(qn('w:hyperlink')):
        if r is not guardado:
            contenedor_p.remove(r)
    partes = NEG.split(texto_nuevo)
    for i, parte in enumerate(partes):
        if not parte:
            continue
        if '\n' in parte:
            trozos = parte.split('\n')
            for k, tr_ in enumerate(trozos):
                if k:
                    br = OxmlElement('w:r'); br.append(OxmlElement('w:br')); contenedor_p.append(br)
                if tr_:
                    _run_texto(contenedor_p, tr_, molde, i % 2 == 1)
            continue
        r = OxmlElement('w:r')
        if molde is not None:
            rpr = copy.deepcopy(molde)
            for b in rpr.findall(qn('w:b')):
                rpr.remove(b)
            if i % 2 == 1:
                b = OxmlElement('w:b')
                (rpr.find(qn('w:rFonts')).addnext(b) if rpr.find(qn('w:rFonts')) is not None else rpr.insert(0, b))
            r.append(rpr)
        t = OxmlElement('w:t')
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = parte
        r.append(t)
        contenedor_p.append(r)


def _run_texto(p, t, molde, negrita):
    r = OxmlElement('w:r')
    if molde is not None:
        rpr = copy.deepcopy(molde)
        for b in rpr.findall(qn('w:b')):
            rpr.remove(b)
        if negrita:
            b = OxmlElement('w:b')
            (rpr.find(qn('w:rFonts')).addnext(b) if rpr.find(qn('w:rFonts')) is not None else rpr.insert(0, b))
        r.append(rpr)
    tt = OxmlElement('w:t')
    tt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    tt.text = t
    r.append(tt)
    p.append(r)


def pon_celda(tc, texto_nuevo):
    ps = tc.findall(qn('w:p'))
    for p in ps[1:]:
        tc.remove(p)
    pon_texto(ps[0], re.sub(r'<<|>>\{#\w+\}', '', texto_nuevo))


def celdas(tr):
    return tr.findall(qn('w:tc'))


def filas(elementos_tramo):
    for el in elementos_tramo:
        if el.tag == qn('w:tbl'):
            for tr in el.findall(qn('w:tr')):
                yield tr


# ---------------------------------------------------------------------------------------------------------------
class Montaje:
    def __init__(self):
        self.d = Document(CONV)
        self.b = self.d.element.body

    def hijos(self):
        return [el for el in self.b if el.tag in (qn('w:p'), qn('w:tbl'))]

    def busca(self, inicio, pred, desde=0):
        hs = self.hijos()
        for i in range(desde, len(hs)):
            if pred(hs[i]):
                return i
        raise ValueError(f'no encuentro {inicio!r}')

    def idx(self, titulo, desde=0, tabla=False):
        """Índice del primer párrafo (o tabla de banner) cuyo texto empieza por «titulo»."""
        objetivo = norm(titulo)

        def pred(el):
            if tabla == 'inicio':
                return norm(texto(el)).startswith(objetivo)
            if tabla:
                return el.tag == qn('w:tbl') and sin_espacios(texto(el)) == sin_espacios(titulo)
            return el.tag == qn('w:p') and norm(texto(el)).startswith(objetivo)
        return self.busca(titulo, pred, desde)

    def limpia(self):
        n = 0
        primer = self.b.find('.//' + qn('w:pPr') + '/' + qn('w:sectPr'))
        pgmar = copy.deepcopy(primer.find(qn('w:pgMar'))) if primer is not None else None
        for p in list(self.b.iter(qn('w:p'))):
            t = norm(texto(p))
            if re.match(r'^Libreta mágica · Supuestos prácticos', t) or re.match(r'^Página \d+ de 138$', t):
                p.getparent().remove(p)
                n += 1
        for s in self.b.findall('.//' + qn('w:pPr') + '/' + qn('w:sectPr')):
            s.getparent().remove(s)
        for h in self.b.iter(qn('w:trHeight')):
            if h.get(qn('w:hRule')) == 'exact':
                h.set(qn('w:hRule'), 'atLeast')
        s = self.d.sections[0]
        s.page_width, s.page_height = Cm(21), Cm(29.7)
        if pgmar is not None:
            sp = self.b.find(qn('w:sectPr'))
            for old in sp.findall(qn('w:pgMar')):
                sp.remove(old)
            sp.append(pgmar)
        s.header_distance, s.footer_distance = Cm(0.9), Cm(0.9)
        h = s.header.paragraphs[0]
        h.alignment = 2
        h._p.append(parse_xml(f'<w:r {PB.NS}>{PB._rpr(negrita=True, color=L.AZUL, tam=8)}<w:t xml:space="preserve">'
                              f'Libreta mágica</w:t></w:r>'))
        h._p.append(parse_xml(f'<w:r {PB.NS}>{PB._rpr(color="6A7075", tam=8)}<w:t xml:space="preserve">  ·  Supuestos '
                              f'prácticos · Educación Primaria · Andalucía 2027</w:t></w:r>'))
        f = s.footer.paragraphs[0]
        f.alignment = 1
        f._p.append(parse_xml(f'<w:r {PB.NS}>{PB._rpr(color="6A7075", tam=8)}<w:t xml:space="preserve">Página '
                              f'</w:t></w:r>'))
        f._p.append(parse_xml(f'<w:fldSimple {PB.NS} w:instr="PAGE"><w:r>{PB._rpr(color="6A7075", tam=8)}<w:t>1</w:t>'
                              f'</w:r></w:fldSimple>'))
        f._p.append(parse_xml(f'<w:r {PB.NS}>{PB._rpr(color="6A7075", tam=8)}<w:t xml:space="preserve"> de </w:t>'
                              f'</w:r>'))
        f._p.append(parse_xml(f'<w:fldSimple {PB.NS} w:instr="NUMPAGES"><w:r>{PB._rpr(color="6A7075", tam=8)}<w:t>1'
                              f'</w:t></w:r></w:fldSimple>'))
        return n

    def sustituye(self, i, j, nuevos):
        hs = self.hijos()
        ancla = hs[i]
        for el in nuevos:
            ancla.addprevious(el)
        for el in hs[i:j]:
            self.b.remove(el)

    def inserta_antes(self, i, nuevos):
        ancla = self.hijos()[i]
        for el in nuevos:
            ancla.addprevious(el)

    def salto_antes(self, i):
        p = parse_xml(f'<w:p {PB.NS}><w:r><w:br w:type="page"/></w:r></w:p>')
        self.hijos()[i].addprevious(p)


def edita_filas(m, i, j, cambios, columna=0):
    """cambios: lista de (clave del texto de la columna «columna», [textos nuevos por celda o None]). Devuelve no hechos."""
    tramo_el = m.hijos()[i:j]
    pendientes = list(cambios)
    for tr in list(filas(tramo_el)):
        cs = celdas(tr)
        if len(cs) <= columna:
            continue
        t = norm(texto(cs[columna]))
        for clave, nuevos in list(pendientes):
            if (t == clave) if not clave.endswith('…') else t.startswith(clave[:-1]):
                if nuevos == 'BORRAR':
                    tr.getparent().remove(tr)
                else:
                    for tc, nuevo in zip(cs, nuevos):
                        if nuevo is not None:
                            pon_celda(tc, nuevo)
                pendientes.remove((clave, nuevos))
                break
    return pendientes


def fila_t(R_titulo, apartado):
    """Celdas nuevas de la fila «apartado» de la tabla de cambios de una ficha de la Parte III (de R.B)."""
    t = tramo(R_titulo, sin=())
    for b in t:
        if b[0] == 'tabla':
            for f in b[2]:
                if re.sub(r'<<|>>\{#\w+\}', '', f[0]) == apartado:
                    return [None] + f[1:]
    raise KeyError((R_titulo, apartado))


def parrafo_r(R_titulo, empieza):
    for b in tramo(R_titulo, sin=()):
        if b[0] == 'p' and b[1].startswith(empieza):
            return re.sub(r'<<|>>\{#\w+\}', '', b[1])
    raise KeyError(empieza)


def monta():
    convierte()
    F = bloques_finales()
    m = Montaje()
    print('cabeceras y pies quitados:', m.limpia())

    # --- anclas en orden de documento (con cursor), y después se aplica de atrás hacia delante
    ops = []
    I1 = m.idx('PARTE I', tabla=True)
    a = m.idx('1.2. Tiempo (135 minutos para el supuesto)', I1); b = m.idx('1.3. Causas de invalidación', a)
    ops.append(('sust', a, b, elementos(F['1.2'])))
    a = m.idx('3. Reparto de las 2.500 palabras', b); b = m.idx('3.2. Por qué este reparto', a)
    ops.append(('sust', a, b, elementos(F['3'])))
    a = m.idx('3.3. Variantes según el tipo de supuesto', b); b = m.idx('4. Coherencia vertical', a)
    ops.append(('sust', a, b, elementos(F['3.3'])))
    a = m.idx('4.1. Orden de planificación', b); b = m.idx('4.3. Recursos de redacción', a)
    ops.append(('sust', a, b, elementos(F['4.1-4.2'])))
    r43 = m.idx('•Remisiones internas breves', b) if True else None
    a = m.idx('6. Normas: primeras menciones y citas mínimas', b); b = m.idx('7.10. Atención a la diversidad', a)
    ops.append(('sust', a, b, elementos_6_a_79()))
    a = m.idx('7.13. Referencias', b); I2 = m.idx('PARTE II', a, tabla=True)
    ops.append(('sust', a, I2, elementos(F['7.13'])))
    a = m.idx('1.6. Antesalas (cierre de la introducción)', I2); b = m.idx('2. Contexto', a)
    ops.append(('sust', a, b, elementos(F['II-1.6'])))
    a = m.idx('2.1. Frases base', b); b23 = m.idx('2.3. Programas educativos del curso 2026/2027', a)
    ops.append(('sust', a, b23, elementos(F['II-2.1-2.2'])))
    b24 = m.idx('2.4. Recursos del entorno', b23)
    ops.append(('filas', b23, b24, [('Comunica (lectura, escritura, oralidad, radio escolar,…', 'COMUNICA'),
                                    ('Proyectos ApS', 'BORRAR')], 1))
    a = m.idx('3.1. Decreto 101/2023, artículo 6: principios pedagógicos', b24)
    b = m.idx('3.4. Autores verificados por temática', a)
    ops.append(('sust', a, b, elementos(F['II-3.1-3.3'])))
    a41 = m.idx('4.1. Intervención a nivel de centro', b); bdoc = m.idx('b) Documentos del centro', a41)
    cdoc = m.idx('c) Medidas de centro que pueden proponerse', bdoc)
    pe = [b_ for b_ in tramo('4.1. Intervención a nivel de centro', sin=()) if b_[0] == 'tabla'][0][2][0]
    ops.append(('filas', bdoc, cdoc, [('Proyecto educativo ★', [None, pe[1], None])], 0))
    a = m.idx('e) Frases de 4.1', cdoc); b = m.idx('4.2. Datos identificativos (transición)', a)
    ops.append(('sust', a, b, elementos(F['II-4.1e'])))
    a = m.idx('a) Base y frases', b); b = m.idx('b) Efemérides del curso 2026-2027', a)
    ops.append(('sust', a, b, elementos(F['II-4.2a'])))
    a = m.idx('b) Elementos curriculares verificados por tipo', b)
    ops.append(('ins', a, None, elementos(F['II-4.2.1'])))
    a422 = m.idx('4.2.2. Metodología', a); a = m.idx('a) Marco normativo', a422)
    b = m.idx('b) Esquema del anexo IV', a)
    ops.append(('sust', a, b, elementos(F['II-4.2.2a'])))
    af = m.idx('f) Recursos digitales', b)
    ops.append(('par', af, None, 'f) Recursos digitales (siempre con finalidad didáctica y cautelas de protección de '
                                 'datos; se citan al final de las actividades de la secuencia, 4.2.3)'))
    a = m.idx('h) Frases de metodología', af); b = m.idx('4.2.3. Secuencia didáctica', a)
    ops.append(('sust', a, b, elementos(F['II-4.2.2h'])))
    a424 = m.idx('4.2.4. Atención a la diversidad', b)
    ops.append(('ins', a424, None, elementos(F['II-4.2.3e'])))
    b424 = m.idx('b)', a424 + 1)
    ops.append(('filas', a424, b424, [('Autorregulación: rutinas, agenda visual, semáforo o diana',
                                       [None, 'Autorregulación: rutinas, agenda visual, semáforo o escala de '
                                              'autovaloración', None])], 1))
    a425 = m.idx('4.2.5. Evaluación', b424); a = m.idx('b) La tríada evidencia-técnica-instrumento', a425)
    b = m.idx('e) Indicadores para evaluar las medidas de diversidad', a)
    ops.append(('sust', a, b, elementos(F['II-4.2.5'])))
    a71 = m.idx('7.1. Estructuras de párrafo', b); a72 = m.idx('7.2. Conectores', a71)
    a73 = m.idx('7.3. Expresiones que se evitan', a72); I3 = m.idx('PARTE III', a73, tabla=True)
    ops.append(('filas', a71, a72, [('E4', [None, 'Siete datos en tres frases (identificar, situar, dar sentido) y una '
                                                  'cuarta con el ODS y la continuidad con el contexto', None])], 0))
    ops.append(('filas', a72, a73, [('◆ Remisión interna', [None, 'Como se indicó en el contexto · En coherencia con las '
                                                                  'líneas generales de actuación pedagógica y la '
                                                                  'concreción curricular señaladas · Criterio ya citado '
                                                                  'en la concreción curricular'])], 0))
    ops.append(('filas', a73, I3, [('Anunciar el índice', ['Olvidar el preíndice o alargarlo',
                                                           'Una o dos frases que recorren los apartados'])], 0))
    # Parte III
    a0 = m.idx('0. Clasificar el enunciado en los cinco minutos de lectura', I3)
    ops.append(('ins', a0, None, elementos(F['III-nota'])))
    a07 = m.idx('0.7. Qué cambia según la familia', a0); aT1 = m.idx('T1. Propuesta didáctica', a07, tabla='inicio')
    fila07 = [b_ for b_ in tramo('0.7. Qué cambia', sin=()) if b_[0] == 'tabla'][0][2][0]
    ops.append(('filas', a07, aT1, [('3. Norma…', fila07)], 0))
    fichas = [('T1. Propuesta didáctica', 'T1. Propuesta didáctica', ['2', '3', '4.1', '4.2', '4.2.2', '4.2.5', '6']),
              ('T2. Mejora de una competencia instrumental', 'T2. Mejora de una competencia', ['2', '3']),
              ('T3. Atención a la diversidad marcada', 'T3. Atención a la diversidad', ['3']),
              ('T4. Convivencia, emociones y acción tutorial', 'T4. Convivencia', ['2', '3']),
              ('T5. Organizativo o de centro', 'T5. Organizativo', ['2', '3']),
              ('T6. Metodología o recurso impuesto', 'T6. Metodología o recurso', ['2', '3', '4.1'])]
    cursor = aT1
    for k, (tit_doc, tit_r, aps) in enumerate(fichas):
        ini = m.idx(tit_doc, cursor, tabla='inicio')
        fin = (m.idx(fichas[k + 1][0], ini + 1, tabla='inicio') if k + 1 < len(fichas)
               else m.idx('PARTE IV', ini, tabla=True))
        qp = m.idx('Qué poner en cada apartado', ini)
        ops.append(('filas', qp, fin, [(ap, fila_t(tit_r, ap)) for ap in aps], 0))
        if tit_r.startswith('T1'):
            ops.append(('filas', qp, fin, [('Solo normativa común', ['Autores genéricos', 'Autores muy específicos del '
                                                                     'subtipo; la normativa es casi la misma'])], 0))
            ins = m.idx('Rúbrica del producto ★ · escala de observación', qp)
            fin_ins = m.idx('Errores frecuentes', ins)
            nuevo = copy.deepcopy(m.hijos()[ins])
            pon_texto(nuevo, parrafo_r(tit_r, '**Instrumentos**').replace('**Instrumentos**: ', '')
                      .replace('rúbrica del producto', 'Rúbrica del producto', 1))
            ops.append(('sust', ins, fin_ins, [nuevo]))
        if tit_r.startswith('T3'):
            ins = m.idx('Instrumentos Escala de participación', qp)
            fin_ins = m.idx('Errores frecuentes', ins)
            nuevo = copy.deepcopy(m.hijos()[ins])
            pon_texto(nuevo, '**Instrumentos**\n' + parrafo_r(tit_r, '**Instrumentos**').replace('**Instrumentos**: ', '')
                      .replace('escala de participación', 'Escala de participación', 1))
            ops.append(('sust', ins, fin_ins, [nuevo]))
        if tit_r.startswith('T6'):
            t6a = [b_ for b_ in tramo('T6. Metodología o recurso', sin=()) if b_[0] == 'tabla'][0][2][0]
            ops.append(('filas', ini, qp, [('T6a. Aprendizaje…', [None] * 6 + [t6a[1]])], 0))
        cursor = fin
    I4 = cursor
    a = m.idx('1. Antes de redactar (borrador, 9 minutos)', I4); b = m.idx('2. Identificación y presentación', a)
    ops.append(('sust', a, b, elementos(F['IV-1'])))
    a = m.idx('3. Apartados 1 a 3', b); b = m.idx('6. Apartados 5 y 6', a)
    ops.append(('sust', a, b, elementos(F['IV-3-5'])))

    # párrafos sueltos de la Parte I y la portada
    ops.append(('par', r43, None, 'Remisiones internas breves: «como se indicó en el contexto», «en coherencia con las '
                                  'líneas generales de actuación pedagógica y la concreción curricular señaladas», '
                                  '«criterio ya citado en la concreción curricular».'))
    v = m.idx('Versión 2.1 · 17 de noviembre de 2026')
    ops.append(('par', v, None, 'Versión 2.2 · 20 de noviembre de 2026 · Revisión de Gem: las correcciones de la Parte I '
                                '(hasta el 7.9), llevadas a toda la libreta'))

    # primero, celdas y párrafos (no cambian el orden de los elementos); después, de atrás hacia delante, sustituciones
    ops = [o for o in ops if o[0] in ('filas', 'par')] + sorted([o for o in ops if o[0] in ('sust', 'ins')],
                                                                 key=lambda o: o[1], reverse=True)
    for op in ops:
        tipo = op[0]
        if tipo == 'sust':
            m.sustituye(op[1], op[2], op[3])
        elif tipo == 'ins':
            m.inserta_antes(op[1], op[3])
        elif tipo == 'filas':
            cambios = op[3]
            if any(c[1] == 'COMUNICA' for c in cambios):
                hs = m.hijos()[op[1]:op[2]]
                for tr in list(filas(hs)):
                    cs = celdas(tr)
                    if len(cs) > 1 and norm(texto(cs[1])).startswith('Comunica (lectura'):
                        nueva = copy.deepcopy(tr)
                        pon_celda(cs[1], 'Comunica (lectura, escritura, oralidad y alfabetización mediática); si hay '
                                         'radio, siempre con la Red de Radios Escolares de Andalucía')
                        tr.addnext(nueva)
                        cn = celdas(nueva)
                        for tc, nuevo in zip(cn, ['◆', 'Red de Radios Escolares de Andalucía, siempre junto con '
                                                       'Comunica', 'Convocatoria específica', 'T2c, T1d']):
                            pon_celda(tc, nuevo)
                cambios = [c for c in cambios if c[1] != 'COMUNICA']
            quedan = edita_filas(m, op[1], op[2], cambios, op[4])
            if quedan:
                print('  AVISO, filas no encontradas:', [q[0] for q in quedan])
        elif tipo == 'par':
            el = m.hijos()[op[1]]
            if op[3] is not None:
                pon_texto(el, op[3], conserva_primero=texto(el).lstrip().startswith('•'))
            else:
                pon_texto(el, texto(el).replace('3. Reparto de las 2.500 palabras', '3. Reparto de las palabras '
                                                                                   '(unas 2.600)'))

    # restos de notas de cambio en textos reutilizados
    for t_ in m.b.iter(qn('w:t')):
        if t_.text and '(sustituye a la diana)' in t_.text:
            t_.text = t_.text.replace(' (sustituye a la diana)', '')
    # portada: menos espacio vertical, para que quepa en una página con la línea de versión nueva (más larga)
    for el in m.hijos():
        if el.tag == qn('w:p') and norm(texto(el)) == 'Índice':
            break
        if el.tag == qn('w:p'):
            sp = el.find('.//' + qn('w:spacing'))
            if sp is not None and int(sp.get(qn('w:before'), '0')) > 500:
                sp.set(qn('w:before'), '220')
    # portada: fuera los párrafos vacíos entre la última línea y el índice, y «2.500» en la tabla de contenido
    hs = m.hijos()
    i_ind = next(i for i, el in enumerate(hs) if el.tag == qn('w:p') and norm(texto(el)) == 'Índice')
    i_mat = max(i for i in range(i_ind) if norm(texto(hs[i])).startswith('Material de estudio personal'))
    for el in hs[i_mat + 1:i_ind]:
        if not texto(el).strip() and el.tag == qn('w:p'):
            m.b.remove(el)
    for tc in m.b.iter(qn('w:tc')):
        if 'Índice completo, 2.500 palabras' in texto(tc):
            pon_celda(tc, texto(tc).replace('2.500 palabras', 'unas 2.600 palabras'))
    for tc in m.b.iter(qn('w:tc')):
        if 'reparto de las 2.500 palabras' in texto(tc):
            pon_celda(tc, texto(tc).replace('reparto de las 2.500 palabras', 'reparto de las palabras'))
            break
    # saltos de página antes de cada parte y de la presentación, el índice y el anexo
    for clave in ('PRESENTACIÓN', 'PARTE V', 'PARTE IV', 'PARTE III', 'PARTE II', 'PARTE I'):
        try:
            m.salto_antes(m.idx(clave, tabla=True))
        except ValueError:
            print('  sin banner', clave)
    for titulo in ('Índice', 'Anexo. Recursos pendientes de verificar'):
        try:
            i = m.idx(titulo, m.idx('PARTE V', tabla=True) if titulo.startswith('Anexo') else 0)
            if titulo == 'Índice' or norm(texto(m.hijos()[i])) == titulo:
                m.salto_antes(i)
        except ValueError:
            print('  sin', titulo)
    return m


ORDEN_RPR = ['rStyle', 'rFonts', 'b', 'bCs', 'i', 'iCs', 'caps', 'smallCaps', 'strike', 'dstrike', 'outline', 'shadow',
             'emboss', 'imprint', 'noProof', 'snapToGrid', 'vanish', 'webHidden', 'color', 'spacing', 'w', 'kern',
             'position', 'sz', 'szCs', 'highlight', 'u', 'effect', 'bdr', 'shd', 'fitText', 'vertAlign', 'rtl', 'cs', 'em',
             'lang', 'eastAsianLayout', 'specVanish', 'oMath']
ORDEN_BORDES = ['top', 'left', 'start', 'bottom', 'right', 'end', 'insideH', 'insideV', 'tl2br', 'tr2bl', 'between', 'bar']


def repara_esquema(body):
    """Arregla lo que pdf2docx deja fuera del esquema: colores con «#», bordes start/end y orden de propiedades."""
    W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    for el in body.iter():
        for atr in ('color', 'fill', 'themeFill'):
            v = el.get(W + atr)
            if v and v.startswith('#'):
                el.set(W + atr, v[1:].upper())
    for cont in ('tcBorders', 'tblBorders', 'pBdr'):
        for el in body.iter(qn('w:' + cont)):
            for h in list(el):
                nombre = h.tag.split('}')[1]
                if nombre in ('start', 'end') and cont != 'pBdr':
                    h.tag = W + ('left' if nombre == 'start' else 'right')
            hijos = sorted(list(el), key=lambda h: ORDEN_BORDES.index(h.tag.split('}')[1])
                           if h.tag.split('}')[1] in ORDEN_BORDES else 99)
            for h in hijos:
                el.remove(h)
            for h in hijos:
                el.append(h)
    for tcpr in body.iter(qn('w:tcPr')):          # márgenes de celda repetidos
        for dup in tcpr.findall(qn('w:tcMar'))[1:]:
            tcpr.remove(dup)
    for shd in body.iter(qn('w:shd')):
        if shd.get(W + 'val') is None:
            shd.set(W + 'val', 'clear')
    sp = body.find(qn('w:sectPr'))
    if sp is not None and sp.find(qn('w:pgMar')) is not None and sp.find(qn('w:pgSz')) is not None:
        pm = sp.find(qn('w:pgMar')); sp.remove(pm); sp.find(qn('w:pgSz')).addnext(pm)
    for rpr in body.iter(qn('w:rPr')):
        hijos = sorted(list(rpr), key=lambda h: ORDEN_RPR.index(h.tag.split('}')[1])
                       if h.tag.split('}')[1] in ORDEN_RPR else 99)
        for h in hijos:
            rpr.remove(h)
        for h in hijos:
            rpr.append(h)
    PB.ordena_esquema(body)


def ids_unicos(d):
    n = 1000
    for dp in d.element.body.iter(qn('wp:docPr')):
        n += 1
        dp.set('id', str(n))


CAMBIOS_INDICE = {'3. Reparto de las 2.500 palabras': '3. Reparto de las palabras (unas 2.600)'}


def entradas_indice():
    """Entradas del índice de la versión 2.1 (páginas 2 y 3 del PDF), con su nivel por la sangría."""
    txt = subprocess.run(['pdftotext', '-f', '2', '-l', '3', '-layout', PDF, '-'], capture_output=True,
                         text=True).stdout
    out = []
    for linea in txt.split('\n'):
        if '...' not in linea:
            continue
        sangria = len(linea) - len(linea.lstrip())
        titulo = re.sub(r'\s*\.{3,}.*$', '', linea.strip()).strip()
        nivel = 0 if sangria < 3 else (1 if sangria < 9 else 2)
        out.append((CAMBIOS_INDICE.get(titulo, titulo), nivel))
    return out


def _parrafo_indice(titulo, nivel, pagina):
    neg = '<w:b/>' if nivel == 0 else ''
    rpr = (f'<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>{neg}'
           f'<w:color w:val="{L.AZUL if nivel == 0 else L.TXT}"/><w:sz w:val="{20 if nivel == 0 else 19}"/></w:rPr>')
    antes = 120 if nivel == 0 else 0
    return parse_xml(f'<w:p {PB.NS}><w:pPr><w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9780"/></w:tabs>'
                     f'<w:spacing w:before="{antes}" w:after="30"/><w:ind w:left="{nivel * 340}"/></w:pPr>'
                     f'<w:r>{rpr}<w:t xml:space="preserve">{titulo}</w:t></w:r><w:r>{rpr}<w:tab/></w:r>'
                     f'<w:r>{rpr}<w:t>{pagina}</w:t></w:r></w:p>')


def pon_indice(d, paginas_por_titulo):
    b = d.element.body
    hs = [el for el in b if el.tag in (qn('w:p'), qn('w:tbl'))]
    i0 = next(i for i, el in enumerate(hs) if el.tag == qn('w:p') and norm(texto(el)) == 'Índice')
    i1 = next(i for i, el in enumerate(hs) if el.tag == qn('w:tbl') and sin_espacios(texto(el)) == 'PRESENTACIÓN')
    fin = i1 - 1 if not texto(hs[i1 - 1]).strip() else i1       # deja el salto de página
    for el in hs[i0 + 1:fin]:
        b.remove(el)
    ancla = hs[fin]
    for titulo, nivel in entradas_indice():
        ancla.addprevious(_parrafo_indice(titulo, nivel, paginas_por_titulo.get(titulo, '')))


def paginas_de(ruta):
    tmp = tempfile.mkdtemp()
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, ruta], capture_output=True)
    pdf = os.path.join(tmp, os.path.basename(ruta).replace('.docx', '.pdf'))
    paginas = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
    res, minimo = {}, 4
    ents = entradas_indice()
    for titulo, nivel in ents:
        if re.match(r'^(Parte [IVX]+\.|Presentación\.|Anexo\.)', titulo):
            continue
        for k in range(minimo - 1, len(paginas)):
            if any(norm(l).startswith(titulo) and '....' not in l for l in paginas[k].split('\n')):
                res[titulo] = k + 1
                minimo = k + 1
                break
    siguiente = None
    for titulo, nivel in reversed(ents):          # las partes, con la página de su primera entrada
        if titulo in res:
            siguiente = res[titulo]
        elif siguiente:
            res[titulo] = siguiente
    return res, len(paginas) - 1


def main():
    m = monta()
    ids_unicos(m.d)
    repara_esquema(m.b)
    zoom = m.d.settings.element.find(qn('w:zoom'))
    if zoom is not None and zoom.get(qn('w:percent')) is None:
        zoom.set(qn('w:percent'), '100')
    pon_indice(m.d, {})
    m.d.save(SALIDA)
    pags, total = paginas_de(SALIDA)
    d = Document(SALIDA)
    pon_indice(d, pags)
    d.save(SALIDA)
    print('índice:', len(pags), 'entradas con página;', total, 'páginas en LibreOffice')
    print(SALIDA)


if __name__ == '__main__':
    main()
