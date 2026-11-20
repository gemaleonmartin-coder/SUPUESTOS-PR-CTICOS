# -*- coding: utf-8 -*-
"""Libreta mágica 2.2, Parte I, apartados 6 y 7.1 a 7.9 (páginas 11 a 20 de la versión 2.1), rehechos en Word desde el
PDF de Rafa mientras llega su Word, con la estética de la libreta y las correcciones de Gem (fase 38).

Uso:  python3 scripts/libreta_v22_parte1.py
Salida: libreta-magica/Libreta_magica_v22_Parte_I_6_a_7.9.docx (lo cambiado en gris y un comentario en cada cambio)
        libreta-magica/Libreta_magica_v22_Parte_I_6_a_7.9_limpio.docx (sin gris ni comentarios). Lo pendiente, en naranja
        en los dos, con su nota dentro.

Marcas en los textos:  <<texto>>{#clave}  nuevo o cambiado (gris) con el comentario COMENTARIOS[clave];
                       !!texto!!          pendiente (naranja), con la nota dentro;
                       **texto**          negrita;   [texto]  hueco de plantilla (verde azulado, negrita).
Las plantillas salen de textos_libreta_v22.py (las mismas del Word de bocadillos); las filas marcadas como nuevas van en
gris con el comentario de COMENT_PLANTILLA.
"""
import os
import re
import sys

from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Cm
from docx.text.paragraph import Paragraph
from docx.text.run import Run

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plantillas_bocadillos as PB  # noqa: E402
import textos_libreta_v22 as T  # noqa: E402

RAIZ = PB.RAIZ
SAL_REV = os.path.join(RAIZ, 'libreta-magica', 'Libreta_magica_v22_Parte_I_6_a_7.9.docx')
SAL_LIM = os.path.join(RAIZ, 'libreta-magica', 'Libreta_magica_v22_Parte_I_6_a_7.9_limpio.docx')
GRIS, NARANJA = 'BFBFBF', 'FFC000'
AZUL, TEAL, NAR, CREMA, CLAVE_F, TXT, BORDE, ALT = ('1F3A5F', '2A7F8E', 'C98A1B', 'FDF6E8', 'E8F3F5', '222B33',
                                                   'C9D6DF', 'F4F8FA')
TAM = 10
AUTOR, INIC = 'Claude', 'C'

# ---------------------------------------------------------------------------------------------------------------
COMENTARIOS = {
    '61a': 'Antes: «… escuelas infantiles de segundo grado …», sin el Decreto 483/2026. Ahora: «segundo ciclo», como en el '
           'texto consolidado del BOJA (31/8/2026) y en tu programación, y «modificado por el Decreto 483/2026», que Gem '
           'quiere ver en el 4.1.',
    '61b': 'Antes: 4.2.1. Ahora: 4.2 (datos). Por qué: el artículo 3.1 de la Orden entra en los datos identificativos (lo '
           'pide Gem, como Edu), así que la primera mención completa se adelanta.',
    '61c': 'Antes: «Norma específica: la del tema (Parte II, apartado 3, y Parte III)». Ahora: la instrucción del área. Por '
           'qué: Gem quiere que la tercera norma del apartado 3 sea siempre una instrucción (lectura, matemáticas o '
           'bibliotecas). Las de bibliotecas de 2013 están sustituidas por las de 10 de septiembre de 2025.',
    '61d': 'Antes: «cinco primeras menciones: 175 palabras». Ahora: seis, con la instrucción y el Decreto 483/2026 '
           '(estimación propia: unas 235 palabras).',
    '62a': 'Antes: «2 | Currículo estatal y andaluz + norma específica». Ahora: artículo 10.2 del Real Decreto 157/2022, '
           'artículo 7.3 del Decreto 101/2023 y una instrucción. Por qué: corrección de Gem; el 7.3 casa con el 10.2 y el '
           '7.2 se queda para metodología (decisión de Gem).',
    '62b': 'Antes: «Decreto 328/2010». Ahora: con el Decreto 483/2026 y el artículo 21.3 (líneas, objetivos y criterios '
           'pedagógicos).',
    '62c': 'Fila nueva: el artículo 3.1 de la Orden, en los datos identificativos (corrección de Gem).',
    '62d': 'Antes: «Orden de 30 de mayo de 2023». Ahora: su anexo II, en forma corta (ya presentada en los datos).',
    '62e': 'Antes: «Decreto 101/2023, artículos 6 y 7». Ahora: artículo 6 con sus tres principios fijos, 7.2 y el anexo II '
           'de la Orden (orientaciones metodológicas del área).',
    '62f': 'Antes: «cinco o seis normas». Ahora: «seis o siete», por la instrucción y el Decreto 483/2026.',
    '71a': 'Antes: «130 palabras · 6 min · 4 párrafos». Ahora: unas 165 y 5 párrafos, por el preíndice. Decisión de Gem (20/11/2026): se aceptan unas 2.600 palabras en total (unos 5 minutos más de escritura).',
    '71b': 'Nuevo: el preíndice (corrección de Gem: faltaba).',
    '71c': 'Antes: «cuatro movimientos». Ahora: cinco, con el preíndice.',
    '71d': 'Antes: «Anunciar el índice … → Suprimirlo: no puntúa». Ahora lo contrario: el preíndice es obligatorio (Gem).',
    '72a': 'Antes: «un recurso que se usará». Ahora, con ejemplos (Gem: biblioteca municipal, talleres gratuitos, '
           'residencia).',
    '72b': 'Antes: «una línea general de actuación pedagógica y un objetivo de mejora». Ahora: los nombres del Decreto '
           '483/2026 (artículo 21.3, letras a y b, del Decreto 328/2010).',
    '72c': 'Nuevo: el sociograma en el alumnado (Gem), que después sirve para los equipos.',
    '72d': 'Antes: «Líneas de actuación y objetivos de mejora … del Reglamento Orgánico (2026)». Ahora: los nombres '
           'completos del Decreto 483/2026, sin siglas, con la norma en el 4.1.',
    '72e': 'Fila nueva: la nomenclatura antigua.',
    '72f': 'Bocadillo nuevo con ejemplos cortos (Gem). Los largos están en el Word de plantillas con bocadillos.',
    '73a': 'Nuevo: lo que Gem quiere dejar claro, la normativa casi fija y los autores muy específicos.',
    '73b': 'Antes: «Dos autores con año y aportación concreta al tema». Ahora: muy específicos del tema.',
    '73c': 'Antes: «Marco curricular estatal y andaluz, con nombre completo». Ahora: el 10.2 del Real Decreto con el 7.3 '
           'del Decreto 101/2023 (corrección de Gem; el 7.2, en metodología).',
    '73d': 'Antes: «Una norma específica del tema con lo que establece». Ahora: una instrucción según el área (Gem).',
    '73e': 'Antes: «…; principio pedagógico u Objetivo de Desarrollo Sostenible vinculado». Ahora sin ellos: los principios '
           'van en metodología y el ODS, en los datos identificativos (Gem).',
    '73f': 'Nuevo: la valoración que pidió Gem de los artículos 5 y 6 (no hay que estudiar nada más: ya están en 4.2.1 y '
           '4.2.2).',
    '73g': 'Antes: «currículo estatal y andaluz en una frase; norma específica en otra». Ahora: el 10.2 y el 7.3; la '
           'instrucción.',
    '73h': 'Antes: «aquí, currículo y norma específica». Ahora: instrucción del área.',
    '73i': 'Fila nueva: los principios pedagógicos no van aquí (Gem: si se explican aquí, no se pueden relacionar luego con '
           'la metodología).',
    '75a': 'Antes: «230 palabras · 10 min · 4 movimientos». Ahora: unas 275 los bloques fijos, por los nombres '
           'completos de los dos decretos, y 5 movimientos. Decisión de Gem (20/11/2026): se aceptan unas 2.600 palabras en total (unos 5 minutos más de escritura).',
    '75b': 'Antes: «Origen de la propuesta en un documento del centro, coherente con el contexto». Ahora: la línea o el '
           'objetivo solo se citan (Gem: van arriba, en el contexto).',
    '75c': 'Antes: «equipo de ciclo, equipo docente y equipo de orientación o especialista». Ahora: el equipo técnico en '
           'lugar del equipo docente, que pasa a los bloques según el supuesto (bloque A de la libreta de Gem).',
    '75d': 'Antes: «Cauce y calendario de coordinación». Ahora: con los especialistas de atención a la diversidad, que '
           'según Gem van siempre.',
    '75e': 'Nuevo: espacios y criterios pedagógicos, fijos (Gem). La actividad complementaria entra aquí y no en el '
           'contexto. Solo ella casa al pie de la letra con uno de los seis criterios del decreto (tiempo escolar y '
           'extraescolar); el recurso digital y la cultura andaluza se presentan como acuerdos del centro.',
    '75f': 'Antes: «Familias: cómo se informan y cómo participan» (obligatorio). Ahora, bloque según el supuesto (Gem).',
    '75g': 'Antes: «Primera mención completa del Decreto 328/2010». Ahora: modificado por el Decreto 483/2026 (Gem).',
    '75h': 'Nuevo: los bloques según el supuesto, de la libreta de Gem (protección de datos, solo si hay imágenes).',
    '75i': 'Antes: «(equipo técnico → ciclo → equipo docente)». Ahora: sin el equipo docente, que es bloque opcional.',
    '75j': 'Antes: «4. Familias, entorno y cierre». Ahora: espacios y criterios pedagógicos y, después, uno o dos bloques.',
    '75k': 'Nuevo: qué son los criterios pedagógicos del Decreto 483/2026 y para qué se usan en el supuesto (Gem).',
    '75l': 'Filas nuevas.',
    '75m': 'Antes: «En el modelo estándar se omite la frase del agente externo o la del trámite…». Ahora: la regla de los '
           'bloques.',
    '76a': 'Antes: «90 palabras · 4 min · 1 párrafo de 3 frases». Ahora: unas 215 y 4 frases, con el ODS y el '
           'nombre completo de la Orden. Decisión de Gem (20/11/2026): se aceptan unas 2.600 palabras en total (unos 5 minutos más de escritura).',
    '77f': 'Antes: «220 palabras · 10 min». Ahora: unas 150, porque el nombre completo de la Orden pasa a los datos '
           'identificativos.',
    '76b': 'Nuevo: la cuarta frase (Gem: el ODS y lo que siempre dice Edu del artículo 3.1 de la Orden).',
    '76c': 'Antes: «vínculo con el principio pedagógico anunciado en 3». Ahora no: los principios ya no se anuncian en 3.',
    '76d': 'Fila nueva.',
    '77a': 'Antes: «Primera mención completa de la Orden de 30 de mayo de 2023». Ahora ya está presentada en los datos.',
    '77b': 'Nuevo y obligatorio: la segunda área (Gem: una sola queda pobre). Antes era recomendable.',
    '77c': 'Antes: «… segunda competencia específica de otra área, solo nombrada; …». Ahora es obligatoria.',
    '77d': 'Antes: «si deja libertad, un área eje y una o dos conectadas». Ahora: una entera y otra con su competencia.',
    '77e': 'Fila nueva.',
    '78a': 'Antes: «3 párrafos». Ahora: 4.',
    '78b': 'Antes: «dos o tres, cada uno con su ejemplo». Ahora: siempre el DUA, Andalucía y lo digital (Gem).',
    '78c': 'Nuevo: técnicas cooperativas concretas (en el Word de plantillas, bocadillo con las técnicas).',
    '78d': 'Antes: «Enfoque integrador, interdisciplinar y holístico: qué aporta cada área». Ahora se acredita en 3 y el '
           'párrafo de la plantilla queda marcado para reubicar (Gem).',
    '78e': 'Antes: «Recursos tecnológicos e innovadores con finalidad didáctica». Ahora: con el principio c) y al final de '
           'las actividades del 4.2.3 (Gem).',
    '78f': 'Nuevo: las orientaciones metodológicas de cada área, último bloque (Gem). Están en el anexo II de la Orden '
           '(introducción de cada área), no en el III: el III es la vinculación de objetivos y descriptores; las páginas '
           'del BOJA llevan la cabecera «ANEXO II y III».',
    '78g': 'Antes: «…; conexión con la realidad andaluza; …». Ahora es obligatoria (principio g).',
    '78h': 'Antes: «(4) interdisciplinariedad; (5) recursos materiales, tecnológicos y de accesibilidad». Ahora: '
           'materiales y formatos; orientaciones del área.',
    '78i': 'Filas nuevas.',
    '79a': 'Nuevo: la frase de los recursos digitales que estaba en metodología (Gem: va en la secuencia, al final de las '
           'actividades). El resto del 7.9 no se ha revisado (se verá en la próxima clase).',
}

COMENT_PLANTILLA = {
    ('7.1', 4): 'Nuevo: el preíndice, en registro académico, a partir de la versión breve de la libreta de Gem.',
    ('7.2', 0): 'Antes: «Dispone de [recurso del entorno], que se aprovechará…». Ahora: recursos, con bocadillo de '
                'ejemplos.',
    ('7.2', 1): 'Antes: «… como línea general de actuación pedagógica [línea] y … el objetivo de mejora de [objetivo]». '
                'Ahora: los nombres del Decreto 483/2026.',
    ('7.2', 2): 'Antes: «Según la evaluación inicial, destaca por…». Ahora, con el sociograma y la cohesión del grupo.',
    ('7.3', 1): 'Antes: Real Decreto y Decreto 101/2023 sin artículo y «cuyo artículo 6 incluye entre los principios '
                'pedagógicos…»; norma específica del tema. Ahora: el 10.2 y el 7.3, sin principios (van en 4.2.2), y la '
                'instrucción del área.',
    ('7.5', 0): 'Antes: «… parte de [objetivo de mejora o línea de actuación] del proyecto educativo…». Ahora solo se cita '
                'lo del contexto.',
    ('7.5', 1): 'Antes: Decreto 328/2010 «de segundo grado», sin el Decreto 483/2026, y la frase del equipo docente. Ahora: '
                'modificado por el Decreto 483/2026; el equipo docente pasa a bloque opcional.',
    ('7.5', 3): 'Nuevo bloque fijo: espacios y criterios pedagógicos (actividad complementaria, recurso digital y cultura '
                'andaluza). El artículo 27.2.f) del Decreto 328/2010 (redacción de 2026) incluye en las programaciones las '
                'actividades complementarias que proponen los equipos de ciclo.',
    ('7.5', 4): 'Antes, fijo: «Las familias son informadas mediante…». Ahora, bloque según el supuesto, en dos líneas.',
    ('7.5', 5): 'Nuevo: protección de datos, opcional (Ley Orgánica 3/2018: menores de catorce años, autorización de las '
                'familias).',
    ('7.5', 6): 'Antes, fijo. Ahora, bloque según el supuesto.',
    ('7.5', 7): 'Nuevo bloque según el supuesto (libreta de Gem, bloque F).',
    ('7.5', 8): 'Nuevo bloque según el supuesto (libreta de Gem, bloque H).',
    ('7.5', 9): 'Nuevo bloque según el supuesto (libreta de Gem). La hora de autonomía del tercer ciclo puede dedicarse a '
                'proyectos interdisciplinares.',
    ('7.6', 1): 'Nuevo: el ODS y el artículo 3.1 de la Orden (primera mención, con su nombre completo).',
    ('7.7', 0): 'Antes: la primera mención completa de la Orden y «contribuye al objetivo de etapa» sin norma. Ahora: el '
                'objetivo con el artículo 5 del Decreto 101/2023 y la Orden en forma corta.',
    ('7.7', 1): 'Antes: «De forma complementaria, desde [segunda área] se trabaja…». Ahora, más claro: la segunda área con '
                'su competencia resumida.',
    ('7.8', 0): 'Antes: «[principio 1] ([ejemplo]), [principio 2] ([ejemplo]) y el DUA». Ahora: siempre el DUA, Andalucía y '
                'lo digital.',
    ('7.8', 1): 'Antes: «De acuerdo con su artículo 7…» en el primer párrafo. Ahora abre el segundo, con la metodología y '
                'las técnicas.',
    ('7.8', 2): 'Antes, dentro del último párrafo. Ahora: materiales y formatos, sin los recursos tecnológicos (pasan al '
                '4.2.3) ni el entorno andaluz (ya es principio).',
    ('7.8', 3): 'Nuevo: las orientaciones metodológicas del área, como último bloque (Gem).',
    ('7.8', 4): 'Marcado para reubicar, como pidió Gem: el párrafo es bueno, pero no va aquí.',
    ('7.9', 0): 'Nuevo: la frase de los recursos digitales, que llega de la metodología.',
}

# ---------------------------------------------------------------------------------------------------------------
# Contenido: las páginas 11 a 20 de la versión 2.1, tal cual, con los cambios marcados.
B = []


def h1(t): B.append(('h1', t))
def h2(t): B.append(('h2', t))
def p(t): B.append(('p', t))
def sub(t): B.append(('sub', t))
def bul(*ts): B.append(('bul', list(ts)))
def num(*ts): B.append(('num', list(ts)))
def tabla(cab, filas, anchos, cab_azul=True): B.append(('tabla', cab, filas, anchos))
def ficha(fin, ext, cri, anchos=(8.6, 4.5, 4.3)): B.append(('tabla', ['Finalidad', 'Extensión', 'Criterio'],
                                                            [[fin, ext, cri]], list(anchos)))
def plantilla(clave): B.append(('plantilla', clave))
def clave(t): B.append(('clave', t))


h1('6. Normas: primeras menciones y citas mínimas')
h2('6.1. Nombre completo para memorizar y dónde se da')
tabla(['Norma', 'Nombre completo (primera mención)', 'Apartado', 'Forma posterior'], [
    ['Ley orgánica', 'Ley Orgánica 2/2006, de 3 de mayo, de Educación, modificada por la Ley Orgánica 3/2020, de 29 de '
                     'diciembre', '1', 'LOE modificada por LOMLOE'],
    ['Currículo estatal', T.RD_COMPLETO, '3', 'Real Decreto 157/2022'],
    ['Currículo andaluz', T.D101_COMPLETO, '3', 'Decreto 101/2023'],
    ['Reglamento Orgánico', '<<' + T.D328_COMPLETO + ', modificado por el ' + T.D483_COMPLETO + '>>{#61a}', '4.1',
     'Decreto 328/2010'],
    ['Orden de desarrollo', T.ORDEN_COMPLETA, '<<4.2 (datos)>>{#61b}', 'Orden de 30 de mayo de 2023'],
    ['<<Instrucción del área>>{#61c}', '<<Instrucciones de 21 de junio de 2023 (lectura), de 18 de junio de 2024 '
                                       '(matemáticas) o de 10 de septiembre de 2025 (bibliotecas), con su nombre '
                                       'completo (Parte II, 3)>>{#61c}', '3', '<<Instrucciones de [fecha]>>{#61c}'],
], [2.9, 9.0, 2.0, 3.5])
p('<<Coste aproximado de las seis primeras menciones (con la instrucción y el Decreto 483/2026): unas 235 '
  'palabras.>>{#61d} Tras cada una, «(en adelante, …)». Cuando se cite el Reglamento Orgánico, el proyecto educativo, las '
  'programaciones o la tutoría, se añade «modificado por el Decreto 483/2026»; cuando se citen medidas de diversidad o '
  'programas de refuerzo, «modificada por la Orden de 31 de agosto de 2026».')
h2('6.2. Citas mínimas por apartado (C13)')
tabla(['Apartado', 'Autores', 'Normas'], [
    ['1', '1', 'Ley orgánica'],
    ['3', '2', '<<Real Decreto 157/2022, artículo 10.2; Decreto 101/2023, artículo 7.3; y una instrucción: lectura '
               '(Instrucciones de 21 de junio de 2023), matemáticas (Instrucciones de 18 de junio de 2024) o bibliotecas '
               '(Instrucciones de 10 de septiembre de 2025)>>{#62a}'],
    ['4.1', '—', '<<Decreto 328/2010, modificado por el Decreto 483/2026 (artículo 21.3)>>{#62b}'],
    ['<<4.2 (datos)>>{#62c}', '<<—>>{#62c}', '<<Orden de 30 de mayo de 2023, artículo 3.1>>{#62c}'],
    ['4.2.1', '—', '<<Orden de 30 de mayo de 2023, anexo II (forma corta)>>{#62d}'],
    ['4.2.2', '1', '<<Decreto 101/2023, artículos 6 (letras c, e y g) y 7.2; Orden de 30 de mayo de 2023, anexo II>>{#62e}'],
    ['4.2.4', '—', 'Orden de 30 de mayo de 2023, artículos 27 y 33'],
    ['4.2.5', '(opcional)', 'Orden de 30 de mayo de 2023, artículos 9 y 10'],
], [2.4, 2.4, 12.6])
p('Total: tres o cuatro autores y <<seis o siete normas>>{#62f}, todos en el apartado 6.')

h1('7. Manual de cada apartado')
p('Cada ficha recoge: finalidad, extensión, criterio que atiende, contenido (obligatorio y recomendable), estructura '
  'interna, errores y plantilla de redacción.')

# 7.1 -------------------------------------------------------------------------------------------------------------
h2('7.1. Introducción')
ficha('**Demostrar en diez líneas que se ha entendido el enunciado, que el tema importa y qué se va a proponer. Primera '
      'impresión sobre la expresión escrita**',
      '<<165 palabras · 7 min · 5 párrafos>>{#71a}', 'C1 (indicador 1: importancia del supuesto), C10, C13')
sub('Contenido obligatorio')
bul('Importancia social y educativa del tema, con las palabras clave del enunciado.',
    'Un respaldo de autor o de informe verificado.',
    'La ley educativa con su nombre completo.',
    'Antesala: qué pide el supuesto y qué se propone (curso, áreas, tipo de propuesta, producto final).',
    '<<Preíndice: en una o dos frases, el recorrido de la resolución (contexto, fundamentación, intervención a nivel de '
    'centro y de aula, conclusión y referencias).>>{#71b}')
p('**Contenido recomendable**: dato o pregunta retórica de apertura; objetivo de etapa del artículo 17 de la LOE '
  'modificada por LOMLOE; título de la situación de aprendizaje; efeméride si vertebra la propuesta.')
sub('Estructura interna (<<cinco movimientos>>{#71c}, un párrafo cada uno)')
num('Gancho de dos líneas con palabras clave.', 'Autor que explica por qué importa en Educación Primaria.', 'Ley.',
    'Antesala, que empieza por «Para dar respuesta al supuesto planteado…».',
    '<<Preíndice, que empieza por «A tal fin…».>>{#71c}')
tabla(['Error', 'Cómo evitarlo'], [
    ['Introducción válida para cualquier supuesto', 'Al menos tres palabras clave literales del enunciado'],
    ['Frase célebre de dudosa atribución o cifra inventada', 'Solo ganchos verificados (Parte II, 1); ante la duda, '
                                                            'pregunta retórica'],
    ['<<Olvidar el preíndice o alargarlo>>{#71d}', '<<Una o dos frases que recorren los apartados, sin '
                                                    'desarrollarlos>>{#71d}'],
    ['Adelantar contexto o medidas', 'La antesala dice qué se propone, no cómo'],
    ['No decir qué se va a hacer', 'Cerrar con curso, áreas, tipo de propuesta y producto'],
], [8.7, 8.7])
plantilla('7.1')

# 7.2 -------------------------------------------------------------------------------------------------------------
h2('7.2. Contexto: entorno, centro y alumnado')
ficha('**Probar que la intervención está contextualizada y que el contexto es funcional: cada dato se usa después**',
      '180 palabras · 8 min · 3 párrafos (entorno 35, centro 65, alumnado 80)', 'C2 (tres elementos, todos necesarios)')
sub('Contenido obligatorio')
bul('Entorno: tipo de localidad andaluza, nivel socioeconómico y cultural, <<uno o dos recursos del entorno que se usarán '
    '(biblioteca municipal, talleres gratuitos, residencia de mayores…)>>{#72a}.',
    'Centro: tipo y líneas; <<una de las líneas generales de actuación pedagógica y uno de los objetivos generales '
    'destinados a la mejora del rendimiento escolar y de la calidad educativa>>{#72b} del proyecto educativo; un plan o '
    'programa; recursos que se usarán.',
    'Alumnado: curso, número, fortaleza y dificultad ligada al tema, <<cohesión e intereses según el sociograma>>{#72c}, '
    'diversidad.',
    'Todo lo que fija el enunciado, respetado al pie de la letra.')
p('**Contenido recomendable**: participación de las familias; hallazgo de la memoria de autoevaluación que origina la '
  'propuesta; fuente del diagnóstico (evaluación inicial, artículo 11 de la Orden de 30 de mayo de 2023); intereses del '
  'grupo; frase puente a 4.2.4.')
sub('Reglas de construcción')
num('Si el enunciado da el contexto, se reproduce sin contradecirlo y se completa solo con lo útil; si no lo da, se '
    'inventa a medida.',
    'Regla del dato tachado: si al tachar un dato la propuesta no cambia, sobra.',
    '<<Líneas generales de actuación pedagógica y objetivos generales destinados a la mejora del rendimiento escolar y de '
    'la calidad educativa: inventables (son propios de cada centro), en infinitivo y realistas. Son los nombres que el '
    'Decreto 483/2026 da al artículo 21.3, letras b) y a), del Reglamento Orgánico; no se usan las siglas antiguas (LGAP, '
    'OMRE). Aquí solo se nombran: la norma se cita en 4.1.>>{#72d}',
    'Si se puede elegir nivel, se elige el que mejor se domina.',
    'Si el enunciado no menciona alumnado con necesidades, un solo perfil sencillo y bien conocido.')
tabla(['Error', 'Cómo evitarlo'], [
    ['Contexto de relleno (historia del barrio, número de docentes)', 'Regla del dato tachado'],
    ['Contradecir el enunciado', 'Releerlo antes de este apartado'],
    ['Describir al alumnado por etiquetas diagnósticas', 'Necesidad + fortaleza + fuente del dato'],
    ['Programas con nombres caducados', 'Solo los de la resolución vigente (Parte II, 2)'],
    ['<<Escribir «objetivo de mejora» o las siglas LGAP y OMRE>>{#72e}', '<<Los nombres completos del Decreto '
                                                                        '483/2026>>{#72e}'],
    ['Explicar qué es el Plan de Centro', 'Se reserva para 4.1'],
], [8.7, 8.7])
plantilla('7.2')

# 7.3 -------------------------------------------------------------------------------------------------------------
h2('7.3. Justificación normativa y epistemológica')
ficha('**Probar que la intervención está razonada y fundamentada: normas y autores que explican decisiones de la '
      'propuesta, no un listado**', '190 palabras · 8 min · 2 párrafos', 'C1 (indicadores 2 y 3), C13')
clave('<<La normativa de este apartado es prácticamente la misma en todos los supuestos y se memoriza. Lo que se adapta '
      'son los autores, que tienen que ser muy específicos del tema del supuesto.>>{#73a}')
sub('Contenido obligatorio')
bul('Dos autores <<muy específicos del tema>>{#73b}, con año y aportación concreta.',
    '<<Marco estatal y andaluz, con nombre completo: artículo 10.2 del Real Decreto 157/2022 (el equipo docente planifica '
    'situaciones de aprendizaje) en correlación con el artículo 7.3 del Decreto 101/2023 (equipos docentes coordinados y '
    'enfoque interdisciplinar, integrador y holístico).>>{#73c}',
    '<<Una instrucción, según el área: lectura, matemáticas o bibliotecas, con lo que establece.>>{#73d}')
p('**Contenido recomendable**: párrafo psicoevolutivo de dos líneas; informe o evaluación externa <<verificados.>>{#73e}')
p('<<**Artículos 5 y 6 del Decreto 101/2023**: no se desarrollan aquí. El artículo 5 (objetivos de etapa, con los propios '
  'de Andalucía en las letras ñ y o) va en la concreción curricular (4.2.1); el artículo 6 (principios pedagógicos), en '
  'la metodología (4.2.2), donde se relaciona con las decisiones metodológicas.>>{#73f}')
sub('Estructura interna')
num('Frase de enlace con el contexto.',
    'Plano epistemológico: autor de didáctica del área o del tema y autor del enfoque metodológico o del desarrollo.',
    'Plano normativo, en el esquema «norma → qué establece → qué fundamenta aquí»: <<artículo 10.2 del Real Decreto '
    '157/2022 y artículo 7.3 del Decreto 101/2023, en dos frases encadenadas; la instrucción del área, en otra>>{#73g}.',
    'Frase de paso a la propuesta.')
tabla(['Error', 'Cómo evitarlo'], [
    ['Lista de normas sin función', 'Cada norma lleva su «que establece… y fundamenta…»'],
    ['Normas derogadas o artículos mal atribuidos', 'Solo banco verificado; ante la duda, la norma sin artículo'],
    ['Autores sin año o sin aportación', 'Fórmula «autor (año) + verbo + idea aplicable»'],
    ['Repetir la cita legal de la introducción', 'En 1, la ley orgánica; aquí, currículo e <<instrucción del '
                                                 'área>>{#73h}'],
    ['<<Explicar aquí los principios pedagógicos>>{#73i}', '<<Se reservan para 4.2.2>>{#73i}'],
    ['Extenderse (el criterio pesa poco)', 'Límite de 190 palabras'],
], [8.7, 8.7])
plantilla('7.3')

# 7.4 -------------------------------------------------------------------------------------------------------------
h2('7.4. Propuesta de intervención: frase de entrada')
p('Una sola frase, al comienzo de 4.1, anuncia los dos planos: «La intervención se articula en dos niveles: el de centro, '
  'de carácter organizativo, y el de aula, que se concreta en una situación de aprendizaje».')

# 7.5 -------------------------------------------------------------------------------------------------------------
h2('7.5. Intervención a nivel de centro (coordinación docente)')
ficha('**Responder a la parte «organizativa»: la propuesta nace de los documentos del centro, varios órganos intervienen '
      'con una función concreta y hay cauces y calendario de coordinación. El tribunal valora que el funcionamiento sea el '
      'real de un colegio andaluz**',
      '<<275 palabras los bloques fijos (300 con un bloque según el supuesto) · 13 min · 5 movimientos>>{#75a}', 'Convocatoria («organizativa»); C8 (cauces de coordinación); C2 secundario')
sub('Contenido obligatorio')
bul('Origen de la propuesta en un documento del centro, coherente con el contexto<<: la línea general de actuación '
    'pedagógica o el objetivo general de mejora ya descritos en 2 solo se citan>>{#75b}.',
    'Al menos tres agentes, cada uno con verbo y acuerdo: <<equipo técnico de coordinación pedagógica, equipo de ciclo y '
    'equipo de orientación o especialista>>{#75c}.',
    'Cauce y calendario de coordinación <<con los especialistas de atención a la diversidad>>{#75d} (qué reunión, cuándo, '
    'para acordar qué).',
    '<<Espacios del centro y del entorno que se usan, y criterios pedagógicos del proyecto educativo aplicados a la '
    'actividad complementaria, al recurso digital y a la cultura andaluza.>>{#75e}',
    'Primera mención completa del Decreto 328/2010<<, modificado por el Decreto 483/2026>>{#75g}.')
p('**Contenido recomendable**: trámite organizativo concreto (reserva de espacio, autorización, partida); agente externo; '
  'retorno a la memoria de autoevaluación; uno o dos artículos del Reglamento Orgánico, no más.')
p('<<**Bloques según el supuesto** (uno o dos, solo si el enunciado lo pide o lo sugiere): familias y entorno, en dos '
  'líneas; protección de datos, si hay grabaciones o difusión de imágenes; especialistas del equipo docente; lo que marca '
  'el proyecto educativo (lectura diaria, modelo común de problemas); servicios complementarios; proyecto '
  'interdisciplinar.>>{#75h} <<Las familias dejan de ser obligatorias.>>{#75f}')
sub('Estructura interna')
num('Frase de entrada del apartado 4 y origen de la propuesta.',
    'Órganos, de mayor a menor <<(equipo técnico → ciclo)>>{#75i}, cada uno con su acuerdo.',
    'Atención a la diversidad: equipo de orientación y especialistas, con calendario.',
    '<<Espacios y criterios pedagógicos: actividad complementaria, recurso digital y cultura andaluza.>>{#75j}',
    '<<Uno o dos bloques según el supuesto y cierre (memoria de autoevaluación).>>{#75j}')
clave('Terminología andaluza: en el colegio, el órgano es el **equipo de orientación**; el **equipo de orientación '
      'educativa** es el servicio de zona al que pertenece el orientador u orientadora de referencia. No existen en un '
      'colegio andaluz el «departamento de orientación», la «comisión de coordinación pedagógica» ni la «programación '
      'general anual».')
clave('<<**Criterios pedagógicos.** El Decreto 483/2026 reúne en el artículo 21.3.c) del Reglamento Orgánico decisiones '
      'que antes estaban dispersas: los criterios pedagógicos del centro, que sirven de base para la evaluación y la '
      'promoción, el tiempo escolar y extraescolar, los agrupamientos y las tutorías, la oferta de áreas, las medidas '
      'organizativas de atención a la diversidad y el tránsito, y los órganos de coordinación docente. En el supuesto se '
      'usan para la actividad complementaria (tiempo escolar y extraescolar), el recurso digital y la cultura andaluza; la '
      'diversidad ya tiene su bloque con los especialistas.>>{#75k}')
tabla(['Error', 'Cómo evitarlo'], [
    ['Lista de órganos sin función', 'Cada órgano, un verbo y un acuerdo: «el equipo de ciclo acuerda…»'],
    ['Terminología de otras comunidades o de institutos', 'Solo el mapa de la Parte II, 4.1'],
    ['Atribuir al equipo técnico decisiones de aula', 'Sentido descendente: centro → ciclo → aula'],
    ['Coordinación sin tiempos', 'Antes de iniciar, semanalmente, al cierre'],
    ['Familias reducidas a «se informará»', 'Un cauce de información y una forma de participación'],
    ['Teoría de la organización escolar', 'Solo lo que sirve a esta propuesta'],
    ['Citar artículos de memoria', 'Dos como máximo y verificados'],
    ['<<Volver a explicar la línea o el objetivo del contexto>>{#75l}', '<<Aquí solo se citan como origen>>{#75l}'],
    ['<<Protección de datos sin que el supuesto lo pida>>{#75l}', '<<Solo si hay grabaciones o difusión de '
                                                                   'imágenes>>{#75l}'],
], [8.7, 8.7])
plantilla('7.5')
p('<<En el modelo estándar se escriben los bloques fijos y, de los bloques según el supuesto, solo uno o dos.>>{#75m}')

# 7.6 -------------------------------------------------------------------------------------------------------------
h2('7.6. Intervención a nivel de aula: datos identificativos (transición)')
ficha('**Presentar la situación de aprendizaje de un vistazo antes de desarrollarla: ubicarla en el tiempo y precisar las '
      'áreas**', '<<215 palabras · 9 min · 1 párrafo de 4 frases>>{#76a}', 'C4 (temporalización); C2 secundario')
p('Si el enunciado no dice curso, se elige aquí y se declara una sola vez; todo el currículo se toma de ese curso.')
p('Los siete datos, en este orden: (1) título; (2) curso y ciclo; (3) área eje y áreas conectadas; (4) trimestre y, si '
  'procede, efeméride; (5) duración en sesiones y semanas; (6) producto final y destinatario; (7) reto de partida con las '
  'palabras del enunciado.')
p('**Cómo redactarlos**: tres frases encadenadas, sin rótulos ni dos puntos. La primera identifica (título, curso, áreas); '
  'la segunda sitúa en el tiempo (trimestre, sesiones, efeméride); la tercera da sentido (reto → producto → '
  'destinatario). <<La cuarta conecta con los intereses del alumnado y con un Objetivo de Desarrollo Sostenible, da '
  'continuidad a la línea o al objetivo del contexto y cita el artículo 3.1 de la Orden de 30 de mayo de 2023, que aquí '
  'se menciona por primera vez con su nombre completo.>>{#76b}')
p('**Recomendable**: <<mención de que forma parte de la programación didáctica del ciclo>>{#76c}. Comprobación '
  'aritmética: las sesiones coinciden con las que suma 4.2.3.')
tabla(['Error', 'Cómo evitarlo'], [
    ['Repetir literalmente la antesala de la introducción', 'Allí se anuncia en una línea; aquí se precisa'],
    ['Formato de ficha («Título:», «Curso:»)', 'Prosa subordinada'],
    ['Sesiones que no cuadran', 'Anotar la suma en el borrador'],
    ['Título ingenioso sin relación con el reto', 'Título que contenga el reto o el producto'],
    ['Duración inverosímil', 'Entre 8 y 15 sesiones; 12 como tipo'],
    ['<<Olvidar el ODS o el artículo 3.1 de la Orden>>{#76d}', '<<Cuarta frase, siempre>>{#76d}'],
], [8.7, 8.7])
plantilla('7.6')
p('Si el enunciado pide un taller o una sesión, la duración se da en minutos y se dice en qué unidad mayor se inserta.')

# 7.7 -------------------------------------------------------------------------------------------------------------
h2('7.7. Concreción curricular')
ficha('**Comprobar el dominio del currículo vigente de Andalucía mediante una selección breve, exacta y asociada al '
      'supuesto**', '<<150 palabras · 7 min>>{#77f} · 1 párrafo en cadena', 'C3 (cinco indicadores de igual valor); C6 secundario')
sub('Contenido obligatorio (uno por indicador de C3)')
bul('Competencia específica del área eje, con su número y su idea central.',
    'Criterio de evaluación del ciclo, con su código.',
    'Saberes básicos: bloque y saber concreto.',
    'Dos descriptores operativos del perfil competencial.',
    'Competencia clave a la que contribuyen.',
    '<<Competencia específica de una segunda área, con su número y su idea central en una línea: nunca una sola '
    'área.>>{#77b}',
    '<<La Orden de 30 de mayo de 2023, ya presentada en los datos identificativos, en forma corta y con su anexo '
    'II.>>{#77a}')
p('**Recomendable**: objetivo de etapa (artículo 5 del Decreto 101/2023); <<glosa de por qué ese elemento responde al '
  'reto>>{#77c}.')
p('**Estructura interna** (cadena de lo general a lo evaluable): objetivo de etapa → competencia específica → criterio de '
  'evaluación → saberes básicos → descriptores operativos y competencia clave → segunda área → frase de enlace con la '
  'secuencia.')
sub('Reglas')
num('Exactitud antes que cantidad: un código erróneo resta más que su ausencia. Criterio con la letra del curso (.a en '
    'cursos impares, .b en pares: 4.2.a en 3.º, 4.2.b en 4.º); saber con su código (CMN.2.A.2.2). Si no se recuerda el '
    'código, número de la competencia específica y paráfrasis del criterio. Banco verificado: Parte II, 4.2.1 (EC1-EC18) '
    'y Parte V (currículo completo de las áreas de la especialidad). En Educación en Valores Cívicos y Éticos (solo 6.º) '
    'los criterios no llevan letra. El descriptor se cita en la redacción del ciclo (Parte V, 0.3).',
    'Los criterios citados aquí son los mismos que se evalúan en 4.2.5.',
    'No se enumeran las ocho competencias clave.',
    'Si el enunciado nombra áreas, elementos de todas; si deja libertad, <<un área eje desarrollada entera y, al menos, '
    'otra con su competencia específica resumida (tabla recortada en el Word de plantillas)>>{#77d}.')
tabla(['Error', 'Cómo evitarlo'], [
    ['Listados interminables', 'Cinco elementos, uno por indicador'],
    ['«Contenidos», «estándares», «objetivos didácticos»', 'Competencias específicas, criterios de evaluación, saberes '
                                                          'básicos, descriptores operativos'],
    ['Elementos de otro ciclo', 'Memorizar los del curso elegido'],
    ['Elementos sin relación con el producto', 'Cada elemento debe verse en una actividad de 4.2.3'],
    ['Tabla descuadrada a mano', 'Prosa encadenada'],
    ['<<Una sola área>>{#77e}', '<<Una desarrollada y otra con su competencia específica>>{#77e}'],
], [8.7, 8.7])
plantilla('7.7')

# 7.8 -------------------------------------------------------------------------------------------------------------
h2('7.8. Metodología')
ficha('**Mostrar el dominio de estrategias docentes: principios y decisiones metodológicas justificados y aplicados a '
      'esta propuesta. El texto debe permitir localizar los seis indicadores de C7**', '280 palabras · 12 min · '
      '<<4 párrafos>>{#78a}', 'C7 (15 %)')
sub('Contenido obligatorio (uno por indicador de C7)')
num('Principios pedagógicos (artículo 6 del Decreto 101/2023), <<siempre estos tres, cada uno con su ejemplo: Diseño '
    'Universal para el Aprendizaje (letra e), patrimonio cultural y natural de Andalucía (letra g) y tecnologías de la '
    'información y la comunicación (letra c)>>{#78b}.',
    'Trabajo individual, cooperativo y entre iguales (artículo 7.2), un ejemplo de cada uno<<, con técnicas cooperativas '
    'concretas>>{#78c}.',
    '<<Enfoque integrador, interdisciplinar y holístico: se acredita en 3 (artículo 7.3); su párrafo de la plantilla '
    'queda pendiente de reubicar.>>{#78d}',
    'Variedad de materiales y recursos.',
    '<<Recursos tecnológicos con finalidad didáctica: con el principio de la letra c) y, al final de las actividades, en '
    '4.2.3.>>{#78e}',
    'Distintas formas de presentación para distintos estilos y ritmos (Diseño Universal para el Aprendizaje).',
    '<<Orientaciones metodológicas para la adquisición de las competencias específicas del área (anexo II de la Orden de '
    '30 de mayo de 2023, introducción de cada área), como último bloque y en tres o cuatro palabras (tabla del Word de '
    'plantillas).>>{#78f}')
p('**Recomendable**: autor de la metodología principal; papel docente y gestión del error; espacios y tiempos; '
  '<<coherencia con la línea de actuación del contexto>>{#78g}; referencia al esquema del anexo IV de la Orden de 30 de '
  'mayo de 2023.')
p('**Estructura interna**: (1) principios ejemplificados<< (DUA, Andalucía y digital)>>{#78h}; (2) metodología principal '
  '(nombre, autor, rasgo esencial, cómo se despliega); (3) agrupamientos y técnicas; <<(4) materiales y formatos; (5) '
  'orientaciones metodológicas del área>>{#78h}.')
p('**Relación con 4.2.3**: aquí se justifica el cómo una sola vez; en la secuencia, técnicas y recursos aparecen entre '
  'paréntesis dentro de las actividades.')
tabla(['Error', 'Cómo evitarlo'], [
    ['Catálogo de metodologías sin aplicar', 'Una principal y, como máximo, dos de apoyo, todas con ejemplo'],
    ['Principios copiados sin ejemplo', 'Fórmula «principio (ejemplo en la propuesta)»'],
    ['Tecnología como fin', 'Decir para qué: buscar, crear, comunicar, evaluar'],
    ['Olvidar el trabajo individual o entre iguales', 'Tres ejemplos, uno por modalidad'],
    ['Definiciones atribuidas a autores sin verificar', 'Solo autores de la Parte II'],
    ['Ignorar la metodología que exige el enunciado', 'En T6 es lo primero que se desarrolla'],
    ['<<Olvidar uno de los tres principios fijos>>{#78i}', '<<DUA, Andalucía y digital, siempre con ejemplo>>{#78i}'],
    ['<<Detallar aquí los recursos digitales>>{#78i}', '<<Van al final de las actividades (4.2.3)>>{#78i}'],
], [8.7, 8.7])
plantilla('7.8')

# 7.9 (sin revisar, salvo la frase que llega de la metodología) ----------------------------------------------------
h2('7.9. Secuencia didáctica')
ficha('**Núcleo de la prueba: secuencia completa, ordenada y coherente, con actividades concretas y aprendizajes que se '
      'integran y se aplican en distintos contextos**', '450 palabras · 20 min · frase de entrada + 5 párrafos',
      'C4, C5, C6 (cerca del 25 %); C7, C8 y C9 secundarios')
sub('Contenido obligatorio')
bul('Producto final anunciado al inicio.',
    'Todas las fases, en orden, con sus sesiones (la suma coincide con los datos identificativos).',
    'Cinco actividades con título, descripción concreta, agrupamiento y recurso.',
    'En cada actividad, el aprendizaje que moviliza (área o criterio).',
    'Difusión del producto y reflexión final.')
p('**Recomendable**: proceso cognitivo dominante de cada fase; contextos variados (aula, centro, entorno, familia, '
  'digital); marca de accesibilidad en una o dos actividades; una actividad con familias y otra con agente externo o '
  'salida; elemento andaluz.')
tabla(['Fase', 'Función', 'Sesiones (de 12)', 'Palabras'], [
    ['Motivación y activación', 'Presentar el reto, despertar interés, recoger conocimientos previos (evaluación inicial '
                                'de la propuesta)', '1-2', '70'],
    ['Exploración', 'Indagar: búsqueda, observación, salida o visita, experto', '3-5', '90'],
    ['Estructuración', 'Organizar y fijar lo aprendido; éxito guiado', '6-8', '90'],
    ['Aplicación', 'Elaborar el producto final', '9-11', '100'],
    ['Conclusión y difusión', 'Presentar, evaluar y transferir', '12', '70'],
    ['Frases de entrada y cierre', '—', '—', '30'],
], [3.6, 9.2, 2.6, 2.0])
p('**Cómo lograr el «detalle concreto»**: cada actividad responde a qué hace el alumnado (verbo observable), con quién '
  '(agrupamiento o técnica), con qué (recurso) y para qué (aprendizaje o parte del producto). La actividad de exploración '
  'en contexto real y la de aplicación se describen con más precisión; las demás, en una o dos frases. Cada fase deja una '
  'evidencia que 4.2.5 recoge.')
tabla(['Error', 'Cómo evitarlo'], [
    ['Actividades genéricas («se trabajará la comprensión»)', 'Verbo observable + producto parcial'],
    ['Sin producto final o con uno que no responde al reto', 'Decidirlo en el borrador, antes que nada'],
    ['Sesiones que no suman', 'Anotar la suma'],
    ['Todo en el aula y con el mismo agrupamiento', 'Variar contexto y agrupamiento'],
    ['300 palabras para la primera actividad', 'Reparto por fase'],
    ['Tabla dibujada a mano', 'Párrafos compactos'],
    ['Actividades sin evidencias para evaluar', 'Una evidencia por fase'],
], [8.7, 8.7])
B.append(('plantilla79', None))
p('Si el enunciado pide una sesión o un taller (F2), las cinco fases se convierten en momentos de la sesión con minutos y '
  'se mide el cambio con la misma pregunta al inicio y al final; si pide una propuesta por ciclo (F3), se repite la misma '
  'estructura con distinto producto y grado de autonomía.')

# Plantilla del 7.9 de la versión 2.1 (sin cambios) y la frase nueva al final
PLANTILLA_79 = [
    'La secuencia conduce a [producto final] y se organiza en cinco fases.',
    'Motivación y activación (sesiones 1 y 2). «[Título]»: [detonante: carta, visita, objeto, noticia] plantea el reto; '
    'mediante [técnica o herramienta] se recogen los conocimientos previos y se forman los equipos.',
    'Exploración (sesiones 3 a 5). «[Título]»: el alumnado [investiga, observa, entrevista] en [contexto real o fuente], en '
    '[agrupamiento], y registra [qué] en [soporte]. [Segunda actividad breve].',
    'Estructuración (sesiones 6 a 8). «[Título]»: los equipos [organizan, clasifican, redactan, calculan] con [recurso], lo '
    'que moviliza [aprendizaje de área 2]; [actividad de éxito guiado].',
    'Aplicación (sesiones 9 a 11). «[Título]»: cada equipo elabora [parte del producto] con [herramienta], aplicando '
    '[técnica cooperativa]; [participación de familias o de agente externo].',
    'Conclusión y difusión (sesión 12). «[Título]»: se presenta el producto a [destinatario], se difunde en [medio] y el '
    'grupo reflexiona con [rutina o instrumento] sobre lo aprendido y su utilidad fuera del aula.',
]

# ---------------------------------------------------------------------------------------------------------------
MARCA = re.compile(r'<<(.*?)>>\{#(\w+)\}|!!(.*?)!!', re.S)
NEG = re.compile(r'\*\*(.*?)\*\*', re.S)
HUECO = re.compile(r'(\[[^\]]*\])')


class Libreta(PB.Constructor):
    def __init__(self, revision):
        super().__init__()
        self.revision = revision
        self.pendientes_com = []      # (lista de elementos w:r, texto)
        s = self.d.sections[0]
        s.left_margin = s.right_margin = Cm(1.8)
        h = s.header.paragraphs[0]
        for r in list(h._p.findall(qn('w:r'))):
            h._p.remove(r)
        h._p.append(parse_xml(f'<w:r {PB.NS}>{PB._rpr(negrita=True, color=AZUL, tam=8)}<w:t xml:space="preserve">'
                              f'Libreta mágica</w:t></w:r>'))
        h._p.append(parse_xml(f'<w:r {PB.NS}>{PB._rpr(color="6A7075", tam=8)}<w:t xml:space="preserve">  ·  Supuestos '
                              f'prácticos · Educación Primaria · Andalucía 2027</w:t></w:r>'))

    # -- runs ------------------------------------------------------------------------------------------------
    def runs(self, texto, tam=TAM, color=TXT, negrita=False, plantilla=False):
        """Devuelve [(xml_run, clave_comentario_o_None)] a partir de un texto con marcas."""
        out = []
        pos = 0
        for m in MARCA.finditer(texto):
            out += self._trozos(texto[pos:m.start()], tam, color, negrita, plantilla, None, None)
            if m.group(1) is not None:
                fondo = GRIS if self.revision else None
                out += self._trozos(m.group(1), tam, color, negrita, plantilla, fondo,
                                    m.group(2) if self.revision else None)
            else:
                out += self._trozos(m.group(3), tam, color, negrita, plantilla, NARANJA, None)
            pos = m.end()
        out += self._trozos(texto[pos:], tam, color, negrita, plantilla, None, None)
        return out

    def _trozos(self, texto, tam, color, negrita, plantilla, fondo, com):
        out = []
        partes = NEG.split(texto)
        for i, parte in enumerate(partes):
            if not parte:
                continue
            neg = negrita or i % 2 == 1
            for trozo in HUECO.split(parte) if plantilla else [parte]:
                if not trozo:
                    continue
                es_hueco = plantilla and trozo.startswith('[') and trozo.endswith(']')
                out.append((PB._run(trozo, tam=tam, negrita=neg or es_hueco, color=TEAL if es_hueco else color,
                                    fondo=fondo), com))
        return out

    def parrafo(self, contenido_runs, contenedor=None, **kw):
        el = PB._parrafo_xml(''.join(x for x, _ in contenido_runs), **kw)
        if contenedor is None:
            self._anade(el)
        else:
            contenedor.append(el)
        # comentarios: agrupar runs consecutivos con la misma clave
        rs = el.findall(qn('w:r'))
        claves = [c for _, c in contenido_runs]
        i = 0
        while i < len(rs):
            if claves[i]:
                j = i
                while j + 1 < len(rs) and claves[j + 1] == claves[i]:
                    j += 1
                self.pendientes_com.append((rs[i], rs[j], el, COMENTARIOS[claves[i]]))
                i = j + 1
            else:
                i += 1
        return el

    # -- bloques -----------------------------------------------------------------------------------------------
    def h1(self, t):
        el = self.parrafo(self.runs(t, tam=15, color=AZUL, negrita=True), antes=360, despues=160)
        for r in el.findall(qn('w:r')):
            r.find(qn('w:rPr')).find(qn('w:rFonts')).attrib.update({qn('w:ascii'): 'Cambria', qn('w:hAnsi'): 'Cambria'})
        ppr = el.find(qn('w:pPr'))
        ppr.insert(0, parse_xml(f'<w:pBdr {PB.NS}><w:bottom w:val="single" w:sz="6" w:space="4" w:color="{NAR}"/>'
                                f'</w:pBdr>'))
        ppr.insert(0, OxmlElement('w:keepNext'))

    def h2(self, t):
        el = self.parrafo(self.runs(t, tam=12, color=TEAL, negrita=True), antes=280, despues=120)
        el.find(qn('w:pPr')).insert(0, OxmlElement('w:keepNext'))

    def p(self, t, **kw):
        return self.parrafo(self.runs(t), despues=kw.get('despues', 120), alin='both')

    def sub(self, t):
        el = self.parrafo(self.runs(t, negrita=True), antes=160, despues=80)
        el.find(qn('w:pPr')).insert(0, OxmlElement('w:keepNext'))

    def lista(self, ts, numerada):
        for i, t in enumerate(ts, 1):
            marca = (PB._run(f'{i}.', negrita=True, color=TEAL, tam=TAM) if numerada else
                     PB._run('•', negrita=True, color=NAR, tam=TAM))
            self.parrafo([(marca, None), (f'<w:r>{PB._rpr(tam=TAM)}<w:tab/></w:r>', None)] + self.runs(t),
                         despues=50, ind='<w:tabs><w:tab w:val="left" w:pos="426"/></w:tabs>'
                                         '<w:ind w:left="426" w:hanging="284"/>', alin='both')

    def tabla_b(self, cab, filas, anchos):
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
                    e.set(qn('w:color'), BORDE); b.append(e)
                tcpr.append(b)
                PB._margenes(celda._tc, 90, 90, 40, 40)
                if r_i == 0:
                    PB._fondo(celda._tc, AZUL)
                    self.parrafo(self.runs(cab[c_i], tam=9, color='FFFFFF', negrita=True), contenedor=celda._tc,
                                 despues=0)
                    continue
                if r_i % 2 == 0:
                    PB._fondo(celda._tc, ALT)
                neg = c_i == 0
                self.parrafo(self.runs(filas[r_i - 1][c_i], tam=9, color=AZUL if neg else TXT, negrita=neg),
                             contenedor=celda._tc, despues=0)
        self._anade(tbl)
        self.p('', despues=60)

    def caja(self, etiqueta, parrafos, fondo, borde, color_et, plantilla=False, bocadillo_tras=None):
        """Recuadro de una celda (plantilla o clave) con borde izquierdo de color."""
        t = self.d.add_table(rows=1, cols=1)
        t.autofit = False
        tbl = t._tbl
        tbl.tblGrid.gridCol_lst[0].w = Cm(17.4)
        celda = t.rows[0].cells[0]
        celda.width = Cm(17.4)
        PB._limpia_celda(celda._tc)
        PB._bordes_celda(celda._tc, izq=borde)
        PB._fondo(celda._tc, fondo)
        PB._margenes(celda._tc, 200, 160, 80, 60)
        self.parrafo([(PB._run(etiqueta, versalitas=True, negrita=True, color=color_et, tam=8), None)],
                     contenedor=celda._tc, despues=40)
        for i, (texto, com, etq) in enumerate(parrafos):
            if etq:
                self.parrafo([(PB._run(etq, versalitas=True, negrita=True, color='7F7F7F' if etq.startswith('⚠')
                                       else AZUL, tam=8), None)], contenedor=celda._tc, antes=80, despues=20)
            rs = self.runs(texto, tam=TAM, plantilla=plantilla)
            if com and self.revision:
                rs = [(self._gris_ordenado(x), None) for x, _ in rs]
            el = self.parrafo(rs, contenedor=celda._tc, despues=80, alin='both')
            if com and self.revision:
                r_ = el.findall(qn('w:r'))
                self.pendientes_com.append((r_[0], r_[-1], el, com))
            if bocadillo_tras is not None and i == bocadillo_tras[0]:
                par = PB._parrafo_xml('', despues=60, ind='<w:ind w:left="3400"/>')
                self.n_id += 1
                par.append(parse_xml(_bocadillo_arriba(self.n_id, bocadillo_tras[1])))
                celda._tc.append(par)
                if self.revision:
                    self.pendientes_com.append((par.findall(qn('w:r'))[0], par.findall(qn('w:r'))[0], par,
                                                COMENTARIOS['72f']))
        self._anade(tbl)
        self.p('', despues=40)

    @staticmethod
    def _gris_ordenado(x):
        """Pone el sombreado gris en su sitio dentro de w:rPr (antes de w:vertAlign)."""
        el = parse_xml(x.replace('<w:r>', f'<w:r {PB.NS}>', 1)) if 'xmlns:w' not in x else parse_xml(x)
        rpr = el.find(qn('w:rPr'))
        for s in rpr.findall(qn('w:shd')):
            rpr.remove(s)
        shd = parse_xml(f'<w:shd {PB.NS} w:val="clear" w:color="auto" w:fill="{GRIS}"/>')
        va = rpr.find(qn('w:vertAlign'))
        if va is not None:
            va.addprevious(shd)
        else:
            rpr.append(shd)
        from lxml import etree
        s = etree.tostring(el, encoding='unicode')
        return re.sub(r' xmlns:\w+="[^"]+"', '', s)

    def plantilla(self, clave):
        datos = T.PLANTILLAS[clave]
        parrafos = []
        for i, f in enumerate(datos['filas']):
            texto = re.sub(r'\[(\d+)\|', '[', f['texto'])
            texto = re.sub(r'\{\d+\|([^}]*)\}', r'\1', texto)
            etq = f.get('etiqueta')
            if etq == T.REUBICAR:
                etq = '⚠ ' + etq
            com = COMENT_PLANTILLA.get((clave, i)) if (f.get('nuevo') or f.get('reubicar')) else None
            parrafos.append((texto, com, etq))
            if f.get('reubicar'):
                parrafos.append(('Nota. ' + T.NOTA_REUBICAR, None, None))
        boc = (0, 'biblioteca municipal · talleres gratuitos · residencia de mayores · centro de interpretación · '
                  'asociaciones vecinales') if clave == '7.2' else None
        self.caja('Plantilla de redacción', parrafos, CREMA, NAR, NAR, plantilla=True, bocadillo_tras=boc)

    def plantilla79(self):
        parrafos = [(t, None, None) for t in PLANTILLA_79]
        f = T.PLANTILLAS['7.9']['filas'][0]
        parrafos.append((re.sub(r'\[(\d+)\|', '[', f['texto']), COMENT_PLANTILLA[('7.9', 0)], None))
        self.caja('Plantilla de redacción', parrafos, CREMA, NAR, NAR, plantilla=True)

    def clave(self, t):
        self.caja('Clave', [(t, None, None)], CLAVE_F, TEAL, TEAL)

    def portadilla(self):
        self.p('**Libreta mágica 2.2 · Parte I, apartados 6 y 7.1 a 7.9** (páginas 11 a 20 de la versión 2.1). Rehecho '
               'en Word desde el PDF de Rafa, con su estética, mientras llega su Word; después se sustituye en él. '
               + ('Lo cambiado va en gris, con un comentario en cada cambio. ' if self.revision else '')
               + 'El 7.9 no se ha revisado: solo recibe la frase de los recursos digitales.')

    def comentarios(self):
        for r1, r2, par, texto in self.pendientes_com:
            P = Paragraph(par, self.d._body)
            self.d.add_comment([Run(r1, P), Run(r2, P)], text=texto, author=AUTOR, initials=INIC)

    def monta(self):
        self.portadilla()
        for b in B:
            tipo = b[0]
            if tipo == 'h1':
                self.h1(b[1])
            elif tipo == 'h2':
                self.h2(b[1])
            elif tipo == 'p':
                self.p(b[1])
            elif tipo == 'sub':
                self.sub(b[1])
            elif tipo == 'bul':
                self.lista(b[1], False)
            elif tipo == 'num':
                self.lista(b[1], True)
            elif tipo == 'tabla':
                self.tabla_b(b[1], b[2], b[3])
            elif tipo == 'plantilla':
                self.plantilla(b[1])
            elif tipo == 'plantilla79':
                self.plantilla79()
            elif tipo == 'clave':
                self.clave(b[1])
        if self.revision:
            self.comentarios()

    def guarda_en(self, ruta):
        PB.ordena_esquema(self.d.element.body)
        zoom = self.d.settings.element.find(qn('w:zoom'))
        if zoom is not None and zoom.get(qn('w:percent')) is None:
            zoom.set(qn('w:percent'), '100')
        self.d.save(ruta)
        return ruta


def _bocadillo_arriba(n_id, texto):
    """Bocadillo pequeño con la cola hacia arriba (hacia el hueco del párrafo anterior)."""
    ancho, alto = 9.6, 0.95
    cx, cy = round(ancho * PB.EMU_CM), round(alto * PB.EMU_CM)
    return (f'<w:r {PB.NS}><mc:AlternateContent><mc:Choice Requires="wps"><w:drawing>'
            f'<wp:inline distT="108000" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/>'
            f'<wp:effectExtent l="0" t="108000" r="0" b="0"/><wp:docPr id="{n_id}" name="Bocadillo {n_id}"/>'
            f'<wp:cNvGraphicFramePr/><a:graphic><a:graphicData '
            f'uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"><wps:wsp><wps:cNvSpPr/>'
            f'<wps:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="wedgeRoundRectCallout"><a:avLst><a:gd name="adj1" fmla="val 20000"/>'
            f'<a:gd name="adj2" fmla="val -95000"/><a:gd name="adj3" fmla="val 16667"/></a:avLst></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="{CLAVE_F}"/></a:solidFill><a:ln w="9525"><a:solidFill>'
            f'<a:srgbClr val="{TEAL}"/></a:solidFill></a:ln></wps:spPr><wps:txbx><w:txbxContent>'
            f'<w:p><w:pPr><w:spacing w:before="0" w:after="0"/><w:jc w:val="center"/></w:pPr>'
            f'{PB._run("Ideas: ", negrita=True, color=TEAL, tam=8.5)}{PB._run(texto, tam=8.5, color=TXT)}</w:p>'
            f'</w:txbxContent></wps:txbx><wps:bodyPr rot="0" vert="horz" wrap="square" lIns="72000" tIns="36000" '
            f'rIns="72000" bIns="36000" anchor="ctr" anchorCtr="0"><a:noAutofit/></wps:bodyPr></wps:wsp>'
            f'</a:graphicData></a:graphic></wp:inline></w:drawing></mc:Choice></mc:AlternateContent></w:r>')


def main():
    for revision, ruta in ((True, SAL_REV), (False, SAL_LIM)):
        lib = Libreta(revision)
        lib.monta()
        print(lib.guarda_en(ruta), len(lib.pendientes_com) if revision else '')


if __name__ == '__main__':
    main()
