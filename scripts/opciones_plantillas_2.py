# -*- coding: utf-8 -*-
"""Plantillas por importancia, segunda versión (fase 38, quinta vuelta, 20 de noviembre de 2026).

Lo que pidió Gem al ver la primera: muchos más ejemplos (de la libreta mágica de Rafa, de su manual educativo, de su
programación y de su libreta definitiva), comodines diferenciadores, lo que se cita de la normativa copiado tal cual,
nada debajo de lo que es fijo, sin ejemplos en «para dar respuesta al supuesto planteado» y, en la instrucción, qué
se toma de ella.

Niveles de cada opción: '1' primera opción (la más importante; si depende del área, una por área), 'C' comodín y
'D' comodín diferenciador (◆, el que sorprende al tribunal). Se escriben en orden de importancia.
Cada opción es (nivel, texto) o (nivel, texto, [elementos]). Dentro de los textos, **...** va en negrita y lo que
sigue a « § » es una nota (de dónde sale o cómo se usa), en gris.
Cada hueco puede llevar 'titulo', 'norma' (citas literales con su fuente) y 'nota' (lo pendiente, en naranja).

Fuentes comprobadas: LOE (artículos 1, 2, 16 y 17), Real Decreto 157/2022 (artículo 10.2 y anexo I), Decreto
101/2023 (artículos 5, 6 y 7), Decreto 328/2010 en la redacción del Decreto 483/2026 (artículo 21.3), Orden de 30 de
mayo de 2023 (artículos 27 y 33), Instrucciones de 21 de junio de 2023 (PDF del repositorio de la programación) y
Resolución de 29 de junio de 2026 (programas). Las Instrucciones de 18 de junio de 2024 van resumidas con la libreta
definitiva de Gem (su PDF no se ha podido abrir).
"""
import copy
import re

import textos_libreta_v22 as T

PLANTILLAS = copy.deepcopy(T.PLANTILLAS)


def _fila(clave, empieza):
    return next(f for f in PLANTILLAS[clave]['filas'] if f['texto'].startswith(empieza))


def _cambia(clave, empieza, viejo, nuevo):
    f = _fila(clave, empieza)
    assert viejo in f['texto'], (clave, viejo)
    f['texto'] = f['texto'].replace(viejo, nuevo)


# Huecos: los fijos pasan a texto normal (sin número y sin nada debajo); los que no llevan ejemplos, sin número;
# los nuevos, con números provisionales (91 a 95), que después se renumeran por orden de aparición.
_cambia('7.1', 'Para dar respuesta', '[4|área eje]', '[área eje]')
f = _fila('7.1', '{5|A tal fin')
f['texto'] = re.sub(r'^\{5\|(.*)\}$', r'\1', f['texto'])
_cambia('7.2', 'Alumnado.', '[perfil: necesidad y fortaleza]', '[91|perfil: necesidad y fortaleza]')
_cambia('7.3', '{2|Desde el punto', '{2|Desde el punto de vista normativo,}', 'Desde el punto de vista normativo,')
_cambia('7.5', 'La intervención se articula', '[1|la línea general', '[la línea general')
_cambia('7.5', 'La intervención se articula', '[necesidad]', '[93|necesidad]')
_cambia('7.5', 'Para su desarrollo', 'del proyecto educativo{6|}', 'del proyecto educativo')
_cambia('7.5', 'Familias y entorno.', '[actividad]', '[94|actividad]')
_cambia('7.5', 'Familias y entorno.', '[entidad]', '[95|entidad]')
_cambia('7.5', 'Proyecto interdisciplinar.', '[15|la hora semanal de autonomía del centro]',
        'la hora semanal de autonomía del centro')
_cambia('7.6', 'A nivel de aula', '[n.º] sesiones', '[91|n.º] sesiones')
f = _fila('7.7', 'La situación de aprendizaje contribuye')
f['texto'] = re.sub(r'\{2\|([^}]*)\}', r'\1', f['texto'])
_cambia('7.8', 'Conforme a su artículo 7.2', 'aprendizaje entre iguales ([ejemplo])',
        'aprendizaje entre iguales ([92|ejemplo])')

# 4.1: los bloques según el supuesto, del más frecuente al menos frecuente
ORDEN_41 = ['Familias y entorno.', 'Especialistas del equipo docente.', 'Lo que marca el proyecto educativo.',
            'Protección de datos.', 'Servicios complementarios.', 'Proyecto interdisciplinar.']
filas41 = PLANTILLAS['7.5']['filas']
siempre = [x for x in filas41 if not any(x['texto'].startswith(o) for o in ORDEN_41) and x.get('etiqueta') != T.CIERRE]
segun = sorted([x for x in filas41 if any(x['texto'].startswith(o) for o in ORDEN_41)],
               key=lambda x: next(k for k, o in enumerate(ORDEN_41) if x['texto'].startswith(o)))
cierre = [x for x in filas41 if x.get('etiqueta') == T.CIERRE]
for k, x in enumerate(segun):
    x['etiqueta'] = f'Según el supuesto · {k + 1}.º' + (' (el más frecuente)' if k == 0 else '')
PLANTILLAS['7.5']['filas'] = siempre + segun + cierre

D101 = 'Decreto 101/2023, artículo 6'

OPCIONES = {
    # ------------------------------------------------------------------------------------------------ 7.1
    '7.1': {
        1: {'titulo': 'Dato, cita fiable o pregunta retórica sobre el tema (copiados tal cual de la libreta mágica y '
                      'del manual; la pregunta, en último lugar)', 'ops': [
            ('1', '★ PIRLS 2021 (4.º de Primaria): España, 521 puntos en comprensión lectora, por debajo de la Unión '
                  'Europea (528) y del promedio de la OCDE (533), y por debajo de su resultado de 2016 (528); Andalucía, '
                  '523 § Gancho de T2 lectura. Es el dato más pertinente para Primaria (libreta mágica, Parte II, 1.2).'),
            ('C', 'PISA 2022: España, 474 en lectura, 473 en matemáticas y 485 en ciencias; promedios de la OCDE, 476, 472 '
                  'y 485 § Solo como contexto general: PISA mide a estudiantes de quince años. España no estaba por debajo '
                  'de la media en matemáticas (libreta mágica, Parte II, 1.2).'),
            ('C', '«La Defensoría de la Infancia y la Adolescencia de Andalucía dedicó un informe especial a la atención '
                  'educativa en los colegios públicos rurales (2022), que subraya sus retos y oportunidades.» (sin cifras '
                  'del informe) § Escuela rural (T5a) (libreta mágica, Parte II, 2.1).'),
            ('C', 'Según los datos provisionales del Instituto Nacional de Estadística (INE), en 2025 se registraron 3808 '
                  'suicidios en España. En 2024, con 3846 según el dato provisional, el suicidio fue la segunda causa de '
                  'muerte externa, tras las caídas accidentales. Según la Junta Internacional de Fiscalización de '
                  'Estupefacientes (JIFE), España es el primer país del mundo en consumo de benzodiacepinas, con unas 110 '
                  'dosis diarias por cada 1000 habitantes (datos de 2021, los últimos que he encontrado). § Educación '
                  'emocional (manual, «Datos para empezar a hablar del tema»).'),
            ('D', 'Citas literales verificadas (libreta mágica, Parte II, 1.3):', [
                '«El lenguaje es el vestido del pensamiento». Samuel Johnson, Life of Cowley, en Lives of the English '
                'Poets (1779-1781) § T2 lengua; T1 comunicación.',
                '«El arte no reproduce lo visible, sino que hace visible». Paul Klee, Confesión creadora (1920); la '
                'traducción varía § Educación artística.',
                '«Solo donde hay lenguaje hay mundo». Martin Heidegger, Hölderlin y la esencia de la poesía (1936); la '
                'redacción española varía § T2 lengua oral.',
                '«Diferentes caminos conducen a veces al mismo castillo». George R. R. Martin, Juego de tronos (1996) '
                '§ T3, solo si se domina; baja idoneidad académica.',
                'Ejemplo de uso: «"El lenguaje es el vestido del pensamiento", escribió Samuel Johnson. En la misma '
                'línea, el dominio de la comunicación oral y escrita condiciona el resto de los aprendizajes…».']),
            ('C', 'Pregunta retórica, solo como última opción (libreta mágica, Parte II, 1.1, copiada tal cual; la libreta '
                  'la acompaña de «LOE, 16.2» en la Parte III, «Qué poner en cada apartado»):', [
                '«¿Es posible aprender ciencias, historia o matemáticas sin comprender lo que se lee?» § Lectura (T2a).',
                '«¿Cómo esperar que el alumnado resuelva problemas si no comprende sus enunciados?» § Resolución de '
                'problemas (T2b).']),
        ]},
        2: {'ops': [('1', 'Se concretará con los temas: un autor del tema, de 2020 en adelante, con un solo apellido.')]},
        3: {'titulo': 'Objetivo de la etapa relacionado (artículo 17 de la LOE, literal)', 'ops': [
            ('1', 'El del área eje, copiado tal cual:', [
                '**Lengua.** e) «Conocer y utilizar de manera apropiada la lengua castellana y, si la hubiere, la lengua '
                'cooficial de la Comunidad Autónoma y desarrollar hábitos de lectura».',
                '**Matemáticas.** g) «Desarrollar las competencias matemáticas básicas e iniciarse en la resolución de '
                'problemas que requieran la realización de operaciones elementales de cálculo, conocimientos geométricos '
                'y estimaciones, así como ser capaces de aplicarlos a las situaciones de su vida cotidiana».',
                '**Conocimiento del Medio.** h) «Conocer los aspectos fundamentales de las Ciencias de la Naturaleza, '
                'las Ciencias Sociales, la Geografía, la Historia y la Cultura».',
                '**Educación Artística.** j) «Utilizar diferentes representaciones y expresiones artísticas e iniciarse '
                'en la construcción de propuestas visuales y audiovisuales».',
                '**Tecnología.** i) «Desarrollar las competencias tecnológicas básicas e iniciarse en su utilización, '
                'para el aprendizaje, desarrollando un espíritu crítico ante su funcionamiento y los mensajes que '
                'reciben y elaboran».',
            ]),
            ('C', 'Según el tema, otro objetivo del mismo artículo, también literal:', [
                '**Convivencia y ciudadanía.** a) «Conocer y apreciar los valores y las normas de convivencia, aprender '
                'a obrar de acuerdo con ellas de forma empática, prepararse para el ejercicio activo de la ciudadanía y '
                'respetar los derechos humanos, así como el pluralismo propio de una sociedad democrática».',
                '**Trabajo en equipo.** b) «Desarrollar hábitos de trabajo individual y de equipo, de esfuerzo y de '
                'responsabilidad en el estudio, así como actitudes de confianza en sí mismo, sentido crítico, iniciativa '
                'personal, curiosidad, interés y creatividad en el aprendizaje, y espíritu emprendedor».',
                '**Conflictos.** c) «Adquirir habilidades para la resolución pacífica de conflictos y la prevención de la '
                'violencia, que les permitan desenvolverse con autonomía en el ámbito escolar y familiar, así como en '
                'los grupos sociales con los que se relacionan».',
                '**Igualdad e interculturalidad.** d) «Conocer, comprender y respetar las diferentes culturas y las '
                'diferencias entre las personas, la igualdad de derechos y oportunidades de hombres y mujeres y la no '
                'discriminación de personas por motivos de etnia, orientación o identidad sexual, religión o creencias, '
                'discapacidad u otras condiciones».',
                '**Lengua extranjera.** f) «Adquirir en, al menos, una lengua extranjera la competencia comunicativa '
                'básica que les permita expresar y comprender mensajes sencillos y desenvolverse en situaciones '
                'cotidianas».',
                '**Salud y deporte.** k) «Valorar la higiene y la salud, aceptar el propio cuerpo y el de los otros, '
                'respetar las diferencias y utilizar la educación física, el deporte y la alimentación como medios para '
                'favorecer el desarrollo personal y social».',
                '**Animales.** l) «Conocer y valorar los animales más próximos al ser humano y adoptar modos de '
                'comportamiento que favorezcan la empatía y su cuidado».',
                '**Emociones y coeducación.** m) «Desarrollar sus capacidades afectivas en todos los ámbitos de la '
                'personalidad y en sus relaciones con los demás, así como una actitud contraria a la violencia, a los '
                'prejuicios de cualquier tipo y a los estereotipos sexistas».',
                '**Educación vial.** n) «Desarrollar hábitos cotidianos de movilidad activa autónoma saludable, '
                'fomentando la educación vial y actitudes de respeto que incidan en la prevención de los accidentes de '
                'tráfico».',
            ]),
            ('D', 'Si ningún objetivo encaja, la finalidad de la etapa (artículo 16.2), y la frase termina «que recoge '
                  'entre las finalidades de la etapa…»: «La finalidad de la Educación Primaria es facilitar a los alumnos '
                  'y alumnas los aprendizajes de la expresión y comprensión oral, la lectura, la escritura, el cálculo, '
                  'la adquisición de nociones básicas de la cultura, y el hábito de convivencia así como los de estudio y '
                  'trabajo, el sentido artístico, la creatividad y la afectividad…».'),
            ('D', 'O un principio del artículo 1 o un fin del artículo 2.1, literal («que recoge entre sus principios…» o '
                  '«entre los fines del sistema educativo…»), como en tu libreta definitiva:', [
                '**Inclusión.** Artículo 1.b) «La equidad, que garantice la igualdad de oportunidades para el pleno '
                'desarrollo de la personalidad a través de la educación, la inclusión educativa, la igualdad de derechos '
                'y oportunidades…».',
                '**Diversidad.** Artículo 1.e) «La flexibilidad para adecuar la educación a la diversidad de aptitudes, '
                'intereses, expectativas y necesidades del alumnado, así como a los cambios que experimentan el alumnado '
                'y la sociedad».',
                '**Familias.** Artículo 1.h bis) «El reconocimiento del papel que corresponde a los padres, madres y '
                'tutores legales como primeros responsables de la educación de sus hijos».',
                '**Convivencia y acoso.** Artículo 1.k) «La educación para la convivencia, el respeto, la prevención de '
                'conflictos y la resolución pacífica de los mismos, así como para la no violencia en todos los ámbitos '
                'de la vida personal, familiar y social, y en especial en el del acoso escolar y ciberacoso…».',
                '**Sostenibilidad.** Artículo 1.r) «La educación para la transición ecológica con criterios de justicia '
                'social como contribución a la sostenibilidad ambiental, social y económica».',
                '**Autonomía y creatividad.** Artículo 2.1.f) «El desarrollo de la capacidad de los alumnos para regular '
                'su propio aprendizaje, confiar en sus aptitudes y conocimientos, así como para desarrollar la '
                'creatividad, la iniciativa personal y el espíritu emprendedor».',
                '**Interculturalidad.** Artículo 2.1.g) «La formación en el respeto y reconocimiento de la pluralidad '
                'lingüística y cultural de España y de la interculturalidad como un elemento enriquecedor de la '
                'sociedad».',
                '**Digital.** Artículo 2.1.l) «La capacitación para garantizar la plena inserción del alumnado en la '
                'sociedad digital y el aprendizaje de un uso seguro de los medios digitales…».',
            ]),
        ]},
    },
    # ------------------------------------------------------------------------------------------------ 7.2
    '7.2': {
        1: {'titulo': 'Recursos del entorno (uno o dos, y que después se usen: salida, persona experta o destinatario '
                      'del producto)', 'ops': [
            ('1', 'La biblioteca municipal, que sirve para casi cualquier tema: préstamo de un lote de libros, búsqueda '
                  'de información, club de lectura o lugar para presentar el producto.'),
            ('C', 'Culturales:', ['casa de la cultura o centro cultural, con salas de exposiciones',
                                  'museo local o centro de interpretación', 'archivo municipal, con fotografías y '
                                  'documentos antiguos', 'teatro o auditorio municipal',
                                  'peña flamenca, escuela de música o banda municipal',
                                  'monumentos y yacimientos del municipio']),
            ('C', 'Naturales:', ['parque periurbano, sendero o vía verde', 'espacio natural protegido de la comarca',
                                 'río, arroyo, fuentes o lavaderos', 'huertos urbanos o granja escuela',
                                 'aula de la naturaleza']),
            ('C', 'Sociales y asociativos:', ['residencia de mayores o centro de día',
                                              'asociación de vecinos y centro cívico',
                                              'asociaciones culturales, de mujeres o de personas con discapacidad',
                                              'organizaciones solidarias, como Cruz Roja o el banco de alimentos',
                                              'Consejo Local de Infancia y Adolescencia, órgano de participación infantil']),
            ('C', 'Instituciones y servicios públicos:', [
                'ayuntamiento y sus concejalías (Medio Ambiente, Cultura, Juventud)', 'centro de salud',
                'Policía Local, para la educación vial', 'bomberos, Protección Civil o el INFOCA',
                'punto limpio, depuradora o empresa municipal de aguas', 'oficina de turismo']),
            ('C', 'Económicos:', ['plaza de abastos o mercado', 'comercios y talleres de oficios tradicionales',
                                  'cooperativa agrícola, almazara o bodega',
                                  'empresas locales que reciben o patrocinan el producto']),
            ('C', 'Deportivos: polideportivo, pistas y piscina municipal.'),
            ('D', 'Medios de comunicación locales, como la radio o el periódico digital del pueblo, para difundir el '
                  'producto.'),
            ('D', 'El entorno como corpus: «El entorno del centro ofrece un corpus de textos sociales (carteles, avisos, '
                  'menús, normas, publicidad) que se convierte en material de la propuesta». § Rafa; para supuestos de '
                  'lectura y escritura.'),
        ]},
        2: {'titulo': 'Línea general de actuación pedagógica, en infinitivo', 'ops': [
            ('1', 'Una de las cuatro de la programación, según el tema:', [
                '**Metodologías activas.** Situar al alumnado como protagonista de su aprendizaje mediante metodologías '
                'activas que potencien la colaboración.',
                '**Diversidad.** Flexibilizar la respuesta educativa para adaptarla a la diversidad de aptitudes, '
                'intereses y necesidades del alumnado.',
                '**Investigación.** Impulsar el pensamiento crítico a través de la búsqueda y el análisis de fuentes para '
                'resolver problemáticas y comunicar hallazgos.',
                '**Digital.** Fomentar la competencia digital del alumnado mediante el uso crítico y responsable de las '
                'herramientas y recursos tecnológicos del aula.',
            ]),
            ('C', 'Otras, inventables y en infinitivo (de tu libreta definitiva y de la de Rafa):', [
                '**Lectura.** Desarrollar el hábito lector diario y mejorar la capacidad comunicativa del alumnado.',
                '**Matemáticas.** Promover la resolución de problemas, aplicando material visual y manipulativo en el '
                'proceso de enseñanza.',
                '**Andalucía.** Acercar al alumnado al conocimiento de la cultura andaluza.',
                '**Medio ambiente.** Conseguir el compromiso del alumnado con el cuidado del medio ambiente.',
                '**Convivencia.** Favorecer un clima de convivencia positiva basado en el diálogo, la gestión de las '
                'emociones y la resolución pacífica de los conflictos.',
                '**Igualdad.** Promover la igualdad efectiva entre alumnas y alumnos y la superación de los estereotipos '
                'sexistas en todas las áreas.',
                '**Familias y entorno.** Abrir el centro a las familias y al entorno mediante propuestas que respondan a '
                'necesidades reales de la localidad.',
            ]),
        ]},
        3: {'titulo': 'Objetivo general destinado a la mejora del rendimiento escolar y de la calidad educativa del '
                      'centro, en infinitivo', 'ops': [
            ('1', '**Si es de Lengua.** Mejorar la comprensión lectora inferencial mediante el tiempo diario de lectura '
                  'planificada y comprobar su progreso con una prueba común trimestral.'),
            ('1', '**Si es de Matemáticas.** Mejorar la resolución de problemas mediante un modelo común de pasos en '
                  'todos los ciclos y comprobar su progreso con una prueba común trimestral.'),
            ('C', 'Otros, inventables (de tu libreta definitiva y de la programación):', [
                '**Expresión escrita.** Elevar la expresión escrita del alumnado, fomentando la coherencia y la '
                'corrección ortográfica de los textos producidos.',
                '**Expresión lectora.** Reducir las carencias en la expresión lectora a través de un plan lector basado '
                'en las Instrucciones de 21 de junio de 2023.',
                '**Clima escolar.** Lograr un buen clima escolar que favorezca el trabajo y el esfuerzo, en el que el '
                'diálogo sea frecuente para prevenir y solucionar los posibles conflictos.',
                '**Competencia socioemocional.** Desarrollar la competencia socioemocional del alumnado mediante una '
                'asamblea semanal de emociones y un sociograma trimestral que permita comprobar la mejora de la '
                'convivencia.',
                '**Contextos reales.** Conectar los contenidos con contextos reales del entorno para mejorar el '
                'rendimiento en las áreas instrumentales.',
                '**Cálculo mental.** Mejorar la agilidad en el cálculo mental mediante retos breves diarios y comprobar '
                'su progreso con una prueba común al final de cada trimestre.',
            ]),
        ]},
        4: {'titulo': 'Plan o programa (Resolución de 29 de junio de 2026): qué tiene que cumplir cada uno', 'ops': [
            ('1', 'Educación Inclusiva, de procedimiento tipo A: «La participación de los centros educativos en los '
                  'siguientes Programas se determinará de oficio por parte de la propia Consejería de Desarrollo Educativo '
                  'y Formación Profesional». § El centro no tiene que pedir nada; vale siempre, porque toda propuesta '
                  'atiende a la diversidad.'),
            ('C', 'Los demás de tipo A, también de oficio: Bienestar Emocional, Bibliotecas Escolares, Plan de Actuación '
                  'Digital, Educación Inclusiva +, Plan de Apertura de Centros Docentes y Plan de Igualdad de Género en '
                  'Educación de Andalucía.'),
            ('D', '**La robótica: Escuela Código 4.0** (tipo A), de oficio solo «en centros que impartan enseñanzas '
                  'incluidas en el Programa de Cooperación Territorial Código Escuela 4.0 (segundo ciclo de Educación '
                  'Infantil, Educación Primaria y/o Educación Secundaria Obligatoria)». Su Proyecto STEAM 4.0 pide «Una '
                  'Línea de Actuación en el Ámbito “Procesos de Enseñanza-Aprendizaje” del PAD, vinculada al desarrollo '
                  'del pensamiento computacional, la programación, la robótica o la inteligencia artificial». § La '
                  'robótica está aquí, no en STEM (página del Proyecto STEAM 4.0 de la Consejería, que desarrolla la '
                  'Resolución de 1 de agosto de 2025).'),
            ('C', 'Tipo B, «participación sin convocatoria específica (convocatoria general)»: «la participación de los '
                  'centros educativos en los siguientes Programas requerirá la previa solicitud de los mismos». Lo que hay '
                  'que cumplir:', [
                '**Plazo.** «del 1 al 30 de septiembre de 2026, ambos inclusive, a excepción del Programa Red Andaluza: '
                '“Escuela Espacio de Paz”, cuyo plazo será del 15 de junio al 30 de septiembre de 2026».',
                '**Aprobación.** «Acta o certificado de la aprobación por parte del Claustro y del Consejo Escolar de la '
                'participación en cada uno de los Programas, con indicación de las líneas de trabajo, en los Programas '
                'que lo requieran».',
                '**Coordinación y profesorado.** «Persona que desempeñará la Coordinación de los diferentes Programas '
                'educativos» y «Profesorado participante», registrados en Séneca.',
                '**Sin límite de plazas.** «se entenderá que participan en dichos Programas educativos, dado que se trata '
                'de Programas sin convocatoria específica y, por tanto, sin límite de participación».',
                '**Cuáles.** Hábitos de Vida Saludable, Aldea, ConRed, ADA, Comunica, aulaDjaque, Programas Culturales, '
                'Vivir y Sentir el Patrimonio, Emprendimiento Educativo, STEM, Red Andaluza: “Escuela Espacio de Paz” y '
                'Fénix Andalucía. § Prácticum y PEBIF también son de tipo B, pero no sirven para la propuesta.']),
            ('C', '**STEM** (tipo B): «El programa STEM es un programa que pretende impulsar el desarrollo de competencias '
                  'científicas, tecnológicas, matemáticas y de ingeniería desde un enfoque interdisciplinar, igualitario, '
                  'creativo y práctico». Para quinto, sus recursos: RetoTech, «un proyecto tecnológico que resuelva una '
                  'necesidad real de su entorno» (5.º y 6.º); Astro Pi, «escribiendo programas informáticos que se '
                  'ejecutan en computadoras Raspberry Pi a bordo de la Estación Espacial Internacional»; Moon Camp, para '
                  '«diseñar y modelar en 3D»; Detectives Climáticos Kids (5-13 años) y Mission X. § Página del programa '
                  'STEM 2026/2027 de la Consejería.'),
            ('D', 'Tipo C, «participación sujeta a convocatoria específica»: «la participación de los centros educativos '
                  'en los siguientes Programas estará sujeta a lo dispuesto en la correspondiente convocatoria de cada uno '
                  'de ellos». § Solo si el enunciado dice que el centro ya participa.', [
                '**Red de Radios Escolares de Andalucía**, con convocatoria en el primer trimestre. § Siempre junto con '
                'Comunica.',
                '**Comunidades de Aprendizaje**, con convocatoria en el segundo trimestre: «dicho acta o certificado deberá '
                'incluir el número de miembros del Claustro, el número de asistentes, así como el número de votos '
                'favorables».',
                '**Investiga y Descubre**: el profesorado «deberá haber implementado el Proyecto del Programa durante al '
                'menos 32 horas».',
                '**Otros**: Red Andaluza de Ecoescuelas, Proyecto Aulas Verdes Abiertas, Red de Escuelas Promotoras de '
                'Salud de Andalucía, Programa Escolar de Consumo de Fruta, Hortalizas y Leche, Más Deporte, PROA Andalucía '
                'y Torneo de Debate.']),
            ('C', 'Para certificarlos: «Haber cumplimentado en Séneca el requisito de la participación y/o asistencia al '
                  'Programa, por un mínimo de 6 meses en los Programas que lo requieran».'),
        ]},
        5: {'titulo': 'Cohesión del grupo según el sociograma (después, sirve para formar los equipos)', 'ops': [
            ('1', 'El grupo está cohesionado y cuenta con líderes positivos.'),
            ('C', 'Se aprecian dos subgrupos que apenas se relacionan (supuestos de convivencia).'),
            ('C', 'Un alumno o una alumna apenas recibe elecciones.'),
            ('C', 'El clima es favorable, si bien con interrupciones en los debates.'),
            ('C', 'El alumnado de incorporación reciente aún no tiene vínculos en el grupo.'),
            ('D', 'Como en la programación: un grupo unido, con tres subgrupos que una alumna conecta entre sí y un '
                  'alumno poco elegido, en el que los líderes cambian según la pregunta.'),
            ('D', 'Las elecciones apenas se cruzan entre alumnos y alumnas (supuestos de igualdad).'),
        ]},
        6: {'titulo': 'Fortaleza o interés del grupo', 'ops': [
            ('1', 'Curiosidad e interés por el tema del supuesto.'),
            ('C', 'Buena expresión oral y ganas de participar en los debates.'),
            ('C', 'Gusto por el trabajo manipulativo y en equipo.'),
            ('C', 'Interés por la tecnología, los videojuegos y la programación.'),
            ('C', 'Sensibilidad ante los problemas ambientales y el cuidado de los animales.'),
            ('C', 'Gusto por la música, el baile y el flamenco.'),
            ('C', 'Espíritu solidario, que muestra en las campañas del centro.'),
            ('C', 'Creatividad plástica y gusto por el dibujo.'),
            ('D', 'Afición a las sagas, los cómics y los misterios, que se convierte en la narrativa de la propuesta.'),
        ]},
        91: {'titulo': 'Perfil: necesidad, fortaleza y fuente del dato (nunca la etiqueta sola)', 'ops': [
            ('1', 'Si el enunciado no impone diversidad, un perfil sencillo y bien conocido, como en la programación: un '
                  'alumno con trastorno por déficit de atención e hiperactividad (TDAH), con necesidades educativas '
                  'especiales, que necesita anticipación, tareas breves y movimiento pautado, y que destaca por su '
                  'creatividad, según su informe de evaluación psicopedagógica.'),
            ('C', 'Una alumna con hipoacusia bilateral moderada (necesidades educativas especiales), que necesita apoyos '
                  'visuales, consignas escritas y la lectura labial, y que destaca por su capacidad de observación. '
                  '§ Programación.'),
            ('C', 'Un alumno con capacidad intelectual límite (dificultades de aprendizaje), que necesita pasos cortos y '
                  'secuenciados, pictogramas y más tiempo, y que destaca por su constancia. § Programación.'),
            ('C', 'Una alumna con dificultad específica en la lectura (dislexia), que necesita textos breves, lectura '
                  'previa y evaluación oral, y que destaca por su comprensión oral.'),
            ('C', 'Un alumno con dificultad en el cálculo (discalculia), que necesita material manipulativo y una '
                  'plantilla de resolución, y que destaca por su razonamiento oral.'),
            ('C', 'Un alumno con trastorno del espectro autista, que necesita agenda visual, anticipación y un espacio '
                  'de calma, y que destaca por su rigor en las tareas que le interesan.'),
            ('C', 'Una alumna con altas capacidades intelectuales, que necesita retos de mayor complejidad y un programa '
                  'de profundización, y que destaca por su curiosidad.'),
            ('C', 'Un alumno de incorporación tardía con desconocimiento del español, que necesita apoyo visual y un '
                  'alumno tutor, y que aporta su lengua y su cultura al grupo.'),
            ('C', 'Una alumna con discapacidad motora, que necesita accesibilidad en los espacios y en las salidas y '
                  'herramientas como el dictado por voz, y que destaca por su liderazgo.'),
            ('C', 'Un alumno con baja visión, que necesita materiales ampliados, un puesto fijo y buena iluminación, y '
                  'que destaca por su escucha.'),
            ('C', 'Un alumno con disfemia, que necesita tiempo para expresarse y exponer primero en pequeño grupo, y que '
                  'destaca por la calidad de sus ideas.'),
            ('C', 'Alumnado en situación o riesgo de vulnerabilidad socioeducativa, que necesita los materiales en el '
                  'aula y tiempo de tarea en el centro. § Decreto 103/2026, de 17 de junio (manual).'),
            ('D', 'Sin necesidad específica de apoyo educativo, como en la programación: un alumno tímido, otro más '
                  'apartado del grupo y otro al que le cuesta autorregularse, que también aprovechan el DUA.'),
            ('D', 'El grupo en tres perfiles: «Según la evaluación inicial, el grupo presenta tres perfiles de desempeño '
                  'en [competencia]: [n.º] estudiantes con un dominio [nivel], [n.º] en proceso y [n.º] que requieren '
                  'apoyo, entre ellos [perfil]». § Rafa.'),
        ]},
    },
    # ------------------------------------------------------------------------------------------------ 7.3
    '7.3': {
        1: {'ops': [('1', 'Se concretarán con los temas: dos autores muy específicos del tema, de 2020 en adelante.')]},
        3: {'titulo': 'En lugar del artículo 10.2: los retos del siglo XXI (anexo I del Real Decreto 157/2022)', 'ops': [
            ('D', 'Se cambia la frase del 10.2 por esta: «…el Real Decreto 157/2022 vincula en su anexo I las competencias '
                  'clave con los principales retos y desafíos globales del siglo XXI, entre ellos [el reto, literal]». '
                  'Se elige el del supuesto:', [
                '**Medio ambiente y maltrato animal.** «Desarrollar una actitud responsable a partir de la toma de '
                'conciencia de la degradación del medioambiente y del maltrato animal basada en el conocimiento de las '
                'causas que los provocan, agravan o mejoran, desde una visión sistémica, tanto local como global».',
                '**Consumo responsable.** «Identificar los diferentes aspectos relacionados con el consumo responsable, '
                'valorando sus repercusiones sobre el bien individual y el común, juzgando críticamente las necesidades '
                'y los excesos y ejerciendo un control social frente a la vulneración de sus derechos».',
                '**Salud.** «Desarrollar estilos de vida saludable a partir de la comprensión del funcionamiento del '
                'organismo y la reflexión crítica sobre los factores internos y externos que inciden en ella, asumiendo '
                'la responsabilidad personal y social en el cuidado propio y en el cuidado de las demás personas, así '
                'como en la promoción de la salud pública».',
                '**Inclusión.** «Desarrollar un espíritu crítico, empático y proactivo para detectar situaciones de '
                'inequidad y exclusión a partir de la comprensión de las causas complejas que las originan».',
                '**Convivencia.** «Entender los conflictos como elementos connaturales a la vida en sociedad que deben '
                'resolverse de manera pacífica».',
                '**Digital.** «Analizar de manera crítica y aprovechar las oportunidades de todo tipo que ofrece la '
                'sociedad actual, en particular las de la cultura en la era digital, evaluando sus beneficios y riesgos '
                'y haciendo un uso ético y responsable que contribuya a la mejora de la calidad de vida personal y '
                'colectiva».',
                '**Creatividad.** «Aceptar la incertidumbre como una oportunidad para articular respuestas más '
                'creativas, aprendiendo a manejar la ansiedad que puede llevar aparejada».',
                '**Diversidad cultural.** «Cooperar y convivir en sociedades abiertas y cambiantes, valorando la '
                'diversidad personal y cultural como fuente de riqueza e interesándose por otras lenguas y culturas».',
                '**Comunidad.** «Sentirse parte de un proyecto colectivo, tanto en el ámbito local como en el global, '
                'desarrollando empatía y generosidad».',
                '**Aprender a aprender.** «Desarrollar las habilidades que le permitan seguir aprendiendo a lo largo de '
                'la vida, desde la confianza en el conocimiento como motor del desarrollo y la valoración crítica de los '
                'riesgos y beneficios de este último».',
            ]),
        ]},
        4: {'titulo': 'Instrucción del área: cuál se cita y qué se toma de ella', 'ops': [
            ('1', '**Si es de Lengua o de cualquier área con lectura.** Instrucciones de 21 de junio de 2023, de la '
                  'Viceconsejería de Desarrollo Educativo y Formación Profesional, sobre el tratamiento de la lectura '
                  'para el despliegue de la competencia en comunicación lingüística en Educación Primaria y Educación '
                  'Secundaria Obligatoria. Qué se toma, literal, según la necesidad:', [
                '**El tiempo diario.** Los centros «deberán garantizar la incorporación de un tiempo diario de lectura '
                'planificada no inferior a 30 minutos para trabajar la comprensión (literal, inferencial y crítica) y la '
                'fluidez lectora en todos los cursos de la etapa». § Se traduce en: las lecturas de la secuencia ocupan '
                'esos treinta minutos, con preguntas de los tres niveles.',
                '**Los tres momentos.** «La organización del tiempo de la lectura planificada deberá incluir tres '
                'momentos de desarrollo: antes, durante y después». § Se traduce en: cada texto de la secuencia se '
                'trabaja en los tres momentos.',
                '**Antes.** «Las actividades de prelectura deberán estar diseñadas para motivar el interés y para activar '
                'el mundo de referencias y conocimientos que previamente posee el alumnado». § Por ejemplo, «Veo, pienso, '
                'me pregunto» con la portada o el titular e hipótesis sobre el contenido.',
                '**Durante.** «Las actividades durante la lectura ayudan a establecer inferencias de distinto tipo, a la '
                'revisión y comprobación de lo que se ha leído, a la toma de conciencia sobre la entonación empleada, a '
                'una relectura formativa en distintas dimensiones textuales y a un proceso de autoaprendizaje». § Por '
                'ejemplo, lectura en voz alta por turnos, subrayado de palabras clave y preguntas de inferencia.',
                '**Después.** «Las actividades tras la prelectura y la lectura deben dirigirse a la recapitulación, '
                'puesta en práctica de lo leído, el debate de ideas, el uso del conocimiento adquirido en distintos '
                'contextos de aprendizaje». § Por ejemplo, un organizador gráfico, una tertulia y una evidencia para el '
                'portafolio de lecturas.',
                '**El carácter social de la lectura.** Las actividades «aprovecharán el carácter social de la lectura '
                'para promover la figura del mediador de lecturas, el intercambio de experiencias, tertulias, clubes, '
                'debates dirigidos, así como la presentación oral y escrita de trabajos personales del alumnado o de '
                'grupo». § Para supuestos de oralidad, tertulias o lectura entre iguales.',
                '**Los cinco ejes.** «1ª. Conciencia fonológica. 2ª. Conocimiento alfabético. 3ª. Fluidez. 4ª. '
                'Vocabulario: ampliación y organización. 5ª. Comprensión». § En quinto pesan la fluidez, el vocabulario '
                'y la comprensión.',
                '**Por qué leer.** «La lectura constituye una actividad clave en la educación y en el aprendizaje '
                'permanente de los individuos ya que supone uno de los principales instrumentos de aprendizaje…». '
                '§ Preámbulo; para justificar que la lectura vertebra la propuesta, también fuera de Lengua.',
            ]),
            ('1', '**Si es de Matemáticas.** Instrucciones de 18 de junio de 2024, de la Viceconsejería de Desarrollo '
                  'Educativo y Formación Profesional, sobre las medidas para el fomento del razonamiento matemático a '
                  'través del planteamiento y la resolución de retos y problemas en Educación Infantil, Educación Primaria '
                  'y Educación Secundaria Obligatoria. Qué se toma, literal, con su apartado:', [
                '**El tiempo semanal (quinta, 5).** «cada semana se establecerá un tiempo definido en el horario. El '
                'mismo, en aplicación de los principios pedagógicos regulados en los Decretos por los que se establecen '
                'la ordenación y el currículo de ambas etapas, deberá distribuirse en tres días distintos con una duración '
                'de, al menos, 30 minutos cada uno». § Se traduce en: tres sesiones semanales de retos.',
                '**El método común (tercera, e).** «La resolución de situaciones problemáticas deberá contar con un método '
                'común, acordado en el centro, con las estrategias adecuadas según las características de la etapa y la '
                'edad del alumnado, sin perjuicio de estimular en el alumnado la búsqueda de estrategias propias de '
                'resolución de problemas».',
                '**El itinerario (tercera, d).** «Los centros deberán diseñar para cada etapa educativa un itinerario de '
                'problemas organizados, de manera que se avance en creciente grado de dificultad y exigencia».',
                '**Las otras áreas (tercera, a).** «Las actividades para el desarrollo de la competencia matemática, '
                'deberán tener un carácter eminentemente instrumental y vinculado a otras áreas del conocimiento, como '
                'las ciencias naturales, las ciencias sociales, el arte, la música, o la tecnología».',
                '**La lectura de enunciados (cuarta, b).** «es imprescindible dedicar el tiempo que sea necesario para '
                'leer adecuadamente los enunciados con un ritmo y una entonación facilitadora, aclarando conceptos, nuevos '
                'léxicos, utilizando sinónimos, fragmentando las partes del enunciado, diferenciando las preguntas del '
                'mismo y sustituyéndolas por otras si fuera necesario…».',
                '**Los textos matemáticos (cuarta, c).** «es conveniente trabajar textos matemáticos de distinta '
                'naturaleza (tablas de datos y gráficas, etiquetas, tickets de compras, presupuestos, facturas, recetas de '
                'cocina, croquis, mapas y escalas, cronogramas, líneas históricas de tiempo, otros textos discontinuos, '
                'etc.)».',
                '**El cálculo mental (cuarta, f).** «El objetivo del cálculo mental radica en la necesidad de automatizar '
                'operaciones aritméticas con la intención de liberar recursos cognitivos necesarios para destinarlos a la '
                'comprensión y al adecuado planteamiento de problemas, retos o tareas más complejas», y puede integrarse '
                '«asignando un tiempo fijo, al menos dos o tres veces por semana a modo de rutina».',
                '**La evaluación (tercera, k).** «debe valorarse el progreso del alumnado en la búsqueda de soluciones, en '
                'el desarrollo de estrategias de razonamiento, es decir en los procesos seguidos, y no solo en los '
                'resultados».',
            ]),
            ('1', '**Los siete pasos heurísticos de educación primaria (cuarta, 4.4)**, literales:', [
                '«1º. Planteamiento de una situación problemática cercana o conocida que requiera el uso de las '
                'Matemáticas. Diálogo sobre la misma, aportación de informaciones complementarias. Relación con otras '
                'situaciones conocidas, ya resueltas o en proceso de resolución».',
                '«2º. La comprensión de la situación es siempre el primer paso hacia su resolución. La representación o '
                'visualización del problema ayuda a su interpretación, así como a la identificación y organización de los '
                'datos y el establecimiento de relaciones entre ellos. […] Identificación de las preguntas a resolver así '
                'como su intención para llegar a una comprensión de las mismas».',
                '«3º. Identificación de estrategias para resolver el problema y para el desarrollo del razonamiento. El '
                'uso de diferentes estrategias permite descubrir una diversidad de opciones para obtener posibles '
                'soluciones: analogía, ensayo-error, resolución inversa, tanteo, descomposición en pasos o problemas más '
                'sencillos. […] Toma de decisiones sobre las operaciones necesarias y el orden de las mismas para la '
                'resolución del problema».',
                '«4º. Aplicación de estrategias y ejecución de los cálculos y operaciones. Búsqueda de las posibles '
                'conexiones entre la información y las operaciones necesarias para la resolución».',
                '«5º. Es de gran importancia la adecuada y sistemática utilización de diferentes colores […] si las '
                'unidades se colorean en azul, las decenas en rojo, las centenas en verde y las unidades de millar en '
                'negro, siempre se deberá utilizar esos mismos colores a lo largo de toda la etapa […] Igualmente será de '
                'utilidad metodológica el uso de distintos colores para subrayar los datos de los enunciados, las palabras '
                'claves que determinen las operaciones a realizar y la estrategia a seguir, así como la pregunta o '
                'preguntas a resolver».',
                '«6º. Resolución: comprobar la corrección matemática de la solución y la validez de los resultados '
                'obtenidos. La representación puede contribuir a valorar la coherencia y sentido de los resultados».',
                '«7º. Reflexión conjunta sobre el proceso seguido. Comunicación oral y/o escrita de dicho proceso y del '
                'resultado obtenido». § Se traduce en: un mural de los siete pasos y una sesión de retos con rutina fija.',
            ]),
            ('C', '**Si es de biblioteca.** Instrucciones de 10 de septiembre de 2025, sobre la organización y '
                  'funcionamiento de las bibliotecas escolares, como las cita el BOJA n.º 57, de 24 de marzo de 2026: la '
                  'biblioteca como recurso para la mediación lectora, la alfabetización mediática e informacional y la '
                  'inclusión. Como en la programación, con el programa Bibliotecas Escolares y el Plan de Fomento de la '
                  'Lectura 2026-2030, que propone leer mejor, y no solo más, contando con las familias (Ministerio de '
                  'Cultura, 2026).'),
        ]},
    },
    # ------------------------------------------------------------------------------------------------ 7.5
    '7.5': {
        93: {'titulo': 'Necesidad detectada (con un dato del centro)', 'ops': [
            ('1', 'La que justifica la línea o el objetivo del contexto:', [
                'las dificultades del alumnado para comprender los enunciados de los problemas',
                'el escaso hábito lector fuera del aula', 'la pobreza de la expresión escrita y las faltas de ortografía',
                'el aumento de los conflictos en el recreo', 'el excesivo gasto de agua y de papel en el centro',
                'los residuos que genera el recreo', 'el desconocimiento del patrimonio y de la historia del pueblo',
                'el uso poco crítico de las pantallas y de las redes',
                'los desayunos poco saludables', 'la escasa participación de las familias']),
        ]},
        2: {'titulo': 'Acuerdo del equipo técnico de coordinación pedagógica', 'ops': [
            ('1', 'acordó trabajar en todo el centro [centro de interés] en torno a [efeméride], y cada ciclo lo adapta a '
                  'su alumnado. § Tu libreta: el ahorro de agua, en torno al Día del Medio Ambiente.'),
            ('C', 'acordó incorporar un itinerario común de lectura (supuestos de lengua) o de resolución de problemas, '
                  'con un modelo común de pasos (supuestos de matemáticas).'),
            ('C', 'acordó organizar una semana temática del centro (de la ciencia, del libro o de Andalucía), con '
                  'talleres rotatorios por ciclos.'),
            ('C', 'acordó celebrar la efeméride con todo el centro, con una aportación de cada ciclo a un producto común, '
                  'como un mural, una exposición o un programa de radio.'),
            ('D', 'En sentido descendente, ciclo a ciclo: en educación infantil aprenden a cerrar el grifo con un cuento '
                  'y una canción; en el primer ciclo forman la patrulla del agua que revisa los grifos del patio; en el '
                  'segundo registran el agua que se gasta en los aseos; y en el tercero, el nuestro, diseñamos una '
                  'campaña de ahorro para las familias. § Tu libreta definitiva.'),
        ]},
        3: {'titulo': 'Lo que concreta el equipo de ciclo', 'ops': [
            ('1', 'el producto final común, el reparto de sesiones entre áreas y una rúbrica compartida.'),
            ('C', 'la misma situación en las dos líneas del curso, de modo que ambos grupos presentan juntos el producto '
                  'en la sala de usos múltiples.'),
            ('C', 'un calendario común de sesiones y una lista de cotejo compartida para el producto.'),
            ('D', 'una coordinación horizontal, con el equipo docente del nivel, y vertical, con el equipo técnico y el '
                  'tránsito entre ciclos. § Rafa.'),
        ]},
        4: {'titulo': 'Reunión con el equipo de orientación: medidas, especialistas y seguimiento', 'ops': [
            ('1', 'revisar si las medidas del DUA de la situación anterior funcionaron con [perfil] y ajustar las de '
                  'esta, como la agenda visual de cada sesión y los roles cooperativos. § Tu libreta definitiva.'),
            ('C', 'Las medidas, según el perfil del contexto:', [
                '**TDAH.** ubicación cerca de la docente, agenda visual, tiempos explícitos con el rol de cronometrador, '
                'pausas activas y medidor emocional. § Programación.',
                '**Hipoacusia.** primera fila y de frente, consignas escritas, subtítulos y apoyos visuales, con el '
                'sistema de frecuencia modulada en sus audífonos. § Programación.',
                '**Capacidad intelectual límite.** pictogramas, pasos secuenciados, tutoría entre iguales y más tiempo. '
                '§ Programación.',
                '**Dislexia.** textos breves o adaptados, tipografía clara, lectura previa y evaluación oral.',
                '**Discalculia.** material manipulativo, plantilla de resolución, colores por órdenes de unidades y '
                'calculadora en las tareas de razonamiento.',
                '**Trastorno del espectro autista.** agenda visual, espacio de calma, compañero de referencia y '
                'anticipación de los cambios.',
                '**Altas capacidades.** tareas de investigación de mayor complejidad, elección de retos y papel de '
                'alumna ayudante.',
                '**Incorporación tardía.** apoyo visual, alumno tutor y diccionario multilingüe.',
            ]),
            ('C', 'Cuándo entran los especialistas:', [
                'Pedagogía Terapéutica, en las sesiones de cálculo o de resolución de problemas',
                'Audición y Lenguaje, en el ensayo de la exposición oral o en la grabación',
                'los dos, en las sesiones de mayor carga lectora']),
            ('C', 'El seguimiento, con indicadores observables:', [
                'quincenal, en la reunión del equipo docente', 'termina la tarea en el tiempo previsto',
                'participa con el rol asignado', 'pide ayuda cuando la necesita']),
            ('D', 'El alumno con programa de refuerzo del aprendizaje lo trabaja dentro de la propia situación, y su '
                  'familia recibe información de su evolución al menos tres veces a lo largo del curso. § Tu libreta '
                  'definitiva.'),
        ]},
        5: {'titulo': 'Espacios del centro y del entorno (según el cuadrante del reglamento de organización y '
                      'funcionamiento)', 'ops': [
            ('1', 'La biblioteca escolar, con un lote de libros del tema que prepara su responsable, los viernes, como en '
                  'la programación.'),
            ('C', 'Del centro:', ['sala de usos múltiples o salón de actos, para presentar el producto',
                                  'huerto escolar, para medir, plantar y registrar',
                                  'patio, para la orientación, la yincana o el dictado a la carrera',
                                  'radio escolar, para difundir el producto',
                                  'carro de portátiles, que reserva la coordinación del Plan de Actuación Digital',
                                  'gimnasio o pista, para dramatizaciones y bailes',
                                  'pasillos y vestíbulo, para exposiciones y murales',
                                  'comedor, para retos de consumo y alimentación',
                                  'estación meteorológica escolar, si la hay']),
            ('C', 'Del entorno, los citados en el contexto:', ['biblioteca municipal', 'plaza de abastos',
                                                               'parque, sendero o vía verde', 'residencia de mayores',
                                                               'casa de la cultura o museo local', 'ayuntamiento']),
            ('D', 'Espacios virtuales: el aula virtual autorizada por la Consejería y el blog del centro.'),
        ]},
        7: {'titulo': 'Uso 1 de los criterios pedagógicos: la actividad complementaria (la planificación del tiempo '
                      'escolar y extraescolar)', 'ops': [
            ('1', 'Visita a la biblioteca municipal, con autorización de las familias por iPasen, que el equipo de ciclo '
                  'incluye en la programación didáctica.'),
            ('C', 'Salidas según el tema:', [
                '**Ciencias y medio ambiente.** depuradora de la comarca, punto limpio, espacio natural o vía verde con '
                'un guía, granja escuela u observatorio astronómico',
                '**Patrimonio e historia.** ruta guiada por el patrimonio del pueblo, museo arqueológico o centro de '
                'interpretación, archivo municipal o castillo de la comarca',
                '**Lectura.** biblioteca municipal, con un encuentro con un autor o una autora, librería del pueblo o '
                'radio local, para grabar un programa',
                '**Matemáticas y consumo.** plaza de abastos o supermercado con un presupuesto cerrado, o una empresa '
                'local',
                '**Salud.** centro de salud, mercado para comprar los ingredientes de un menú saludable o ruta a pie',
                '**Convivencia y servicio.** residencia de mayores, entidad que lanza el reto o ayuntamiento, para '
                'entregar una propuesta',
                '**Artística.** teatro o auditorio municipal, exposición en la casa de la cultura o peña flamenca',
            ]),
            ('C', 'La visita al aula de personas expertas del entorno, como una abuela, una madre bombera, un agricultor, '
                  'Protección Civil o Cruz Roja.'),
            ('D', 'Organizada según el reglamento de organización y funcionamiento: autorización de las familias por '
                  'iPasen, una persona acompañante por cada [n.º] estudiantes y transporte adaptado con el apoyo del '
                  'profesional técnico de integración social si hay alumnado con discapacidad motora. § Tu libreta '
                  'definitiva.'),
            ('D', 'En el propio centro: la celebración de la efeméride con todo el centro, una semana cultural o un recreo '
                  'inclusivo y activo en el que el grupo atiende un punto informativo.'),
        ]},
        8: {'titulo': 'Uso 2 de los criterios pedagógicos: el recurso digital común', 'ops': [
            ('1', 'Google Classroom y Drive, con licencia de la Consejería, para alojar y compartir los trabajos, como en '
                  'la programación.'),
            ('C', 'Moodle Centros, el aula virtual autorizada por la Consejería.'),
            ('C', 'iPasen, para la comunicación con las familias y las autorizaciones.'),
            ('C', 'Una herramienta común de creación, según el producto:', [
                'Canva, para carteles e infografías', 'Book Creator, para un libro digital',
                'Genially, para presentaciones interactivas o un breakout', 'Padlet, como muro colaborativo',
                'Scratch o micro:bit, para programar', 'Audacity, para el pódcast']),
            ('D', 'MyClassGame, que no exige registrar al alumnado, como plataforma común de la gamificación, con '
                  'avatares y puntos que no cuentan en la nota. § Programación.'),
            ('D', 'La radio escolar o el blog del centro, como canal común para difundir los productos.'),
        ]},
        9: {'titulo': 'Uso 3 de los criterios pedagógicos: la cultura andaluza', 'ops': [
            ('1', 'El Día de Andalucía (28 de febrero), con una aportación de cada ciclo.'),
            ('C', 'Efemérides andaluzas:', ['Día del Flamenco (16 de noviembre)',
                                            'Día de la Bandera Andaluza (4 de diciembre)',
                                            'Día de la Lectura en Andalucía (16 de diciembre)',
                                            'Día de la Empresa Andaluza (28 de octubre)']),
            ('C', 'Patrimonio y tradición:', ['el patrimonio y las leyendas del pueblo',
                                              'los oficios tradicionales, como las recoveras o los tejeros',
                                              'la gastronomía andaluza y lo que trajo al-Ándalus a la cocina',
                                              'refranes, coplas y romances', 'el cante, el baile y el traje de flamenca']),
            ('C', 'Lengua y literatura:', ['la modalidad lingüística andaluza, con palabras y expresiones del pueblo',
                                           'poetas andaluces, como Machado, Lorca o Juan Ramón Jiménez',
                                           'leyendas de Sevilla, de Al-Mutamid a Bécquer']),
            ('C', 'Arte y ciencia:', ['pintores andaluces, como Velázquez o Murillo',
                                      'las simetrías y los teselados de la Alhambra',
                                      'mujeres andaluzas referentes en la ciencia y en el arte']),
            ('D', 'Las instituciones de Andalucía, como la Junta, el Parlamento o el plan INFOCA contra los incendios '
                  'forestales. § Programación, UDP 4.'),
        ]},
        10: {'titulo': 'Cauce para informar a las familias', 'ops': [
            ('1', 'una reunión informativa al inicio, en la que se presenta el reto, e iPasen y la tutoría de tarde para '
                  'informar de los avances.'),
            ('C', 'la tutoría electrónica e iPasen, con una nota breve al cerrar cada fase.'),
            ('C', 'la persona delegada de madres y padres, que traslada la información al grupo de familias.'),
        ]},
        94: {'titulo': 'En qué participan las familias', 'ops': [
            ('1', 'la difusión del producto final.'),
            ('C', 'Otras formas de participar:', [
                'visitan el aula como personas expertas, como una madre que trabaja en la empresa municipal de aguas',
                'la persona delegada de madres y padres ayuda a difundir la campaña',
                'la asociación de madres y padres financia la impresión de los carteles',
                'acompañan al grupo en la salida',
                'cocinan una receta saludable o presentan sus juegos en el aula',
                'aportan objetos y fotografías antiguas para un museo de aula',
                'responden a un cuestionario breve sobre la propuesta']),
            ('D', 'Una tarea compartida en casa, como registrar durante una semana el consumo de agua o el tiempo de '
                  'pantallas.'),
        ]},
        95: {'titulo': 'Con quién se colabora en el entorno, y para qué', 'ops': [
            ('1', 'la concejalía del ayuntamiento relacionada con el tema, que lanza el reto con una carta al inicio y '
                  'recibe el producto al final. § Tu libreta definitiva.'),
            ('C', 'Otras colaboraciones:', [
                'la biblioteca municipal, que presta un lote de libros y acoge la presentación',
                'la residencia de mayores, que recibe el servicio',
                'una asociación vecinal o cultural, que comparte sus testimonios',
                'Cruz Roja, Protección Civil o el centro de salud, que aportan una persona experta',
                'la radio local, que difunde el producto']),
            ('D', 'El Consejo Local de Infancia y Adolescencia, que eleva la propuesta del grupo al ayuntamiento.'),
        ]},
        11: {'titulo': 'Grabaciones o imágenes que se difunden', 'ops': [
            ('1', 'un vídeo grabado por el alumnado. Grabar con fines educativos no requiere consentimiento si solo se '
                  'comparte con el grupo y sus familias en la plataforma del centro; difundirlo en la web o en las redes '
                  'exige la autorización de las familias. § Guía del Consejo de Transparencia y Protección de Datos de '
                  'Andalucía (2024), como en tu libreta.'),
            ('C', 'Quien no tenga autorización no queda fuera: participa como cámara, con voz en off o con un avatar, o '
                  'su imagen se difumina en la versión pública.'),
            ('C', 'Se graba con las tabletas del centro, nunca con móviles personales ni por aplicaciones de mensajería.'),
            ('C', 'Otros productos que lo requieren: un pódcast con voces del alumnado, fotografías de la exposición o el '
                  'blog de la clase.'),
        ]},
        12: {'titulo': 'Aportación de los especialistas de área', 'ops': [
            ('1', 'con la especialista de Música, que compone con el grupo la canción de la campaña.'),
            ('C', 'Otras aportaciones:', ['Educación Física organiza una ruta a pie o una yincana de orientación',
                                          'Inglés traduce con el alumnado los eslóganes o el folleto',
                                          'Francés prepara un saludo para el vídeo',
                                          'Religión o Atención Educativa trabaja los valores del proyecto',
                                          'la persona responsable de la biblioteca prepara el lote de libros',
                                          'la coordinación del Plan de Actuación Digital reserva los portátiles']),
        ]},
        13: {'titulo': 'Lo que marca el proyecto educativo', 'ops': [
            ('1', '**Si es de Lengua.** los treinta minutos diarios de lectura se dedican a textos del tema (noticias, '
                  'infografías, cartas), con antes, durante y después.'),
            ('1', '**Si es de Matemáticas.** los problemas se resuelven con el modelo común de siete pasos del centro, con '
                  'un mural en el aula.'),
            ('C', 'el plan de orientación y acción tutorial aporta una sesión sobre el tema, como el consumo responsable, '
                  'las emociones o la convivencia digital.'),
            ('C', 'el plan de convivencia aporta las normas consensuadas y la mediación entre iguales.'),
            ('C', 'el plan de igualdad aporta referentes femeninos y un lenguaje no sexista.'),
        ]},
        14: {'titulo': 'Servicio complementario al que llega la propuesta', 'ops': [
            ('1', 'el comedor, donde el alumnado de quinto actúa como inspector del agua y mide con una jarra graduada la '
                  'que sobra en las mesas, datos que después se usan en Matemáticas. § Tu libreta definitiva.'),
            ('C', 'el aula matinal, donde se proyectan los vídeos de la campaña y se juega al juego de mesa que ha creado '
                  'el grupo.'),
            ('C', 'el comedor, para medir las sobras de comida y calcular el desperdicio. § Como en la UDP 5.'),
            ('C', 'la actividad extraescolar de robótica, donde se programa un sensor de humedad para el riego del '
                  'huerto.'),
            ('D', 'el comedor, si el centro de interés es la alimentación: el alumnado diseña con la empresa del comedor '
                  'un menú saludable de temporada.'),
        ]},
    },
    # ------------------------------------------------------------------------------------------------ 7.6
    '7.6': {
        91: {'titulo': 'Número de sesiones', 'ops': [
            ('1', '12 sesiones en 3 o 4 semanas, lo más habitual.'),
            ('C', 'Entre 8 y 15 sesiones, según el producto.'),
            ('C', '14 sesiones de 60 minutos distribuidas en tres semanas. § Tu libreta definitiva.'),
        ]},
        1: {'titulo': 'Efeméride (instrucción de efemérides del curso 2026-2027; los nombres, tal cual)', 'ops': [
            ('1', 'Las más útiles, según el tema:', [
                '**Patrimonio.** Día de Andalucía (28 de febrero)',
                '**Convivencia.** Día Escolar de la No-violencia y la Paz (30 de enero)',
                '**Lectura.** Día Internacional del Libro (23 de abril)',
                '**Sostenibilidad.** Día del Medio Ambiente (5 de junio)']),
            ('C', 'Primer trimestre:', [
                'Día Mundial de la Salud Mental (10 de octubre)', 'Día de la Hispanidad (12 de octubre)',
                'Día de la Empresa Andaluza (28 de octubre)', 'Día del Flamenco (16 de noviembre)',
                'Día Mundial de la Infancia (20 de noviembre)', 'Día Internacional de la Música (22 de noviembre)',
                'Día Internacional de la Eliminación de la Violencia contra la Mujer (25 de noviembre)',
                'Día de la Bandera Andaluza (4 de diciembre)', 'Día de la Constitución Española (6 de diciembre)',
                'Día de la Lectura en Andalucía (16 de diciembre)']),
            ('C', 'Segundo trimestre:', [
                'Día Escolar de la No-violencia y la Paz (30 de enero)',
                'Día Internacional de la Mujer y la Niña en la Ciencia (11 de febrero)',
                'Día de Andalucía (28 de febrero)', 'Día Internacional de la Mujer (8 de marzo)']),
            ('C', 'Tercer trimestre:', [
                'Día Mundial de la Salud (7 de abril)', 'Día Internacional del Libro (23 de abril)',
                'Día Internacional contra el Acoso y el Ciberacoso (2 de mayo)', 'Día de Europa (9 de mayo)',
                'Día Internacional de las Familias (15 de mayo)', 'Día del Medio Ambiente (5 de junio)',
                'Día de la Memoria Histórica y Democrática (14 de junio)']),
            ('D', 'Una fecha internacional que no está en la instrucción, citada como tal y no como efeméride del centro: '
                  'el Día Internacional del Juego (11 de junio), de Naciones Unidas. § Rafa.'),
        ]},
        2: {'titulo': 'Objetivo de Desarrollo Sostenible (número y nombre)', 'ops': [
            ('1', 'El del tema:', ['**Salud.** 3 Salud y bienestar', '**Igualdad.** 5 Igualdad de género',
                                   '**Agua.** 6 Agua limpia y saneamiento',
                                   '**Pueblo y patrimonio.** 11 Ciudades y comunidades sostenibles',
                                   '**Consumo.** 12 Producción y consumo responsables', '**Clima.** 13 Acción por el clima',
                                   '**Convivencia.** 16 Paz, justicia e instituciones sólidas']),
            ('C', 'Otros:', ['1 Fin de la pobreza', '2 Hambre cero', '7 Energía asequible y no contaminante',
                             '10 Reducción de las desigualdades', '14 Vida submarina', '15 Vida de ecosistemas terrestres',
                             '17 Alianzas para lograr los objetivos, si colabora una entidad del entorno']),
            ('C', '4 Educación de calidad, que encaja con cualquier propuesta educativa.'),
            ('D', 'Junto al ODS, un reto del siglo XXI del anexo I del Real Decreto 157/2022, literal (están en el 7.3). '
                  '§ Tu libreta definitiva.'),
        ]},
    },
    # ------------------------------------------------------------------------------------------------ 7.7
    '7.7': {
        1: {'titulo': 'Objetivo de la etapa (artículo 5 del Decreto 101/2023, literal)', 'ops': [
            ('1', 'El del área eje:', [
                '**Lengua.** e) «Conocer y utilizar de manera apropiada la lengua castellana y desarrollar hábitos de '
                'lectura».',
                '**Matemáticas.** g) «Desarrollar las competencias matemáticas básicas e iniciarse en la resolución de '
                'problemas que requieran la realización de operaciones elementales de cálculo, conocimientos geométricos '
                'y estimaciones, así como ser capaces de aplicarlos a las situaciones de su vida cotidiana».',
                '**Conocimiento del Medio.** h) «Conocer los aspectos fundamentales de las Ciencias de la Naturaleza, '
                'las Ciencias Sociales, la Geografía, la Historia y la Cultura, así como reconocer, valorar y proteger la '
                'riqueza patrimonial, paisajística, social, medioambiental, histórica y cultural de su Comunidad».',
                '**Educación Artística.** j) «Utilizar diferentes representaciones y expresiones artísticas, e iniciarse '
                'en la construcción de propuestas visuales y audiovisuales».',
            ]),
            ('D', 'Los dos propios de Andalucía, para el patrimonio, el flamenco o la oralidad:', [
                'ñ) «Conocer y apreciar la peculiaridad lingüística andaluza en todas sus variedades».',
                'o) «Conocer y respetar el patrimonio cultural de Andalucía, partiendo del conocimiento y de la '
                'comprensión de nuestra cultura, reconociendo a Andalucía como comunidad de encuentro de culturas».']),
            ('C', 'Para cualquier propuesta: b) «Desarrollar hábitos de trabajo individual y de equipo, de esfuerzo y de '
                  'responsabilidad en el estudio, así como actitudes de confianza en sí mismo, iniciativa personal, '
                  'sentido crítico, curiosidad, interés y creatividad en el aprendizaje y espíritu emprendedor».'),
            ('C', 'Según el tema, el resto, también literal:', [
                '**Convivencia.** a) «Conocer y apreciar los valores y las normas de convivencia, aprender a obrar de '
                'acuerdo con ellas de forma empática, prepararse para el ejercicio activo de la ciudadanía y respetar '
                'los derechos humanos, así como el pluralismo propio de una sociedad democrática».',
                '**Conflictos.** c) «Adquirir habilidades para la resolución pacífica de conflictos y la prevención de la '
                'violencia, que le permitan desenvolverse con autonomía en el ámbito escolar y familiar, así como en los '
                'grupos sociales con los que se relaciona».',
                '**Igualdad e interculturalidad.** d) «Conocer, comprender y respetar las diferentes culturas, así como '
                'las diferencias entre las personas, la igualdad de derechos y oportunidades de hombres y mujeres y la '
                'no discriminación de personas por motivos de etnia, orientación o identidad sexual, religión o '
                'creencias, discapacidad u otras condiciones, así como reconocer la interculturalidad existente en '
                'Andalucía».',
                '**Tecnología.** i) «Desarrollar las competencias tecnológicas básicas e iniciarse en su utilización, '
                'desarrollando un espíritu crítico ante su funcionamiento y los mensajes que recibe y elabora».',
                '**Salud.** k) «Valorar la higiene y la salud, aceptar el propio cuerpo y el de las demás personas, '
                'respetar las diferencias propias y ajenas y utilizar la educación física, el deporte y la alimentación '
                'como medios para favorecer el desarrollo personal y social».',
                '**Animales.** l) «Conocer y valorar los animales más próximos al ser humano y adoptar modos de '
                'comportamiento que favorezcan la empatía y su cuidado».',
                '**Emociones.** m) «Desarrollar capacidades afectivas en todos los ámbitos de su personalidad y en sus '
                'relaciones con las demás personas, así como una actitud contraria a la violencia, a los prejuicios de '
                'cualquier tipo y a los estereotipos sexistas».',
                '**Educación vial.** n) «Desarrollar hábitos cotidianos de movilidad activa, autónoma y saludable, '
                'fomentando la educación vial y actitudes de respeto que incidan en la prevención de los accidentes de '
                'tráfico».',
            ]),
        ]},
        3: {'titulo': 'Competencia específica del área eje', 'ops': [
            ('1', 'La del área eje en la tabla de elementos de abajo, con su criterio de quinto, su saber y sus dos '
                  'descriptores.')]},
        4: {'titulo': 'Segunda área (solo la competencia específica, resumida en una línea)', 'ops': [
            ('1', 'Lengua o Matemáticas, que casi siempre están: «Asimismo, desde Lengua Castellana y Literatura se '
                  'desarrolla la competencia específica 5, que persigue producir textos escritos y multimodales '
                  'coherentes».'),
            ('C', 'Matemáticas: «…desde Matemáticas se desarrolla la competencia específica 2, que persigue resolver '
                  'situaciones problematizadas con distintas estrategias y comprobar las soluciones».'),
            ('C', 'Conocimiento del Medio: «…desde Conocimiento del Medio Natural, Social y Cultural se desarrolla la '
                  'competencia específica 6, que persigue identificar las causas y consecuencias de la intervención '
                  'humana para actuar de forma sostenible».'),
            ('C', 'Educación Artística, si el producto es artístico: «…desde Educación Artística se desarrolla la '
                  'competencia específica 3, que persigue expresar ideas y emociones con el sonido, la imagen, el cuerpo '
                  'y los medios digitales».'),
            ('D', 'Matemáticas 8, la socioafectiva, para supuestos de emociones o de trabajo en equipo: «…la competencia '
                  'específica 8, que persigue desarrollar destrezas sociales participando en equipos heterogéneos». '
                  '§ Tu tabla de elementos.'),
        ]},
    },
    # ------------------------------------------------------------------------------------------------ 7.8
    '7.8': {
        1: {'titulo': 'Ejemplo de DUA: cómo se lleva a la propuesta',
            'norma': [('e) «Se potenciará el Diseño Universal para el Aprendizaje (DUA) con objeto de garantizar una '
                       'efectiva educación inclusiva, permitiendo el acceso al currículo a todo el alumnado. Para ello, en '
                       'la práctica docente se desarrollarán dinámicas de trabajo que ayuden a descubrir el talento y el '
                       'potencial del mismo, y se integrarán diferentes formas de presentación del currículo, '
                       'metodologías variadas y recursos que respondan a los distintos estilos y ritmos de aprendizaje '
                       'del alumnado».', D101)],
            'ops': [
            ('1', 'Los tres elementos fijos para todo el grupo, como en la programación: el KPSI o el Q-sort al comenzar, '
                  'la base de orientación del producto durante la situación (herramienta de evaluación y de DUA, para '
                  'saber desde el principio qué se espera y cómo regularse) y una minientrevista a cada equipo antes '
                  'del producto final.'),
            ('C', 'Compromiso:', [
                'actividades multinivel: un mismo reto con tres niveles de dificultad que suman puntos, y cada estudiante '
                'elige cómo llegar al mínimo',
                'elegir entre retos, roles, compañero o formato del producto, con un menú de tareas',
                'un problema real del pueblo y un destinatario real del producto § Consideración 7.2 del DUA 3.0.',
                'equipos heterogéneos con roles rotativos y tutoría entre iguales § Consideración 8.3.',
                'metas visibles en el tablón y misiones secundarias de ampliación',
                'el medidor emocional y el metamomento antes de empezar a trabajar',
                'fomentar la alegría y el juego § Consideración 7.3, nueva en el DUA 3.0.']),
            ('C', 'Representación:', [
                'la misma información en texto, imagen, audio y vídeo subtitulado',
                'clarificar el vocabulario antes de leer, con un glosario visual o un mapa mental a cuatro bandas',
                'consignas con pictogramas de ARASAAC y textos en lectura fácil § Consideración 2.2.',
                'activar los conocimientos previos con un objeto sorpresa o la tabla «¿Qué sé? ¿Qué quiero saber? ¿Qué '
                'he aprendido?» § Consideración 3.1.',
                'material manipulativo para apoyar la notación matemática, como regletas o bloques multibase',
                'modelos del producto terminado a la vista y criterios de éxito visibles',
                'el tamaño del texto, el contraste, la velocidad del audio y los subtítulos, ajustables']),
            ('C', 'Acción y expresión:', [
                'elegir cómo presentar el producto: exposición, póster, vídeo, cómic, maqueta o pódcast '
                '§ Consideración 5.1.',
                'respuestas orales, escritas o dibujadas en las tareas diarias',
                'planificar y organizar el contenido con la agenda visual, listas de pasos y plantillas '
                '§ Consideración 6.3.',
                'organizadores gráficos para planificar antes de escribir',
                'dar más apoyo y más tiempo, y retirarlo poco a poco, sin una tarea aparte',
                'plantillas para resolver problemas',
                'herramientas de acceso, como el dictado por voz, el teclado adaptado o los pulsadores '
                '§ Consideración 4.2.']),
            ('D', 'Preguntar a tres antes que al docente, recogido en la base de orientación, para la autorregulación. '
                  '§ Sanmartí, en el manual.'),
            ('D', 'Estaciones de aprendizaje: varios rincones con tareas distintas sobre el mismo objetivo (de lectura, '
                  'manipulativa y digital), con la docente en la estación de quien más lo necesita.'),
            ('D', 'La Feria del Conocimiento: el alumnado elige puesto según su interés, visual, auditivo, manipulativo, '
                  'interactivo o artístico. § Manual.'),
            ('D', 'Inteligencia artificial que usa la docente, sin datos del alumnado: Napkin convierte un texto en un '
                  'esquema y Video Highlight transcribe y resume los vídeos, útil para el alumnado con discapacidad '
                  'auditiva. § Manual.'),
        ]},
        2: {'titulo': 'Ejemplo de Andalucía',
            'norma': [('g) «El patrimonio cultural y natural de nuestra comunidad, su historia, sus paisajes, su folclore, '
                       'las distintas variedades de la modalidad lingüística andaluza, la diversidad de sus '
                       'manifestaciones artísticas como el flamenco, la música, la literatura o la pintura, entre ellas, '
                       'tanto tradicionales como actuales, así como las contribuciones de su ciudadanía a la '
                       'construcción del acervo cultural andaluz, formarán parte del desarrollo del currículo».', D101)],
            'ops': [
            ('1', 'El patrimonio y las leyendas del pueblo, trabajados en el propio entorno, con una salida.'),
            ('C', 'Un ejemplo de cada parte de la letra g):', [
                '**Patrimonio cultural.** una ruta guiada por los monumentos del pueblo, con un código QR en cada parada',
                '**Patrimonio natural y paisajes.** un parque natural de la comarca o la vía verde, con una guía '
                'ilustrada de su flora y su fauna',
                '**Historia.** lo que trajo al-Ándalus a la cocina o la vida de las mujeres del pueblo hace cien años',
                '**Folclore.** refranes, coplas, romances de ciego y juegos populares de las personas mayores',
                '**Modalidad lingüística.** un diccionario del habla del pueblo, con palabras y expresiones recogidas en '
                'entrevistas',
                '**Flamenco y música.** un cancionero de cantes de trabajo y un recital el Día del Flamenco',
                '**Literatura.** poemas de Machado y Lorca o leyendas de Sevilla contadas en audiocuentos',
                '**Pintura.** los bodegones de Velázquez o el mural de una artista del pueblo',
                '**Contribuciones de su ciudadanía.** los oficios tradicionales o las personas del pueblo que han dejado '
                'huella']),
            ('C', 'Las efemérides andaluzas: Día de Andalucía, Día de la Bandera Andaluza, Día del Flamenco o Día de la '
                  'Lectura en Andalucía.'),
            ('D', 'Andalucía en las matemáticas: escalas con mapas de Andalucía, simetrías y teselados de la Alhambra o '
                  'problemas con datos reales del pueblo.'),
            ('D', 'Mujeres andaluzas referentes en la ciencia, en las matemáticas y en el arte, para supuestos de '
                  'igualdad.'),
        ]},
        3: {'titulo': 'Ejemplo de lo digital',
            'norma': [('c) «Desde las distintas áreas se favorecerá la integración y la utilización de las tecnologías '
                       'de la información y la comunicación».', D101)],
            'ops': [
            ('1', 'Canva o Book Creator para elaborar el producto final.'),
            ('C', 'Según la fase de la secuencia:', [
                '**Activación.** Kahoot!, Mentimeter, con una nube de palabras, o Plickers, sin dispositivos del alumnado',
                '**Exploración.** búsqueda guiada en fuentes fiables, Google Earth o mapas por satélite y códigos QR',
                '**Estructuración.** Genially, Wordwall, Educaplay o Liveworksheets, con autocorrección',
                '**Aplicación.** Canva, Book Creator, Scratch, micro:bit o Audacity para el pódcast',
                '**Difusión.** el blog del centro, la radio escolar o el aula virtual',
                '**Evaluación.** formularios para el KPSI, Plickers o Kahoot!']),
            ('C', 'El uso seguro y responsable de la red, con un decálogo de uso de internet elaborado por el grupo.'),
            ('D', 'Pensamiento computacional: un simulador programado en Scratch, como el de incendios de la UDP 4, o '
                  'robots educativos.'),
            ('D', 'Alfabetización mediática: detectar bulos e imágenes falsas creadas por la docente con inteligencia '
                  'artificial y comprobar su fiabilidad. § Manual; la docente crea y enseña las imágenes.'),
        ]},
        4: {'titulo': 'Metodología principal: qué es, su autor y cómo se concreta', 'ops': [
            ('1', '**Aprendizaje-servicio (ApS).** Integra en un mismo proyecto el aprendizaje curricular y un servicio a '
                  'la comunidad, de modo que el alumnado aprende actuando sobre necesidades reales de su entorno para '
                  'mejorarlo; Batlle (2020) lo resume como un «compromiso social en acción». Se concreta en el servicio, '
                  'que es el producto final, con cuatro fases: preparación, planificación, ejecución y '
                  'evaluación-reconocimiento (Santos-Pastor et al., 2021). § Ejemplos: una campaña de ahorro de agua para '
                  'las familias, una ruta guiada por el patrimonio o audiocuentos para el alumnado ciego.'),
            ('C', '**Aprendizaje basado en retos (ABR).** Parte de una idea general, la concreta en una pregunta esencial '
                  'y en un reto que el alumnado asume como propio, y avanza en tres fases en las que el alumnado se '
                  'implica, investiga y actúa (Universidad Politécnica de Madrid, 2020). § Ejemplo: idea general, el '
                  'agua; pregunta esencial, ¿por qué no se bebe el agua del pueblo?; reto, pedir que se proteja.'),
            ('C', '**Aprendizaje basado en proyectos (ABP).** El alumnado, como protagonista, aprende a través de un '
                  'proyecto que culmina en una acción final comprometida con la realidad (Vergara, 2021), en torno a una '
                  'pregunta guía desafiante, abierta y realista. § Ejemplo: «¿Cómo convertir el pueblo en un centro de '
                  'interés turístico?», con una guía como producto.'),
            ('C', '**Aprendizaje cooperativo.** Equipos heterogéneos estables con interdependencia positiva, '
                  'responsabilidad individual, roles rotativos y técnicas sencillas, como el 1-2-4, el folio giratorio '
                  'o los lápices al centro (Alonso et al., 2024). § Como en la programación; la evaluación de cada '
                  'criterio, siempre individual.'),
            ('C', '**Gamificación.** No es un método en sí, sino el envoltorio narrativo y lúdico de la metodología, que '
                  'toma elementos del juego (narrativa, avatares, puntos, rangos e insignias) para despertar la '
                  'motivación y el compromiso, y mejora la motivación y el rendimiento (Prieto-Andreu et al., 2022). Los '
                  'puntos nunca cuentan en la nota. § Se distingue del aprendizaje basado en juegos, que usa un juego '
                  'concreto para aprender, como un Kahoot!'),
            ('C', '**Aula invertida.** El alumnado accede a los contenidos antes de la clase y el aula se dedica a '
                  'resolver problemas y colaborar, con efectos positivos en el rendimiento (Rodríguez-Jiménez et al., '
                  '2021). § Solo en el tercer ciclo, con acceso garantizado, o si el enunciado la impone.'),
            ('C', 'Como apoyo de cualquiera de ellas, las rutinas de pensamiento del Proyecto Cero, que Furman (2021) '
                  'recomienda como estructuras sencillas que, usadas una y otra vez, se convierten en hábitos de '
                  'pensamiento. § Como en la programación.'),
            ('D', '**Pensamiento de diseño.** Cinco fases: empatizar con el problema, definirlo, idear soluciones, '
                  'prototipar y evaluar cómo funcionan. § Manual (Ana); sin autor de 2020 en adelante.'),
            ('D', '**Escape room o breakout.** El alumnado resuelve retos encadenados, cada uno con una pista para '
                  '«escapar», siempre con una narrativa y una reflexión final. § Manual; como producto intermedio o '
                  'final.'),
        ]},
        5: {'titulo': 'Ejemplo de trabajo individual', 'ops': [
            ('1', 'el ticket de salida, con un par de preguntas sobre lo aprendido que el alumnado entrega antes de salir, '
                  'para decidir si hay que reformular la explicación. § Disparadores: «hoy aprendí…», «me sorprendió '
                  'que…», «una cosa que no tengo claro es…»; o resumir la clase en 140 caracteres o rodear tres emojis.'),
            ('C', 'Más técnicas individuales del manual:', [
                'el KPSI o el Q-sort al comenzar, que se vuelve a analizar al final',
                'la escalera de la metacognición: ¿qué he aprendido?, ¿cómo lo he aprendido?, ¿qué problemas he '
                'encontrado?, ¿para qué me ha servido? y ¿en qué otra situación puedo aplicarlo?',
                'el diario de aprendizaje o el grimorio, en el que cada estudiante anota lo aprendido y cómo se ha '
                'sentido',
                'la escala de autovaloración, al cerrar cada tarea',
                'la base de orientación, para autorregularse con los pasos y los criterios del producto',
                'el CLC (cerebro, libro, compañero), que empieza con lo que cada uno recuerda',
                'el semáforo: verde, lo que entiende; amarillo, lo que le genera dudas; rojo, lo que no sabe',
                'la rutina 3, 2, 1: tres preguntas, dos ideas y una imagen',
                'el titular, que sintetiza lo aprendido como en un periódico',
                'la lectura de libre elección, con una reseña de cada libro',
                'un reto de escritura al llegar, con tres líneas sobre el tema',
                'la hoja de saberlo todo, antes de una prueba']),
            ('D', 'Estrella, martillo, bombilla y tijera: reconocer una acción buena de un compañero, lo que ha gustado, '
                  'algo aprendido y lo que no ha gustado. § Manual.'),
        ]},
        6: {'titulo': 'Técnicas cooperativas (dos)', 'ops': [
            ('1', 'El 1-2-4, individual, en parejas y en el equipo de cuatro hasta una respuesta común, y el folio '
                  'giratorio, en el que el folio pasa por el equipo y cada uno añade su aportación con su color, lo que '
                  'muestra quién ha participado.'),
            ('C', 'Más técnicas y en qué consisten:', [
                '**Lápices al centro.** se debate con los lápices en el centro y, después, cada uno escribe la respuesta '
                'acordada',
                '**Cabezas numeradas juntas.** el equipo se asegura de que todos saben responder y el azar decide quién '
                'responde',
                '**Rompecabezas o grupo de expertos.** cada miembro prepara una parte con los expertos de otros equipos '
                'y la explica al suyo',
                '**Rally coach.** por parejas, uno resuelve y el otro entrena, y se alternan',
                '**Rally Robin.** las parejas comparten por turnos, como el 1-2-4 sin la última fase',
                '**Lectura compartida.** uno lee un párrafo y el de su derecha, con ayuda del resto, lo resume',
                '**Mapa mental a cuatro bandas.** cada miembro desarrolla una rama y la explica a los demás',
                '**Gemelos pensantes.** la pareja comparte tarea, información y objetivo y trabaja hombro con hombro',
                '**Abanica y escoge.** cuatro papeles rotatorios: quien muestra las tarjetas, quien escoge y lee, quien '
                'responde y quien comprueba',
                '**El saco de dudas.** cada uno escribe sus dudas en un pósit y otro equipo las resuelve',
                '**Equipos de oyentes.** un equipo expone y los demás preguntan, sacan ideas útiles, retroalimentan o '
                'ponen ejemplos',
                '**Sombrero de cuatro picos.** ante un tema polémico, cada uno defiende un papel: a favor, en contra, '
                'escéptico o neutro',
                '**Parafraseo por parejas.** uno explica el problema con sus palabras y el otro comprueba y completa',
                '**Construir un problema.** cada miembro redacta un enunciado y el equipo elige y mejora el mejor',
                '**Escritura cooperativa.** redacción en equipo con lista de requisitos y revisión cruzada por parejas',
                '**Dictado a la carrera.** por parejas, uno corre a leer el texto colocado lejos, en el patio, y lo '
                'dicta al otro',
                '**Grammar casino.** los equipos apuestan puntos sobre frases verdaderas o falsas',
                '**Boli giratorio.** cada uno, con un color, continúa la descripción del anterior, y al final revisan la '
                'ortografía']),
            ('D', 'Para cohesionar al grupo al inicio o al cierre: la red de lana, en la que el ovillo pasa mientras se '
                  'dice algo positivo de quien lo recibe. § Rafa.'),
            ('D', 'Para evaluar el trabajo cooperativo: el GIG (grupo, individual, grupo) o un torneo de preguntas creado '
                  'por los equipos. § Manual; la calificación, siempre por criterios.'),
        ]},
        92: {'titulo': 'Ejemplo de aprendizaje entre iguales', 'ops': [
            ('1', 'la tutoría entre iguales, en la que un alumno o una alumna ayuda a otro con un rol definido.'),
            ('C', 'Más ejemplos:', [
                'la lectura entre iguales, con los gemelos lectores, en pareja y con papeles de tutor y tutorado',
                'padrinos lectores: el alumnado de quinto lee cuentos al del primer ciclo',
                '«dos aciertos y una mejora», para revisar el trabajo del compañero',
                '«te regalo, te pido prestado», con la rúbrica de un solo punto: regalo una mejora y tomo prestado algo '
                'bueno del compañero',
                'la escalera de la retroalimentación: aclarar, valorar, expresar inquietudes y hacer sugerencias',
                'preguntar a tres antes que al docente',
                '«me examino y examino»: cada estudiante corrige la prueba de un compañero con propuestas de mejora, no '
                'con nota',
                'la alumna con altas capacidades como tutora de un compañero',
                '«dilo tú»: repetir con sus palabras lo que acaba de leer o escuchar el compañero']),
        ]},
        7: {'titulo': 'Idea clave del área (anexo II de la Orden de 30 de mayo de 2023)', 'ops': [
            ('1', 'Una idea ★ del área eje en la tabla de orientaciones de abajo.'),
            ('C', 'Otra idea de la misma área, en la misma tabla.'),
            ('C', 'Con el ejemplo de la programación (figura 14):', [
                '**Conocimiento del Medio.** indagando problemas reales del entorno, como por qué no se bebe el agua del '
                'pueblo',
                '**Lengua.** produciendo textos orales y multimodales para destinatarios reales, como un reportaje sobre '
                'los oficios del pueblo',
                '**Matemáticas.** manipulando y jugando, como en un mercado con dinero de mentira',
                '**Educación Artística.** creando obras de land art en una ruta por el entorno']),
        ]},
    },
    # ------------------------------------------------------------------------------------------------ 7.9
    '7.9': {
        1: {'titulo': 'Materiales variados', 'ops': [
            ('1', 'Manipulativos de matemáticas: regletas, bloques multibase, ábaco, geoplanos y material de medida, como '
                  'el metro, la báscula o las jarras graduadas.'),
            ('C', 'Más materiales, por tipos:', [
                '**Didácticos comunes.** el grimorio o cuaderno de la misión, el mural del tema, el KPSI o el Q-sort, las '
                'bases de orientación y las tarjetas de roles',
                '**Impresos.** prensa local, infografías, cartas reales, folletos, recetarios, mapas, romances y libros '
                'de la biblioteca de aula',
                '**Para pensar.** plantillas de resolución de problemas, el mural de los siete pasos, organizadores '
                'gráficos y las llaves de los pensadores',
                '**Para jugar.** juegos de mesa, Story Cubes, cartas e insignias, dados y tableros creados por el grupo',
                '**Para experimentar.** lupas, una clave dicotómica, botellas con grava, arena y arcilla, col lombarda, '
                'lana y papel de plata',
                '**Del entorno.** objetos y fotografías antiguas de las familias, productos de la plaza de abastos y '
                'materiales reciclados',
                '**Plásticos.** cartulinas, témperas, arcilla y materiales para maquetas',
                '**Para la escape room.** candados, criptex, tinta invisible con linterna ultravioleta, walkie-talkies, '
                'mensajes cifrados y códigos QR',
                '**Para el aula.** los vasos de colores, el medidor emocional, el rincón de la calma, las cajas de '
                'aprendizaje y, alguna vez, el libro de texto, para que resulte realista']),
            ('D', 'Personales: familias, personas mayores y entidades del pueblo que entran en el aula como personas '
                  'expertas o reciben el servicio. § Programación, figura 19.'),
            ('D', 'De acceso, si hay alumnado que los necesita: el sistema de frecuencia modulada, el atril, la lupa o el '
                  'teclado adaptado.'),
        ]},
        2: {'titulo': 'Herramienta digital y para qué', 'ops': [
            ('1', 'Canva o Book Creator para elaborar el producto final.'),
            ('C', 'Herramientas y su función:', [
                '**Kahoot!, Mentimeter o Plickers.** ideas previas, repaso y cuestionario final; Plickers, sin '
                'dispositivos del alumnado',
                '**Padlet.** muro colaborativo de hallazgos',
                '**Genially.** presentaciones interactivas y breakout',
                '**Wordwall, Educaplay, Liveworksheets, Gimkit o Blooket.** actividades multinivel con autocorrección y '
                'metas colectivas',
                '**Edpuzzle.** vídeos con preguntas',
                '**GeoGebra.** geometría y representación',
                '**Scratch, micro:bit o robots educativos.** programación y pensamiento computacional',
                '**Audacity.** grabar y editar el pódcast',
                '**Google Earth o mapas por satélite.** localizar y medir distancias',
                '**Inkarnate.** el mapa de la narrativa de la gamificación',
                '**MyClassGame o ClassDojo.** puntos, avatares y gestión del aula',
                '**Classroomscreen.** temporizador y semáforo de ruido o de ayuda',
                '**ARASAAC y Pictotraductor.** pictogramas para consignas y agendas visuales',
                '**Lector inmersivo.** lectura en voz alta y separación silábica',
                '**Códigos QR.** enlaces a las fuentes y al producto',
                '**Google Classroom, Drive o Moodle Centros.** entregas y difusión segura',
                '**iPasen.** comunicación con las familias y autorizaciones']),
            ('D', 'Inteligencia artificial que usa la docente desde su cuenta y sin datos del alumnado: Suno, para una '
                  'canción que ayude a recordar conceptos; Bing o Ideogram, para ilustrar un cuento o un cómic histórico; '
                  'Napkin, para convertir un texto en esquema, y ElevenLabs, para convertir un texto en voz. § Manual; '
                  'muchas exigen una edad mínima de 13 años o más.'),
            ('D', 'Impresión 3D, cámara de documentos o grabación de las exposiciones, si el centro tiene el '
                  'equipamiento. § Rafa.'),
        ]},
    },
}


def renumera():
    """Numera los huecos de cada apartado por orden de aparición y ajusta las claves de OPCIONES."""
    for clave, datos in PLANTILLAS.items():
        mapa, n = {}, 0
        for fila in datos['filas']:
            for m in re.finditer(r'[\[{](\d+)\|', fila['texto']):
                viejo = int(m.group(1))
                if viejo not in mapa:
                    n += 1
                    mapa[viejo] = n
        for fila in datos['filas']:
            fila['texto'] = re.sub(r'([\[{])(\d+)\|', lambda m: f'{m.group(1)}{mapa[int(m.group(2))]}|', fila['texto'])
        if clave in OPCIONES:
            sobran = set(OPCIONES[clave]) - set(mapa)
            assert not sobran, (clave, sobran)
            faltan = set(mapa) - set(OPCIONES[clave])
            assert not faltan, (clave, faltan)
            OPCIONES[clave] = {mapa[k]: v for k, v in OPCIONES[clave].items()}


renumera()
