# -*- coding: utf-8 -*-
"""Plantillas por importancia (fase 38): las plantillas de redacción de la libreta mágica (7.1 a 7.9) y, para cada hueco,
las opciones ordenadas por grado de importancia: lo fijo, la primera opción y los comodines. Sustituye al Word de
bocadillos (petición de Gem del 20 de noviembre de 2026).

Niveles: 'F' fijo (se escribe siempre así); '1' primera opción (la más importante; si depende del área, una por área);
'C' comodín (por si no se puede usar la primera; se numeran en orden).
Las plantillas salen de textos_libreta_v22.py; aquí solo se añaden huecos numerados (números provisionales 91 a 93)
y se reordenan los bloques del 4.1 por frecuencia; después se renumera todo por orden de aparición.
Contenido solo comprobado (normativa en los PDF del repositorio de la programación; efemérides con el nombre de la
instrucción, como en la programación de Gem); los autores se concretarán con los temas.
"""
import copy
import re

import textos_libreta_v22 as T

PLANTILLAS = copy.deepcopy(T.PLANTILLAS)


def _fila(clave, empieza):
    return next(f for f in PLANTILLAS[clave]['filas'] if f['texto'].startswith(empieza))


# huecos nuevos
f = _fila('7.2', 'Alumnado.')
f['texto'] = f['texto'].replace('[perfil: necesidad y fortaleza]', '[91|perfil: necesidad y fortaleza]')
f = _fila('7.3', 'La respuesta a la necesidad')
f['texto'] = f['texto'].replace('[rasgo evolutivo]', '[91|rasgo evolutivo]')
f = _fila('7.6', 'A nivel de aula')
f['texto'] = f['texto'].replace('[n.º] sesiones', '[91|n.º] sesiones')
f = _fila('7.6', 'La situación conecta')
f['texto'] = f['texto'].replace('[la línea general de actuación pedagógica y de concreción curricular o el objetivo',
                                '[92|la línea general de actuación pedagógica y de concreción curricular o el objetivo')

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

D = 'Día'
OPCIONES = {
    '7.1': {
        1: {'ops': [
            ('1', 'Pregunta retórica del tema (sin riesgo de verificación). Lectura: «¿Es posible aprender ciencias, historia '
                  'o matemáticas sin comprender lo que se lee?». Matemáticas: «¿Cómo esperar que el alumnado resuelva '
                  'problemas si no comprende sus enunciados?». Medio ambiente: «¿Cómo esperar que las nuevas generaciones '
                  'protejan el planeta si no aprenden a valorarlo?». Inclusión: «¿Por qué diseñar para un alumno o alumna '
                  '“tipo” si en el aula no existe?». Convivencia: «¿Puede aprender quien no se siente seguro ni aceptado en '
                  'su aula?». Tecnología: «¿Cómo convertir a una generación que consume pantallas en una que crea con ellas '
                  'de forma segura y crítica?». Patrimonio: «¿Qué sabe el alumnado del patrimonio que pisa cada día de '
                  'camino al colegio?».'),
            ('C', 'Dato verificado, solo en supuestos de lectura: PIRLS 2021 (cuarto curso), España obtuvo 521 puntos en '
                  'comprensión lectora, por debajo de la Unión Europea (528) y de la OCDE (533); Andalucía, 523.'),
            ('C', 'Cita literal verificada: «El lenguaje es el vestido del pensamiento» (Samuel Johnson), para lengua; '
                  '«El arte no reproduce lo visible, sino que hace visible» (Paul Klee), para artística.')]},
        2: {'ops': [('1', 'Se concretará con los temas: un autor del tema, de 2020 en adelante.')]},
        3: {'ops': [
            ('F', 'La frase con la LOE y su nombre completo se escribe siempre así.'),
            ('1', 'Artículo 17, objetivo de la etapa relacionado: e) lengua castellana y hábitos de lectura; g) competencias '
                  'matemáticas y resolución de problemas; h) ciencias, geografía, historia y cultura; i) competencias '
                  'tecnológicas; j) representaciones y expresiones artísticas; k) higiene, salud y alimentación; a) '
                  'convivencia; c) resolución pacífica de conflictos; d) igualdad y diversidad; m) afectividad.'),
            ('C', 'Artículo 16.2, finalidad de la etapa: «… que recoge entre las finalidades de la etapa [la expresión y '
                  'comprensión oral, la lectura, la escritura, el cálculo, la convivencia, el sentido artístico, la '
                  'creatividad o la afectividad]».'),
            ('C', 'Artículo 1, principios (equidad e inclusión, b; flexibilidad ante la diversidad, e; esfuerzo compartido '
                  'con las familias, h) o artículo 2.1, fines (resolución pacífica de conflictos, c; creatividad, f; '
                  'interculturalidad, g; hábitos saludables, h; uso seguro de los medios digitales, l).')]},
        4: {'ops': [
            ('F', 'Siempre dos áreas como mínimo: un área eje y otra conectada.'),
            ('1', 'El área que pide el enunciado como eje, con Lengua Castellana y Literatura o Matemáticas como conectada '
                  '(casi siempre están, por su carga horaria).'),
            ('C', 'Educación Artística para el producto final (cartel, vídeo, maqueta, canción).')]},
        5: {'titulo': 'Preíndice', 'ops': [('F', 'Se memoriza tal cual: es igual en todos los supuestos.')]},
    },
    '7.2': {
        1: {'ops': [('1', 'Biblioteca municipal (sirve para casi cualquier tema: lectura, búsqueda de información).'),
                    ('C', 'Talleres gratuitos del ayuntamiento.'),
                    ('C', 'Residencia de mayores (memoria oral, patrimonio, convivencia entre generaciones).'),
                    ('C', 'Centro de interpretación o museo local; asociaciones vecinales y culturales; mercado de abastos, '
                          'parques o polideportivo.')]},
        2: {'ops': [('1', 'Situar al alumnado como protagonista de su aprendizaje mediante metodologías activas que '
                          'potencien la colaboración (encaja con cualquier propuesta).'),
                    ('C', 'Flexibilizar la respuesta educativa para adaptarla a la diversidad de aptitudes, intereses y '
                          'necesidades del alumnado (si el supuesto trae diversidad).'),
                    ('C', 'Impulsar el pensamiento crítico a través de la búsqueda y el análisis de fuentes para resolver '
                          'problemáticas y comunicar hallazgos (investigación, Conocimiento del Medio).'),
                    ('C', 'Fomentar la competencia digital del alumnado mediante el uso crítico y responsable de las '
                          'herramientas y recursos tecnológicos del aula (tecnología).')]},
        3: {'ops': [('1', 'Si es de Lengua: mejorar la comprensión lectora inferencial mediante el tiempo diario de lectura '
                          'planificada y comprobar su progreso con una prueba común trimestral.'),
                    ('1', 'Si es de Matemáticas: mejorar la resolución de problemas mediante un modelo común de pasos en todos '
                          'los ciclos y comprobar su progreso con una prueba común trimestral.'),
                    ('C', 'Desarrollar la competencia socioemocional del alumnado mediante una asamblea semanal de emociones y '
                          'un sociograma trimestral que permita comprobar la mejora de la convivencia.')]},
        4: {'ops': [('1', 'Educación Inclusiva (tipo A, de oficio: vale siempre).'),
                    ('C', 'Plan de Actuación Digital (tipo A, de oficio).'),
                    ('C', 'El programa del tema (tipo B, a solicitud del centro): STEM; Vivir y Sentir el Patrimonio; '
                          'Hábitos de Vida Saludable; Comunica, y si hay radio, con la Red de Radios Escolares de Andalucía '
                          '(tipo C).')]},
        5: {'ops': [('1', 'El grupo está cohesionado y cuenta con líderes positivos.'),
                    ('C', 'Se aprecian dos subgrupos que apenas se relacionan (supuestos de convivencia).'),
                    ('C', 'Un alumno o una alumna apenas recibe elecciones.')]},
        6: {'ops': [('1', 'Curiosidad e interés por el tema del supuesto.'), ('C', 'Buena expresión oral.'),
                    ('C', 'Gusto por el trabajo manipulativo y en equipo.')]},
        91: {'ops': [('F', 'Necesidad + fortaleza + fuente del dato, nunca la etiqueta sola.'),
                     ('1', 'Si el enunciado no trae diversidad, un solo perfil sencillo y bien conocido: alumno con trastorno '
                           'por déficit de atención e hiperactividad.'),
                     ('C', 'Alumna con dificultad específica en la lectura.'),
                     ('C', 'Alumnado de incorporación tardía.')]},
    },
    '7.3': {
        1: {'ops': [('1', 'Se concretarán con los temas: dos autores muy específicos del tema, de 2020 en adelante.')]},
        91: {'ops': [('1', 'Transita de las operaciones concretas al pensamiento formal, por lo que se combinan actividades '
                           'manipulativas con otras de mayor abstracción.')]},
        2: {'titulo': 'Normativa fija', 'ops': [
            ('F', 'Se memoriza: artículo 10.2 del Real Decreto 157/2022 (el equipo docente planifica situaciones de '
                  'aprendizaje para adquirir las competencias clave y las específicas) y artículo 7.3 del Decreto '
                  '101/2023 (equipos docentes coordinados y enfoque interdisciplinar, integrador y holístico). Sin '
                  'principios pedagógicos: van en metodología.')]},
        3: {'titulo': 'En lugar del 10.2', 'ops': [
            ('C', 'Los retos del siglo XXI del anexo I del Real Decreto 157/2022 (se elige el del supuesto): medio ambiente y '
                  'maltrato animal; consumo responsable; vida saludable; inequidad y exclusión; resolución pacífica de los '
                  'conflictos; cultura digital ética y responsable; la incertidumbre como oportunidad creativa; convivir '
                  'valorando la diversidad; sentirse parte de un proyecto colectivo; aprender a lo largo de la vida.')]},
        4: {'ops': [
            ('1', 'Si es de Lengua o de otra área con lectura: Instrucciones de 21 de junio de 2023, de la Viceconsejería de '
                  'Desarrollo Educativo y Formación Profesional, sobre el tratamiento de la lectura para el despliegue de '
                  'la competencia en comunicación lingüística en Educación Primaria y Educación Secundaria Obligatoria, '
                  'que garantizan un tiempo diario de lectura no inferior a treinta minutos, con antes, durante y después.'),
            ('1', 'Si es de Matemáticas: Instrucciones de 18 de junio de 2024, de la Viceconsejería de Desarrollo Educativo '
                  'y Formación Profesional, sobre las medidas para el fomento del razonamiento matemático a través del '
                  'planteamiento y resolución de retos y problemas en Educación Infantil, Educación Primaria y Educación '
                  'Secundaria Obligatoria, con un itinerario de problemas de dificultad creciente y pasos comunes.'),
            ('C', 'Biblioteca: Instrucciones de 10 de septiembre de 2025, sobre la organización y funcionamiento de las '
                  'bibliotecas escolares (la biblioteca como recurso para la mediación lectora, la alfabetización mediática '
                  'e informacional y la inclusión), con el programa Bibliotecas Escolares y el Plan de Fomento de la '
                  'Lectura 2026-2030 (Ministerio de Cultura, 2026).')]},
    },
    '7.5': {
        1: {'ops': [('F', 'Solo se cita la línea o el objetivo descrito en el contexto, con su nombre completo.'),
                    ('1', 'Detectado en la memoria de autoevaluación.'), ('C', 'Detectado en la evaluación inicial.')]},
        2: {'ops': [('1', 'Trabajar en todo el centro [centro de interés] en torno a [efeméride]; cada ciclo lo adapta.'),
                    ('C', 'Incorporar un itinerario común de lectura o de resolución de problemas (supuestos de lengua o de '
                          'matemáticas).')]},
        3: {'ops': [('1', 'Producto final común, reparto de sesiones entre áreas y rúbrica compartida.'),
                    ('C', 'La misma situación en las dos líneas del curso, que presentan juntas el producto.')]},
        4: {'ops': [('1', 'Ajustar las medidas del DUA para [perfil]: agenda visual, roles cooperativos.'),
                    ('1', 'PT en las sesiones de cálculo; AL en el ensayo de la exposición oral.'),
                    ('1', 'Seguimiento quincenal con indicadores: termina la tarea, participa con su rol.')]},
        5: {'ops': [('1', 'Biblioteca escolar.'), ('C', 'Sala de usos múltiples.'),
                    ('C', 'Huerto o carro de portátiles; del entorno, los del contexto (biblioteca municipal, residencia).')]},
        6: {'titulo': 'Los seis criterios pedagógicos (artículo 21.3.c)', 'ops': [
            ('F', 'Evaluación y promoción del alumnado; tiempo escolar y extraescolar; agrupamientos y tutorías; oferta de '
                  'áreas; atención a la diversidad y tránsito entre etapas; órganos de coordinación docente. En el supuesto '
                  'se usan para la actividad complementaria (tiempo escolar y extraescolar), el recurso digital y la '
                  'cultura andaluza.')]},
        7: {'ops': [('1', 'Visita a la biblioteca municipal, con autorización de las familias por iPasen.'),
                    ('C', 'Salida a un centro de interpretación o a un espacio natural de la comarca.'),
                    ('C', 'Visita a la entidad que lanza el reto o recibe el producto (residencia, asociación, ayuntamiento).')]},
        8: {'ops': [('1', 'Google Classroom, como plataforma común del centro.'),
                    ('C', 'Canva o Book Creator para el producto.'), ('C', 'Padlet para compartir hallazgos.')]},
        9: {'ops': [('1', f'{D} de Andalucía (28 de febrero).'), ('C', f'El flamenco ({D} del Flamenco, 16 de noviembre).'),
                    ('C', 'La modalidad lingüística andaluza o el patrimonio y las leyendas del pueblo.')]},
        10: {'ops': [('1', 'Reunión inicial e iPasen para informar; participación en una actividad o en la difusión del '
                           'producto.'),
                     ('C', 'Tutoría de tarde; la persona delegada de madres y padres difunde el producto; el ayuntamiento '
                           'lanza el reto y lo recibe.')]},
        12: {'ops': [('1', 'Música compone la canción de la campaña.'),
                     ('C', 'Educación Física organiza una ruta a pie; Inglés traduce los eslóganes.')]},
        13: {'ops': [('1', 'Si es de Lengua: los treinta minutos diarios de lectura, con textos del tema.'),
                     ('1', 'Si es de Matemáticas: los siete pasos comunes de resolución de problemas (situación cercana y '
                           'diálogo; comprender datos y pregunta; elegir estrategia; aplicar y calcular; colores; comprobar; '
                           'comunicar el proceso).')]},
        11: {'ops': [('F', 'Solo si hay vídeo, fotos o difusión en la web.'),
                     ('1', 'Quien no tenga autorización participa con voz en off o con un avatar.'),
                     ('C', 'Se graba con las tabletas del centro, nunca con móviles personales.')]},
        14: {'ops': [('1', 'En el comedor, el grupo mide el agua que sobra en las mesas.'),
                     ('C', 'En el aula matinal, se juega al juego que ha creado la clase.')]},
        15: {'ops': [('F', 'Solo en el tercer ciclo: la hora de autonomía del centro puede dedicarse a proyectos '
                           'interdisciplinares.')]},
    },
    '7.6': {
        91: {'ops': [('1', '12 sesiones en 3 o 4 semanas (lo más habitual).'), ('C', 'Entre 8 y 15 sesiones.')]},
        1: {'ops': [('1', 'Las cuatro más útiles, según el tema: Día de Andalucía (28 de febrero), patrimonio; Día Escolar de '
                          'la No-violencia y la Paz (30 de enero), convivencia; Día Internacional del Libro (23 de abril), '
                          'lectura; Día del Medio Ambiente (5 de junio), sostenibilidad.'),
                    ('C', 'Día de la Lectura en Andalucía (16 de diciembre); Día Internacional de la Mujer y la Niña en la '
                          'Ciencia (11 de febrero); Día Internacional contra el Acoso y el Ciberacoso (2 de mayo).'),
                    ('C', 'Día del Flamenco (16 de noviembre); Día Mundial de la Salud Mental (10 de octubre); Día de la '
                          'Constitución Española (6 de diciembre).')]},
        2: {'ops': [('1', 'El del tema: 3 Salud y bienestar; 5 Igualdad de género; 6 Agua limpia y saneamiento; 11 Ciudades '
                          'y comunidades sostenibles; 12 Producción y consumo responsables; 13 Acción por el clima; 16 Paz, '
                          'justicia e instituciones sólidas.'),
                    ('C', 'ODS 4, Educación de calidad, que encaja con cualquier propuesta educativa.')]},
        92: {'ops': [('F', 'La misma línea u objetivo del contexto, con su nombre completo.')]},
    },
    '7.7': {
        1: {'ops': [('1', 'Según el área eje: Lengua, e) lengua castellana y hábitos de lectura; Matemáticas, g) competencias '
                          'matemáticas y resolución de problemas; Conocimiento del Medio, h) ciencias, historia y patrimonio '
                          'de Andalucía; Artística, j) representaciones y expresiones artísticas.'),
                    ('C', 'b) hábitos de trabajo individual y de equipo, esfuerzo y espíritu emprendedor (sirve para '
                          'cualquier propuesta).'),
                    ('C', 'ñ) modalidad lingüística andaluza u o) patrimonio cultural de Andalucía (si hay patrimonio o habla '
                          'andaluza).')]},
        2: {'titulo': 'Orden de 30 de mayo de 2023', 'ops': [('F', 'Se memoriza: es su primera mención, con el nombre '
                                                                   'completo.')]},
        3: {'ops': [('1', 'La competencia del área eje en la tabla de abajo, con su criterio de quinto, su saber y sus dos '
                          'descriptores.')]},
        4: {'ops': [('F', 'Solo la competencia específica, resumida en una línea; nunca una sola área.'),
                    ('1', 'Lengua o Matemáticas (casi siempre están). Ejemplo: «Asimismo, desde Lengua Castellana y Literatura '
                          'se desarrolla la competencia específica 5, que persigue producir textos escritos y multimodales '
                          'coherentes».'),
                    ('C', 'Educación Artística, si el producto es artístico (competencia específica 3).')]},
    },
    '7.8': {
        1: {'ops': [('F', 'Los tres principios van siempre: DUA, Andalucía y digital.'),
                    ('1', 'Agenda visual de cada sesión.'),
                    ('C', 'Consignas con pictogramas de ARASAAC; elegir el formato del producto final; glosario visual.')]},
        2: {'ops': [('1', 'El patrimonio y las leyendas del pueblo, trabajados en el entorno.'),
                    ('C', 'El Día de Andalucía; el flamenco; el habla andaluza.')]},
        3: {'ops': [('1', 'Canva o Book Creator para elaborar el producto.'),
                    ('C', 'Padlet para compartir hallazgos; Kahoot para activar las ideas previas.')]},
        4: {'ops': [('1', 'Aprendizaje-servicio (Batlle, 2020): el aprendizaje curricular, al servicio de una necesidad real '
                          'de la comunidad; el producto es el servicio.'),
                    ('C', 'Aprendizaje basado en proyectos (Vergara, 2021): investigar un reto real hasta un producto con '
                          'destinatario.'),
                    ('C', 'Aprendizaje basado en retos (Universidad Politécnica de Madrid, 2020): idea general, pregunta '
                          'esencial y reto.'),
                    ('C', 'Gamificación (Vázquez y Sevillano, 2022), como apoyo: narrativa, misiones, insignias y niveles. '
                          'Aula invertida (Rodríguez et al., 2021), solo si el enunciado la impone.')]},
        5: {'ops': [('1', 'Individual: lectura y ticket de salida. Entre iguales: tutoría entre iguales.'),
                    ('C', 'Individual: diario de aprendizaje. Entre iguales: «dos aciertos y una mejora».')]},
        6: {'ops': [('1', '1-2-4 (individual, parejas y equipo hasta una respuesta común) y folio giratorio (el folio pasa '
                          'por el equipo y cada uno añade su aportación).'),
                    ('C', 'Lápices al centro (se debate sin escribir; después cada uno escribe lo acordado); rally coach (por '
                          'parejas, uno resuelve y otro entrena).'),
                    ('C', 'Cabezas numeradas (el azar decide quién explica); rompecabezas o expertos (cada uno prepara una '
                          'parte y la explica a su equipo).')]},
        7: {'ops': [('1', 'Una idea ★ del área eje en la tabla de orientaciones de abajo.'),
                    ('C', 'Otra idea del mismo área en la misma tabla.')]},
    },
    '7.9': {
        1: {'ops': [('1', 'Manipulativos: regletas, bloques multibase, ábaco, material de medida.'),
                    ('C', 'Impresos y del entorno: prensa, infografías, cartas reales, mural de los pasos de los problemas.')]},
        2: {'ops': [('1', 'Canva o Book Creator para el producto final.'),
                    ('C', 'Padlet para los hallazgos; Kahoot o Mentimeter para las ideas previas; Genially para presentar.'),
                    ('C', 'GeoGebra (geometría), Scratch (programar), ARASAAC y Lector inmersivo (accesibilidad), Google '
                          'Classroom (entregas).')]},
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
            OPCIONES[clave] = {mapa[k]: v for k, v in OPCIONES[clave].items() if k in mapa}


renumera()
