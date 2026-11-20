# -*- coding: utf-8 -*-
"""Word de plantillas por importancia (fase 38), que sustituye al de bocadillos: por cada apartado, la plantilla de
redacción párrafo a párrafo en su cuadro amarillo y, debajo, las opciones para completar cada hueco ordenadas por grado
de importancia: lo fijo arriba, después la primera opción y, al final, los comodines.

Uso:  python3 scripts/plantillas_por_importancia.py   →   libreta-magica/Plantillas_por_importancia_v22.docx
Textos: opciones_plantillas_v22.py (plantillas y opciones) y textos_libreta_v22.py (tablas de elementos y de
orientaciones).
"""
import os
import re
import sys

from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Cm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opciones_plantillas_v22 as O  # noqa: E402
import plantillas_bocadillos as PB  # noqa: E402
import textos_libreta_v22 as T  # noqa: E402

SALIDA = os.path.join(PB.RAIZ, 'libreta-magica', 'Plantillas_por_importancia_v22.docx')
ANCHO = 17.4
INSIGNIA = {'F': (' FIJO ', PB.NARANJA_BORDE), '1': (' 1.ª OPCIÓN ', PB.VERDE_AZ), 'C': (' COMODÍN {n} ', '8C8C8C')}


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
               antes=600, despues=120)
        self.p(PB._run('Plantillas por importancia', negrita=True, color=PB.AZUL, tam=26), despues=60)
        self.p(PB._run('Las plantillas de redacción de la libreta mágica (apartados 7.1 a 7.9) y, debajo de cada párrafo, '
                       'con qué se completa cada hueco, de lo más importante a lo menos', color=PB.VERDE_AZ, tam=12),
               despues=240)
        self.p(PB._run('Cómo se lee', negrita=True, color=PB.AZUL, tam=12), despues=60)
        for nivel, texto in (('F', 'se escribe siempre así; va arriba.'),
                             ('1', 'la opción más importante; si depende del área, hay una por área.'),
                             ('C', 'por si no se puede usar la primera; el 1 antes que el 2.')):
            etq, color = INSIGNIA[nivel]
            self.p(PB._run(etq.format(n=1), negrita=True, color='FFFFFF', tam=8, fondo=color)
                   + PB._run('  ' + texto, tam=10.5, color='262626'), despues=80)
        self.p(PB._run('El número naranja de cada hueco lleva a sus opciones, justo debajo del cuadro. En el 4.1, los '
                       'bloques «según el supuesto» van del más frecuente al menos frecuente: se escriben uno o dos. Los '
                       'autores se concretarán con los temas.', tam=10.5, color='262626'), antes=120, despues=60,
               alin='both')
        self.p(PB._run('Versión 2.2 · 20 de noviembre de 2026 · Acompaña a la libreta mágica 2.2. Material de estudio '
                       'personal.', color=PB.GRIS_TXT, tam=8.5, cursiva=True), antes=360)

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
        for par in c._tc.findall(qn('w:p')):        # el cuadro, con sus opciones en la misma página
            par.find(qn('w:pPr')).insert(0, OxmlElement('w:keepNext'))
        t._tbl.find(qn('w:tr')).get_or_add_trPr().append(OxmlElement('w:cantSplit'))
        self._anade(t._tbl)

    def opciones(self, clave, n, fila_texto):
        datos = O.OPCIONES[clave][n]
        m = re.search(r'\[%d\|([^\]]*)\]' % n, fila_texto)
        if m:
            titulo = datos.get('titulo') or '[' + m.group(1) + ']'
        else:
            titulo = datos.get('titulo') or 'Frase fija'
        el = self.p(PB._run(f'{n}  ', negrita=True, color=PB.NARANJA_BORDE, tam=10)
                    + PB._run(titulo, negrita=True, color=PB.VERDE_AZ, tam=10), antes=100, despues=40,
                    ind='<w:ind w:left="120"/>')
        el.find(qn('w:pPr')).insert(0, OxmlElement('w:keepNext'))
        k_com = 0
        orden = sorted(datos['ops'], key=lambda o: 'F1C'.index(o[0]))
        for nivel, texto in orden:
            etq, color = INSIGNIA[nivel]
            if nivel == 'C':
                k_com += 1
                etq = etq.format(n=k_com)
            el = self.p(PB._run(etq, negrita=True, color='FFFFFF', tam=7.5, fondo=color)
                        + PB._run('  ' + texto, tam=9.5, color='262626'), despues=50, alin='both',
                        ind='<w:ind w:left="440" w:hanging="0"/>')
            el.find(qn('w:pPr')).insert(0, OxmlElement('w:keepLines'))

    def apartado(self, clave):
        datos = O.PLANTILLAS[clave]
        self.titulo(datos['titulo'])
        for i, fila in enumerate(datos['filas']):
            if fila.get('etiqueta'):
                el = self.p(PB._run(fila['etiqueta'], negrita=True, versalitas=True, color=PB.AZUL, tam=8.5), antes=160,
                            despues=40)
                el.find(qn('w:pPr')).insert(0, OxmlElement('w:keepNext'))
            self.cuadro(PB.runs_plantilla(fila['texto'], tam=10.5),
                        'Plantilla de redacción' if i == 0 else None)
            for m in re.finditer(r'[\[{](\d+)\|', fila['texto']):
                self.opciones(clave, int(m.group(1)), fila['texto'])
            self.p('', despues=80)

    def tabla_elementos(self):
        self.p(PB._run('Tabla de elementos curriculares de quinto', negrita=True, color=PB.AZUL, tam=12), antes=200,
               despues=60)
        self.p(PB._run('Una competencia por fila, con su criterio de quinto, un saber vinculado a ese criterio y dos '
                       'descriptores, comprobados en el BOJA; los textos son resúmenes. El área eje, entera; la segunda, '
                       'solo la competencia.', tam=9.5, color=PB.GRIS_TXT, cursiva=True), despues=100, alin='both')
        self.tabla(['Área', 'Competencia específica', 'Criterio de 5.º', 'Un saber básico', 'Descriptores'],
                   [list(f) for f in T.ELEMENTOS], [1.2, 5.0, 4.4, 4.6, 2.2])


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
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    PB.ordena_esquema(c.d.element.body)
    zoom = c.d.settings.element.find(qn('w:zoom'))
    if zoom is not None and zoom.get(qn('w:percent')) is None:
        zoom.set(qn('w:percent'), '100')
    c.d.save(SALIDA)
    print(SALIDA)


if __name__ == '__main__':
    main()
