# -*- coding: utf-8 -*-
"""Textos de la libreta mágica, versión 2.2 (fase 38, 20 de noviembre de 2026).

Plantillas de redacción corregidas de la Parte I (apartados 7.1 a 7.8 y la frase que pasa al 7.9) y los
bocadillos con ejemplos. Los usan los dos Word: la libreta corregida y las plantillas con bocadillos.

Marcas dentro de las plantillas:
  [texto]      hueco que se rellena con el supuesto (va en verde azulado, como en la libreta de Rafa);
  [n|texto]    hueco con bocadillo número n;
  {n|texto}    texto fijo (se memoriza) con bocadillo número n.
Cada fila es un párrafo de la plantilla; «etiqueta» separa los bloques fijos de los que dependen del supuesto.

Normativa comprobada en los PDF del repositorio PROGRAMACION-DIDACTICA (normativa/ y raíz):
  Decreto 328/2010, artículo 21.3, en la redacción del Decreto 483/2026 (artículo 4, punto dos) y artículo 27.2.f);
  Real Decreto 157/2022, artículo 10.2; Decreto 101/2023, artículos 5, 6 y 7; Orden de 30 de mayo de 2023,
  artículo 3.1 y anexo II (introducción de cada área); LOE, artículo 17; Resolución de 29 de junio de 2026
  (programas); Instrucciones de 21 de junio de 2023 (título en su PDF). Instrucciones de 10 de septiembre de 2025:
  citadas así en el BOJA n.º 57, de 24 de marzo de 2026 (título completo, por comprobar).
"""

ORDEN_COMPLETA = ('Orden de 30 de mayo de 2023, por la que se desarrolla el currículo correspondiente a la etapa de '
                  'Educación Primaria en la Comunidad Autónoma de Andalucía, se regulan determinados aspectos de la '
                  'atención a la diversidad y a las diferencias individuales, se establece la ordenación de la evaluación '
                  'del proceso de aprendizaje del alumnado y se determina el proceso de tránsito entre las diferentes '
                  'etapas educativas')
D328_COMPLETO = ('Decreto 328/2010, de 13 de julio, por el que se aprueba el Reglamento Orgánico de las escuelas infantiles '
                 'de segundo ciclo, de los colegios de educación primaria, de los colegios de educación infantil y primaria, '
                 'y de los centros públicos específicos de educación especial')
D483_COMPLETO = ('Decreto 483/2026, de 31 de agosto, por el que se adoptan medidas para la mejora del funcionamiento del '
                 'sistema educativo y de la gestión de la actividad docente en la enseñanza no universitaria en Andalucía')
RD_COMPLETO = ('Real Decreto 157/2022, de 1 de marzo, por el que se establecen la ordenación y las enseñanzas mínimas de '
               'la Educación Primaria')
D101_COMPLETO = ('Decreto 101/2023, de 9 de mayo, por el que se establece la ordenación y el currículo de la etapa de '
                 'Educación Primaria en la Comunidad Autónoma de Andalucía')

SIEMPRE = 'SIEMPRE'
SEGUN = 'SEGÚN EL SUPUESTO (uno o dos bloques)'
CIERRE = 'CIERRE (SIEMPRE)'
REUBICAR = 'REUBICACIÓN PREVISTA'

PLANTILLAS = {
    '7.1': {
        'titulo': '7.1. Introducción',
        'filas': [
            {'texto': '[1|Pregunta retórica o dato sobre el tema, con las palabras clave del enunciado]. '
                      '[Consecuencia educativa en una frase].'},
            {'texto': 'En este sentido, [2|autor (año)] señala que [idea que justifica trabajarlo en Educación Primaria].'},
            {'texto': 'Esta relevancia se refleja en la Ley Orgánica 2/2006, de 3 de mayo, de Educación, modificada por la '
                      'Ley Orgánica 3/2020, de 29 de diciembre (en adelante, LOE modificada por LOMLOE), que recoge entre '
                      'los objetivos de la etapa [3|objetivo relacionado].'},
            {'texto': 'Para dar respuesta al supuesto planteado, que solicita [demanda literal resumida], se presenta una '
                      'intervención educativa dirigida a un grupo de [curso] de Educación Primaria que, desde [4|área eje] '
                      'en conexión con [otras áreas], se concreta en la situación de aprendizaje «[título]», cuyo producto '
                      'final es [producto].'},
            {'texto': '{5|A tal fin, tras contextualizar la propuesta en su entorno, centro y alumnado y fundamentarla en la '
                      'normativa vigente y en autores actuales, se desarrolla la intervención a nivel de centro, mediante la '
                      'coordinación docente, y a nivel de aula, mediante la situación de aprendizaje, para cerrar con la '
                      'conclusión y las referencias.}',
             'nuevo': True, 'fijo': True},
        ],
    },
    '7.2': {
        'titulo': '7.2. Contexto: entorno, centro y alumnado',
        'filas': [
            {'texto': 'Entorno. El centro se ubica en [tipo de localidad] de [provincia o comarca andaluza], con un nivel '
                      'socioeconómico y cultural [nivel] y [grado] de participación de las familias. Dispone de '
                      '[1|recursos del entorno], que se aprovecharán en la propuesta.', 'nuevo': True},
            {'texto': 'Centro. Se trata de un colegio de educación infantil y primaria de [n.º] líneas cuyo proyecto '
                      'educativo recoge, entre sus líneas generales de actuación pedagógica, [2|línea, en infinitivo] y, '
                      'entre sus objetivos generales destinados a la mejora del rendimiento escolar y de la calidad '
                      'educativa, [3|objetivo, en infinitivo], fijado a raíz de la última memoria de autoevaluación. '
                      'Participa en [4|plan o programa] y cuenta con [recursos que se usarán].', 'nuevo': True},
            {'texto': 'Alumnado. El grupo de [curso] está formado por [n.º] alumnos y alumnas. Según la evaluación inicial '
                      'y el sociograma, [5|cohesión del grupo], destaca por [6|fortaleza o interés] y presenta dificultades '
                      'en [aspecto ligado al tema]. Incluye [perfil: necesidad y fortaleza], cuya respuesta educativa se '
                      'concreta en el apartado 4.2.4.', 'nuevo': True},
        ],
    },
    '7.3': {
        'titulo': '7.3. Justificación normativa y epistemológica',
        'filas': [
            {'texto': 'La respuesta a la necesidad descrita se fundamenta en un doble plano. Desde el punto de vista '
                      'epistemológico, [1|autor 1 (año)] sostiene que [idea sobre el tema], mientras que [autor 2 (año)] '
                      'destaca [idea sobre el enfoque], lo que justifica [decisión didáctica], adecuada a un alumnado que, '
                      'a esta edad, [rasgo evolutivo].'},
            {'texto': '{2|Desde el punto de vista normativo, el ' + RD_COMPLETO + ' (en adelante, Real Decreto 157/2022), '
                      'establece en su artículo 10.2 que, para la adquisición y el desarrollo de las competencias clave y '
                      'de las competencias específicas, el equipo docente planificará situaciones de aprendizaje. En '
                      'coherencia, el ' + D101_COMPLETO + ' (en adelante, Decreto 101/2023), garantiza en su artículo 7.3 '
                      'el funcionamiento coordinado de los equipos docentes al plantear las situaciones de aprendizaje, con '
                      'un enfoque interdisciplinar, integrador y holístico,} que esta propuesta concreta en [conexión entre '
                      'áreas o acuerdo del equipo docente]. Asimismo, [3|instrucción del área] [qué establece], que aquí se '
                      'traduce en [decisión de la propuesta].', 'nuevo': True},
        ],
    },
    '7.5': {
        'titulo': '7.5. Intervención a nivel de centro (coordinación docente)',
        'filas': [
            {'etiqueta': SIEMPRE,
             'texto': 'La intervención se articula en dos niveles: el de centro, de carácter organizativo, y el de aula. A '
                      'nivel de centro, la propuesta parte de [1|la línea general de actuación pedagógica o el objetivo '
                      'general de mejora citado en el contexto], tras detectarse en [memoria de autoevaluación o '
                      'evaluación inicial] [necesidad].', 'nuevo': True},
            {'texto': 'De acuerdo con el ' + D328_COMPLETO + ', modificado por el ' + D483_COMPLETO + ' (en adelante, '
                      'Decreto 328/2010), el equipo técnico de coordinación pedagógica [2|acuerdo de centro] y el equipo de '
                      '[ciclo] lo concreta en [3|producto final, calendario, instrumento común], que se incorpora a la '
                      'programación didáctica.', 'nuevo': True},
            {'texto': 'Antes del inicio, la tutoría se reúne con el equipo de orientación para [4|ajustar las medidas de …]; '
                      'el profesorado de [Pedagogía Terapéutica o Audición y Lenguaje] interviene dentro del aula en '
                      '[sesiones], y el seguimiento se realiza [periodicidad].'},
            {'texto': 'Para su desarrollo, se reservan [5|espacios del centro y del entorno] conforme al reglamento de '
                      'organización y funcionamiento. Además, los criterios pedagógicos del proyecto educativo, que el '
                      'artículo 21.3.c) del Decreto 328/2010 establece como base para planificar, entre otros aspectos, el '
                      'tiempo escolar y extraescolar, orientan la actividad complementaria [6|salida o visita], que el '
                      'equipo de ciclo incluye en la programación didáctica; el uso de [7|recurso digital] como herramienta '
                      'común, y la integración de la cultura andaluza mediante [8|elemento andaluz].', 'nuevo': True},
            {'etiqueta': SEGUN,
             'texto': 'Familias y entorno. Las familias son informadas mediante [9|cauce] y participan en [actividad]; con '
                      'el entorno, se colabora con [entidad] para [función].', 'nuevo': True},
            {'texto': 'Protección de datos. Conforme a la Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos '
                      'Personales y garantía de los derechos digitales, al ser el alumnado menor de catorce años, se recaba '
                      'por [iPasen] la autorización de las familias antes de difundir [10|grabaciones o imágenes].',
             'nuevo': True},
            {'texto': 'Especialistas del equipo docente. El equipo docente, coordinado por la tutoría, acuerda '
                      '[11|aportación de especialistas de área].', 'nuevo': True},
            {'texto': 'Lo que marca el proyecto educativo. Siguiendo los acuerdos del proyecto educativo, [12|lectura diaria '
                      'o modelo común de resolución de problemas].', 'nuevo': True},
            {'texto': 'Servicios complementarios. La propuesta se extiende a [13|comedor o aula matinal], en coordinación '
                      'con [responsable del Plan de Apertura de Centros Docentes].', 'nuevo': True},
            {'texto': 'Proyecto interdisciplinar. Al tratarse de un proyecto interdisciplinar, se desarrolla también en '
                      '[14|la hora semanal de autonomía del centro].', 'nuevo': True},
            {'etiqueta': CIERRE,
             'texto': 'Las conclusiones se trasladarán a la memoria de autoevaluación.'},
        ],
    },
    '7.6': {
        'titulo': '7.6. Intervención a nivel de aula: datos identificativos (transición)',
        'filas': [
            {'texto': 'A nivel de aula, la propuesta se concreta en la situación de aprendizaje «[título]», dirigida al '
                      'grupo de [curso] de Educación Primaria y planteada desde [área eje], en conexión con [áreas]. Se '
                      'desarrolla durante el [trimestre], a lo largo de [n.º] sesiones distribuidas en [n.º] semanas, '
                      '[coincidiendo con [1|efeméride]]. Parte del reto de [reto con palabras del enunciado] y culmina en '
                      '[producto final], que se presentará a [destinatario].'},
            {'texto': 'La situación conecta con los intereses del alumnado y con el Objetivo de Desarrollo Sostenible (ODS) '
                      '[2|número y nombre], y da continuidad a [la línea o el objetivo de mejora del contexto]. Asimismo, '
                      '{3|la ' + ORDEN_COMPLETA + ' (en adelante, Orden de 30 de mayo de 2023), establece en su artículo 3.1 '
                      'que las situaciones de aprendizaje integren los elementos curriculares de las distintas áreas para '
                      'atender a la diversidad, las necesidades y los intereses del alumnado, sentido que guía esta '
                      'propuesta.}', 'nuevo': True},
        ],
    },
    '7.7': {
        'titulo': '7.7. Concreción curricular',
        'filas': [
            {'texto': 'La situación de aprendizaje contribuye al objetivo de etapa [1|letra]), recogido en el artículo 5 '
                      'del Decreto 101/2023. Conforme al anexo II de la Orden de 30 de mayo de 2023, se centra, en [área '
                      'eje], en la competencia específica [2|n.º], referida a [idea central], que se valorará mediante el '
                      'criterio de evaluación [código], [paráfrasis]. Moviliza saberes básicos del bloque [bloque], en '
                      'particular [saber]. Esta competencia se vincula con los descriptores operativos [código 1] y '
                      '[código 2] y contribuye así a la competencia [competencia clave].', 'nuevo': True},
            {'texto': 'Asimismo, desde [3|segunda área] se desarrolla la competencia específica [n.º], que persigue [idea '
                      'central resumida en una línea]. Estos elementos se movilizan en la secuencia que se describe más '
                      'adelante.', 'nuevo': True},
        ],
    },
    '7.8': {
        'titulo': '7.8. Metodología',
        'filas': [
            {'texto': 'La propuesta responde a los principios pedagógicos del artículo 6 del Decreto 101/2023, en especial '
                      'el Diseño Universal para el Aprendizaje ([1|ejemplo]), el conocimiento del patrimonio cultural y '
                      'natural de Andalucía ([2|ejemplo]) y la integración de las tecnologías de la información y la '
                      'comunicación ([3|ejemplo]).', 'nuevo': True},
            {'texto': 'Conforme a su artículo 7.2, la metodología es activa, motivadora y participativa y parte de los '
                      'intereses del alumnado. Se articula mediante [4|metodología principal], que según [autor (año)] '
                      '[rasgo esencial] y que aquí se concreta en [despliegue]. Se combinan el trabajo individual '
                      '([5|ejemplo]), el cooperativo, en equipos heterogéneos con roles rotativos y técnicas como '
                      '[6|técnica 1] y [técnica 2], y el aprendizaje entre iguales ([ejemplo]).', 'nuevo': True},
            {'texto': 'Se emplean materiales variados ([manipulativos, impresos, del entorno]) y la información se presenta '
                      'en distintos formatos ([visual, oral, manipulativo]) para atender a los diferentes ritmos y estilos.',
             'nuevo': True},
            {'texto': 'Por último, de acuerdo con las orientaciones que el anexo II de la Orden de 30 de mayo de 2023 recoge '
                      'para [área], la propuesta [7|idea clave del área], como [ejemplo en la propuesta].', 'nuevo': True},
            {'etiqueta': REUBICAR,
             'texto': 'El enfoque es interdisciplinar: [área eje] aporta [qué], [área 2] aporta [qué] y [área 3], [qué].',
             'reubicar': True},
        ],
    },
    '7.9': {
        'titulo': '7.9. Secuencia didáctica (solo la frase que llega de la metodología)',
        'filas': [
            {'texto': 'En las actividades se emplean recursos tecnológicos con finalidad didáctica, como [1|herramienta] '
                      'para [función] y [herramienta] para [función].', 'nuevo': True},
        ],
    },
}

# Bocadillos: (título, tipo, líneas). Tipo: «FIJO» (se escribe tal cual) o «IDEAS» (se elige una o se adapta).
BOCADILLOS = {
    '7.1': {
        1: ('Gancho', 'IDEAS', ['Solo datos verificados (Parte II, 1); ante la duda, pregunta retórica.',
                                '«¿Qué ocurre cuando…?», «¿Cómo puede un grupo de quinto…?»']),
        2: ('Autor', 'IDEAS', ['Uno específico del tema, del banco de la Parte II (1 y 3).']),
        3: ('Objetivo de la etapa (artículo 17 de la LOE)', 'IDEAS',
            ['e) lengua castellana y hábitos de lectura.', 'g) competencias matemáticas y resolución de problemas.',
             'h) ciencias, geografía, historia y cultura.', 'i) competencias tecnológicas.',
             'j) representaciones y expresiones artísticas.', 'k) higiene, salud y alimentación.']),
        4: ('Áreas', 'IDEAS', ['Siempre dos como mínimo: un área eje y otra conectada.']),
        5: ('Preíndice', 'FIJO', ['Se memoriza tal cual: es igual en todos los supuestos.']),
    },
    '7.2': {
        1: ('Recursos del entorno', 'IDEAS',
            ['Biblioteca municipal.', 'Talleres gratuitos del ayuntamiento.', 'Residencia de mayores.',
             'Centro de interpretación o museo local.', 'Asociaciones vecinales y culturales.',
             'Mercado de abastos, parques, polideportivo.', 'Uno o dos, y que después se usen.']),
        2: ('Líneas generales de actuación pedagógica (las cuatro de la programación)', 'IDEAS',
            ['Situar al alumnado como protagonista de su aprendizaje mediante metodologías activas que potencien la '
             'colaboración.',
             'Flexibilizar la respuesta educativa para adaptarla a la diversidad de aptitudes, intereses y necesidades '
             'del alumnado.',
             'Impulsar el pensamiento crítico a través de la búsqueda y el análisis de fuentes para resolver problemáticas '
             'y comunicar hallazgos.',
             'Fomentar la competencia digital del alumnado mediante el uso crítico y responsable de las herramientas y '
             'recursos tecnológicos del aula.']),
        3: ('Objetivos generales de mejora (uno de lengua, otro de matemáticas)', 'IDEAS',
            ['Lengua. Mejorar la comprensión lectora inferencial mediante el tiempo diario de lectura planificada y '
             'comprobar su progreso con una prueba común trimestral.',
             'Matemáticas. Mejorar la resolución de problemas mediante un modelo común de pasos en todos los ciclos y '
             'comprobar su progreso con una prueba común trimestral.']),
        4: ('Planes y programas (Resolución de 29 de junio de 2026)', 'IDEAS',
            ['Tipo A. Educación Inclusiva; Plan de Actuación Digital; Bibliotecas Escolares.',
             'Tipo B. STEM; Vivir y Sentir el Patrimonio; Hábitos de Vida Saludable; Comunica.',
             'Radio. Red de Radios Escolares de Andalucía (tipo C), siempre junto con Comunica.',
             'Proyectos ApS, no.']),
        5: ('Sociograma', 'IDEAS',
            ['El grupo está cohesionado y cuenta con líderes positivos.',
             'Se aprecian dos subgrupos que apenas se relacionan.',
             'Un alumno o una alumna apenas recibe elecciones.',
             'Después, sirve para formar los equipos (4.2.2).']),
        6: ('Fortalezas e intereses', 'IDEAS',
            ['Curiosidad por los animales, el deporte o los videojuegos.', 'Buena expresión oral.',
             'Gusto por el trabajo manipulativo y en equipo.']),
    },
    '7.3': {
        1: ('Autores', 'IDEAS', ['La normativa es casi siempre la misma; los autores marcan la diferencia.',
                                 'Dos, muy específicos del tema: banco de la Parte II, apartado 3.']),
        2: ('Normativa fija', 'FIJO', ['Se memoriza: Real Decreto 157/2022, artículo 10.2, y Decreto 101/2023, '
                                       'artículo 7.3. Sin principios pedagógicos (van en 4.2.2).']),
        3: ('Instrucción, según el área', 'IDEAS',
            ['Lectura. Instrucciones de 21 de junio de 2023, de la Viceconsejería de Desarrollo Educativo y Formación '
             'Profesional, sobre el tratamiento de la lectura para el despliegue de la competencia en comunicación '
             'lingüística en Educación Primaria y Educación Secundaria Obligatoria: tiempo diario de lectura no inferior '
             'a treinta minutos, con antes, durante y después.',
             'Matemáticas. Instrucciones de 18 de junio de 2024, de la Viceconsejería de Desarrollo Educativo y Formación '
             'Profesional, sobre las medidas para el fomento del razonamiento matemático a través del planteamiento y '
             'resolución de retos y problemas en Educación Infantil, Educación Primaria y Educación Secundaria '
             'Obligatoria: itinerario de problemas de dificultad creciente y pasos comunes.',
             'Biblioteca. Instrucciones de 10 de septiembre de 2025, sobre la organización y funcionamiento de las '
             'bibliotecas escolares: biblioteca como recurso para la mediación lectora, la alfabetización mediática e '
             'informacional y la inclusión.']),
    },
    '7.5': {
        1: ('Origen', 'IDEAS', ['Solo se cita la línea o el objetivo del contexto; no se vuelve a explicar.']),
        2: ('Acuerdo del equipo técnico', 'IDEAS',
            ['Trabajar en todo el centro [centro de interés] en torno a [efeméride]; cada ciclo lo adapta.']),
        3: ('Concreción del ciclo', 'IDEAS', ['Producto final común, reparto de sesiones entre áreas, rúbrica compartida.',
                                              'La misma situación en las dos líneas del curso.']),
        4: ('Especialistas de atención a la diversidad', 'IDEAS',
            ['Ajustar las medidas del DUA para [perfil]: agenda visual, roles cooperativos.',
             'PT en las sesiones de cálculo; AL en el ensayo de la exposición oral.',
             'Seguimiento quincenal con indicadores: termina la tarea, participa con su rol.']),
        5: ('Espacios', 'IDEAS', ['Del centro: biblioteca escolar, sala de usos múltiples, huerto, carro de portátiles.',
                                  'Del entorno: los del contexto (biblioteca municipal, residencia…).']),
        6: ('Actividad complementaria', 'IDEAS', ['Visita a la biblioteca municipal, al centro de interpretación o a la '
                                                  'depuradora de la comarca, con autorización de las familias por iPasen.']),
        7: ('Recurso digital', 'IDEAS', ['Google Classroom, Canva, Book Creator, Genially, Padlet.']),
        8: ('Cultura andaluza', 'IDEAS', ['Día de Andalucía (28 de febrero); flamenco; modalidad lingüística andaluza; '
                                          'patrimonio y leyendas del pueblo.']),
        9: ('Familias y entorno', 'IDEAS', ['Reunión inicial, iPasen, tutoría de tarde.',
                                            'La persona delegada de madres y padres difunde el producto; el ayuntamiento '
                                            'lanza el reto y lo recibe.']),
        10: ('Protección de datos', 'IDEAS', ['Solo si hay vídeo, fotos o difusión en la web.',
                                              'Quien no tenga autorización participa con voz en off o con un avatar.']),
        11: ('Especialistas de área', 'IDEAS', ['Música compone la canción de la campaña; Educación Física organiza una '
                                                'ruta a pie; Inglés traduce los eslóganes.']),
        12: ('Proyecto educativo', 'IDEAS', ['Los treinta minutos diarios de lectura, con textos del tema.',
                                             'Los pasos comunes de resolución de problemas del centro.']),
        13: ('Servicios complementarios', 'IDEAS', ['En el comedor, el grupo mide el agua que sobra; en el aula matinal, '
                                                    'se juega al juego que ha creado la clase.']),
        14: ('Proyecto interdisciplinar', 'IDEAS', ['Solo en el tercer ciclo: la hora de autonomía puede dedicarse a '
                                                    'proyectos interdisciplinares.']),
    },
    '7.6': {
        1: ('Efeméride', 'IDEAS', ['Día de la Lectura en Andalucía (16 de diciembre).',
                                   'Día Escolar de la No Violencia y la Paz (30 de enero).',
                                   'Día Internacional de la Mujer y la Niña en la Ciencia (11 de febrero).',
                                   'Día de Andalucía (28 de febrero).', 'Día Internacional del Libro (23 de abril).',
                                   'Día Mundial del Medio Ambiente (5 de junio).']),
        2: ('ODS', 'IDEAS', ['3 Salud y bienestar.', '5 Igualdad de género.', '6 Agua limpia y saneamiento.',
                             '11 Ciudades y comunidades sostenibles.', '12 Producción y consumo responsables.',
                             '13 Acción por el clima.', '16 Paz, justicia e instituciones sólidas.']),
        3: ('Orden de 30 de mayo de 2023', 'FIJO', ['Se memoriza: es la primera mención de la Orden, con su nombre '
                                                    'completo.']),
    },
    '7.7': {
        1: ('Objetivo de etapa (artículo 5 del Decreto 101/2023)', 'IDEAS',
            ['e) lengua castellana y lectura; g) matemáticas; h) ciencias, historia y patrimonio de Andalucía.',
             'ñ) modalidad lingüística andaluza; o) patrimonio cultural de Andalucía.']),
        2: ('Área eje', 'IDEAS', ['Competencia, criterio, saber y dos descriptores: tabla de elementos curriculares.']),
        3: ('Segunda área', 'IDEAS', ['Solo la competencia específica, resumida en una línea.',
                                      'Ejemplo. Desde Lengua Castellana y Literatura se desarrolla la competencia '
                                      'específica 5, que persigue producir textos escritos y multimodales coherentes.']),
    },
    '7.8': {
        1: ('DUA', 'IDEAS', ['Agenda visual de cada sesión.', 'Consignas con pictogramas de ARASAAC.',
                             'Elegir el formato del producto final.', 'Glosario visual del vocabulario clave.']),
        2: ('Andalucía', 'IDEAS', ['Día de Andalucía; flamenco; habla andaluza; patrimonio y leyendas del pueblo.']),
        3: ('Digital', 'IDEAS', ['Kahoot para activar ideas previas; Padlet para compartir hallazgos; Canva o Book '
                                 'Creator para el producto.']),
        4: ('Metodología principal y su autor', 'IDEAS',
            ['Aprendizaje-servicio (Batlle, 2020).', 'Aprendizaje basado en proyectos (Vergara, 2021).',
             'Aprendizaje basado en retos (Universidad Politécnica de Madrid, 2020).',
             'Gamificación (Vázquez y Sevillano, 2022).', 'Aula invertida (Rodríguez et al., 2021).']),
        6: ('Técnicas cooperativas', 'IDEAS',
            ['Folio giratorio.', '1-2-4.', 'Lápices al centro.', 'Rally coach.', 'Cabezas numeradas.',
             'Rompecabezas o expertos.', 'Parafraseo por parejas.', 'Roles rotativos.']),
        5: ('Individual y entre iguales', 'IDEAS', ['Individual: lectura, ticket de salida, diario de aprendizaje.',
                                                    'Entre iguales: tutoría entre iguales, «dos aciertos y una '
                                                    'mejora».']),
        7: ('Orientaciones del área', 'IDEAS', ['Tres o cuatro palabras de la tabla de abajo.']),
    },
    '7.9': {
        1: ('Recursos digitales', 'IDEAS', ['Canva o Book Creator (producto), Padlet (hallazgos), Kahoot (ideas '
                                            'previas), Scratch (programar), Google Classroom (entregas).']),
    },
}

NOTA_REUBICAR = ('Contenido valioso que, por coherencia con la nueva estructura, se trasladará a otro apartado. Su '
                 'ubicación definitiva (la justificación normativa, junto al artículo 7.3, o la concreción curricular) '
                 'se decidirá en la próxima revisión.')

# Orientaciones metodológicas de cada área (anexo II de la Orden de 30 de mayo de 2023, introducción del área).
# Una idea por frase del texto oficial, en tres o cuatro palabras; ★ las más útiles para citar en el supuesto.
# Se omiten las frases que solo enumeran los bloques de saberes.
ORIENTACIONES = {
    'Lengua Castellana y Literatura': [
        ('Cuatro destrezas integradas', True), ('Uso eficaz y ético de la palabra', False),
        ('Progreso gradual e individual', False), ('Aprecio de la diversidad lingüística', False),
        ('Reflexionar, comprender y producir textos', False), ('Alfabetización mediática e informacional', True),
        ('Lectura literaria compartida', True), ('Reflexión sobre la lengua', False),
        ('Paz a través del lenguaje', False), ('Construcción, no transmisión', True),
        ('Situaciones comunicativas reales', True), ('Interacción y colaboración', False),
        ('Tratamiento integrado de las lenguas', False),
    ],
    'Matemáticas': [
        ('Alfabetización matemática', False), ('Carácter instrumental', True), ('Estructurar la realidad', False),
        ('Espacio, medida e incertidumbre', False), ('Razonar y argumentar', False),
        ('Datos y pensamiento computacional', False), ('Comprender el entorno', False),
        ('Formular, resolver, interpretar', False), ('Decisiones fundamentadas', False),
        ('Problemas como método', True), ('Problemas de la vida diaria', False), ('Seis sentidos matemáticos', False),
        ('Gestión de las emociones', False), ('El error como aprendizaje', True),
        ('Referentes, hombres y mujeres', False), ('Experiencial y manipulativa', True),
        ('Juego y magia educativa', True),
    ],
    'Conocimiento del Medio Natural, Social y Cultural': [
        ('Actitudes responsables y democráticas', False), ('Proyecto vital con éxito', False),
        ('Transformar el mundo sosteniblemente', False), ('Perspectiva sistémica del entorno', False),
        ('Fuentes fiables, ciudadanía global', False), ('Indagación y pensamiento crítico', True),
        ('Indagación interdisciplinar', True), ('Comprender y conservar el entorno', False),
        ('Investigar como científicos', True), ('Método científico y descubrimiento', False),
        ('Cuerpo, salud y energía', False), ('Cultura del esfuerzo', False), ('Proyectos de diseño cooperativos', False),
        ('Herramientas digitales seguras', False), ('Alumnado protagonista', True), ('De las TIC a las TAC', False),
        ('Retos locales y globales', True), ('Pensamiento histórico', False), ('Hábitos sostenibles y ODS', False),
        ('Andalucía en primer plano', True),
    ],
    'Educación Artística': [
        ('Desarrollo integral y creativo', False), ('Raíces andaluzas y flamenco', True), ('Arte sostenible', False),
        ('Recepción y producción', True), ('Sentido crítico cultural', False), ('Diálogo intercultural', False),
        ('El arte comunica', False), ('Evitar estereotipos', False), ('Conservar el patrimonio andaluz', True),
        ('Descubrir, investigar, expresar', False), ('Contextos cercanos y significativos', True),
        ('Transformar la sociedad', False),
    ],
}
