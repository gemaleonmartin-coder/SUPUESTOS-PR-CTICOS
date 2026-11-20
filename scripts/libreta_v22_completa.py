# -*- coding: utf-8 -*-
"""Libreta mágica 2.2: todas las páginas que cambian (Partes I a IV), rehechas en Word desde el PDF de Rafa con su
estética, mientras llega su Word (fase 38). Une los apartados 6 a 7.9 de libreta_v22_parte1.py con los bloques del
resto de la libreta de libreta_v22_resto.py.

Uso:  python3 scripts/libreta_v22_completa.py
Salida: libreta-magica/Libreta_magica_v22_paginas_que_cambian.docx (lo cambiado en gris y un comentario en cada cambio)
        libreta-magica/Libreta_magica_v22_paginas_que_cambian_limpio.docx
"""
import os
import sys

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libreta_v22_parte1 as L  # noqa: E402
import libreta_v22_resto as R  # noqa: E402
import plantillas_bocadillos as PB  # noqa: E402
import textos_libreta_v22 as T  # noqa: E402

SAL_REV = os.path.join(L.RAIZ, 'libreta-magica', 'Libreta_magica_v22_paginas_que_cambian.docx')
SAL_LIM = os.path.join(L.RAIZ, 'libreta-magica', 'Libreta_magica_v22_paginas_que_cambian_limpio.docx')

L.COMENTARIOS.update(R.COMENTARIOS)


class Completa(L.Libreta):
    primera_parte = True

    def portadilla(self):
        self.p('**Libreta mágica 2.2 · Todas las páginas que cambian (Partes I a IV).** Rehechas en Word desde el PDF de '
               'Rafa (versión 2.1), con su estética, mientras llega su Word; después se pasan a él. La presentación (uso, '
               'reglas de oro y chuleta) y la Parte V no cambian. Cada bloque indica a qué página sustituye. '
               + ('Lo cambiado va en gris, con un comentario en cada cambio; lo pendiente, en naranja. ' if self.revision
                  else 'Lo pendiente va en naranja. ')
               + 'Los apartados 6 a 7.9 de la Parte I van enteros; el 7.9 solo recibe lo que llega de la metodología.')

    def parte(self, t):
        self.h1(t)
        el = self.d.element.body.find(qn('w:sectPr')).getprevious()
        if not self.primera_parte:
            el.find(qn('w:pPr')).insert(0, OxmlElement('w:pageBreakBefore'))
        self.primera_parte = False

    def nota(self, t):
        self.parrafo([(PB._run('▸ ', color=L.NAR, tam=9, negrita=True), None)] + self.runs(t, tam=9, color='6A7075'),
                     despues=80)

    def check(self, ts):
        for t in ts:
            self.parrafo([(PB._run('☐', color=L.TEAL, tam=L.TAM, negrita=True), None),
                          (f'<w:r>{PB._rpr(tam=L.TAM)}<w:tab/></w:r>', None)] + self.runs(t),
                         despues=40, ind='<w:tabs><w:tab w:val="left" w:pos="426"/></w:tabs>'
                                         '<w:ind w:left="426" w:hanging="426"/>', alin='both')

    def orientaciones(self, clave):
        areas = list(T.ORIENTACIONES)
        n = max(len(v) for v in T.ORIENTACIONES.values())
        filas = []
        for i in range(n):
            fila = []
            for a in areas:
                ideas = T.ORIENTACIONES[a]
                if i < len(ideas):
                    idea, est = ideas[i]
                    fila.append(f'<<{"★ **" + idea + "**" if est else idea}>>{{#{clave}}}')
                else:
                    fila.append('')
            filas.append(fila)
        self.tabla_libre(areas, filas, [17.4 / len(areas)] * len(areas))

    def tabla_libre(self, cab, filas, anchos):
        """Como tabla_b, pero sin la primera columna en negrita."""
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
                    e = OxmlElement(f'w:{lado}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4')
                    e.set(qn('w:color'), L.BORDE); b.append(e)
                tcpr.append(b)
                PB._margenes(celda._tc, 80, 80, 30, 30)
                if r_i == 0:
                    PB._fondo(celda._tc, L.AZUL)
                    self.parrafo(self.runs(cab[c_i], tam=9, color='FFFFFF', negrita=True), contenedor=celda._tc,
                                 despues=0)
                    continue
                if r_i % 2 == 0:
                    PB._fondo(celda._tc, L.ALT)
                self.parrafo(self.runs(filas[r_i - 1][c_i], tam=9), contenedor=celda._tc, despues=0)
        self._anade(tbl)
        self.p('', despues=60)

    def bloque(self, b):
        tipo = b[0]
        if tipo == 'h1':
            self.parte(b[1])
        elif tipo == 'h2':
            self.h2(b[1])
        elif tipo == 'p':
            self.p(b[1])
        elif tipo == 'sub':
            self.sub(b[1])
        elif tipo == 'nota':
            self.nota(b[1])
        elif tipo == 'bul':
            self.lista(b[1], False)
        elif tipo == 'num':
            self.lista(b[1], True)
        elif tipo == 'check':
            self.check(b[1])
        elif tipo == 'tabla':
            self.tabla_b(b[1], b[2], b[3])
        elif tipo == 'ficha':
            self.tabla_b(['Finalidad', 'Extensión', 'Criterio'], [['**' + b[1] + '**', b[2], b[3]]], [8.6, 4.5, 4.3])
        elif tipo == 'clave':
            self.clave(b[1])
        elif tipo == 'plantilla':
            self.plantilla(b[1])
        elif tipo == 'plantilla79':
            self.plantilla79()
        elif tipo == 'plantilla_txt':
            self.caja('Plantilla de redacción', [(t, c, None) for t, c in b[1]], L.CREMA, L.NAR, L.NAR, plantilla=True)
        elif tipo == 'orientaciones':
            self.orientaciones(b[1])
        else:
            raise ValueError(tipo)

    def monta(self):
        self.portadilla()
        for b in R.B:
            if b[0] == 'apartados_6_a_79':
                for b2 in L.B:
                    if b2[0] == 'h1' and b2[1].startswith('6.'):
                        self.h1(b2[1])
                    elif b2[0] == 'h1':
                        self.h1(b2[1])
                    else:
                        self.bloque(b2)
            else:
                self.bloque(b)
        if self.revision:
            self.comentarios()


def main():
    for revision, ruta in ((True, SAL_REV), (False, SAL_LIM)):
        lib = Completa(revision)
        lib.monta()
        print(lib.guarda_en(ruta), len(lib.pendientes_com) if revision else '')


if __name__ == '__main__':
    main()
