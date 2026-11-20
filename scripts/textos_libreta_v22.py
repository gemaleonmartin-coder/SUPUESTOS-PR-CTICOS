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
                      'educativo recoge, entre sus líneas generales de actuación pedagógica y la concreción curricular, '
                      '[2|línea, en infinitivo] y, entre sus objetivos generales destinados a la mejora del rendimiento '
                      'escolar y de la calidad educativa del centro, [3|objetivo, en infinitivo], fijado a raíz de la última memoria de autoevaluación. '
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
            {'texto': '{2|Desde el punto de vista normativo,} el ' + RD_COMPLETO + ' (en adelante, Real Decreto 157/2022), '
                      'establece en su artículo 10.2{3|} que, para la adquisición y el desarrollo de las competencias clave y '
                      'de las competencias específicas, el equipo docente planificará situaciones de aprendizaje. En '
                      'coherencia, el ' + D101_COMPLETO + ' (en adelante, Decreto 101/2023), garantiza en su artículo 7.3 '
                      'el funcionamiento coordinado de los equipos docentes al plantear las situaciones de aprendizaje, con '
                      'un enfoque interdisciplinar, integrador y holístico, que esta propuesta concreta en [conexión entre '
                      'áreas o acuerdo del equipo docente]. Asimismo, [4|instrucción del área] [qué establece], que aquí se '
                      'traduce en [decisión de la propuesta].', 'nuevo': True},
        ],
    },
    '7.5': {
        'titulo': '7.5. Intervención a nivel de centro (coordinación docente)',
        'filas': [
            {'etiqueta': SIEMPRE,
             'texto': 'La intervención se articula en dos niveles: el de centro, de carácter organizativo, y el de aula. A '
                      'nivel de centro, la propuesta parte de [1|la línea general de actuación pedagógica y de concreción '
                      'curricular o el objetivo general destinado a la mejora del rendimiento escolar y de la calidad '
                      'educativa del centro, ya citado en el contexto], tras detectarse en [memoria de autoevaluación o '
                      'evaluación inicial] [necesidad].', 'nuevo': True},
            {'texto': 'De acuerdo con el ' + D328_COMPLETO + ', modificado por el ' + D483_COMPLETO + ' (en adelante, '
                      'Decreto 328/2010), el equipo técnico de coordinación pedagógica [2|acuerdo de centro] y el equipo de '
                      '[ciclo] lo concreta en [3|producto final, calendario, instrumento común], que se incorpora a la '
                      'programación didáctica.', 'nuevo': True},
            {'texto': 'Antes del inicio, la tutoría se reúne con el equipo de orientación para [4|ajustar las medidas de …]; '
                      'el profesorado de [Pedagogía Terapéutica o Audición y Lenguaje] interviene dentro del aula en '
                      '[sesiones], y el seguimiento se realiza [periodicidad].'},
            {'texto': 'Para su desarrollo, se reservan [5|espacios del centro y del entorno] conforme al reglamento de '
                      'organización y funcionamiento. Además, los criterios pedagógicos del proyecto educativo{6|}, que el '
                      'artículo 21.3.c) del Decreto 328/2010 establece como base para planificar, entre otros aspectos, el '
                      'tiempo escolar y extraescolar, orientan la actividad complementaria [7|salida o visita], que el '
                      'equipo de ciclo incluye en la programación didáctica; el uso de [8|recurso digital] como herramienta '
                      'común, y la integración de la cultura andaluza mediante [9|elemento andaluz].', 'nuevo': True},
            {'etiqueta': SEGUN,
             'texto': 'Familias y entorno. Las familias son informadas mediante [10|cauce] y participan en [actividad]; con '
                      'el entorno, se colabora con [entidad] para [función].', 'nuevo': True},
            {'texto': 'Protección de datos. Conforme a la Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos '
                      'Personales y garantía de los derechos digitales, al ser el alumnado menor de catorce años, se recaba '
                      'por [iPasen] la autorización de las familias antes de difundir [11|grabaciones o imágenes].',
             'nuevo': True},
            {'texto': 'Especialistas del equipo docente. El equipo docente, coordinado por la tutoría, acuerda '
                      '[12|aportación de especialistas de área].', 'nuevo': True},
            {'texto': 'Lo que marca el proyecto educativo. Siguiendo los acuerdos del proyecto educativo, [13|lectura diaria '
                      'o modelo común de resolución de problemas].', 'nuevo': True},
            {'texto': 'Servicios complementarios. La propuesta se extiende a [14|comedor o aula matinal], en coordinación '
                      'con [responsable del Plan de Apertura de Centros Docentes].', 'nuevo': True},
            {'texto': 'Proyecto interdisciplinar. Al tratarse de un proyecto interdisciplinar, se desarrolla también en '
                      '[15|la hora semanal de autonomía del centro].', 'nuevo': True},
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
                      '[2|número y nombre], y da continuidad a [la línea general de actuación pedagógica y de concreción curricular o el objetivo general destinado a la mejora del rendimiento escolar y de la calidad educativa del centro, citado en el contexto].', 'nuevo': True},
        ],
    },
    '7.7': {
        'titulo': '7.7. Concreción curricular',
        'filas': [
            {'texto': 'La situación de aprendizaje contribuye al objetivo de etapa [1|letra]), recogido en el artículo 5 '
                      'del Decreto 101/2023. Conforme al anexo II de la {2|' + ORDEN_COMPLETA + ' (en adelante, Orden de 30 de '
                      'mayo de 2023)}, se centra, en [área eje], en la competencia específica [3|n.º], referida a [idea central], que se valorará mediante el '
                      'criterio de evaluación [código], [paráfrasis]. Moviliza saberes básicos del bloque [bloque], en '
                      'particular [saber]. Esta competencia se vincula con los descriptores operativos [código 1] y '
                      '[código 2] y contribuye así a la competencia [competencia clave].', 'nuevo': True},
            {'texto': 'Asimismo, desde [4|segunda área] se desarrolla la competencia específica [n.º], que persigue [idea '
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
            {'texto': 'Por último, de acuerdo con las orientaciones que el anexo II de la Orden de 30 de mayo de 2023 recoge '
                      'para [área], la propuesta [7|idea clave del área], como [ejemplo en la propuesta].', 'nuevo': True},
        ],
    },
    '7.9': {
        'titulo': '7.9. Secuencia didáctica (solo lo que llega de la metodología)',
        'filas': [
            {'texto': 'En las actividades se emplean materiales variados ([1|manipulativos, impresos, del entorno]) y '
                      'recursos tecnológicos con finalidad didáctica, como [2|herramienta] para [función], y la '
                      'información se presenta en distintos formatos ([visual, oral, manipulativo]) para atender a los '
                      'diferentes ritmos y estilos.', 'nuevo': True},
        ],
    },
}

# Bocadillos: (título, tipo, líneas). Tipo: «FIJO» (se escribe tal cual) o «IDEAS» (se elige una o se adapta).
# Llevan el contenido para estudiar (salvo los autores, que se concretarán con los temas).
BOCADILLOS = {
    '7.1': {
        1: ('Gancho: preguntas retóricas y un dato', 'IDEAS', [
            'Lectura. ¿Es posible aprender ciencias, historia o matemáticas sin comprender lo que se lee?',
            'Matemáticas. ¿Cómo esperar que el alumnado resuelva problemas si no comprende sus enunciados?',
            'Medio ambiente. ¿Cómo esperar que las nuevas generaciones protejan el planeta si no aprenden a valorarlo?',
            'Inclusión. ¿Por qué diseñar para un alumno o alumna «tipo» si en el aula no existe?',
            'Convivencia. ¿Puede aprender quien no se siente seguro ni aceptado en su aula?',
            'Tecnología. ¿Cómo convertir a una generación que consume pantallas en una que crea con ellas de forma '
            'segura y crítica?',
            'Patrimonio. ¿Qué sabe el alumnado del patrimonio que pisa cada día de camino al colegio?',
            'Dato. PIRLS 2021 (cuarto curso): España, 521 puntos en comprensión lectora, por debajo de la Unión '
            'Europea (528) y de la OCDE (533); Andalucía, 523.']),
        2: ('Autor', 'IDEAS', ['Se concretará con los temas.']),
        3: ('Objetivos de la etapa (artículo 17 de la LOE)', 'IDEAS', [
            'a) convivencia, ciudadanía y derechos humanos.', 'b) trabajo individual y en equipo, esfuerzo, '
            'creatividad y espíritu emprendedor.', 'c) resolución pacífica de conflictos.',
            'd) diversidad cultural e igualdad entre hombres y mujeres.', 'e) lengua castellana y hábitos de lectura.',
            'f) lengua extranjera.', 'g) competencias matemáticas y resolución de problemas.',
            'h) ciencias, geografía, historia y cultura.', 'i) competencias tecnológicas y espíritu crítico.',
            'j) representaciones y expresiones artísticas.', 'k) higiene, salud, deporte y alimentación.',
            'l) cuidado de los animales.', 'm) afectividad y rechazo de la violencia y los estereotipos.',
            'n) movilidad activa y educación vial.']),
        4: ('Áreas', 'IDEAS', ['Siempre dos como mínimo: un área eje y otra conectada.',
                               'CMN, LCL, MAT, EAR (y VCE solo en sexto).']),
        5: ('Preíndice', 'FIJO', ['Se memoriza tal cual: es igual en todos los supuestos.']),
    },
    '7.2': {
        1: ('Recursos del entorno', 'IDEAS',
            ['Biblioteca municipal.', 'Talleres gratuitos del ayuntamiento.', 'Residencia de mayores.',
             'Centro de interpretación o museo local.', 'Asociaciones vecinales y culturales.',
             'Mercado de abastos, parques, polideportivo.', 'Uno o dos, y que después se usen.']),
        2: ('Líneas generales de actuación pedagógica y la concreción curricular (las cuatro de la programación)', 'IDEAS',
            ['Situar al alumnado como protagonista de su aprendizaje mediante metodologías activas que potencien la '
             'colaboración.',
             'Flexibilizar la respuesta educativa para adaptarla a la diversidad de aptitudes, intereses y necesidades '
             'del alumnado.',
             'Impulsar el pensamiento crítico a través de la búsqueda y el análisis de fuentes para resolver problemáticas '
             'y comunicar hallazgos.',
             'Fomentar la competencia digital del alumnado mediante el uso crítico y responsable de las herramientas y '
             'recursos tecnológicos del aula.']),
        3: ('Objetivos generales destinados a la mejora del rendimiento escolar y de la calidad educativa del centro (uno de lengua, otro de matemáticas)', 'IDEAS',
            ['Lengua. Mejorar la comprensión lectora inferencial mediante el tiempo diario de lectura planificada y '
             'comprobar su progreso con una prueba común trimestral.',
             'Matemáticas. Mejorar la resolución de problemas mediante un modelo común de pasos en todos los ciclos y '
             'comprobar su progreso con una prueba común trimestral.']),
        4: ('Planes y programas (Resolución de 29 de junio de 2026)', 'IDEAS',
            ['Tipo A, de oficio. Educación Inclusiva (atención a la diversidad); Plan de Actuación Digital (las '
             'tecnologías en el aula); Bibliotecas Escolares (lectura y biblioteca).',
             'Tipo B, a solicitud del centro. STEM (ciencia, tecnología y matemáticas); Vivir y Sentir el Patrimonio; '
             'Hábitos de Vida Saludable; Comunica (lectura, escritura, oralidad y radio).',
             'Tipo C, con convocatoria. Red de Radios Escolares de Andalucía, siempre junto con Comunica.',
             ]),
        5: ('Sociograma', 'IDEAS',
            ['El grupo está cohesionado y cuenta con líderes positivos.',
             'Se aprecian dos subgrupos que apenas se relacionan.',
             'Un alumno o una alumna apenas recibe elecciones.',
             'Después, sirve para formar los equipos heterogéneos (4.2.2).']),
        6: ('Fortalezas e intereses', 'IDEAS',
            ['Curiosidad por los animales, el deporte o los videojuegos.', 'Buena expresión oral.',
             'Gusto por el trabajo manipulativo y en equipo.']),
    },
    '7.3': {
        1: ('Autores', 'IDEAS', ['Dos, muy específicos del tema: se concretarán con los temas.',
                                 'La normativa es casi siempre la misma; los autores marcan la diferencia.']),
        2: ('Normativa fija', 'FIJO', [
            'Artículo 10.2 del Real Decreto 157/2022: el equipo docente planifica situaciones de aprendizaje para '
            'adquirir las competencias clave y las específicas; el anexo III da orientaciones para diseñarlas.',
            'Artículo 7.3 del Decreto 101/2023: equipos docentes coordinados y enfoque interdisciplinar, integrador y '
            'holístico.',
            'Sin principios pedagógicos: van en 4.2.2.']),
        3: ('En lugar del 10.2: los retos del siglo XXI (anexo I del Real Decreto 157/2022)', 'IDEAS', [
            'Actitud responsable ante la degradación del medio ambiente y el maltrato animal.',
            'Consumo responsable.', 'Estilos de vida saludable.',
            'Espíritu crítico, empático y proactivo ante la inequidad y la exclusión.',
            'Resolver los conflictos de manera pacífica.',
            'Uso ético y responsable de la cultura digital.',
            'La incertidumbre como oportunidad para dar respuestas creativas.',
            'Cooperar y convivir valorando la diversidad personal y cultural.',
            'Sentirse parte de un proyecto colectivo, local y global.',
            'Seguir aprendiendo a lo largo de la vida.']),
        4: ('Instrucción, según el área', 'IDEAS',
            ['Lectura. Instrucciones de 21 de junio de 2023, de la Viceconsejería de Desarrollo Educativo y Formación '
             'Profesional, sobre el tratamiento de la lectura para el despliegue de la competencia en comunicación '
             'lingüística en Educación Primaria y Educación Secundaria Obligatoria: tiempo diario de lectura no inferior '
             'a treinta minutos, con antes, durante y después.',
             'Matemáticas. Instrucciones de 18 de junio de 2024, de la Viceconsejería de Desarrollo Educativo y Formación '
             'Profesional, sobre las medidas para el fomento del razonamiento matemático a través del planteamiento y '
             'resolución de retos y problemas en Educación Infantil, Educación Primaria y Educación Secundaria '
             'Obligatoria: itinerario de problemas de dificultad creciente y pasos comunes.',
             'Biblioteca. Instrucciones de 10 de septiembre de 2025, sobre la organización y funcionamiento de las '
             'bibliotecas escolares (así las cita el BOJA n.º 57, de 24 de marzo de 2026): biblioteca como recurso '
             'para la mediación lectora, la alfabetización mediática e informacional y la inclusión. Como en la '
             'programación: el programa Bibliotecas Escolares (de oficio) y el Plan de Fomento de la Lectura 2026-2030 '
             '(Ministerio de Cultura, 2026), leer mejor y no solo más, con las familias.']),
    },
    '7.5': {
        1: ('Origen', 'IDEAS', ['Solo se cita la línea general de actuación pedagógica y de concreción curricular o el objetivo general destinado a la mejora del rendimiento escolar y de la calidad educativa del centro del contexto; no se vuelve a explicar.']),
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
        6: ('Los seis criterios pedagógicos (artículo 21.3.c)', 'FIJO', [
            'Evaluación y promoción del alumnado.', 'Tiempo escolar y extraescolar.', 'Agrupamientos y tutorías.',
            'Oferta de áreas.', 'Atención a la diversidad y tránsito entre etapas.',
            'Órganos de coordinación docente.']),
        7: ('Actividad complementaria', 'IDEAS', ['Visita a la biblioteca municipal, al centro de interpretación o a la '
                                                  'depuradora de la comarca, con autorización de las familias por iPasen.']),
        8: ('Recurso digital', 'IDEAS', ['Google Classroom, Canva, Book Creator, Genially, Padlet.']),
        9: ('Cultura andaluza', 'IDEAS', ['Día de Andalucía (28 de febrero); flamenco; modalidad lingüística andaluza; '
                                          'patrimonio y leyendas del pueblo.']),
        10: ('Familias y entorno', 'IDEAS', ['Reunión inicial, iPasen, tutoría de tarde.',
                                             'La persona delegada de madres y padres difunde el producto; el ayuntamiento '
                                             'lanza el reto y lo recibe.']),
        11: ('Protección de datos', 'IDEAS', ['Solo si hay vídeo, fotos o difusión en la web.',
                                              'Quien no tenga autorización participa con voz en off o con un avatar.',
                                              'Se graba con las tabletas del centro, nunca con móviles personales.']),
        12: ('Especialistas de área', 'IDEAS', ['Música compone la canción de la campaña; Educación Física organiza una '
                                                'ruta a pie; Inglés traduce los eslóganes.']),
        13: ('Proyecto educativo', 'IDEAS', [
            'Lectura: treinta minutos diarios con textos del tema, con antes, durante y después.',
            'Problemas, los siete pasos de las Instrucciones de 18 de junio de 2024: situación cercana y diálogo; '
            'comprender (datos y pregunta); elegir estrategia; aplicar y calcular; colores; comprobar; comunicar el '
            'proceso.']),
        14: ('Servicios complementarios', 'IDEAS', ['En el comedor, el grupo mide el agua que sobra; en el aula matinal, '
                                                    'se juega al juego que ha creado la clase.']),
        15: ('Proyecto interdisciplinar', 'IDEAS', ['Solo en el tercer ciclo: la hora de autonomía puede dedicarse a '
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
    },
    '7.7': {
        1: ('Objetivos de etapa (artículo 5 del Decreto 101/2023)', 'IDEAS', [
            'Los de la LOE (a a n) y dos propios de Andalucía:',
            'e) lengua castellana y hábitos de lectura.', 'g) matemáticas y resolución de problemas.',
            'h) ciencias, historia y cultura, y la riqueza patrimonial de Andalucía.',
            'ñ) la modalidad lingüística andaluza en todas sus variedades.',
            'o) el patrimonio cultural de Andalucía, comunidad de encuentro de culturas.']),
        2: ('Orden de 30 de mayo de 2023', 'FIJO', ['Se memoriza: es su primera mención, con el nombre completo.']),
        3: ('Área eje', 'IDEAS', ['Competencia, criterio, saber y dos descriptores: tabla de abajo.']),
        4: ('Segunda área', 'IDEAS', ['Solo la competencia específica, resumida en una línea.',
                                      'Ejemplo. Desde Lengua Castellana y Literatura se desarrolla la competencia '
                                      'específica 5, que persigue producir textos escritos y multimodales coherentes.']),
    },
    '7.8': {
        1: ('DUA (artículo 6.e)', 'IDEAS', [
            'Acceso de todo el alumnado al currículo: distintas formas de presentación, metodologías variadas y '
            'recursos para todos los estilos y ritmos.',
            'Agenda visual de cada sesión; consignas con pictogramas de ARASAAC; elegir el formato del producto final; '
            'glosario visual.']),
        2: ('Andalucía (artículo 6.g)', 'IDEAS', [
            'Patrimonio cultural y natural, historia, paisajes, folclore, modalidad lingüística andaluza y '
            'manifestaciones artísticas, como el flamenco.',
            'Día de Andalucía; flamenco; habla andaluza; patrimonio y leyendas del pueblo.']),
        3: ('Digital (artículo 6.c)', 'IDEAS', [
            'Integración y uso de las tecnologías de la información y la comunicación desde todas las áreas.',
            'Kahoot para activar ideas previas; Padlet para compartir hallazgos; Canva o Book Creator para el producto.']),
        4: ('Metodología principal', 'IDEAS', [
            'Aprendizaje-servicio (Batlle, 2020): aprendizaje curricular al servicio de una necesidad real de la '
            'comunidad; el producto es el servicio.',
            'Aprendizaje basado en proyectos (Vergara, 2021): investigar un reto real hasta un producto con destinatario.',
            'Aprendizaje basado en retos (Universidad Politécnica de Madrid, 2020): idea general, pregunta esencial y '
            'reto.',
            'Gamificación (Vázquez y Sevillano, 2022): narrativa, misiones, insignias y niveles para implicar.',
            'Aula invertida (Rodríguez et al., 2021): contenidos antes de clase; en el aula, aplicar.']),
        5: ('Individual y entre iguales', 'IDEAS', ['Individual: lectura, ticket de salida, diario de aprendizaje.',
                                                    'Entre iguales: tutoría entre iguales, «dos aciertos y una '
                                                    'mejora».']),
        6: ('Técnicas cooperativas', 'IDEAS', [
            'Folio giratorio: el folio pasa por el equipo y cada uno añade su aportación.',
            '1-2-4: individual, parejas y equipo hasta una respuesta común.',
            'Lápices al centro: se debate sin escribir; después cada uno escribe lo acordado.',
            'Rally coach: por parejas, uno resuelve y el otro entrena; se alternan.',
            'Cabezas numeradas: tras resolver juntos, el azar decide quién explica.',
            'Rompecabezas o expertos: cada uno prepara una parte y la explica a su equipo.',
            'Roles rotativos: portavoz, secretaría, coordinación y tiempo o material.']),
        7: ('Orientaciones del área', 'IDEAS', ['Tres o cuatro palabras de la tabla de abajo.']),
    },
    '7.9': {
        1: ('Materiales', 'IDEAS', [
            'Manipulativos: regletas, bloques multibase, ábaco, material de medida.',
            'Impresos y del entorno: prensa, infografías, cartas reales, mural de los pasos de los problemas.',
            'Espacios: huerto, biblioteca escolar y municipal.']),
        2: ('Recursos digitales y para qué', 'IDEAS', [
            'Canva o Book Creator: el producto final.', 'Padlet: muro de hallazgos.',
            'Kahoot o Mentimeter: ideas previas y repaso.', 'Genially: presentaciones interactivas.',
            'GeoGebra: geometría.', 'Scratch: programar.', 'ARASAAC y Lector inmersivo: accesibilidad.',
            'Google Classroom: entregas y difusión.']),
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

# Tabla recortada de elementos curriculares (de la tabla de Gem, ELEMENTOS_CURRICULARES_DEFINITIVOS, segunda tabla):
# una competencia específica por fila con su criterio de quinto, un saber vinculado a ese criterio y dos descriptores.
# Comprobado con normativa/criterios_5_boja.json y saberes_3ciclo_boja.json (BOJA n.º 104, de 2 de junio de 2023) y con
# la conexión de cada competencia con los descriptores del anexo II de la Orden. Resúmenes propios, no literales.
ELEMENTOS = [
    ('CMN', '1. Utilizar recursos digitales de forma segura para buscar información y crear contenidos.',
     '1.1.a Usar recursos digitales con seguridad para buscar, comunicarse y crear.',
     'CMN.3.B.1.2 Búsquedas de información seguras y eficientes en internet.', 'CD1, CD2'),
    ('CMN', '2. Plantear y responder cuestiones científicas con técnicas y modelos científicos.',
     '2.2.a Buscar y contrastar información de fuentes seguras y fiables.',
     'CMN.3.A.1.1 Fases de la investigación científica.', 'CCL3, STEM2'),
    ('CMN', '4. Conocer el propio cuerpo y desarrollar hábitos saludables para el bienestar.',
     '4.2.a Valorar hábitos de vida saludables desde las funciones vitales.',
     'CMN.3.A.2.3 Alimentación saludable y sostenible: menús equilibrados.', 'STEM5, CPSAA2'),
    ('CMN', '6. Identificar causas y consecuencias de la intervención humana para actuar de forma sostenible.',
     '6.2.a Buscar y evaluar propuestas ante problemas ecosociales.',
     'CMN.3.C.4.3 El desarrollo sostenible y la explotación de los recursos.', 'STEM5, CC4'),
    ('CMN', '7. Interpretar cambios y continuidades sociales y culturales para valorar la historia.',
     '7.1.a Analizar causalidad, simultaneidad y sucesión en las Edades Media y Moderna.',
     'CMN.3.C.2.5 El patrimonio natural y cultural como bien y recurso.', 'CC1, CCEC1'),
    ('LCL', '3. Producir textos orales y multimodales y participar en interacciones orales.',
     '3.1.a Producir textos orales y multimodales coherentes y fluidos.',
     'LCL.3.B.3.3 Producción oral: prosodia y comunicación no verbal.', 'CCL1, CCL5'),
    ('LCL', '5. Producir textos escritos y multimodales planificando, redactando y revisando.',
     '5.1.a Producir textos escritos coherentes con las normas ortográficas básicas.',
     'LCL.3.B.3.5 Producción escrita: ortografía, coherencia y cohesión.', 'CCL1, CPSAA5'),
    ('LCL', '7. Leer de manera autónoma obras diversas para construir la identidad lectora.',
     '7.1.a Leer de forma autónoma textos ajustados a sus gustos, como fuente de placer.',
     'LCL.3.B.3.4 Comprensión lectora antes, durante y después de la lectura.', 'CCL4, CCEC2'),
    ('MAT', '1. Interpretar situaciones cotidianas representándolas matemáticamente.',
     '1.1.a Comprender problemas cotidianos reformulando la pregunta.',
     'MAT.3.A.6.1 Problemas de consumo responsable y de dinero.', 'STEM1, STEM2'),
    ('MAT', '2. Resolver situaciones problematizadas con distintas estrategias y comprobar las soluciones.',
     '2.2.a Obtener soluciones seleccionando estrategias, tanteando y descomponiendo.',
     'MAT.3.A.3.7 Tantear soluciones antes de operar.', 'STEM1, CPSAA5'),
    ('MAT', '3. Explorar, formular y comprobar conjeturas y plantear problemas.',
     '3.2.a Plantear nuevos problemas sobre situaciones cotidianas.',
     'MAT.3.D.2.2 Invención de problemas de la vida cotidiana.', 'CCL1, STEM2'),
    ('MAT', '4. Utilizar el pensamiento computacional para modelizar situaciones cotidianas.',
     '4.1.a Modelizar situaciones cotidianas con principios del pensamiento computacional.',
     'MAT.3.D.4.1 Interpretación y creación de algoritmos sencillos.', 'STEM1, CD5'),
    ('MAT', '5. Conectar las matemáticas con otras áreas y con la vida cotidiana.',
     '5.2.a Usar las matemáticas en otras áreas y en problemas del entorno.',
     'MAT.3.C.4.4 Las ideas geométricas en el arte, las ciencias y la vida cotidiana.', 'STEM3, CCEC1'),
    ('MAT', '6. Comunicar y representar ideas matemáticas con distintos lenguajes.',
     '6.2.a Comunicar en distintos formatos conjeturas y procesos.',
     'MAT.3.E.1.3 Gráficos estadísticos sencillos.', 'CCL1, STEM4'),
    ('EAR', '3. Expresar ideas y emociones con el sonido, la imagen, el cuerpo y los medios digitales.',
     '3.1.a Producir obras propias básicas con confianza.',
     'EAR.3.B.1 Fases del proceso creativo.', 'CPSAA1, CCEC3'),
]
