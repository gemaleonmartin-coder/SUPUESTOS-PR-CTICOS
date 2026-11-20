# -*- coding: utf-8 -*-
"""Libreta mágica 2.2: los bloques del resto de la libreta (fuera de los apartados 6 a 7.9 de la Parte I) que cambian
por las correcciones de Gem de la fase 38, rehechos desde el PDF de Rafa (versión 2.1) con su estética.

Las mismas marcas que libreta_v22_parte1.py: <<texto>>{#clave} nuevo o cambiado (gris + comentario), !!texto!!
pendiente (naranja), **negrita**. Bloques nuevos: ('nota', texto) indica qué sustituye cada bloque y en qué página;
('check', [..]) lista de verificación con casillas.

Instrumentos de evaluación (Parte II, 4.2.5): se comparan con el manual educativo de Gem (bloque de evaluación) y con
su decisión de la fase 37 (la diana es de infantil y se quita): fuera la diana de autoevaluación y la diana
cooperativa; entran el KPSI, el Q-sort, la escala de autovaloración, la escalera de la metacognición, la base de
orientación y la mini entrevista con cada equipo.
"""
import textos_libreta_v22 as T

B = []


def parte(t): B.append(('h1', t))
def h2(t): B.append(('h2', t))
def h3(t): B.append(('sub', t))
def p(t): B.append(('p', t))
def nota(t): B.append(('nota', t))
def bul(*ts): B.append(('bul', list(ts)))
def num(*ts): B.append(('num', list(ts)))
def check(*ts): B.append(('check', list(ts)))
def tabla(cab, filas, anchos): B.append(('tabla', cab, filas, anchos))
def clave(t): B.append(('clave', t))
def plantilla_txt(parrafos): B.append(('plantilla_txt', parrafos))


COMENTARIOS = {
    'r12a': 'Antes: «Unas 2.500 palabras (22-23 palabras por minuto)». Ahora: unas 2.600 en los mismos 110 minutos. '
            'Decisión de Gem (20/11/2026): se aceptan unas 2.600 palabras sin recortar otros apartados.',
    'r12b': 'Antes: «Las 2.500 palabras…». Ahora: 2.600 (decisión de Gem).',
    'r31a': 'Antes: 130, 230 y 90 palabras. Ahora: 165 (preíndice), 275 (los dos decretos con su nombre completo en el '
            '4.1) y 105 (ODS en los datos). Los minutos no cambian: el ritmo pasa a 23-24 palabras por minuto.',
    'r31b': 'Antes: «Total 2.500». Ahora: 2.595 (decisión de Gem: unas 2.600).',
    'r31c': 'Nuevo: la nota que explica el cambio del reparto.',
    'r33a': 'Antes: 1 = 130, 4.1 = 230/260/320/360/220, datos = 90/80/80/90/90. Ahora: +35, +45 y +15 en todas las '
            'variantes, por las mismas razones; totales de 2.595.',
    'r41a': 'Antes: «Dos autores y la norma específica del tema». Ahora: autores muy específicos e instrucción del área '
            '(la normativa del apartado 3 es fija, Gem).',
    'r42a': 'Antes: «Norma específica y autor». Ahora: la instrucción del área (Gem).',
    'r42b': 'Antes: «objetivo de mejora». Ahora: el nombre del Decreto 483/2026.',
    'r42c': 'Antes: «Principio pedagógico que la respalda» en el apartado 3. Ahora los principios van en 4.2.2 (Gem).',
    'r42d': 'Las familias pasan a bloque según el supuesto en el 4.1 (Gem).',
    'r42e': 'Nuevo: el sociograma del contexto, que después forma los equipos (Gem).',
    'r713a': 'Antes: «cinco o seis entradas». Ahora: seis o siete (instrucción del área y Decreto 483/2026).',
    'r713b': 'Antes: «[Norma específica del tema]». Ahora: la instrucción del área (Gem).',
    'p2nota': 'Bloques de la Parte II que cambian; lo demás de la Parte II sigue igual.',
    'p16a': 'Nuevo: el preíndice, que Gem quiere siempre (antes, la libreta decía que no puntuaba).',
    'p21a': 'Antes: «[recurso]». Ahora con ejemplos (Gem).',
    'p21b': 'Antes: «… como línea general de actuación pedagógica [línea] y … el objetivo de mejora de [objetivo]». Ahora: '
            'los nombres del Decreto 483/2026.',
    'p21c': 'Antes: «Según la evaluación inicial, el grupo destaca por…». Ahora con el sociograma (Gem).',
    'p22a': 'Antes, versiones cortas de las cuatro líneas. Ahora: las cuatro de la programación de Gem, tal cual, que '
            'sirven para cualquier supuesto.',
    'p22b': 'Nuevo: ejemplos de objetivos generales de mejora, uno de lengua y otro de matemáticas (Gem).',
    'p22c': 'Antes: «letras a) (objetivos de mejora) y b) (líneas generales de actuación pedagógica)». Ahora: los nombres '
            'completos del Decreto 483/2026.',
    'p23a': 'Antes: «Comunica (lectura, escritura, oralidad, radio escolar, alfabetización mediática)». Ahora: con la radio '
            'siempre unida a Comunica (Gem).',
    'p23b': 'Fila nueva: la Red de Radios Escolares de Andalucía (Resolución de 29 de junio de 2026, tipo C).',
    'p23c': 'Antes: Proyectos ApS como programa para T6c. Ahora se quita: todavía no está aprobado (Gem).',
    'p31a': 'Antes: «3.1. Decreto 101/2023, artículo 6: principios pedagógicos». Ahora: la normativa fija del apartado 3 '
            '(Gem: 10.2 del Real Decreto con el 7.3 del Decreto 101/2023, o los retos del anexo I). La tabla de los '
            'principios pasa a 4.2.2, a).',
    'p31b': 'Nuevo: los diez retos del siglo XXI del anexo I del Real Decreto 157/2022 (comprobados en su PDF), como '
            'alternativa al 10.2 (Gem: «los puntitos del anexo 1»).',
    'p32a': 'Antes: «3.2. Norma específica según el tema», con la fila «Cualquier propuesta: Decreto 101/2023, artículos 6 '
            'y 7». Ahora: la tercera norma es siempre una instrucción, según el área (Gem); las demás normas por tema se '
            'conservan para otros apartados. Bibliotecas: las de 10 de septiembre de 2025 (las de 2013 están '
            'sustituidas).',
    'p32b': 'Nuevo: dónde se cita cada norma, porque ya no va como tercera norma del apartado 3.',
    'p32c': 'Antes: «Instrucciones de 10 de septiembre de 2025, de la Dirección General de Innovación y Formación del '
            'Profesorado…» [POR COMPROBAR]. Ahora: como las cita el BOJA (sin el órgano, que no se ha podido comprobar) y, '
            'como en la programación de Gem, el programa Bibliotecas Escolares y el Plan de Fomento de la Lectura 2026-2030.',
    'pt1i': 'Antes: «Origen en el proyecto de centro o en una línea de actuación; … familias». Ahora: con el nombre del '
            'Decreto 483/2026, los criterios pedagógicos y las familias solo si el supuesto lo pide.',
    'p43a': 'Antes: «en coherencia con la línea de actuación señalada». Ahora: con el nombre del Decreto 483/2026.',
    'p33a': 'Antes: «6: principios pedagógicos» sin destino. Ahora: van en 4.2.2.',
    'p41a': 'Antes: «a) objetivos de mejora; b) líneas generales de actuación pedagógica; c) criterios pedagógicos, entre '
            'ellos las medidas organizativas de diversidad». Ahora: los nombres completos y los seis criterios '
            'pedagógicos del Decreto 483/2026.',
    'p41b': 'Antes: «[objetivo de mejora o línea]». Ahora: los nombres del Decreto 483/2026, solo citados.',
    'p41c': 'Fila nueva: el bloque fijo de los criterios pedagógicos (actividad complementaria, recurso digital y cultura '
            'andaluza), como pide Gem.',
    'p41d': 'Antes, «Familias» sin más. Ahora: bloque según el supuesto (Gem).',
    'p41e': 'Fila nueva: protección de datos, solo si hay imágenes (Ley Orgánica 3/2018, artículo 7).',
    'p42a': 'Nuevo: la frase del ODS y de la continuidad con el contexto (Gem).',
    'p42b': 'Antes: la Orden, artículo 3, como base de los datos. Ahora se cita en la concreción curricular (Gem: la Orden '
            'se dice después).',
    'p421a': 'Nuevo: la tabla de elementos curriculares de Gem, recortada a una competencia por fila y comprobada con el '
             'BOJA (criterios y saberes vinculados; descriptores de la conexión oficial). Algunos códigos de su tabla '
             'original no casaban con el BOJA y aquí van corregidos.',
    'p422a': 'Antes: «— Orden de 30 de mayo de 2023, anexo II … No hay orientaciones metodológicas por competencia». Ahora: '
             'imprescindible, como último bloque de la metodología (Gem).',
    'p422b': 'Antes: «Principios pedagógicos (tabla del apartado 3.1) · Dos o tres con ejemplo». Ahora: siempre el DUA, '
             'Andalucía y lo digital (Gem); la tabla viene aquí.',
    'p422c': 'Antes: «Interdisciplinariedad (C7)». Ahora: se cita en el apartado 3, con el 10.2 del Real Decreto.',
    'p422d': 'La tabla de los principios pasa aquí desde el antiguo 3.1 (Gem: los principios van en metodología). Con ★, '
             'los tres fijos.',
    'p422e': 'Nuevo: la tabla de las orientaciones metodológicas de cada área (anexo II de la Orden), una idea por frase.',
    'p422f': 'Antes: «… en especial [principio] ([ejemplo en la propuesta])». Ahora: los tres fijos.',
    'p422g': 'Nueva: la frase de las orientaciones del área.',
    'p422h': 'Los recursos digitales se citan al final de las actividades de la secuencia (Gem).',
    'p423a': 'Nuevo: la frase de cierre de las actividades con materiales, formatos y recursos digitales, que estaba en '
             'metodología (Gem).',
    'p424a': 'Antes: «semáforo o diana». Ahora sin la diana (Gem, fase 37: es de infantil).',
    'p425a': 'Antes: «Diana, semáforo, rúbrica de un solo punto, escala, ficha de equipo». Ahora, sin la diana y con los '
             'instrumentos del manual educativo de Gem.',
    'p425b': 'Fuera: «Diana de autoevaluación» (★) y «Diana cooperativa». Por qué: Gem decidió en la fase 37 que la diana es '
             'de infantil.',
    'p425c': 'Nuevo, del manual educativo de Gem (evaluación formativa): KPSI, Q-sort, escala de autovaloración '
             '(«Esta me gusta»), escalera de la metacognición, base de orientación y mini entrevista con cada equipo '
             '(su decisión para las UDP).',
    'p425d': 'Antes: «autoevaluación (diana, semáforo, rutina; imprescindible)». Ahora: KPSI, escala de autovaloración, '
             'escalera de la metacognición o semáforo.',
    'p425e': 'Antes: inicial con lista de control, cuestionario digital o tabla «Qué sé…»; final con la rúbrica. Ahora: el '
             'KPSI o el Q-sort al empezar y el mismo al acabar para comparar, como en las UDP de Gem.',
    'p71a': 'Antes: «Siete datos en tres frases». Ahora: y una cuarta con el ODS.',
    'p73a': 'Antes: «Anunciar el índice → —». Ahora el preíndice es obligatorio (Gem).',
    'p3nota': 'Nuevo: lo que cambia en todas las fichas, para no repetirlo en cada una.',
    'p07a': 'Antes: «3. Norma específica», con una base propia por familia. Ahora: la normativa fija y la instrucción en '
            'todas; las normas de cada familia van a otros apartados.',
    'pt1a': 'Antes: «línea de actuación y programa del subtipo … Decreto 328/2010, artículo 21.3 (solo nombrado)». Ahora: '
            'los nombres del Decreto 483/2026 y el sociograma.',
    'pt1b': 'Antes: «… currículo; principio del artículo 6; norma propia del subtipo». Ahora: normativa fija e instrucción; '
            'el principio va a 4.2.2 y la norma del subtipo, a 4.1 o 4.2.4.',
    'pt1c': 'Antes: sin ODS. Ahora con el ODS (Gem).',
    'pt1d': 'Antes: «Proyectos o indagación; cooperativo; aportación de cada área; tecnología…; elemento andaluz». Ahora: '
            'los tres principios fijos y las orientaciones del área; la tecnología, a 4.2.3.',
    'pt1e': 'Antes: «… diana; coevaluación…». Ahora: sin diana; KPSI y escala de autovaloración.',
    'pt1f': 'Antes: «Cinco normas básicas + la del subtipo». Ahora: con la instrucción del área.',
    'pt1g': 'Antes: «… lista de control de ideas previas · diana · …». Ahora: KPSI o Q-sort y escala de autovaloración.',
    'pt1h': 'Antes: «Solo normativa común → Base normativa propia del subtipo». Ahora lo contrario, como dice Gem: la '
            'normativa es casi la misma y lo que distingue son los autores.',
    'pt2a': 'Antes: «objetivo de mejora». Ahora: el nombre del Decreto 483/2026.',
    'pt2b': 'Antes, solo las instrucciones. Ahora, con la normativa fija delante.',
    'pt3a': 'Antes: «… Diseño Universal para el Aprendizaje (…; Decreto 101/2023, 6.e); norma de diversidad». Ahora: '
            'normativa fija e instrucción; el DUA, en 4.2.2, y la norma de diversidad, en 4.2.4.',
    'pt3b': 'Antes: «semáforo o diana con pictogramas». Ahora: escala de autovaloración con pictogramas.',
    'pt4a': 'Antes: «Escuela: Espacio de Paz o Bienestar Emocional». Ahora: con el nombre de la Resolución («Red Andaluza: '
            '“Escuela Espacio de Paz”») y el sociograma (Gem).',
    'pt4b': 'Antes: «Decreto 101/2023, 6.f) y h); norma de convivencia». Ahora: normativa fija e instrucción; los principios, '
            'en 4.2.2, y la Orden de 2011, en 4.1.',
    'pt5a': 'Antes: «planes y programas». Ahora con los nombres del Decreto 483/2026.',
    'pt5b': 'Antes: «principio del artículo 6 del tema; Reglamento Orgánico». Ahora: normativa fija e instrucción; el '
            'Reglamento, en 4.1.',
    'pt6a': 'Antes: «Decreto 328/2010, 21.3.b) y f)». Ahora con el nombre de la letra b) y del plan de formación.',
    'pt6b': 'Antes: «Decreto 101/2023, 7.2 …». Ahora: normativa fija e instrucción; el 7.2, en 4.2.2.',
    'pt6c': 'Antes: «programa afín (Proyectos ApS, …)». Ahora sin Proyectos ApS: todavía no está aprobado (Gem).',
    'pt6d': 'Antes: «diana cooperativa por roles». Ahora: escala de coevaluación por roles (sin diana, Gem).',
    'p4nota': 'Secciones de la lista de verificación que cambian, enteras para poder repasarlas.',
    'c1a': 'Antes: «línea de actuación». Ahora: los nombres del Decreto 483/2026 y el sociograma.',
    'c1b': 'Antes: «normas (cinco o seis)». Ahora: seis o siete.',
    'c1c': 'Antes: «Sin anuncio del índice». Ahora: con preíndice (Gem).',
    'c1d': 'Nuevo: el sociograma.',
    'c1e': 'Antes: «Línea de actuación (en infinitivo) y objetivo de mejora». Ahora: los nombres del Decreto 483/2026.',
    'c1f': 'Antes: «Real Decreto 157/2022 y Decreto 101/2023 con nombre completo; Principio pedagógico del artículo 6 '
           'vinculado; Norma específica del tema». Ahora: 10.2 y 7.3; sin principios; instrucción.',
    'c1g': 'Antes: «Familias: un cauce…» obligatorio. Ahora: bloques fijos y uno o dos según el supuesto (Gem).',
    'c1h': 'Antes: «Los siete datos en tres frases». Ahora: y la cuarta frase con el ODS.',
    'c1i': 'Nuevo: la segunda área (Gem).',
    'c1j': 'Antes: «Dos o tres principios…; Qué aporta cada área; Materiales variados y tecnología…; Distintas formas…; '
           'Conexión con Andalucía». Ahora: los tres principios fijos, las técnicas y las orientaciones del área; '
           'materiales, formatos y digital, a 4.2.3.',
    'c1k': 'Nuevo: la frase de cierre de las actividades (Gem).',
    'c1l': 'Nuevo: el KPSI o el Q-sort al empezar y al acabar.',
}

# ===============================================================================================================
parte('Parte I. Método (resto de apartados que cambian)')
nota('Bloques que sustituyen a los de las páginas 7 a 10 y 23 de la versión 2.1. Los apartados 6 a 7.9 van más abajo, '
     'enteros.')
h2('1.2. Tiempo (135 minutos para el supuesto)')
tabla(['Fase', 'Minutos', 'Qué se hace'], [
    ['Lectura y elección', '5', 'Leer los tres supuestos, elegir y subrayar palabras clave y preguntas del enunciado'],
    ['Borrador', '9', 'Producto final y cinco actividades; competencia específica, criterio y saberes; datos del contexto '
                      'que se van a usar; autores y normas (se anotan para 6)'],
    ['Identificación e índice', '3', '«SUPUESTO N.º [X]» e índice fijo'],
    ['Redacción', '110', '<<Unas 2.600 palabras (23-24 palabras por minuto)>>{#r12a}'],
    ['Revisión', '8', 'Ortografía y tildes, paginación, palabras clave, coherencia'],
], [3.6, 1.8, 12.0])
p('<<Las 2.600 palabras>>{#r12b} son un techo realista, no un mínimo. Sin plantillas memorizadas y sin borrador, no se '
  'llega.')
h2('3.1. Reparto estándar')
tabla(['Apartado', 'Palabras', '%', 'Minutos', 'Criterios'], [
    ['1. Introducción', '<<165>>{#r31a}', '<<6,4>>{#r31a}', '6', 'C1'],
    ['2. Contexto', '180', '<<6,9>>{#r31a}', '8', 'C2'],
    ['3. Justificación normativa y epistemológica', '190', '<<7,3>>{#r31a}', '8', 'C1, C13'],
    ['4.1. Intervención a nivel de centro', '<<275>>{#r31a}', '<<10,6>>{#r31a}', '10',
     'C8 (coordinación), anexo IV («organizativa»)'],
    ['4.2. Datos identificativos (transición)', '<<105>>{#r31a}', '<<4,0>>{#r31a}', '4', 'C4'],
    ['4.2.1. Concreción curricular', '220', '<<8,5>>{#r31a}', '10', 'C3'],
    ['4.2.2. Metodología', '280', '<<10,8>>{#r31a}', '12', 'C7'],
    ['4.2.3. Secuencia didáctica', '450', '<<17,3>>{#r31a}', '20', 'C4, C5, C6'],
    ['4.2.4. Atención a la diversidad', '290', '<<11,2>>{#r31a}', '13', 'C8'],
    ['4.2.5. Evaluación', '240', '<<9,2>>{#r31a}', '10', 'C9'],
    ['5. Conclusión', '90', '<<3,5>>{#r31a}', '4', 'C12'],
    ['6. Referencias', '110', '<<4,2>>{#r31a}', '5', 'C13'],
    ['Total', '<<2.595>>{#r31b}', '100', '110', ''],
], [6.6, 2.0, 1.6, 1.8, 5.4])
p('Bloques: apartados 1 a 3, <<535 palabras (20,6 %); apartado 4, 1.860 (71,7 %); apartados 5 y 6, 200 (7,7 %)>>{#r31a}.')
p('<<**Por qué unas 2.600.** El preíndice (35 palabras), los nombres completos de los Decretos 328/2010 y 483/2026 en el '
  '4.1 (45) y la frase del ODS en los datos (15) suben el total. Decisión de Gem: se aceptan sin recortar otros '
  'apartados y en los mismos 110 minutos de redacción.>>{#r31c}')
h2('3.3. Variantes según el tipo de supuesto (filas que cambian)')
tabla(['Apartado', 'Estándar', 'V1 Diversidad (T3)', 'V2 Convivencia (T4)', 'V3 Centro (T5)', 'V4 Metodología (T6)'], [
    ['1', '<<165>>{#r33a}', '<<165>>{#r33a}', '<<165>>{#r33a}', '<<165>>{#r33a}', '<<165>>{#r33a}'],
    ['4.1', '<<275>>{#r33a}', '<<305>>{#r33a}', '<<365>>{#r33a}', '<<405>>{#r33a}', '<<265>>{#r33a}'],
    ['4.2 (datos)', '<<105>>{#r33a}', '<<95>>{#r33a}', '<<95>>{#r33a}', '<<105>>{#r33a}', '<<105>>{#r33a}'],
    ['Total', '<<2.595>>{#r33a}', '<<2.595>>{#r33a}', '<<2.595>>{#r33a}', '<<2.595>>{#r33a}', '<<2.595>>{#r33a}'],
], [2.6, 2.4, 3.0, 3.2, 2.8, 3.4])
h2('4.1. Orden de planificación en el borrador (inverso al de redacción)')
num('Qué pide el enunciado, palabra por palabra (subrayar verbos y objetos).', 'Problemática o reto.',
    'Producto final que la resuelve, con destinatario.', 'Cinco actividades que conducen al producto (una por fase).',
    'Competencia específica, criterio de evaluación y saberes que esas actividades movilizan.',
    'Contexto a medida: entorno, centro y alumnado que hacen verosímil y necesaria la propuesta.',
    '<<Dos autores muy específicos del tema y la instrucción del área (la normativa del apartado 3 es fija).>>{#r41a}')
p('El contexto se redacta el segundo, pero se diseña el sexto.')
h2('4.2. Cadena de dependencias')
tabla(['Dato que se fija en 2 (o en el enunciado)', 'Condiciona en 3', 'Condiciona en 4.1', 'Condiciona en 4.2'], [
    ['Problemática del grupo (por ejemplo, baja comprensión lectora en la evaluación inicial)',
     '<<Instrucción del área>>{#r42a} y autor de didáctica del área',
     'Origen: memoria de autoevaluación, <<objetivo general destinado a la mejora del rendimiento escolar y de la '
     'calidad educativa del centro>>{#r42b}, acuerdo de ciclo',
     'Competencia y criterio (4.2.1); producto (4.2.3); evidencia e instrumento con comparación inicial-final (4.2.5)'],
    ['<<Línea general de actuación pedagógica y de concreción curricular>>{#r42b}', '<<—>>{#r42c}', 'Documento del que parte la propuesta',
     'Metodología principal <<y principio pedagógico que la respalda>>{#r42c} (4.2.2)'],
    ['Plan o programa del centro', '—', 'Persona coordinadora y recurso que aporta',
     'Recurso o espacio de una actividad (4.2.3)'],
    ['Recurso del entorno', '—', 'Trámite de la salida; agente externo', 'Actividad de exploración en contexto real'],
    ['Familias (nivel de participación)', '—', 'Cauces de información y colaboración <<(bloque según el '
                                                 'supuesto)>>{#r42d}', 'Actividad con familias; difusión del producto'],
    ['Curso y momento evolutivo', 'Párrafo psicoevolutivo', '—', 'Tipo de actividades y nivel curricular'],
    ['Fortalezas e intereses del grupo <<(sociograma)>>{#r42e}', '—', '—',
     'Centro de interés; actividad de motivación<<; equipos heterogéneos (4.2.2)>>{#r42e}'],
    ['Alumnado con necesidades específicas', 'Principio de inclusión',
     'Equipo de orientación y especialistas: cauce, calendario, acuerdos',
     'Ajustes en actividades (4.2.3); medidas (4.2.4); evaluación de las medidas (4.2.5)'],
], [4.6, 3.6, 4.4, 4.8])

h2('4.3. Recursos de redacción que hacen visible la coherencia (viñeta que cambia)')
nota('Sustituye a la segunda viñeta del 4.3 de la página 11.')
bul('**Remisiones internas breves**: «como se indicó en el contexto», <<«en coherencia con las líneas generales de '
    'actuación pedagógica y la concreción curricular señaladas»>>{#p43a}, «criterio ya citado en la concreción '
    'curricular».')

# 7.13 -----------------------------------------------------------------------------------------------------------
B.append(('apartados_6_a_79', None))       # aquí entran, enteros, los apartados 6 a 7.9 ya rehechos
h2('7.13. Referencias')
B.append(('ficha', 'Acreditar que lo citado es real, actual y está bien referenciado. La lista solo confirma lo que ya se '
                   'ha citado en el cuerpo', '110 palabras · 5 min · 2 bloques',
          'C13 (la rúbrica oficial de la unidad didáctica fija como umbral más de tres citas)'))
p('**Contenido obligatorio**: todas las normas citadas en el cuerpo, y solo esas; todos los autores citados, y solo esos, '
  'con año coincidente; dos bloques (normativas y bibliográficas).')
p('**Recomendable**: normas de mayor a menor rango y por fecha; formato autor-año homogéneo; una referencia digital '
  'institucional si se ha usado.')
p('**Estructura interna**: bloque normativo (<<seis o siete entradas>>{#r713a} abreviadas con boletín) y bloque '
  'bibliográfico (tres o cuatro entradas: apellidos, inicial, año, título y editorial o revista).')
tabla(['Error', 'Cómo evitarlo'], [
    ['Referencias no citadas en el texto, o citas sin referencia', 'Anotar en el borrador cada autor y norma al citarlos'],
    ['Años que no coinciden', 'Copiar de la misma anotación'],
    ['Autores, títulos o editoriales inventados', 'Repertorio corto y verificado'],
    ['Normas derogadas o con fecha errónea', 'Las de 2026 figuran si se cita el Reglamento Orgánico o las medidas '
                                             'modificadas'],
    ['Robar tiempo a la revisión', 'Cinco minutos con la lista ya preparada'],
], [8.7, 8.7])
plantilla_txt([
    ('**Referencias normativas**', None),
    ('– Ley Orgánica 2/2006, de 3 de mayo, de Educación (BOE núm. 106), modificada por la Ley Orgánica 3/2020, de 29 de '
     'diciembre (BOE núm. 340).', None),
    ('– Real Decreto 157/2022, de 1 de marzo (BOE núm. 52).', None),
    ('– Decreto 328/2010, de 13 de julio (BOJA núm. 139), modificado por el Decreto 483/2026, de 31 de agosto (BOJA '
     'núm. 168).', None),
    ('– Decreto 101/2023, de 9 de mayo (BOJA núm. 90).', None),
    ('– Orden de 30 de mayo de 2023 (BOJA núm. 104), modificada por la Orden de 31 de agosto de 2026 (BOJA núm. 168).',
     None),
    ('<<– Instrucciones de [fecha], de la [órgano], sobre [lectura, razonamiento matemático o bibliotecas].>>{#r713b}',
     None),
    ('**Referencias bibliográficas**', None),
    ('– [Apellido, N. (año). Título. Editorial.] × 3 o 4.', None),
])

# ===============================================================================================================
parte('Parte II. Banco de recursos por apartado (bloques que cambian)')
nota('<<Solo los bloques que cambian, con la página de la versión 2.1 a la que sustituyen; lo demás de la Parte II sigue '
     'igual.>>{#p2nota}')
h2('1.6. Antesalas (cierre de la introducción) ★')
nota('Sustituye al 1.6 de la página 26.')
bul('«Para dar respuesta al supuesto planteado, que solicita [demanda], se presenta una intervención educativa dirigida '
    'a [curso] que se concreta en la situación de aprendizaje «[título]», cuyo producto final es [producto].»',
    '«El presente supuesto parte de [problemática]. En respuesta, se plantea una intervención en dos niveles, de centro y '
    'de aula, centrada en [área eje] y conectada con [áreas].»',
    '<<★ Preíndice, siempre detrás de la antesala: «A tal fin, tras contextualizar la propuesta en su entorno, centro y '
    'alumnado y fundamentarla en la normativa vigente y en autores actuales, se desarrolla la intervención a nivel de '
    'centro, mediante la coordinación docente, y a nivel de aula, mediante la situación de aprendizaje, para cerrar con la '
    'conclusión y las referencias.»>>{#p16a}')
h2('2.1. Frases base ★')
nota('Sustituye a la tabla 2.1 de la página 26.')
tabla(['Pieza', 'Frase'], [
    ['Entorno', '«El centro se ubica en [localidad] de [provincia], con un nivel socioeconómico y cultural [nivel] y '
                '[grado] de participación de las familias, y dispone de <<[recursos del entorno: biblioteca municipal, '
                'talleres gratuitos, residencia de mayores]>>{#p21a}, que se aprovecharán en la propuesta.»'],
    ['Centro', '<<«Su proyecto educativo recoge, entre sus líneas generales de actuación pedagógica y la concreción '
               'curricular, [línea en infinitivo] y, entre sus objetivos generales destinados a la mejora del rendimiento '
               'escolar y de la calidad educativa del centro, [objetivo], fijado a raíz de la última memoria de autoevaluación.»>>{#p21b}'],
    ['Alumnado', '<<«Según la evaluación inicial y el sociograma, [cohesión del grupo], destaca por [fortaleza] y presenta '
                 'dificultades en [aspecto], que justifican la presente propuesta.»>>{#p21c}'],
    ['Puente', '«Su respuesta educativa se concreta en el apartado 4.2.4.»'],
    ['◆ Grupo en tres perfiles', '«Según la evaluación inicial, el grupo presenta tres perfiles de desempeño en '
                                 '[competencia]: [n.º] estudiantes con un dominio [nivel], [n.º] en proceso y [n.º] que '
                                 'requieren apoyo, entre ellos [perfil].»'],
    ['Entorno como corpus (T2d, T2a)', '«El entorno del centro ofrece un corpus de textos sociales (carteles, avisos, '
                                       'menús, normas, publicidad) que se convierte en material de la propuesta.»'],
    ['Proyecto educativo (cita literal, Decreto 328/2010, artículo 21.1)', '«El proyecto educativo constituye las señas de '
                                                                          'identidad del centro docente y expresa la '
                                                                          'educación que desea y va a desarrollar en unas '
                                                                          'condiciones concretas.»'],
    ['Escuela rural (T5a)', '«La Defensoría de la Infancia y la Adolescencia de Andalucía dedicó un informe especial a la '
                            'atención educativa en los colegios públicos rurales (2022), que subraya sus retos y '
                            'oportunidades.» (sin cifras del informe)'],
], [4.6, 12.8])
h2('<<2.2. Líneas generales de actuación pedagógica y la concreción curricular y objetivos generales destinados a la '
   'mejora del rendimiento escolar y de la calidad educativa del centro (en infinitivo, inventables)>>{#p22c}')
nota('Sustituye al 2.2 de las páginas 26 y 27.')
h3('<<Líneas generales de actuación pedagógica y la concreción curricular>>{#p22c}')
bul('<<Situar al alumnado como protagonista de su aprendizaje mediante metodologías activas que potencien la '
    'colaboración.>>{#p22a}',
    '<<Flexibilizar la respuesta educativa para adaptarla a la diversidad de aptitudes, intereses y necesidades del '
    'alumnado.>>{#p22a}',
    '<<Fomentar la competencia digital del alumnado mediante el uso crítico y responsable de las herramientas y recursos '
    'tecnológicos del aula.>>{#p22a}',
    '<<Impulsar el pensamiento crítico a través de la búsqueda y el análisis de fuentes para resolver problemáticas y '
    'comunicar hallazgos.>>{#p22a}',
    'Desarrollar el hábito lector diario.', 'Promover la resolución de problemas con material visual y manipulativo.',
    'Acercar al alumnado a la cultura andaluza.', 'Conseguir el compromiso del alumnado con el cuidado del medio ambiente.')
h3('<<Objetivos generales destinados a la mejora del rendimiento escolar y de la calidad educativa del centro>>{#p22b}')
bul('<<Lengua. Mejorar la comprensión lectora inferencial mediante el tiempo diario de lectura planificada y comprobar su '
    'progreso con una prueba común trimestral.>>{#p22b}',
    '<<Matemáticas. Mejorar la resolución de problemas mediante un modelo común de pasos en todos los ciclos y comprobar su '
    'progreso con una prueba común trimestral.>>{#p22b}')
p('Base: Decreto 328/2010, artículo 21.3, letras <<a) (objetivos generales destinados a la mejora del rendimiento escolar '
  'y de la calidad educativa del centro) y b) (líneas generales de actuación pedagógica y la concreción curricular)>>{#p22c}, en la '
  'redacción de 2026. No se usan las siglas antiguas (LGAP, OMRE).')
h2('2.3. Programas educativos del curso 2026/2027 (filas que cambian)')
nota('Sustituyen a las filas correspondientes de la tabla 2.3 de la página 27; las demás filas siguen igual.')
tabla(['Utilidad', 'Programa', 'Procedimiento', 'Para qué tipo'], [
    ['◆', '<<Comunica (lectura, escritura, oralidad y alfabetización mediática); si hay radio, siempre con la Red de '
          'Radios Escolares de Andalucía>>{#p23a}', 'Solicitud del centro', 'T2a, T2c, T2d, T1d'],
    ['<<◆>>{#p23b}', '<<Red de Radios Escolares de Andalucía, siempre junto con Comunica>>{#p23b}',
     '<<Convocatoria específica>>{#p23b}', '<<T2c, T1d>>{#p23b}'],
], [1.8, 8.6, 3.6, 3.4])
nota('<<Se elimina la fila «◆ Proyectos ApS · Convocatoria específica · T6c»: todavía no está aprobado.>>{#p23c}')

h2('3.1. Normativa fija del apartado 3 ★')
nota('<<Sustituye al 3.1 de la página 29 (la tabla de los principios pedagógicos pasa a 4.2.2, a).>>{#p31a}')
clave('<<La normativa del apartado 3 es prácticamente la misma en todos los supuestos y se memoriza; lo que se adapta son '
      'los autores, que tienen que ser muy específicos del tema. Los principios pedagógicos no se explican aquí: van en '
      'la metodología.>>{#p31a}')
tabla(['Norma', 'Qué establece', 'Qué fundamenta'], [
    ['<<Real Decreto 157/2022, artículo 10.2>>{#p31a}', '<<Para adquirir las competencias clave y las específicas, el '
                                                       'equipo docente planifica situaciones de aprendizaje; el anexo III '
                                                       'da orientaciones para su diseño>>{#p31a}',
     '<<Que la propuesta sea una situación de aprendizaje planificada por el equipo docente>>{#p31a}'],
    ['<<Decreto 101/2023, artículo 7.3>>{#p31a}', '<<Funcionamiento coordinado de los equipos docentes al plantear las '
                                                  'situaciones de aprendizaje, con un enfoque interdisciplinar, integrador '
                                                  'y holístico>>{#p31a}',
     '<<La conexión entre áreas y el acuerdo del equipo docente>>{#p31a}'],
    ['<<En lugar del 10.2: Real Decreto 157/2022, anexo I (retos del siglo XXI)>>{#p31b}',
     '<<El alumnado debe saber activar lo aprendido ante los desafíos del siglo XXI>>{#p31b}',
     '<<El reto del supuesto (se elige el que encaja)>>{#p31b}'],
], [4.8, 7.4, 5.2])
h3('<<Los diez retos del siglo XXI (Real Decreto 157/2022, anexo I)>>{#p31b}')
num(*['<<' + r + '>>{#p31b}' for r in T.BOCADILLOS['7.3'][3][2]])

h2('3.2. Instrucción según el área y otras normas por tema')
nota('<<Sustituye al 3.2 de las páginas 29 a 31.>>{#p32a}')
h3('<<a) La instrucción del área: la tercera norma del apartado 3, siempre una>>{#p32a}')
tabla(['Área o tema', 'Instrucción', 'Qué establece (para la frase «que establece… y fundamenta…»)'], [
    ['★ Lectura (Lengua o cualquier área)', 'Instrucciones de 21 de junio de 2023, de la Viceconsejería de Desarrollo '
                                            'Educativo y Formación Profesional, sobre el tratamiento de la lectura para el '
                                            'despliegue de la competencia en comunicación lingüística en Educación '
                                            'Primaria y Educación Secundaria Obligatoria',
     'Tiempo diario no inferior a 30 minutos; lectura integrada en la función docente, no aislada; antes, durante y '
     'después; comprensión literal, inferencial y crítica; cinco ejes en Primaria (conciencia fonológica, conocimiento '
     'alfabético, fluidez, vocabulario, comprensión)'],
    ['★ Resolución de problemas (Matemáticas)', 'Instrucciones de 18 de junio de 2024, de la Viceconsejería de Desarrollo '
                                                'Educativo y Formación Profesional, sobre las medidas para el fomento del '
                                                'razonamiento matemático a través del planteamiento y la resolución de '
                                                'retos y problemas en Educación Infantil, Educación Primaria y Educación '
                                                'Secundaria Obligatoria',
     'Itinerario de problemas por etapa; método común de resolución acordado en el centro (de lo corporal a lo oral y a lo '
     'simbólico); tiempo para leer y comprender enunciados; coordinación del equipo técnico'],
    ['◆ Biblioteca', '<<Instrucciones de 10 de septiembre de 2025, sobre la organización y funcionamiento de las '
                     'bibliotecas escolares (así las cita el BOJA n.º 57, de 24 de marzo de 2026)>>{#p32c}',
     'Biblioteca como recurso estratégico para la mediación lectora, la alfabetización mediática e informacional, la '
     'inclusión y la dinamización cultural. <<Como en la programación: el programa Bibliotecas Escolares, de oficio '
     '(Resolución de 29 de junio de 2026), y el Plan de Fomento de la Lectura 2026-2030 (Ministerio de Cultura, 2026), '
     'leer mejor y no solo más, contando con las familias>>{#p32c}'],
], [3.6, 7.0, 6.8])
h3('<<b) Otras normas por tema: no sustituyen a la instrucción; se citan en el apartado que se indica>>{#p32b}')
tabla(['Tema', 'Norma', 'Qué establece', 'Dónde se cita'], [
    ['★ Diversidad', 'Orden de 30 de mayo de 2023, artículos 26 a 37 (modificada por la Orden de 31 de agosto de 2026); '
                     'LOE modificada por LOMLOE, artículo 4.3', 'Medidas generales, programas y medidas específicas; '
                                                              'inclusión conforme al Diseño Universal para el Aprendizaje',
     '<<4.2.4>>{#p32b}'],
    ['◆ Diversidad (detección)', 'Instrucciones de 8 de marzo de 2017, de la Dirección General de Participación y Equidad, '
                                 'por las que se actualiza el protocolo de detección, identificación del alumnado con '
                                 'necesidades específicas de apoyo educativo y organización de la respuesta educativa',
     'Detección en la evaluación inicial y en las sesiones de evaluación; evaluación psicopedagógica', '<<4.1 o 4.2.4>>{#p32b}'],
    ['★ Convivencia', 'Orden de 20 de junio de 2011, por la que se adoptan medidas para la promoción de la convivencia en '
                      'los centros docentes sostenidos con fondos públicos y se regula el derecho de las familias a '
                      'participar en el proceso educativo de sus hijos e hijas',
     'Plan de convivencia; actuaciones preventivas; mediación; delegados de familias; protocolos; compromisos',
     '<<4.1>>{#p32b}'],
    ['◆ Convivencia (violencia)', 'Ley Orgánica 8/2021, de 4 de junio, de protección integral a la infancia y la '
                                  'adolescencia frente a la violencia, artículos 34 y 35',
     'Protocolos contra el acoso y el ciberacoso; coordinador o coordinadora de bienestar y protección', '<<4.1>>{#p32b}'],
    ['◆ Coeducación', 'Ley 12/2007, de 26 de noviembre, para la promoción de la igualdad de género en Andalucía, artículos '
                      '14 y 15', 'La igualdad inspira el sistema educativo; Plan de Igualdad en el Plan de Centro y persona '
                                 'responsable de coeducación', '<<4.1>>{#p32b}'],
    ['★ Organización y tutoría', 'Decreto 328/2010 (modificado por el Decreto 483/2026)', 'Proyecto educativo, órganos de '
                                                                                          'coordinación, tutoría',
     '<<4.1>>{#p32b}'],
    ['★ Evaluación', 'Orden de 30 de mayo de 2023, artículos 9 a 11', 'Carácter, procedimientos, instrumentos, evaluación '
                                                                      'inicial', '<<4.2.5>>{#p32b}'],
    ['◆ Patrimonio andaluz', 'Ley 17/2007, artículo 40', 'Medio natural, historia, cultura y hechos diferenciadores de '
                                                         'Andalucía, como el flamenco', '<<4.2.2 (con el principio g)>>{#p32b}'],
    ['◆ Tecnología y datos', 'Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los '
                             'derechos digitales, artículo 7', 'Por debajo de catorce años, consentimiento de quien ejerza '
                                                               'la patria potestad (grabaciones, publicación del producto)',
     '<<4.1 (bloque de protección de datos)>>{#p32b}'],
    ['◆ Proyectos', 'LOE modificada por LOMLOE, artículo 19.4', 'Tiempo lectivo para proyectos significativos y resolución '
                                                               'colaborativa de problemas', '<<4.2.2>>{#p32b}'],
    ['Alumnado no hispanohablante', 'Real Decreto 157/2022, artículo 19; Orden de 15 de enero de 2007 (Aulas Temporales de '
                                    'Adaptación Lingüística)', 'Atención específica simultánea a la escolarización en '
                                                               'grupos ordinarios', '<<4.2.4>>{#p32b}'],
    ['◆ Coeducación (T1a)', 'LOE modificada por LOMLOE, artículo 1.l)', 'Igualdad efectiva mediante la coeducación, '
                                                                       'educación afectivo-sexual y prevención de la '
                                                                       'violencia de género (con la Ley 12/2007)',
     '<<1 o 4.1>>{#p32b}'],
    ['◆ Inclusión y diseño universal (T3a, T3b)', 'Preámbulo de la Ley Orgánica 3/2020', 'Educación inclusiva como derecho '
                                                                                        'humano y aplicación de los '
                                                                                        'principios del Diseño universal '
                                                                                        'de aprendizaje: «múltiples medios '
                                                                                        'de representación, de acción y '
                                                                                        'expresión y de formas de '
                                                                                        'implicación»', '<<4.2.4>>{#p32b}'],
    ['Desventaja (T3d, T3e)', 'LOE modificada por LOMLOE, artículo 71.1', 'Medios para el máximo desarrollo de todo el '
                                                                        'alumnado; planes de centros prioritarios',
     '<<2 o 4.2.4>>{#p32b}'],
    ['Escuela rural (T5a)', 'LOE modificada por LOMLOE, artículo 82', 'Igualdad de oportunidades en el ámbito rural',
     '<<2 o 4.1>>{#p32b}'],
    ['◆ Orientación y tutoría (T4d, T4a, T4b)', 'LOE modificada por LOMLOE, artículos 18.6 y 2.2', 'La orientación y la '
                                                                                                  'acción tutorial '
                                                                                                  'acompañan el proceso '
                                                                                                  'individual y colectivo',
     '<<4.1>>{#p32b}'],
    ['Familias (T4c)', 'LOE modificada por LOMLOE, artículos 1.h bis) y 121.5', 'Padres, madres y tutores como primeros '
                                                                               'responsables de la educación; compromisos '
                                                                               'educativos', '<<4.1 (bloque de '
                                                                                            'familias)>>{#p32b}'],
    ['Espacios y tiempos flexibles (T6e, T1g, T5a)', 'LOE modificada por LOMLOE, artículo 19.5', 'Flexibilización de áreas, '
                                                                                                'espacios y tiempos y '
                                                                                                'alternativas '
                                                                                                'metodológicas',
     '<<4.1 o 4.2.2>>{#p32b}'],
    ['◆ Competencia digital y medios (T1d, T6b)', 'Real Decreto 157/2022, anexo I', 'Definición: «uso seguro, saludable, '
                                                                                   'sostenible, crítico y responsable de '
                                                                                   'las tecnologías digitales»',
     '<<4.2.2 (con el principio c)>>{#p32b}'],
    ['Marco europeo (todos)', 'Recomendación del Consejo de la Unión Europea, de 22 de mayo de 2018, relativa a las '
                              'competencias clave para el aprendizaje permanente', 'Referente del Perfil de salida y de las '
                                                                                  'ocho competencias clave',
     '<<1>>{#p32b}'],
    ['Lengua y comunicación (T2)', 'Orden de 30 de mayo de 2023, anexo II, introducción de Lengua Castellana y Literatura',
     'Papel de cada competencia: 1 diversidad lingüística; 2 a 5 código oral y escrito; 6 alfabetización mediática; 7 y 8 '
     'lectura literaria; 9 reflexión sobre la lengua; 10 comunicación ética', '<<4.2.2 (orientaciones del área)>>{#p32b}'],
], [3.4, 5.8, 5.6, 2.6])
h2('3.3. Otras normas útiles en la justificación (fila que cambia)')
nota('Sustituye a la primera fila de la tabla 3.3 de la página 31.')
tabla(['Norma', 'Artículo y contenido', 'Tipos'], [
    ['Real Decreto 157/2022', '5.4: medidas regidas por los principios del Diseño Universal para el Aprendizaje · 6: '
                              'principios pedagógicos <<(se citan en 4.2.2, no aquí)>>{#p33a} · anexo III: orientaciones '
                              'para las situaciones de aprendizaje', 'Todos'],
], [3.4, 12.0, 2.0])

h2('4.1. Intervención a nivel de centro (filas que cambian)')
nota('b) Documentos del centro, página 37: fila «Proyecto educativo». e) Frases de 4.1, páginas 38 y 39: la tabla entera.')
tabla(['Documento', 'Base', 'Uso'], [
    ['Proyecto educativo ★', '<<Decreto 328/2010, artículos 20 y 21.3 (redacción del Decreto 483/2026): a) objetivos '
                             'generales destinados a la mejora del rendimiento escolar y de la calidad educativa del centro; '
                             'b) líneas generales de actuación pedagógica y la concreción curricular; c) criterios pedagógicos que sirven '
                             'de base para la evaluación y la promoción, el tiempo escolar y extraescolar, los agrupamientos '
                             'y las tutorías, la oferta de áreas, las medidas organizativas de atención a la diversidad y el '
                             'tránsito, y los órganos de coordinación docente; d) plan de orientación y acción tutorial; e) '
                             'plan de convivencia; f) plan de formación; g) evaluación interna; h) planes '
                             'estratégicos>>{#p41a} · Ley 17/2007, artículo 127', 'Origen y marco'],
], [3.4, 11.4, 2.6])
h3('e) Frases de 4.1')
tabla(['Pieza', 'Frase'], [
    ['★ Entrada', '«La intervención se articula en dos niveles: el de centro, de carácter organizativo, y el de aula, que '
                  'se concreta en una situación de aprendizaje.»'],
    ['Origen', '«La propuesta nace de [necesidad] detectada en [memoria de autoevaluación o evaluación inicial] y se '
               'vincula con <<[la línea general de actuación pedagógica y de concreción curricular o el objetivo general '
               'destinado a la mejora del rendimiento escolar y de la calidad educativa del centro]>>{#p41b} del proyecto '
               'educativo.»'],
    ['★ Sentido descendente', '«El equipo técnico de coordinación pedagógica acordó [línea de centro], que cada equipo de '
                              'ciclo concreta para su alumnado.»'],
    ['Ciclo', '«En el equipo de ciclo se acuerdan el producto final común, el reparto de sesiones entre áreas y una '
              'rúbrica compartida.»'],
    ['Diversidad', '«Antes del inicio, la tutoría se reúne con el equipo de orientación para ajustar las medidas de [alumno '
                   'o alumna]; el profesorado de [especialidad] interviene dentro del aula en [sesiones].»'],
    ['<<★ Criterios pedagógicos>>{#p41c}', '<<«Los criterios pedagógicos del proyecto educativo, que el artículo 21.3.c) '
                                          'del Decreto 328/2010 establece como base para planificar, entre otros aspectos, '
                                          'el tiempo escolar y extraescolar, orientan la actividad complementaria '
                                          '[salida], el uso de [recurso digital] como herramienta común y la integración '
                                          'de la cultura andaluza mediante [elemento].»>>{#p41c}'],
    ['Equipo docente <<(según el supuesto)>>{#p41d}', '«En la reunión del equipo docente, coordinada por la tutoría, se '
                                                      'acuerda la aportación de [especialistas] al producto final.»'],
    ['Familias <<(según el supuesto)>>{#p41d}', '«Las familias son informadas en [cauce] y participan en [actividad].»'],
    ['<<Protección de datos (según el supuesto)>>{#p41e}', '<<«Conforme a la Ley Orgánica 3/2018, de 5 de diciembre, de '
                                                          'Protección de Datos Personales y garantía de los derechos '
                                                          'digitales, al ser el alumnado menor de catorce años, se recaba '
                                                          'por [iPasen] la autorización de las familias antes de difundir '
                                                          '[grabaciones o imágenes].»>>{#p41e}'],
    ['◆ Coordinación horizontal y vertical', '«La coordinación es horizontal (equipo docente del nivel o del ciclo) y '
                                             'vertical (equipo técnico de coordinación pedagógica y tránsito entre '
                                             'ciclos).»'],
    ['★ Cierre', '«Las conclusiones se trasladarán a la memoria de autoevaluación como logros, dificultades y propuestas de '
                 'mejora.»'],
], [4.2, 13.2])

h2('4.2. Datos identificativos: a) Base y frases')
nota('Sustituye a la lista a) de la página 39.')
bul('Definición: el Decreto 101/2023, artículo 7.1, define la situación de aprendizaje; la Orden de 30 de mayo de 2023, '
    'artículo 3, exige que integren elementos de distintas áreas y atiendan a la diversidad, los intereses y la igualdad '
    '<<(la Orden se presenta en la concreción curricular, no en los datos)>>{#p42b}.',
    'Paso 1 del anexo IV de la Orden de 30 de mayo de 2023: localización de un centro de interés.',
    '★ «A nivel de aula, la propuesta se concreta en la situación de aprendizaje «[título]», dirigida al grupo de [curso] '
    'y planteada desde [área eje], en conexión con [áreas].»',
    '«Se desarrolla durante el [trimestre], a lo largo de [n.º] sesiones, coincidiendo con [efeméride].»',
    '«Parte del reto de [reto] y culmina en [producto], que se presentará a [destinatario].»',
    '<<★ «La situación conecta con los intereses del alumnado y con el Objetivo de Desarrollo Sostenible (ODS) [número y '
    'nombre], y da continuidad a [la línea general de actuación pedagógica y de concreción curricular o el objetivo '
    'general destinado a la mejora del rendimiento escolar y de la calidad educativa del centro].»>>{#p42a}',
    'Variante T2 y T5: «Esta situación de aprendizaje forma parte de [plan de lectura, itinerario de problemas o proyecto '
    'de centro] que se desarrolla a lo largo del curso.»',
    'Temporalización realista: veinticinco sesiones semanales con el recreo (Orden de 30 de mayo de 2023, artículo 8.1); '
    'respeto al horario mínimo de cada área (artículo 8.2, 2026); 30 minutos diarios de lectura (artículo 8.3).')

h2('4.2.1. Concreción curricular: tabla de elementos de quinto')
nota('<<Nuevo, antes del banco EC de la página 40 (que sigue igual).>>{#p421a}')
p('<<De la tabla de elementos curriculares de Gem: una competencia específica por fila, con su criterio de quinto, un '
  'saber vinculado a ese criterio en el BOJA y dos descriptores de la conexión oficial de la competencia. Los textos son '
  'resúmenes. La primera área se desarrolla entera; de la segunda, solo la competencia.>>{#p421a}')
tabla(['Área', 'Competencia específica', 'Criterio de 5.º', 'Un saber básico', 'Descriptores'],
      [['<<' + c + '>>{#p421a}' for c in f] for f in T.ELEMENTOS], [1.3, 5.0, 4.4, 4.6, 2.1])

h2('4.2.2. Metodología: a) Marco normativo')
nota('Sustituye a la tabla a) de las páginas 43 y 44, y recibe la tabla de los principios del antiguo 3.1.')
tabla(['Utilidad', 'Norma', 'Qué dice', 'Uso'], [
    ['★', 'Decreto 101/2023, artículo 7.2', 'Metodología activa, motivadora y participativa, que parte de los intereses del '
                                           'alumnado y favorece el trabajo individual, cooperativo y el aprendizaje entre '
                                           'iguales', 'Frase de arranque (coincide con C7)'],
    ['◆', 'Instrucciones de 18 de junio de 2024, método común de resolución', 'Subrayar con colores los datos, las palabras '
                                                                             'clave y la pregunta', 'T2b'],
    ['<<★>>{#p422a}', 'Orden de 30 de mayo de 2023, anexo II, introducción de cada área',
     '<<Orientaciones metodológicas para la adquisición de las competencias específicas: están en la introducción de cada '
     'área (tabla siguiente)>>{#p422a}', '<<Último bloque de la metodología, en tres o cuatro palabras>>{#p422a}'],
    ['★', 'Decreto 101/2023, artículo 6', 'Principios pedagógicos <<(tabla siguiente)>>{#p422b}',
     '<<Siempre el DUA (e), Andalucía (g) y lo digital (c), cada uno con su ejemplo>>{#p422b}'],
    ['★', 'Orden de 30 de mayo de 2023, artículo 3 y anexo IV', 'Situaciones que integran áreas; esquema orientativo de '
                                                               'diseño en nueve pasos', 'Acreditar que el índice responde '
                                                                                        'a la norma'],
    ['—', 'Decreto 101/2023, artículo 7.3', 'Funcionamiento coordinado de los equipos docentes para un enfoque '
                                           'interdisciplinar, integrador y holístico', '<<En el apartado 3, con el 10.2 del '
                                                                                       'Real Decreto 157/2022>>{#p422c}'],
    ['—', 'Real Decreto 157/2022, anexo III', 'Centros de interés; tareas de creciente complejidad; agrupamientos diversos; '
                                             'interacción oral; recursos auténticos analógicos y digitales; alineación con '
                                             'el Diseño Universal para el Aprendizaje', 'Justificación de la secuencia'],
    ['—', 'Decreto 101/2023, artículo 4.b) y e)', 'Globalidad; aprendizaje significativo', 'Fundamentación'],
    ['—', 'LOE modificada por LOMLOE, artículo 19.4', 'Tiempo para proyectos significativos y resolución colaborativa de '
                                                     'problemas', 'Proyectos'],
    ['—', 'Ley 17/2007, artículo 40 (rúbrica oficial)', 'Cultura andaluza', 'Conexión con Andalucía'],
], [1.6, 4.4, 6.4, 5.0])
h3('<<Decreto 101/2023, artículo 6: principios pedagógicos (★ los tres fijos)>>{#p422d}')
tabla(['Letra', 'Principio', 'Tipos'], [
    ['a)', 'Lectura, con tiempo diario no inferior a 30 minutos', 'T2 lectura, T1 lengua'],
    ['b)', 'Bases para el Perfil competencial', 'Todos'],
    ['<<★ c)>>{#p422d}', 'Tecnologías de la información', 'T1 tecnología, T6 <<y todos>>{#p422d}'],
    ['d)', 'Desarrollo sostenible', 'T1 medio ambiente'],
    ['<<★ e)>>{#p422d}', 'Diseño Universal para el Aprendizaje', 'T3 y todos'],
    ['f)', 'Inteligencia emocional', 'T4'],
    ['<<★ g)>>{#p422d}', 'Patrimonio cultural y natural de Andalucía y modalidad lingüística andaluza',
     'T1 patrimonio, oralidad <<y todos>>{#p422d}'],
    ['h)', 'Igualdad y resolución pacífica de conflictos (con referencia a la Ley 12/2007)', 'T4, coeducación'],
    ['i)', 'Proyectos significativos', 'T1, T5, T6'],
    ['j)', 'Recopilación y presentación de la información, cálculo, resolución de problemas y razonamiento matemático',
     'T2 matemáticas, T1 ciencias'],
], [1.6, 11.6, 4.2])
h3('<<Orientaciones metodológicas de cada área (anexo II de la Orden; una idea por frase; ★ las más citables)>>{#p422e}')
B.append(('orientaciones', 'p422e'))
h3('4.2.2. f) Recursos digitales (encabezado que cambia)')
p('<<Recursos digitales, siempre con finalidad didáctica y cautelas de protección de datos: se citan al final de las '
  'actividades de la secuencia (4.2.3), no en la metodología.>>{#p422h}')
h3('4.2.2. h) Frases de metodología')
nota('Sustituye a la lista h) de la página 47.')
bul('<<★ «La propuesta responde a los principios pedagógicos del artículo 6 del Decreto 101/2023, en especial el Diseño '
    'Universal para el Aprendizaje ([ejemplo]), el conocimiento del patrimonio cultural y natural de Andalucía ([ejemplo]) '
    'y la integración de las tecnologías de la información y la comunicación ([ejemplo]).»>>{#p422f}',
    '★ «De acuerdo con su artículo 7, la metodología es activa, motivadora y participativa y combina el trabajo '
    'individual, el cooperativo y el aprendizaje entre iguales.»',
    '<<★ «Por último, de acuerdo con las orientaciones que el anexo II de la Orden de 30 de mayo de 2023 recoge para [área], '
    'la propuesta [idea clave del área], como [ejemplo].»>>{#p422g}',
    '◆ «La situación sigue el esquema orientativo de diseño del anexo IV de la Orden de 30 de mayo de 2023.»',
    '«El docente actúa como guía y mediador, que acompaña al alumnado hacia la autonomía.»',
    '«El error se trata como una oportunidad de aprendizaje.»')

h2('4.2.3. Secuencia didáctica: e) Frase de cierre de las actividades')
nota('<<Nuevo, después del banco AC de la página 49.>>{#p423a}')
p('<<★ «En las actividades se emplean materiales variados ([manipulativos, impresos, del entorno]) y recursos tecnológicos '
  'con finalidad didáctica, como [herramienta] para [función], y la información se presenta en distintos formatos '
  '([visual, oral, manipulativo]) para atender a los diferentes ritmos y estilos.»>>{#p423a}')

h2('4.2.4. Atención a la diversidad: a) Diseño Universal para el Aprendizaje (fila que cambia)')
nota('Sustituye a la cuarta fila de la tabla a) de la página 50.')
tabla(['Principio', 'Aplicación en la secuencia', 'Recurso'], [
    ['Implicación', 'Autorregulación: rutinas, agenda visual, semáforo <<o escala de autovaloración>>{#p424a}',
     'Classroomscreen'],
], [3.4, 10.4, 3.6])

h2('4.2.5. Evaluación: b), c) y d)')
nota('Sustituye a b), c) y d) de las páginas 54 y 55; a) y e) siguen igual.')
h3('b) La tríada evidencia-técnica-instrumento ★')
tabla(['Técnica', 'Instrumentos', 'Evidencias típicas'], [
    ['★ Observación sistemática', 'Registro anecdótico, lista de control, escala de estimación',
     'Participación en equipos, debates, uso de materiales'],
    ['★ Análisis de producciones', 'Rúbrica, lista de control, portfolio', 'Producto final, fichas, cuaderno, textos, '
                                                                           'maquetas, vídeos'],
    ['★ Autoevaluación y coevaluación', '<<KPSI, escala de autovaloración, rúbrica de un solo punto, escalera de la '
                                        'metacognición, semáforo, ficha de equipo>>{#p425a}',
     'Reflexión final, funcionamiento del equipo'],
    ['Intercambios orales', 'Escala de estimación, rúbrica de exposición oral<<, mini entrevista con cada '
                            'equipo>>{#p425a}', 'Exposición, entrevista, asamblea'],
    ['Pruebas orales, escritas o prácticas', 'Cuestionario, prueba competencial con rúbrica', 'Resolución de problemas, '
                                                                                            'comprensión de textos'],
], [4.4, 7.4, 5.6])
h3('c) Instrumentos')
tabla(['Utilidad', 'Instrumento', 'Qué es', 'Cuándo'], [
    ['★', 'Rúbrica', 'Criterios por niveles de logro descritos', 'Producto final; el que más esperan los tribunales'],
    ['★', 'Lista de control', 'Indicadores sí/no', 'Evaluación inicial de la propuesta, procesos, práctica docente'],
    ['★', 'Escala de estimación', 'Indicadores con grados', 'Observación, coevaluación, práctica docente'],
    ['<<★>>{#p425c}', '<<KPSI>>{#p425c}', '<<Inventario de conocimientos previos: cada estudiante valora de 1 a 4 lo que '
                                          'sabe de cada objetivo>>{#p425c}',
     '<<Al empezar y, el mismo, al acabar para comparar (evaluación formativa y formadora)>>{#p425c}'],
    ['<<★>>{#p425c}', '<<Escala de autovaloración>>{#p425c}', '<<Indicadores de un criterio con niveles y una casilla para '
                                                              'decir cómo mejorar>>{#p425c}',
     '<<Autoevaluación al cierre (sustituye a la diana)>>{#p425b}'],
    ['<<◆>>{#p425c}', '<<Q-sort>>{#p425c}', '<<Clasificar afirmaciones en «no lo conozco», «me suena» y «conozco y puedo '
                                            'explicarlo»>>{#p425c}', '<<Inicio y final; alternativa al KPSI>>{#p425c}'],
    ['<<◆>>{#p425c}', '<<Base de orientación>>{#p425c}', '<<Guía con los pasos de la tarea y lo que se va a evaluar, '
                                                         'entregada al empezar>>{#p425c}',
     '<<Durante la tarea; autorregulación>>{#p425c}'],
    ['<<◆>>{#p425c}', '<<Escalera de la metacognición>>{#p425c}', '<<Qué he aprendido, cómo, para qué me sirve y en qué '
                                                                  'otras ocasiones puedo usarlo>>{#p425c}',
     '<<Cierre, de forma oral o escrita>>{#p425c}'],
    ['<<◆>>{#p425c}', '<<Mini entrevista con cada equipo>>{#p425c}', '<<Conversación breve que revisa lo hecho con los '
                                                                     'criterios de éxito>>{#p425c}',
     '<<Antes del producto final; retroalimentación>>{#p425c}'],
    ['◆', 'Rúbrica de un solo punto', 'Solo el nivel esperado, con espacio para lo superado y lo mejorable',
     'Coevaluación sencilla'],
    ['◆', 'Portfolio', 'Evidencias seleccionadas con reflexión', 'Proyectos largos; lectura'],
    ['◆', 'Semáforo', 'Tres colores de logro o de ayuda', 'Autoevaluación rápida'],
    ['◆', 'Cuestionario digital', 'Respuesta inmediata', 'Inicio y final de la propuesta'],
    ['◆', 'Tabla «Qué sé… qué he aprendido» y «Antes pensaba… ahora pienso»', 'Comparan inicio y final',
     'Inicial y final; metacognición'],
    ['◆', 'Sociograma', 'Mapa de relaciones', 'T4: inicial y final'],
    ['—', 'Registro anecdótico', 'Hechos significativos', 'Procesual; convivencia'],
    ['—', 'Diario de clase', 'Registro reflexivo del docente', 'Práctica docente'],
    ['—', 'Ficha o plan de equipo', 'Funcionamiento y aportaciones', 'Coevaluación del cooperativo'],
    ['◆', 'Lista de comprobación del producto', 'Elementos que debe tener el producto (cómic, cartel, carta), usada por el '
                                                 'alumnado antes de entregar', 'Autorregulación (T2d, T1h)'],
    ['◆', 'Ticket de salida', 'Qué he aprendido, qué dudas tengo, cómo ha funcionado la sesión', 'Cierre de sesión; evalúa '
                                                                                                 'a la vez el aprendizaje '
                                                                                                 'y la práctica'],
    ['—', 'Rúbrica de cinco niveles', 'Niveles vinculados a los tramos de calificación (insuficiente a sobresaliente)',
     'Evaluación final de un criterio'],
    ['—', 'Banco de rúbricas y diario de aprendizaje del CEDEC (INTEF)', 'Instrumentos de una institución oficial, con '
                                                                         'licencia abierta, filtrables por área y nivel',
     'Fuente de instrumentos adaptables'],
], [1.6, 4.0, 6.6, 5.2])
p('<<**Fuera**: la diana de autoevaluación y la diana cooperativa (la diana es de infantil, decisión de Gem).>>{#p425b}')
h3('d) Momentos y agentes')
tabla(['Momento', 'Instrumento recomendado'], [
    ['Inicial (de la propuesta)', '<<KPSI o Q-sort de los objetivos de la situación;>>{#p425e} cuestionario digital; '
                                  'tabla «Qué sé…»'],
    ['Continua', 'Observación con registro o escala; revisión de la evidencia de cada fase<<; base de orientación; mini '
                 'entrevista con cada equipo antes del producto final>>{#p425e}'],
    ['Final', 'Rúbrica del producto; <<el mismo KPSI o Q-sort del inicio para comparar>>{#p425e}'],
], [5.0, 12.4])
p('Contraste de evidencias: «se contrastan las evidencias de varios instrumentos, momentos y agentes» (Orden, artículo '
  '10.4), en lugar de una supuesta «técnica de triangulación». Heteroevaluación compartida: los especialistas de apoyo '
  'observan con la misma escala que la tutoría. Retroalimentación inmediata durante la tarea y orientaciones para la '
  'siguiente.')
p('Heteroevaluación (rúbrica, escala, registro) · coevaluación (escala del trabajo en equipo; puede omitirse de forma '
  'razonada si perjudica a alumnado vulnerable) · autoevaluación (<<KPSI, escala de autovaloración, escalera de la '
  'metacognición o semáforo>>{#p425d}; imprescindible).')

h2('7. Recursos transversales de redacción (filas que cambian)')
nota('7.1, fila E4 (página 58); 7.2, fila «Remisión interna», y 7.3, fila «Anunciar el índice» (página 59).')
tabla(['N.º', 'Estructura', 'Apartado'], [
    ['E4', '<<Siete datos en tres frases (identificar, situar, dar sentido) y una cuarta con el ODS y la continuidad con '
           'el contexto>>{#p71a}', '4.2'],
], [1.6, 13.0, 2.8])
tabla(['Función', 'Conectores'], [
    ['◆ Remisión interna', 'Como se indicó en el contexto · <<En coherencia con las líneas generales de actuación '
                           'pedagógica y la concreción curricular señaladas>>{#p43a} · Criterio ya citado en la concreción '
                           'curricular'],
], [4.2, 13.2])
tabla(['Evitar', 'Usar'], [
    ['<<Olvidar el preíndice o alargarlo>>{#p73a}', '<<Una o dos frases que recorren los apartados>>{#p73a}'],
], [8.7, 8.7])

# ===============================================================================================================
parte('Parte III. Fichas por tipo de supuesto (filas que cambian)')
clave('<<**Lo que cambia en todas las fichas.** En el apartado 2, los nombres del Decreto 483/2026 (líneas generales de '
      'actuación pedagógica y la concreción curricular; objetivos generales destinados a la mejora del rendimiento '
      'escolar y de la calidad educativa del centro) y el sociograma. En el 3, la normativa fija (artículo 10.2 del Real Decreto 157/2022 y 7.3 del Decreto '
      '101/2023) y la instrucción del área; la norma propia de cada familia pasa al apartado que se indica y los principios '
      'pedagógicos, a 4.2.2. En 4.2, el ODS. En 4.2.1, dos áreas. En 4.2.2, el DUA, Andalucía y lo digital, y las '
      'orientaciones del área. En 4.2.3, materiales, formatos y recursos digitales al final de las actividades. En 4.2.5, '
      'sin diana; KPSI o Q-sort y escala de autovaloración.>>{#p3nota}')
h2('0.7. Qué cambia según la familia (fila «3»)')
nota('Sustituye a la fila «3. Norma específica» de la tabla 0.7 de la página 62.')
tabla(['Apartado', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6'], [
    ['<<3. Normativa>>{#p07a}', '<<Fija + instrucción; autores del tema>>{#p07a}', '<<Fija + instrucción de lectura o de '
                                                                                   'matemáticas>>{#p07a}',
     '<<Fija + instrucción; diversidad, en 4.2.4>>{#p07a}', '<<Fija + instrucción; Orden de 2011, en 4.1>>{#p07a}',
     '<<Fija + instrucción; Reglamento Orgánico, en 4.1>>{#p07a}', '<<Fija + instrucción; autor de la '
                                                                   'metodología>>{#p07a}'],
], [2.2, 2.6, 2.6, 2.6, 2.6, 2.6, 2.2])

h2('T1. Propuesta didáctica sobre una temática (filas que cambian)')
nota('Tabla «Qué poner en cada apartado» de las páginas 64 y 65; las demás filas siguen igual.')
tabla(['Apartado', 'Qué poner', 'Normas y autores'], [
    ['2', 'Recurso del entorno que se usará; <<línea general de actuación pedagógica y de concreción curricular u objetivo '
          'general destinado a la mejora del rendimiento escolar y de la calidad educativa del centro, '
          'sociograma>>{#pt1a} y programa del subtipo; interés y dificultad del grupo ligados al tema; un perfil',
     '<<Solo se nombran: la norma se cita en 4.1>>{#pt1a}'],
    ['3', 'Autor de didáctica del área + autor del enfoque, <<muy específicos del subtipo>>{#pt1b}; psicoevolutivo '
          'aplicado a una tarea; <<normativa fija e instrucción del área>>{#pt1b}',
     '<<Real Decreto 157/2022, 10.2; Decreto 101/2023, 7.3; instrucción del área>>{#pt1b}'],
    ['4.1', 'Origen en el proyecto de centro o en <<una línea general de actuación pedagógica y de concreción '
            'curricular>>{#pt1i}; ciclo (producto, calendario, rúbrica); reserva de espacio; criterios pedagógicos; agente '
            'externo; familias si el supuesto lo pide', 'Decreto 328/2010, artículos 79-83, 24.2; 81.f) si hay salida'],
    ['4.2', 'Título con el reto; áreas del enunciado; trimestre y efeméride; 12 sesiones; producto y destinatario<<; '
            'ODS>>{#pt1c}', 'Decreto 101/2023, artículo 7.1'],
    ['4.2.2', '<<Principios fijos (DUA, Andalucía y digital) con ejemplo; proyectos o indagación; cooperativo con técnicas; '
              'orientaciones del área>>{#pt1d}', '<<Decreto 101/2023, artículos 6 y 7.2; Orden, anexo II;>>{#pt1d} '
                                                 'Vergara (2021) o Pujol (2003)'],
    ['4.2.5', 'Rúbrica del producto; escala del proceso; cuaderno de campo o portfolio; <<KPSI o Q-sort; escala de '
              'autovaloración>>{#pt1e}; coevaluación; práctica docente', 'Orden de 30 de mayo de 2023, artículos 9 y 10; '
                                                                         'Castillo y Cabrerizo (2010)'],
    ['6', '<<Seis normas básicas (con la instrucción del área)>>{#pt1f} + la del subtipo si se citó; tres autores',
     'Parte II, 6'],
], [1.8, 10.4, 5.2])
p('**Instrumentos**: rúbrica del producto ★ · escala de observación del trabajo en equipo · cuaderno de campo o dosier de '
  'investigación (T1g) · lista de comprobación del producto antes de entregar · <<KPSI o Q-sort al empezar y al acabar · '
  'escala de autovaloración>>{#pt1g} · rúbrica de un solo punto · lista de control de la práctica docente. En T1d, '
  'indicador de seguridad y bienestar digital.')
tabla(['Error', 'Corrección'], [
    ['<<Autores genéricos>>{#pt1h}', '<<Autores muy específicos del subtipo; la normativa es casi la misma>>{#pt1h}'],
], [8.7, 8.7])

h2('T2. Mejora de una competencia instrumental (filas que cambian)')
nota('Tabla de las páginas 66 y 67.')
tabla(['Apartado', 'Lectura (T2a) y oralidad o escritura (T2c, T2d)', 'Resolución de problemas (T2b)'], [
    ['2', 'Dato de la evaluación inicial o de la memoria de autoevaluación; <<objetivo general destinado a la mejora del '
          'rendimiento escolar y de la calidad educativa del centro>>{#pt2a}; '
          'Bibliotecas Escolares o Comunica; en T2d, el entorno como corpus de textos; grupo en tres perfiles de desempeño',
     'Dato de la evaluación inicial; <<objetivo general destinado a la mejora del rendimiento escolar y de la calidad '
     'educativa del centro>>{#pt2a}; STEM o aulaDjaque; itinerario de problemas'],
    ['3', '<<Normativa fija +>>{#pt2b} Instrucciones de lectura (30 minutos diarios; antes, durante y después; literal, '
          'inferencial y crítica; cinco ejes); en T2d, proceso de escritura (Cassany, 1989)',
     '<<Normativa fija +>>{#pt2b} Instrucciones de 18 de junio de 2024 (itinerario; método común; de lo corporal a lo '
     'simbólico); Pólya y Alsina; distinción entre ejercicio y problema'],
], [1.8, 7.8, 7.8])

h2('T3. Atención a la diversidad marcada (filas que cambian)')
nota('Tabla de la página 69 e instrumentos de la página 70.')
tabla(['Apartado', 'Qué poner', 'Normas y autores'], [
    ['3', 'Echeita (2006) o Elizondo (2022); Rose y Meyer (2002); <<normativa fija e instrucción del área (el DUA, en '
          '4.2.2; la norma de diversidad, en 4.2.4)>>{#pt3a}', '<<Real Decreto 157/2022, 10.2; Decreto 101/2023, 7.3; '
                                                             'instrucción del área>>{#pt3a}'],
], [1.8, 10.4, 5.2])
p('**Instrumentos**: escala de participación con el rol asignado ★ · lista de control de las medidas ★ · comparación '
  'inicial-final del indicador de partida · prueba adaptada en formato y tiempo · prueba paralela con referente en la '
  'adaptación significativa · <<escala de autovaloración o semáforo con pictogramas>>{#pt3b} · entrevista o cuestionario '
  'trimestral a la familia.')

h2('T4. Convivencia, emociones y acción tutorial (filas que cambian)')
nota('Tabla de las páginas 71 y 72.')
tabla(['Apartado', 'Qué poner', 'Normas y autores'], [
    ['2', '<<Dato de clima (sociograma, incidencias); plan de convivencia; Red Andaluza: «Escuela Espacio de Paz»; '
          'familias y su delegado o delegada>>{#pt4a}', 'Decreto 328/2010, artículo 22'],
    ['3', 'Álvarez y Bisquerra (1996); Uruñuela (2006); <<normativa fija e instrucción del área (los principios f y h, en '
          '4.2.2; la Orden de 2011 y la Ley Orgánica 8/2021, en 4.1)>>{#pt4b}', '<<Real Decreto 157/2022, 10.2; Decreto '
                                                                              '101/2023, 7.3; instrucción del '
                                                                              'área>>{#pt4b}'],
], [1.8, 10.4, 5.2])

h2('T5. Organizativo o de centro (filas que cambian)')
nota('Tabla de las páginas 73 y 74.')
tabla(['Apartado', 'Qué poner', 'Normas y autores'], [
    ['2', 'Tamaño del centro y unidades; <<líneas generales de actuación pedagógica y la concreción curricular, objetivos '
          'generales destinados a la mejora del rendimiento escolar y de la calidad educativa del centro,>>{#pt5a} '
          'planes y programas; recursos y espacios; en T5a, agrupamiento y ratio (LOE, 157.1.a: 25; 87.2: hasta un 10 % '
          'más)', '<<Solo se nombran: la norma se cita en 4.1>>{#pt5a}'],
    ['3', 'Antúnez (1987) o Bolívar (2000); Zabala y Arnau (2007); <<normativa fija e instrucción del área (el Reglamento '
          'Orgánico y la autonomía de los centros, en 4.1)>>{#pt5b}', '<<Real Decreto 157/2022, 10.2; Decreto 101/2023, '
                                                                      '7.3; instrucción del área>>{#pt5b}'],
], [1.8, 10.4, 5.2])

h2('T6. Metodología o recurso impuesto (filas que cambian)')
nota('Subtipo T6a (página 76) y tabla de las páginas 76 y 77.')
tabla(['Subtipo', 'Evaluación propia'], [
    ['T6a. Aprendizaje cooperativo', 'Rúbrica del trabajo en equipo; <<escala de coevaluación por roles>>{#pt6d}'],
], [5.0, 12.4])
tabla(['Apartado', 'Qué poner', 'Normas y autores'], [
    ['2', 'La metodología en las líneas del centro o en su plan de formación; recurso disponible',
     '<<Decreto 328/2010, 21.3.b) (líneas generales de actuación pedagógica y la concreción curricular) y f) (plan de '
     'formación)>>{#pt6a}'],
    ['3', 'Autor de la metodología; <<normativa fija e instrucción del área (el 7.2, en 4.2.2)>>{#pt6b}; en T6b, definición '
          'de la competencia digital', '<<Real Decreto 157/2022, 10.2; Decreto 101/2023, 7.3; instrucción del área;>>{#pt6b} '
                                       'Real Decreto 157/2022, anexo I'],
    ['4.1', '<<Línea general de actuación pedagógica y de concreción curricular>>{#pt6a} o plan de formación; acuerdo de ciclo sobre roles, estructuras o '
            'recompensas; programa afín (<<Emprendimiento Educativo, Escuela Código 4.0, Plan de Actuación '
            'Digital>>{#pt6c}); en T6e, calendario de uso, responsable y reglamento de organización y funcionamiento; '
            'autorizaciones de imagen', 'Decreto 328/2010, 81.g) y 24.2; Ley Orgánica 3/2018, 7'],
], [1.8, 10.4, 5.2])

# ===============================================================================================================
parte('Parte IV. Lista de verificación final (secciones que cambian)')
nota('<<Secciones 1, 3, 4 y 5 enteras (páginas 78 a 81); las demás siguen igual.>>{#p4nota}')
h2('1. Antes de redactar (borrador, 9 minutos)')
check('Palabras clave del enunciado subrayadas (verbos y objetos de la demanda).',
      'Tipo principal, secundarios y formato decididos (Parte III, apartado 0).',
      'Perfiles nombrados en el enunciado anotados (T3), metodología o recurso impuesto anotado (T6), proyecto o salida '
      'anotados (T5b o T5e).', 'Curso elegido y declarado si el enunciado no lo fija.',
      'Reto y producto final con destinatario real.', 'Cinco actividades, una por fase, y suma de sesiones anotada.',
      'Competencia específica, criterio de evaluación, saberes y dos descriptores anotados.',
      'Contexto a medida: recurso del entorno, <<línea general de actuación pedagógica y de concreción curricular u '
      'objetivo general destinado a la mejora del rendimiento escolar y de la calidad educativa del centro, programa, '
      'sociograma>>{#c1a}, perfil.',
      'Autores (tres o cuatro) y normas (<<seis o siete>>{#c1b}) anotados para el apartado 6.')
h2('3. Apartados 1 a 3')
h3('1. Introducción')
check('Gancho con al menos tres palabras clave literales del enunciado.',
      'Autor con año (o informe verificado), parafraseado.',
      'LOE modificada por LOMLOE con nombre completo y «(en adelante, LOE modificada por LOMLOE)».',
      'Antesala: curso, áreas, tipo de propuesta, título y producto final.',
      '<<Preíndice en una o dos frases;>>{#c1c} sin cifras ni citas dudosas.')
h3('2. Contexto')
check('Tres párrafos: entorno, centro y alumnado.', 'Nada contradice el enunciado.',
      '<<Una de las líneas generales de actuación pedagógica y la concreción curricular y uno de los objetivos generales '
      'destinados a la mejora del rendimiento escolar y de la calidad educativa del centro, en infinitivo y sin '
      'siglas.>>{#c1e}', 'Programa del curso vigente con su nombre exacto.',
      'Alumnado: fortaleza, dificultad ligada al tema, <<sociograma>>{#c1d} y fuente del dato (evaluación inicial).',
      'Perfil o perfiles descritos por necesidad y fortaleza; frase puente a 4.2.4.',
      'Cada dato reaparece después (regla del dato tachado).')
h3('3. Justificación normativa y epistemológica')
check('Dos autores con año, muy específicos del tema, y aportación aplicada a una decisión de la propuesta.',
      '<<Real Decreto 157/2022 (artículo 10.2) y Decreto 101/2023 (artículo 7.3) con nombre completo.>>{#c1f}',
      '<<Instrucción del área con «que establece… y fundamenta…».>>{#c1f}',
      '<<Sin principios pedagógicos (van en 4.2.2).>>{#c1f}', 'Párrafo psicoevolutivo breve.',
      'No supera las 190 palabras.')
h2('4. Apartado 4.1. Intervención a nivel de centro')
check('Frase de entrada con los dos niveles.',
      'Origen en un documento del centro (proyecto educativo, memoria de autoevaluación, evaluación inicial).',
      'Decreto 328/2010 con nombre completo, <<«modificado por el Decreto 483/2026, …», también con nombre completo>>{#c1g}.',
      'Al menos tres agentes, cada uno con verbo y acuerdo (<<equipo técnico, ciclo, equipo de orientación>>{#c1g}).',
      '<<Especialistas de atención a la diversidad (PT y AL) con calendario: antes, durante, al cierre.>>{#c1g}',
      '<<Espacios del centro y del entorno.>>{#c1g}',
      '<<Criterios pedagógicos: actividad complementaria, recurso digital y cultura andaluza.>>{#c1g}',
      '<<Uno o dos bloques según el supuesto (familias, protección de datos, especialistas de área, proyecto educativo, '
      'servicios complementarios, proyecto interdisciplinar).>>{#c1g}',
      'Terminología andaluza (equipo de orientación; nunca «departamento de orientación» ni «programación general anual»).',
      'Cierre con la memoria de autoevaluación.',
      'Si hay proyecto o semana de centro (T5b): circuito, reparto por ciclos, calendario y difusión.',
      'Si hay salida (T5e): autorización de las familias, gratuidad y alternativa, acompañantes, accesibilidad, plan de '
      'autoprotección.')
h2('5. Apartado 4.2. Situación de aprendizaje')
h3('Datos identificativos')
check('<<Los siete datos en tres frases, sin rótulos, y una cuarta con el ODS.>>{#c1h}',
      'Título con el reto o el producto.', 'Sesiones y semanas coinciden con la secuencia.',
      'Efeméride solo si es de la instrucción vigente.')
h3('4.2.1. Concreción curricular')
check('Orden de 30 de mayo de 2023 con nombre completo.',
      'Objetivo de etapa, competencia específica, criterio, saberes, dos descriptores y competencia clave.',
      '<<Una segunda área con su competencia específica resumida.>>{#c1i}',
      'Criterios con la letra del curso (.a impar, .b par) y saberes con su código; si hay duda, número de la competencia y '
      'paráfrasis del criterio.', 'Elementos de todas las áreas que nombra el enunciado.',
      'Saberes elegidos entre los que la tabla oficial vincula al criterio (Parte V); descriptores en la redacción del '
      'ciclo.', 'Vocabulario vigente (sin «contenidos», «estándares», «objetivos didácticos»).')
h3('4.2.2. Metodología')
check('<<Los tres principios del artículo 6 del Decreto 101/2023: DUA, Andalucía y digital, cada uno con ejemplo.>>{#c1j}',
      'Trabajo individual, cooperativo <<(con técnicas)>>{#c1j} y entre iguales, con un ejemplo de cada uno.',
      'Metodología principal con autor y despliegue (en T6, la impuesta, desarrollada a fondo y visible también en 3, 4.2.3 '
      'y 4.2.5).',
      '<<Orientaciones metodológicas del área (anexo II de la Orden) como último bloque.>>{#c1j}')
h3('4.2.3. Secuencia didáctica')
check('Producto final anunciado al principio.', 'Cinco fases en orden, con sesiones.',
      'Cada actividad responde a qué, con quién, con qué y para qué.',
      'Contextos variados (aula, centro, entorno, familia, digital).',
      'Al menos una actividad con agente externo o salida y otra con familias.',
      'Ajustes para el alumnado del contexto en dos o tres actividades.', 'Cada fase deja una evidencia evaluable.',
      'Difusión del producto y reflexión final.',
      '<<Al final de las actividades, materiales variados, recursos digitales con su función y formatos.>>{#c1k}',
      'Al menos 400 palabras.')
h3('4.2.5. Evaluación')
check('Mismos criterios de evaluación que en 4.2.1.', 'Tríada evidencia-técnica-instrumento.',
      'Evaluación inicial de la propuesta, continua y final <<(KPSI o Q-sort al empezar y al acabar)>>{#c1l}.',
      'Autoevaluación y coevaluación con instrumento (o exclusión razonada de la coevaluación).',
      'Evaluación de las medidas de diversidad con indicadores.',
      'Evaluación de la práctica docente con indicadores, instrumento y evidencias.',
      'Uso de los resultados (ajustes, memoria de autoevaluación).')
