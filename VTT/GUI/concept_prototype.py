from nicegui import ui
import copy
import json
import inspect

# ==========================================
# 1. BASE DE DATOS Y ESTADO DE LA APLICACIÓN
# ==========================================
atributos = {
    "Físicos": {"Fuerza": 1, "Destreza": 1, "Resistencia": 1},
    "Sociales": {"Carisma": 1, "Manipulación": 1, "Apariencia": 1},
    "Mentales": {"Percepción": 1, "Inteligencia": 1, "Astucia": 1}
}

habilidades = {
    "Talentos": ["Alerta", "Atletismo", "Callejeo", "Consciencia", "Empatía", "Expresión", "Intimidación", "Liderazgo", "Pelea", "Subterfugio"],
    "Técnicas": ["Armas de Fuego", "Artesanía", "Conducir", "Etiqueta", "Interpretación", "Latrocinio", "Pelea con Armas", "Sigilo", "Supervivencia", "T.c. Animales"],
    "Conocimientos": ["Academicismo", "Ciencias", "Finanzas", "Informática", "Investigación", "Leyes", "Medicina", "Ocultismo", "Política", "Tecnología"]
}

ventajas_valores = {
    "Disciplinas": {0: 0, 1: 0, 2: 0},
    "Trasfondos": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
    "Virtudes": {"Conciencia": 1, "Autocontrol": 1, "Coraje": 1} 
}

prioridades_attr = {"Físicos": None, "Sociales": None, "Mentales": None}
prioridades_hab = {"Talentos": None, "Técnicas": None, "Conocimientos": None}

fase_creacion = {"estado": "base"}
puntos_gratuitos = {"restantes": 15}

habilidades_valores = {
    "Talentos": {h: 0 for h in habilidades["Talentos"]},
    "Técnicas": {h: 0 for h in habilidades["Técnicas"]},
    "Conocimientos": {h: 0 for h in habilidades["Conocimientos"]}
}

especializaciones = {
    "Talentos": {h: "" for h in habilidades["Talentos"]},
    "Técnicas": {h: "" for h in habilidades["Técnicas"]},
    "Conocimientos": {h: "" for h in habilidades["Conocimientos"]}
}

# NUEVO: Guardamos las compras directas de derivados hechas con Puntos Gratuitos
mejoras_derivados = {
    "Humanidad": 0
}

selects_prioridad = {}
selects_prioridad_hab = {}
contenedores_atributos = {}
contenedores_habilidades = {}
contenedores_derivados = {}
contenedores_ventajas = {}
labels_contadores_attr = {}
labels_contadores_hab = {}

clan_seleccionado = {"nombre": None}
valores_base_fijos = {}
label_puntos_gratuitos = {"ui": None}

datos_concepto = {
    "Nombre": "", "Jugador": "", "Crónica": "", "Naturaleza": "",
    "Conducta": "", "Concepto": "", "Generación": "", "Sire": ""
}

datos_concepto = {
    "Nombre": "", "Jugador": "", "Crónica": "", "Naturaleza": "",
    "Conducta": "", "Concepto": "", "Generación": "", "Sire": "",
    "Detalle_Debilidad": "" # NUEVO: Guarda el texto de la debilidad
}

# NUEVO: Define qué clanes requieren un campo de texto extra obligatorio
requisitos_debilidad = {
    "Malkavian": "Trastorno Mental",
    "Ravnos": "Vicio o Crimen",
    "Tzimisce": "Objeto de Apego",
    "Ventrue": "Restricción de Sangre"
}

# NUEVO: Costes en puntos de Trasfondo para cada Generación
costes_generacion = {
    "13ª Generación": 0,
    "12ª Generación": 1,
    "11ª Generación": 2,
    "10ª Generación": 3,
    "9ª Generación": 4,
    "8ª Generación": 5
}

nombres_ventajas = {
    "Disciplinas": {"0": "", "1": "", "2": ""},
    "Trasfondos": {"0": "", "1": "", "2": "", "3": "", "4": ""}
}
referencias_ui = {"clan_select": None, "texto_guia": None, "resumen_dialog": None, "resumen_markdown": None}


# ==========================================
# 2. DICCIONARIOS DE LORE 
# ==========================================
# (Mantenemos los diccionarios limpios y sin cambios)
lore_clanes = {
    "Assamita": "Los Asesinos y jueces de la Estirpe, originarios de Oriente Medio. Operan de forma independiente y son temidos por su maestría en el asesinato y su sed de sangre vampírica.\n\n• Disciplinas: Celeridad, Extinción, Ofuscación.\n• Debilidad: Adicción a la sangre vampírica (Vitae). Si prueban la sangre de otro vampiro, corren el riesgo de volverse adictos a ella.",
    "Brujah": "Los Brujah son rebeldes, apasionados y violentos. Antaño fueron reyes filósofos en Cartago, pero hoy son conocidos por su furia y su lucha contra el orden establecido.\n\n• Disciplinas: Celeridad, Potencia, Presencia.\n• Debilidad: Su sangre hierve fácilmente; la dificultad de las tiradas para resistir el frenesí aumenta en 2.",
    "Gangrel": "Solitarios y nómadas, son los vampiros más cercanos a su Bestia interior y a la naturaleza. A menudo prefieren la compañía de los animales a la de otros vampiros.\n\n• Disciplinas: Animalismo, Fortaleza, Protean.\n• Debilidad: Cada vez que entran en frenesí, adquieren un rasgo animal temporal o permanente.",
    "Giovanni": "Un clan hermético compuesto por una única familia mortal de nigromantes venecianos. Están obsesionados con la riqueza, el poder y el control de las almas de los muertos.\n\n• Disciplinas: Dominación, Nigromancia, Potencia.\n• Debilidad: Su Mordisco es insoportablemente doloroso en lugar de placentero. Infligen daño extra al alimentarse.",
    "Lasombra": "Líderes natos, despiadados y aristocráticos. Creen en el darwinismo social y en gobernar desde las sombras, siendo el principal clan dirigente de la secta del Sabbat.\n\n• Disciplinas: Dominación, Obtenebración, Potencia.\n• Debilidad: No tienen reflejo. No aparecen en espejos, cámaras de seguridad ni superficies reflectantes.",
    "Malkavian": "Todos los miembros de este clan están irremediablemente locos, pero su locura a menudo les otorga una visión profética y una sabiduría incomprensible para el resto de la Estirpe.\n\n• Disciplinas: Auspex, Dementación, Ofuscación.\n• Debilidad: Comienzan con un trastorno mental permanente que no puede ser curado con Fuerza de Voluntad.",
    "Nosferatu": "Sufren la Maldición de Caín en su propia carne. El Abrazo los deforma monstruosamente. Aislados en las alcantarillas, son los grandes espías y traficantes de secretos.\n\n• Disciplinas: Animalismo, Ofuscación, Potencia.\n• Debilidad: Apariencia cero. Jamás pueden aumentar este atributo debido a su deformidad física.",
    "Ravnos": "Nómadas, embaucadores y maestros de las ilusiones. A menudo son marginados y vistos con desconfianza debido a su reputación de estafadores y vividores.\n\n• Disciplinas: Animalismo, Fortaleza, Quimerismo.\n• Debilidad: Tienen un vicio o crimen específico (como robar, mentir o apostar) del que les cuesta mucho resistirse.",
    "Seguidores de Set": "Adoradores de un antiguo dios-serpiente. Son maestros de la corrupción, los secretos ocultos y los vicios, buscando siempre seducir a otros hacia la oscuridad.\n\n• Disciplinas: Ofuscación, Presencia, Serpentis.\n• Debilidad: Extremadamente sensibles a la luz. Reciben daño agravado adicional de la luz solar y sufren bajo focos intensos.",
    "Toreador": "Artistas, seductores y hedonistas. Se obsesionan con la belleza y la cultura humana, siendo el clan más integrado en la alta sociedad mortal.\n\n• Disciplinas: Auspex, Celeridad, Presencia.\n• Debilidad: Pueden quedar extasiados al contemplar algo verdaderamente hermoso, perdiendo la noción del entorno.",
    "Tremere": "Un clan de hechiceros de la sangre y antiguos magos que robaron la inmortalidad. Son estrictos, organizados y sumamente desconfiados con los demás clanes.\n\n• Disciplinas: Auspex, Dominación, Taumaturgia.\n• Debilidad: Su sangre está muy controlada. Todos los neófitos dan un paso hacia el Vínculo de Sangre con el consejo gobernante de los Siete al ser Abrazados.",
    "Tzimisce": "Eruditos inhumanos, monstruosos y maestros de la carne. Consideran que han superado los límites humanos y moldean los cuerpos de sus víctimas a su antojo.\n\n• Disciplinas: Animalismo, Auspex, Vicisitud.\n• Debilidad: Apego a su tierra. Deben descansar rodeados de al menos dos puñados de tierra de un lugar importante para ellos.",
    "Ventrue": "Los Ventrue son la realeza de los Condenados. Dirigen la Camarilla y valoran el linaje, el éxito corporativo y la influencia en la sociedad mortal por encima de todo.\n\n• Disciplinas: Dominación, Fortaleza, Presencia.\n• Debilidad: Gusto refinado y exclusivo. Solo pueden beber sangre de un tipo específico de mortal."
}

lore_conceptos = {
    "Naturaleza": "La Naturaleza es el verdadero 'yo' de tu personaje, su personalidad más profunda y auténtica. En términos de juego, recuperas puntos de Fuerza de Voluntad cuando actúas de acuerdo a tu Naturaleza.",
    "Conducta": "La Conducta es la máscara o fachada que tu vampiro presenta al mundo. Es cómo te perciben los demás. En la traicionera sociedad de la Estirpe, mostrar tu verdadera Naturaleza es peligroso, por lo que la Conducta suele ser diferente.",
    "Generación": "La Generación indica a qué distancia está tu vampiro de Caín, el Primero. Los jugadores suelen empezar en la 13ª Generación. Cuanto más baja es, más poderosa es tu sangre, pero para ello debes comprar el Trasfondo 'Generación'."
}

lore_atributos = {
    "Fuerza": "Fuerza (Físico)\n\nMide la potencia muscular pura. Determina cuánto peso puedes levantar, tu rendimiento en proezas físicas y la cantidad de daño que infliges al golpear cuerpo a cuerpo.",
    "Destreza": "Destreza (Físico)\n\nDefine tu agilidad, reflejos y coordinación. Es fundamental para esquivar ataques, moverse con sigilo y determinar la precisión con armas de fuego o ataques físicos.",
    "Resistencia": "Resistencia (Físico)\n\nRefleja tu dureza y salud general. Determina cuánto castigo físico y daño puedes absorber antes de caer incapacitado, además de tu capacidad para resistir venenos o enfermedades.",
    "Carisma": "Carisma (Social)\n\nEs tu encanto innato, tu magnetismo y tu capacidad para caer bien y ganarte la confianza de los demás de forma natural. Un personaje carismático lidera inspirando a los demás.",
    "Manipulación": "Manipulación (Social)\n\nEs el arte de hacer que los demás hagan lo que tú quieres. Implica engaño, coacción, extorsión o seducción calculada. Es liderar mediante hilos invisibles.",
    "Apariencia": "Apariencia (Social)\n\nMide tu atractivo físico puro y tu presencia visual. Determina la primera impresión que causas en los demás antes de hablar. (Recuerda: Los Nosferatu siempre tienen 0).",
    "Percepción": "Percepción (Mental)\n\nEs tu capacidad para notar lo que pasa a tu alrededor. Define tu nivel de alerta ante emboscadas, tu ojo para los detalles ocultos y tu intuición para saber si alguien te está mintiendo.",
    "Inteligencia": "Inteligencia (Mental)\n\nRefleja tu memoria, capacidad de razonamiento lógico y asimilación de conocimientos. Se usa para resolver acertijos complejos, recordar datos eruditos o comprender sistemas tecnológicos y mágicos.",
    "Astucia": "Astucia (Mental)\n\nEs tu agilidad mental y tu 'sabiduría de la calle'. Mide lo rápido que reaccionas ante situaciones inesperadas, tu ingenio para dar respuestas cortantes y tu capacidad para improvisar bajo presión."
}

lore_opciones_concepto = {
    "13ª Generación": "La generación más común para neonatos. \n• Capacidad de Sangre: 10\n• Puntos por turno: 1\n• Coste: 0 puntos de Trasfondo.",
    "12ª Generación": "Tu sangre es un poco más fuerte. \n• Capacidad de Sangre: 11\n• Puntos por turno: 1\n• Coste: 1 punto de Trasfondo (Generación).",
    "11ª Generación": "Un paso más cerca de Caín. \n• Capacidad de Sangre: 12\n• Puntos por turno: 1\n• Coste: 2 puntos de Trasfondo (Generación).",
    "10ª Generación": "Tu sangre empieza a ser respetable. \n• Capacidad de Sangre: 13\n• Puntos por turno: 1\n• Coste: 3 puntos de Trasfondo (Generación).",
    "9ª Generación": "Sangre poderosa. \n• Capacidad de Sangre: 14\n• Puntos por turno: 2\n• Coste: 4 puntos de Trasfondo (Generación).",
    "8ª Generación": "El límite para un personaje inicial. Eres notablemente poderoso. \n• Capacidad de Sangre: 15\n• Puntos por turno: 3\n• Coste: 5 puntos de Trasfondo (Generación).",
    "Ansioso": "Vives para el riesgo y la adrenalina. Recuperas 1 punto de Fuerza de Voluntad cuando realizas una tarea peligrosa y sobrevives sin rasguños.",
    "Arquitecto": "Tu sentido de la vida es construir un legado. Recuperas 1 punto de Fuerza de Voluntad cuando estableces algo de importancia o valor duradero.",
    "Autócrata": "Necesitas tener el control absoluto de la situación. Recuperas 1 punto de Fuerza de Voluntad cuando consigues el control sobre un grupo o una crisis.",
    "Bizarro": "Estás orgulloso de ser un marginado o diferente. Recuperas 1 punto de Fuerza de Voluntad cuando ignoras las normas sociales impunemente.",
    "Bribón": "Solo te importas tú mismo. Recuperas 1 punto de Fuerza de Voluntad cuando tu actitud egoísta te salva de perder algo o te proporciona una ventaja.",
    "Bufón": "Eres el eterno bromista, incluso en el peligro. Recuperas 1 punto de Fuerza de Voluntad cuando logras levantar el ánimo de los demás o escapas usando el humor.",
    "Capitalista": "Todo tiene un precio. Recuperas 1 punto de Fuerza de Voluntad cuando realizas un negocio o intercambio altamente beneficioso para ti.",
    "Celebrante": "Encuentras tu alegría en una causa o pasión. Recuperas 1 punto de Fuerza de Voluntad cuando persigues tu causa o disfrutas abiertamente de lo que amas.",
    "Competidor": "Vives para ganar. Recuperas 1 punto de Fuerza de Voluntad cuando ganas una competición o superas a un rival en algo importante.",
    "Conformista": "Prefieres seguir antes que liderar. Recuperas 1 punto de Fuerza de Voluntad cuando el grupo o tu líder logra un objetivo gracias a tu apoyo.",
    "Creador": "Sientes la necesidad de dar forma a lo nuevo. Recuperas 1 punto de Fuerza de Voluntad cuando creas un objeto o concepto de verdadero valor.",
    "Cuidador": "Sientes la necesidad de proteger a los demás. Recuperas 1 punto de Fuerza de Voluntad cuando proteges o sanas a alguien que lo necesita.",
    "Defensor": "Eres el escudo de algo mayor. Recuperas 1 punto de Fuerza de Voluntad cuando tu defensa de una persona, grupo o ideal tiene éxito bajo presión.",
    "Director": "Odias el caos y amas el orden. Recuperas 1 punto de Fuerza de Voluntad cuando logras liderar a un grupo y completar una tarea difícil.",
    "Enigma": "Tus motivos son un misterio. Recuperas 1 punto de Fuerza de Voluntad cuando tus acciones dejan perplejo a alguien o deduces algo oculto.",
    "Fanático": "Consumes tu existencia por una causa suprema. Recuperas 1 punto de Fuerza de Voluntad cuando logras avanzar significativamente en tu causa.",
    "Galán": "Eres deslumbrante y amas ser el centro de atención. Recuperas 1 punto de Fuerza de Voluntad cuando logras impresionar enormemente a otra persona.",
    "Gurú": "Tu sabiduría es tu guía. Recuperas 1 punto de Fuerza de Voluntad cuando alguien busca tu consejo espiritual o filosófico y este le resulta útil.",
    "Juez": "Buscas la verdad y el equilibrio. Recuperas 1 punto de Fuerza de Voluntad cuando resuelves una disputa de forma justa o separas la verdad de la mentira.",
    "Mártir": "Sufres por los demás. Recuperas 1 punto de Fuerza de Voluntad cuando te sacrificas de forma genuina por otro o por un ideal.",
    "Monstruo": "Has abrazado la Bestia interior. Recuperas 1 punto de Fuerza de Voluntad cuando realizas un acto verdaderamente atroz sin mostrar remordimientos.",
    "Niño": "Aún buscas la protección que perdiste. Recuperas 1 punto de Fuerza de Voluntad cuando alguien te consuela, ayuda o asume tus responsabilidades.",
    "Pedagogo": "Vives para enseñar. Recuperas 1 punto de Fuerza de Voluntad cuando alguien aprende algo importante y saca provecho de tus enseñanzas.",
    "Penitente": "Sientes que no mereces el perdón. Recuperas 1 punto de Fuerza de Voluntad cuando tu sufrimiento sirve para expiar una de tus malas acciones.",
    "Perfeccionista": "Solo toleras lo impecable. Recuperas 1 punto de Fuerza de Voluntad cuando logras hacer algo a la perfección, sin un solo error.",
    "Rebelde": "La autoridad está para desafiarla. Recuperas 1 punto de Fuerza de Voluntad cuando tus acciones de rebeldía contra el sistema tienen éxito.",
    "Sádico": "Vives para causar dolor. Recuperas 1 punto de Fuerza de Voluntad cuando infliges sufrimiento físico o emocional a alguien sin sufrir repercusiones.",
    "Solitario": "No necesitas a nadie. Recuperas 1 punto de Fuerza de Voluntad cuando logras un objetivo importante por tus propios medios, sin depender de otros.",
    "Sobreviviente": "Nada puede acabar contigo. Recuperas 1 punto de Fuerza de Voluntad cuando sobrevives a una amenaza extrema mediante tu astucia o resistencia.",
    "Tradicionalista": "El pasado contiene las respuestas. Recuperas 1 punto de Fuerza de Voluntad cuando los métodos probados y antiguos demuestran ser los mejores.",
    "Visionario": "Ves más allá del presente. Recuperas 1 punto de Fuerza de Voluntad cuando das un paso importante hacia tu visión de futuro o convences a otros de ella."
}

lore_habilidades = {
    "Alerta": "Alerta (Talento)\n\nSentidos básicos y percepción instintiva. Se usa para notar emboscadas o escuchar ruidos extraños.",
    "Atletismo": "Atletismo (Talento)\n\nCapacidad física general: correr, saltar, trepar o nadar.",
    "Callejeo": "Callejeo (Talento)\n\nConocimiento de los bajos fondos, las reglas de la calle y cómo conseguir información en la ciudad.",
    "Consciencia": "Consciencia (Talento)\n\nSensibilidad mística para detectar el uso de Disciplinas, magia o presencias sobrenaturales.",
    "Empatía": "Empatía (Talento)\n\nCapacidad de comprender y sentir las emociones de los demás. Ayuda a saber si alguien miente.",
    "Expresión": "Expresión (Talento)\n\nHabilidad para comunicar ideas de forma elocuente, ya sea escribiendo, hablando o actuando.",
    "Intimidación": "Intimidación (Talento)\n\nEl arte de asustar y dominar a los demás mediante amenazas físicas, psicológicas o pura presencia.",
    "Liderazgo": "Liderazgo (Talento)\n\nCapacidad de dirigir y motivar a grupos de personas. Un buen líder mantiene la moral alta.",
    "Pelea": "Pelea (Talento)\n\nCombate cuerpo a cuerpo sin armas. Incluye artes marciales, boxeo o peleas de bar.",
    "Subterfugio": "Subterfugio (Talento)\n\nEl arte del engaño, la intriga y la manipulación social. Útil para ocultar intenciones o seducir.",
    "Armas de Fuego": "Armas de Fuego (Técnica)\n\nHabilidad para usar, limpiar y reparar armas de fuego, desde pistolas hasta rifles.",
    "Artesanía": "Artesanía (Técnica)\n\nHabilidad para crear, reparar o modificar objetos con las manos (carpintería, herrería, etc.).",
    "Conducir": "Conducir (Técnica)\n\nHabilidad para manejar vehículos en situaciones extremas (persecuciones, evasión).",
    "Etiqueta": "Etiqueta (Técnica)\n\nSaber cómo comportarse en la alta sociedad, ya sea en una gala o en el Elíseo.",
    "Interpretación": "Interpretación (Técnica)\n\nHabilidad para actuar, cantar, tocar instrumentos o entretener a un público.",
    "Latrocinio": "Latrocinio (Técnica)\n\nHabilidades de los ladrones: forzar cerraduras, robar bolsillos y desactivar alarmas.",
    "Pelea con Armas": "Pelea con Armas (Técnica)\n\nCombate utilizando armas blancas (espadas, cuchillos, bates, estacas).",
    "Sigilo": "Sigilo (Técnica)\n\nHabilidad para moverse sin hacer ruido, ocultarse en las sombras y pasar desapercibido.",
    "Supervivencia": "Supervivencia (Técnica)\n\nSaber cómo sobrevivir en la naturaleza: orientarse, encontrar refugio y evitar peligros.",
    "T.c. Animales": "Trato con Animales (Técnica)\n\nCapacidad para calmar, adiestrar y comprender a los animales.",
    "Academicismo": "Academicismo (Conocimiento)\n\nConocimiento de humanidades: historia, literatura, arte y cultura general.",
    "Ciencias": "Ciencias (Conocimiento)\n\nConocimientos de ciencias empíricas: física, química, biología, matemáticas.",
    "Finanzas": "Finanzas (Conocimiento)\n\nComprensión de la economía, contabilidad, mercado de valores y movimiento de dinero.",
    "Informática": "Informática (Conocimiento)\n\nHabilidad para programar, hackear y operar sistemas informáticos avanzados.",
    "Investigación": "Investigación (Conocimiento)\n\nCapacidad para buscar información en archivos, bibliotecas o la escena de un crimen.",
    "Leyes": "Leyes (Conocimiento)\n\nConocimiento del sistema judicial y legal mortal, así como de los resquicios legales.",
    "Medicina": "Medicina (Conocimiento)\n\nConocimiento de anatomía, primeros auxilios, diagnóstico y cirugía.",
    "Ocultismo": "Ocultismo (Conocimiento)\n\nConocimiento de mitos, leyendas, magia, sectas y criaturas sobrenaturales.",
    "Política": "Política (Conocimiento)\n\nConocimiento de la estructura de poder local y nacional, tanto mortal como de la Estirpe.",
    "Tecnología": "Tecnología (Conocimiento)\n\nConocimiento de ingeniería, electrónica y diseño de maquinaria moderna."
}

lore_ventajas = {
    "Conciencia": "Conciencia (Virtud)\n\nMide tu capacidad para sentir remordimiento y distinguir lo correcto de lo incorrecto. Es vital para mantener tu Humanidad frente a la Bestia.",
    "Autocontrol": "Autocontrol (Virtud)\n\nDefine tu disciplina emocional. Te permite resistir el frenesí cuando la Bestia se ve provocada por hambre, ira o humillación.",
    "Coraje": "Coraje (Virtud)\n\nTu entereza ante el miedo, el sol y el fuego (el Rötschreck). Además, tu puntuación en Coraje determinará tu Fuerza de Voluntad inicial.",
    "Disciplinas": "Disciplinas\n\nSon los poderes sobrenaturales de tu sangre vampírica. En la creación, tienes 3 puntos para repartir entre las Disciplinas propias de tu Clan.",
    "Trasfondos": "Trasfondos\n\nRepresentan lo que posees en el mundo mortal y de la Estirpe: Recursos (dinero), Aliados, Contactos, Generación, Mentor, Rebaño... Tienes 5 puntos a repartir.",
    "Humanidad": "Humanidad\n\nMide tu moralidad y tu ancla con la vida mortal. Inicialmente se calcula sumando tu Conciencia y tu Autocontrol. Si llega a 0, la Bestia toma el control.",
    "Fuerza de Voluntad": "Fuerza de Voluntad\n\nTu determinación y fuerza mental. Se usa para resistir poderes sobrenaturales, ignorar heridas o asegurar un éxito crítico. Su valor inicial es igual a tu Coraje."
}

# NUEVO DICCIONARIO: Relaciona cada clan con sus disciplinas oficiales
disciplinas_por_clan = {
    "Assamita": ["Celeridad", "Extinción", "Ofuscación"],
    "Brujah": ["Celeridad", "Potencia", "Presencia"],
    "Gangrel": ["Animalismo", "Fortaleza", "Protean"],
    "Giovanni": ["Dominación", "Nigromancia", "Potencia"],
    "Lasombra": ["Dominación", "Obtenebración", "Potencia"],
    "Malkavian": ["Auspex", "Dementación", "Ofuscación"],
    "Nosferatu": ["Animalismo", "Ofuscación", "Potencia"],
    "Ravnos": ["Animalismo", "Fortaleza", "Quimerismo"],
    "Seguidores de Set": ["Ofuscación", "Presencia", "Serpentis"],
    "Toreador": ["Auspex", "Celeridad", "Presencia"],
    "Tremere": ["Auspex", "Dominación", "Taumaturgia"],
    "Tzimisce": ["Animalismo", "Auspex", "Vicisitud"],
    "Ventrue": ["Dominación", "Fortaleza", "Presencia"]
}


# ==========================================
# 3. FUNCIONES LÓGICAS (EL CEREBRO DEL SISTEMA)
# ==========================================

def actualizar_guia_clan(evento):
    clan = evento.value
    if not clan: return 
    
    clan_seleccionado["nombre"] = clan
    
    # Lógica de Nosferatu (Apariencia 0)
    if clan == "Nosferatu":
        atributos["Sociales"]["Apariencia"] = 0
        if "Apariencia" in contenedores_atributos:
            renderizar_puntos(contenedores_atributos["Apariencia"], "Sociales", "Apariencia")
            actualizar_contador_attr("Sociales")
    elif atributos["Sociales"]["Apariencia"] == 0:
        atributos["Sociales"]["Apariencia"] = 1
        if "Apariencia" in contenedores_atributos:
            renderizar_puntos(contenedores_atributos["Apariencia"], "Sociales", "Apariencia")
            actualizar_contador_attr("Sociales")

    # Lógica de Disciplinas predictivas
    opciones_disciplinas = disciplinas_por_clan.get(clan, [])
    for sel in referencias_ui.get("selectores_disciplinas", []):
        sel.options = opciones_disciplinas
        sel.update()
        
    # NUEVA LÓGICA: Debilidades específicas que requieren texto
    if clan in requisitos_debilidad:
        referencias_ui["input_debilidad"].set_visibility(True)
        referencias_ui["input_debilidad"].label = requisitos_debilidad[clan]
        referencias_ui["input_debilidad"].update()
    elif "input_debilidad" in referencias_ui:
        referencias_ui["input_debilidad"].set_visibility(False)
        datos_concepto["Detalle_Debilidad"] = "" # Limpiamos el texto si cambia a un clan normal
        referencias_ui["input_debilidad"].update()

    # Actualizar texto lateral
    info = lore_clanes.get(clan, "Información de este clan no disponible aún.")
    if referencias_ui.get("texto_guia"):
        referencias_ui["texto_guia"].set_text(f"CLAN {clan.upper()}\n\n{info}")

def actualizar_guia_desplegable(evento, categoria):
    seleccion = evento.value
    if not seleccion: return 
    
    info_general = lore_conceptos.get(categoria, "")
    info_especifica = lore_opciones_concepto.get(seleccion, "Información no disponible.")
    texto_combinado = f"{categoria.upper()}\n\n{info_general}\n\n{'='*30}\n\n{seleccion.upper()}\n\n{info_especifica}"
    
    if referencias_ui.get("texto_guia"):
        referencias_ui["texto_guia"].set_text(texto_combinado)
        
def actualizar_generacion(evento):
    """Actualiza la guía lateral y asigna automáticamente los puntos de Trasfondo."""
    # 1. Primero, mantenemos la lógica anterior de mostrar la guía en el panel derecho
    actualizar_guia_desplegable(evento, "Generación")
    
    seleccion = evento.value
    if not seleccion: return
    
    # 2. Obtenemos el coste matemático
    coste = costes_generacion.get(seleccion, 0)
    
    # 3. Buscamos si ya existe el trasfondo "Generación" o buscamos un hueco vacío
    indice_generacion = None
    indice_vacio = None
    
    for i in range(5):
        # Leemos lo que hay escrito en las cajas, en minúsculas para evitar errores
        nombre_actual = nombres_ventajas["Trasfondos"].get(str(i), "").strip().lower()
        
        # Eliminamos las tildes para la comparación por si el usuario lo escribió a mano
        if nombre_actual in ["generación", "generacion"]:
            indice_generacion = i
            break
        elif nombre_actual == "" and indice_vacio is None:
            indice_vacio = i
            
    # 4. Si no existe y necesitamos asignar puntos, lo metemos en un hueco vacío
    if indice_generacion is None and coste > 0:
        if indice_vacio is not None:
            indice_generacion = indice_vacio
            nombres_ventajas["Trasfondos"][str(indice_generacion)] = "Generación"
            
            # Actualizamos visualmente la caja de texto en la web
            if "inputs_trasfondos" in referencias_ui:
                referencias_ui["inputs_trasfondos"][indice_generacion].value = "Generación"
        else:
            ui.notify("No hay huecos vacíos en Trasfondos para auto-asignar tu Generación.", type='warning')
            return
            
    # 5. Asignamos los puntos a la base de datos y redibujamos la pantalla
    if indice_generacion is not None:
        ventajas_valores["Trasfondos"][indice_generacion] = coste
        clave_str = f"Trasfondos_{indice_generacion}"
        if clave_str in contenedores_ventajas:
            renderizar_puntos_ventajas(contenedores_ventajas[clave_str], "Trasfondos", indice_generacion)

def actualizar_guia_atributo(atributo):
    info = lore_atributos.get(atributo, "Información no disponible.")
    if referencias_ui.get("texto_guia"):
        referencias_ui["texto_guia"].set_text(f"ATRIBUTO\n\n{info}")
    
def actualizar_guia_habilidad(habilidad):
    info = lore_habilidades.get(habilidad, "Información no disponible.")
    if referencias_ui.get("texto_guia"):
        referencias_ui["texto_guia"].set_text(f"HABILIDAD\n\n{info}")

def actualizar_guia_ventaja(ventaja):
    info = lore_ventajas.get(ventaja, "Información no disponible.")
    if referencias_ui.get("texto_guia"):
        referencias_ui["texto_guia"].set_text(f"VENTAJA\n\n{info}")

def actualizar_contador_attr(categoria):
    if categoria not in labels_contadores_attr: return
    prio_texto = prioridades_attr[categoria]
    if not prio_texto:
        labels_contadores_attr[categoria].set_text("")
        return
        
    max_pts = 7 if "7" in prio_texto else (5 if "5" in prio_texto else 3)
    gastados = sum(max(0, atributos[categoria][a] - 1) for a in atributos[categoria])
    color = "text-green-500 font-bold" if gastados == max_pts else "text-gray-400"
    labels_contadores_attr[categoria].set_text(f"Gastados: {gastados}/{max_pts}").classes(replace=f'text-sm mb-2 {color}')

def actualizar_contador_hab(categoria):
    if categoria not in labels_contadores_hab: return
    prio_texto = prioridades_hab[categoria]
    if not prio_texto:
        labels_contadores_hab[categoria].set_text("")
        return
        
    max_pts = 13 if "13" in prio_texto else (9 if "9" in prio_texto else 5)
    gastados = sum(habilidades_valores[categoria].values())
    color = "text-green-500 font-bold" if gastados == max_pts else "text-gray-400"
    labels_contadores_hab[categoria].set_text(f"Gastados: {gastados}/{max_pts}").classes(replace=f'text-sm mb-2 {color}')

def cambiar_prioridad(evento, categoria_actual):
    nueva_prioridad = evento.value
    
    if not nueva_prioridad:
        prioridades_attr[categoria_actual] = None
        actualizar_contador_attr(categoria_actual)
        return

    for cat, select in selects_prioridad.items():
        if cat != categoria_actual and select.value == nueva_prioridad:
            select.value = None 
            prioridades_attr[cat] = None 
            actualizar_contador_attr(cat)
            ui.notify(f"La prioridad '{nueva_prioridad}' se ha movido de {cat} a {categoria_actual}.", type='info')

    prioridades_attr[categoria_actual] = nueva_prioridad
    actualizar_contador_attr(categoria_actual)

def cambiar_prioridad_hab(evento, categoria_actual):
    nueva_prioridad = evento.value
    if not nueva_prioridad:
        prioridades_hab[categoria_actual] = None
        actualizar_contador_hab(categoria_actual)
        return

    for cat, select in selects_prioridad_hab.items():
        if cat != categoria_actual and select.value == nueva_prioridad:
            select.value = None
            prioridades_hab[cat] = None
            actualizar_contador_hab(cat)
            ui.notify(f"La prioridad '{nueva_prioridad}' se ha movido de {cat} a {categoria_actual}.", type='info')

    prioridades_hab[categoria_actual] = nueva_prioridad
    actualizar_contador_hab(categoria_actual)

def intentar_cambiar_puntos(categoria, atributo, nuevo_valor, container):
    if clan_seleccionado.get("nombre") == "Nosferatu" and atributo == "Apariencia":
        ui.notify("La maldición Nosferatu impide aumentar la Apariencia.", type='negative')
        return

    prio_texto = prioridades_attr[categoria]
    if not prio_texto:
        ui.notify(f"Selecciona primero una prioridad para los atributos {categoria}.", type='warning')
        return

    max_pts = 7 if "7" in prio_texto else (5 if "5" in prio_texto else 3)
    old_value = atributos[categoria][atributo]
    
    if nuevo_valor == old_value:
        nuevo_valor -= 1
        
    delta = nuevo_valor - old_value
    if delta == 0: return

    if fase_creacion.get("estado") == "gratuitos":
        base_fija = valores_base_fijos["atributos"][categoria][atributo]
        if nuevo_valor < base_fija:
            ui.notify("No puedes reducir una estadística por debajo de su valor base.", type='warning')
            return
        coste = delta * 5 
        if puntos_gratuitos["restantes"] - coste < 0:
            ui.notify("No tienes Puntos Gratuitos suficientes.", type='negative')
            return
        puntos_gratuitos["restantes"] -= coste
        label_puntos_gratuitos["ui"].set_text(f'Puntos Gratuitos Restantes: {puntos_gratuitos["restantes"]}')
        atributos[categoria][atributo] = nuevo_valor
        renderizar_puntos(container, categoria, atributo)
        return
  
    if delta > 0: 
        gastados = sum(max(0, atributos[categoria][a] - 1) for a in atributos[categoria])
        if gastados + delta > max_pts:
            ui.notify(f"Límite de {max_pts} alcanzado en {categoria}.", type='info')
            return
    elif delta < 0: 
        if nuevo_valor < 1: nuevo_valor = 1 

    atributos[categoria][atributo] = nuevo_valor
    renderizar_puntos(container, categoria, atributo)
    actualizar_contador_attr(categoria)

def intentar_cambiar_puntos_hab(categoria, habilidad, nuevo_valor, container):
    prio_texto = prioridades_hab[categoria]
    if not prio_texto:
        ui.notify(f"Selecciona primero una prioridad para {categoria}.", type='warning')
        return

    max_pts = 13 if "13" in prio_texto else (9 if "9" in prio_texto else 5)
    old_value = habilidades_valores[categoria][habilidad]
    
    if nuevo_valor == old_value: nuevo_valor -= 1
        
    delta = nuevo_valor - old_value
    if delta == 0: return

    if fase_creacion.get("estado") == "gratuitos":
        base_fija = valores_base_fijos["habilidades"][categoria][habilidad]
        if nuevo_valor < base_fija:
            ui.notify("No puedes reducir una estadística por debajo de su valor base.", type='warning')
            return
        coste = delta * 2
        if puntos_gratuitos["restantes"] - coste < 0:
            ui.notify("No tienes Puntos Gratuitos suficientes.", type='negative')
            return
        puntos_gratuitos["restantes"] -= coste
        label_puntos_gratuitos["ui"].set_text(f'Puntos Gratuitos Restantes: {puntos_gratuitos["restantes"]}')
        habilidades_valores[categoria][habilidad] = nuevo_valor
        
        if nuevo_valor < 4:
            especializaciones[categoria][habilidad] = ""
            
        renderizar_puntos_hab(container, categoria, habilidad)
        return
   
    if delta > 0:
        if nuevo_valor > 3:
            ui.notify("Regla V20: En esta fase, ninguna habilidad puede superar los 3 puntos.", type='negative')
            return
            
        gastados = sum(habilidades_valores[categoria].values())
        if gastados + delta > max_pts:
            ui.notify(f"Límite de {max_pts} alcanzado en {categoria}.", type='info')
            return
            
    elif delta < 0:
        if nuevo_valor < 0: nuevo_valor = 0 

    habilidades_valores[categoria][habilidad] = nuevo_valor
    renderizar_puntos_hab(container, categoria, habilidad)
    actualizar_contador_hab(categoria)

def intentar_cambiar_puntos_ventajas(categoria, clave, nuevo_valor, container):
    if categoria == "Disciplinas": max_pts = 3
    elif categoria == "Trasfondos": max_pts = 5
    elif categoria == "Virtudes": max_pts = 7
    
    old_value = ventajas_valores[categoria][clave]
    if nuevo_valor == old_value: nuevo_valor -= 1
        
    delta = nuevo_valor - old_value
    if delta == 0: return

    if fase_creacion.get("estado") == "gratuitos":
        # SOLUCIÓN: Acceso seguro. Si no existe la foto base (al cargar un json), asumimos el límite inferior legal.
        if "ventajas" in valores_base_fijos and categoria in valores_base_fijos["ventajas"]:
            base_fija = valores_base_fijos["ventajas"][categoria][clave]
        else:
            base_fija = 1 if categoria == "Virtudes" else 0

        if nuevo_valor < base_fija:
            ui.notify("No puedes reducir una estadística por debajo de su valor base.", type='warning')
            return
            
        if categoria == "Disciplinas":
            clan_actual = clan_seleccionado.get("nombre")
            valor_texto = nombres_ventajas["Disciplinas"].get(str(clave))
            nombre_disciplina = (valor_texto if valor_texto is not None else "").strip()
            
            if not nombre_disciplina:
                ui.notify("Primero escribe o selecciona el nombre de la Disciplina.", type='warning')
                return
                
            es_de_clan = nombre_disciplina in disciplinas_por_clan.get(clan_actual, [])
            multiplicador = 7 if es_de_clan else 10 
            
        elif categoria == "Trasfondos": multiplicador = 1
        elif categoria == "Virtudes": multiplicador = 2
        
        coste = delta * multiplicador
        if puntos_gratuitos["restantes"] - coste < 0:
            mensaje = "No tienes Puntos Gratuitos suficientes"
            if categoria == "Disciplinas" and not es_de_clan:
                mensaje += " (recuerda que una disciplina fuera de clan cuesta más)."
            ui.notify(mensaje, type='negative')
            return
            
        puntos_gratuitos["restantes"] -= coste
        label_puntos_gratuitos["ui"].set_text(f'Puntos Gratuitos Restantes: {puntos_gratuitos["restantes"]}')
        ventajas_valores[categoria][clave] = nuevo_valor
        renderizar_puntos_ventajas(container, categoria, clave)
        if categoria == "Virtudes": actualizar_derivados()
        return
            
    if delta > 0:
        if categoria == "Virtudes":
            gastados = sum(ventajas_valores[categoria][v] - 1 for v in ventajas_valores[categoria])
        else:
            gastados = sum(ventajas_valores[categoria].values())
            
        if gastados + delta > max_pts:
            ui.notify(f"Límite de {max_pts} puntos alcanzado en {categoria}.", type='info')
            return
            
    elif delta < 0:
        limite_inf = 1 if categoria == "Virtudes" else 0
        if nuevo_valor < limite_inf: nuevo_valor = limite_inf

    ventajas_valores[categoria][clave] = nuevo_valor
    renderizar_puntos_ventajas(container, categoria, clave)
    if categoria == "Virtudes": actualizar_derivados()

# NUEVO: Lógica para controlar la compra de Humanidad interactiva
def intentar_cambiar_humanidad(nuevo_valor, container):
    """Calcula si es válido aumentar/disminuir la Humanidad directamente."""
    if fase_creacion.get("estado") != "gratuitos":
        ui.notify("Solo puedes comprar Humanidad directa en la fase de Puntos Gratuitos.", type='warning')
        return

    # La Humanidad no puede bajar de la suma de Conciencia y Autocontrol de la ficha
    base = ventajas_valores["Virtudes"]["Conciencia"] + ventajas_valores["Virtudes"]["Autocontrol"]
    valor_actual = base + mejoras_derivados["Humanidad"]

    if nuevo_valor == valor_actual: 
        nuevo_valor -= 1

    delta = nuevo_valor - valor_actual
    if delta == 0: return

    if nuevo_valor < base:
        ui.notify("No puedes reducir tu Humanidad por debajo de la base de tus Virtudes.", type='warning')
        return

    # Si prefieres jugar con la regla homebrew de 1 PG, cambia este '2' por un '1'
    coste = delta * 2

    if puntos_gratuitos["restantes"] - coste < 0:
        ui.notify("No tienes Puntos Gratuitos suficientes.", type='negative')
        return

    puntos_gratuitos["restantes"] -= coste
    label_puntos_gratuitos["ui"].set_text(f'Puntos Gratuitos Restantes: {puntos_gratuitos["restantes"]}')
    
    mejoras_derivados["Humanidad"] += delta
    actualizar_derivados()

def renderizar_puntos(container, categoria, atributo):
    container.clear()
    valor = atributos[categoria][atributo]
    with container:
        for i in range(1, 6):
            dot_text = "●" if i <= valor else "○"
            ui.label(dot_text).classes(
                'text-red-700 text-2xl font-mono cursor-pointer mx-[1px] select-none hover:text-red-400 transition-colors'
            ).on('click', lambda e, cat=categoria, attr=atributo, nv=i, cont=container: intentar_cambiar_puntos(cat, attr, nv, cont))

def renderizar_puntos_hab(container, categoria, habilidad):
    container.clear()
    valor = habilidades_valores[categoria][habilidad]
    with container:
        with ui.row().classes('no-wrap items-center gap-0 w-full justify-between'):
            puntos_box = ui.row().classes('no-wrap items-center gap-0')
            with puntos_box:
                for i in range(1, 6):
                    dot_text = "●" if i <= valor else "○"
                    ui.label(dot_text).classes(
                        'text-red-700 text-xl font-mono cursor-pointer mx-[1px] select-none hover:text-red-400 transition-colors'
                    ).on('click', lambda e, cat=categoria, hab=habilidad, nv=i, cont=container: intentar_cambiar_puntos_hab(cat, hab, nv, cont))
            if valor >= 4:
                ui.input(placeholder='Especialidad').bind_value(especializaciones[categoria], habilidad).classes('w-32 text-xs ml-4')

def renderizar_puntos_ventajas(container, categoria, clave):
    container.clear()
    valor = ventajas_valores[categoria][clave]
    with container:
        for i in range(1, 6):
            dot_text = "●" if i <= valor else "○"
            ui.label(dot_text).classes(
                'text-red-700 text-2xl font-mono cursor-pointer mx-[1px] select-none hover:text-red-400 transition-colors'
            ).on('click', lambda e, cat=categoria, c=clave, nv=i, cont=container: intentar_cambiar_puntos_ventajas(cat, c, nv, cont))

def actualizar_derivados():
    # NUEVO: Sumamos la mejora directa comprada a la base que dan las virtudes
    base_humanidad = ventajas_valores["Virtudes"]["Conciencia"] + ventajas_valores["Virtudes"]["Autocontrol"]
    humanidad_val = base_humanidad + mejoras_derivados["Humanidad"]
    
    fdv_val = ventajas_valores["Virtudes"]["Coraje"]
    
    if "Humanidad" in contenedores_derivados: 
        contenedores_derivados["Humanidad"].clear()
        with contenedores_derivados["Humanidad"]:
            for i in range(1, 11): 
                dot_text = "●" if i <= humanidad_val else "○"
                # Ahora la Humanidad tiene evento onClick propio para su compra
                ui.label(dot_text).classes(
                    'text-red-700 text-2xl font-mono mx-[1px] cursor-pointer select-none hover:text-red-400 transition-colors'
                ).on('click', lambda e, nv=i, cont=contenedores_derivados["Humanidad"]: intentar_cambiar_humanidad(nv, cont))
                
    if "Fuerza de Voluntad" in contenedores_derivados: 
        # La FdV la dejamos como de solo lectura por el momento
        renderizar_puntos_derivados(contenedores_derivados["Fuerza de Voluntad"], fdv_val)

def renderizar_puntos_derivados(container, valor):
    container.clear()
    with container:
        for i in range(1, 11): 
            dot_text = "●" if i <= valor else "○"
            ui.label(dot_text).classes('text-red-700 text-2xl font-mono mx-[1px] select-none')
            
def validar_ficha_base(pestañas, pestaña_destino):
    errores = []
    
    # NUEVO: Validar que la debilidad específica esté rellena
    clan_actual = clan_seleccionado.get("nombre")
    if clan_actual in requisitos_debilidad:
        if not datos_concepto.get("Detalle_Debilidad", "").strip():
            errores.append(f"Por ser {clan_actual}, debes especificar tu {requisitos_debilidad[clan_actual]}.")

    if not all(prioridades_attr.values()): errores.append("Falta asignar prioridades a los Atributos.")
    else:
        for cat in atributos:
            max_pts = 7 if "7" in prioridades_attr[cat] else (5 if "5" in prioridades_attr[cat] else 3)
            if sum(max(0, atributos[cat][a] - 1) for a in atributos[cat]) < max_pts:
                errores.append(f"Faltan puntos en Atributos {cat}.")

    if not all(prioridades_hab.values()): errores.append("Falta asignar prioridades a las Habilidades.")
    else:
        for cat in habilidades_valores:
            max_pts = 13 if "13" in prioridades_hab[cat] else (9 if "9" in prioridades_hab[cat] else 5)
            if sum(habilidades_valores[cat].values()) < max_pts:
                errores.append(f"Faltan puntos en Habilidades ({cat}).")

    if sum(ventajas_valores["Disciplinas"].values()) < 3: errores.append("Faltan puntos en Disciplinas.")
    if sum(ventajas_valores["Trasfondos"].values()) < 5: errores.append("Faltan puntos en Trasfondos.")
    if sum(ventajas_valores["Virtudes"][v] - 1 for v in ventajas_valores["Virtudes"]) < 7: errores.append("Faltan puntos en Virtudes.")

    if errores:
        for e in errores: ui.notify(e, type='negative')
    else:
        ui.notify("¡Ficha base completada! Entrando en fase de Puntos Gratuitos.", type='positive')
        
        valores_base_fijos["atributos"] = copy.deepcopy(atributos)
        valores_base_fijos["habilidades"] = copy.deepcopy(habilidades_valores)
        valores_base_fijos["ventajas"] = copy.deepcopy(ventajas_valores)
        
        fase_creacion["estado"] = "gratuitos"
        pestaña_destino.enable() 
        pestañas.value = pestaña_destino 
        
        if label_puntos_gratuitos["ui"]:
            label_puntos_gratuitos["ui"].set_text(f'Puntos Gratuitos Restantes: {puntos_gratuitos["restantes"]}')
            
def descargar_ficha():
    # Añadido mejoras_derivados al JSON descargable
    ficha_completa = {
        "Concepto": datos_concepto,
        "Clan": clan_seleccionado["nombre"],
        "Atributos": atributos,
        "Habilidades": habilidades_valores,
        "Especializaciones": especializaciones,
        "Ventajas": ventajas_valores,
        "Mejoras_Derivados": mejoras_derivados,
        "Nombres_Disciplinas": nombres_ventajas["Disciplinas"],
        "Nombres_Trasfondos": nombres_ventajas["Trasfondos"],
        "Puntos_Gratuitos_Sobrantes": puntos_gratuitos["restantes"]
    }
    
    json_str = json.dumps(ficha_completa, indent=4, ensure_ascii=False)
    nombre_personaje = datos_concepto["Nombre"].replace(" ", "_") if datos_concepto["Nombre"] else "Vastago"
    nombre_archivo = f"Ficha_{nombre_personaje}.json"
    
    ui.download(json_str.encode('utf-8'), nombre_archivo)
    ui.notify(f"¡Ficha guardada como {nombre_archivo}!", type='positive')
    
async def cargar_ficha(evento):
    try:
        archivo = getattr(evento, 'content', None) or getattr(evento, 'file', None)
        if archivo is None: raise AttributeError("No se encontró el contenido del archivo.")

        if hasattr(archivo, 'seek'):
            resultado_seek = archivo.seek(0)
            if inspect.isawaitable(resultado_seek): await resultado_seek

        datos_brutos = archivo.read()
        if inspect.isawaitable(datos_brutos): datos_brutos = await datos_brutos
        
        contenido = datos_brutos.decode('utf-8-sig').strip()
        datos = json.loads(contenido)
        
        datos_concepto.update(datos.get("Concepto", {}))
        nombres_ventajas["Disciplinas"].update(datos.get("Nombres_Disciplinas", {}))
        nombres_ventajas["Trasfondos"].update(datos.get("Nombres_Trasfondos", {}))
        
        if datos.get("Clan") and referencias_ui.get("clan_select"): referencias_ui["clan_select"].value = datos.get("Clan")
            
        for cat, attrs in datos.get("Atributos", {}).items():
            atributos[cat].update(attrs)
            if cat in prioridades_attr and prioridades_attr[cat]: actualizar_contador_attr(cat)
            for attr in attrs:
                if attr in contenedores_atributos: renderizar_puntos(contenedores_atributos[attr], cat, attr)
                    
        if "Especializaciones" in datos:
            for cat, especs in datos["Especializaciones"].items(): especializaciones[cat].update(especs)

        for cat, habs in datos.get("Habilidades", {}).items():
            habilidades_valores[cat].update(habs)
            if cat in prioridades_hab and prioridades_hab[cat]: actualizar_contador_hab(cat)
            for hab in habs:
                if hab in contenedores_habilidades: renderizar_puntos_hab(contenedores_habilidades[hab], cat, hab)
                    
        for cat, vent in datos.get("Ventajas", {}).items():
            for k, v in vent.items():
                clave = int(k) if k.isdigit() else k
                ventajas_valores[cat][clave] = v
                clave_str = f"{cat}_{clave}"
                if clave_str in contenedores_ventajas: renderizar_puntos_ventajas(contenedores_ventajas[clave_str], cat, clave)
                    
        # NUEVO: Cargamos las compras de Humanidad si las hubiera
        if "Mejoras_Derivados" in datos:
            mejoras_derivados.update(datos["Mejoras_Derivados"])
            
        actualizar_derivados()
        
        if "Puntos_Gratuitos_Sobrantes" in datos:
            puntos_gratuitos["restantes"] = datos["Puntos_Gratuitos_Sobrantes"]
            fase_creacion["estado"] = "gratuitos"
            if label_puntos_gratuitos.get("ui"): label_puntos_gratuitos["ui"].set_text(f'Puntos Gratuitos Restantes: {puntos_gratuitos["restantes"]}')
                
        ui.notify("¡Ficha cargada con éxito!", type='positive')
        
    except Exception as ex:
        ui.notify(f"Error al cargar: {ex}", type='negative')

def generar_texto_resumen():
    concepto = datos_concepto
    lineas = []

    lineas.append(f"## {concepto.get('Nombre') or 'Vástago sin nombre'}")
    lineas.append(f"**Jugador:** {concepto.get('Jugador') or '—'}  |  **Crónica:** {concepto.get('Crónica') or '—'}  ")
    lineas.append(f"**Clan:** {clan_seleccionado.get('nombre') or '—'}  |  **Generación:** {concepto.get('Generación') or '—'}  ")
    lineas.append(f"**Naturaleza:** {concepto.get('Naturaleza') or '—'}  |  **Conducta:** {concepto.get('Conducta') or '—'}  ")
    lineas.append(f"**Concepto:** {concepto.get('Concepto') or '—'}  |  **Sire:** {concepto.get('Sire') or '—'}  ")
    lineas.append("---")

    lineas.append("### Atributos")
    for cat, attrs in atributos.items():
        valores = "  ·  ".join(f"{nombre}: {val}" for nombre, val in attrs.items())
        lineas.append(f"**{cat}:** {valores}  ")
    lineas.append("---")

    lineas.append("### Habilidades")
    for cat, habs in habilidades_valores.items():
        con_puntos = {h: v for h, v in habs.items() if v > 0}
        if con_puntos:
            valores = []
            for nombre, val in con_puntos.items():
                espec = especializaciones[cat].get(nombre, "")
                txt = f"{nombre}: {val}" + (f" ({espec})" if espec else "")
                valores.append(txt)
            lineas.append(f"**{cat}:** {'  ·  '.join(valores)}  ")
        else:
            lineas.append(f"**{cat}:** *(ninguna)*  ")
    lineas.append("---")

    lineas.append("### Ventajas")
    disciplinas_txt = []
    for i in range(3):
        # SOLUCIÓN: Convertimos de manera segura cualquier 'None' a una cadena vacía antes de hacer .strip()
        valor_bruto = nombres_ventajas["Disciplinas"].get(str(i))
        nombre = (valor_bruto if valor_bruto is not None else "").strip()
        valor = ventajas_valores["Disciplinas"].get(i, 0)
        if nombre or valor: disciplinas_txt.append(f"{nombre or f'Disciplina {i + 1}'}: {valor}")
    lineas.append(f"**Disciplinas:** {'  ·  '.join(disciplinas_txt) if disciplinas_txt else '*(ninguna)*'}  ")

    trasfondos_txt = []
    for i in range(5):
        # SOLUCIÓN: Repetimos la protección segura para los Trasfondos
        valor_bruto_tras = nombres_ventajas["Trasfondos"].get(str(i))
        nombre = (valor_bruto_tras if valor_bruto_tras is not None else "").strip()
        valor = ventajas_valores["Trasfondos"].get(i, 0)
        if nombre or valor: trasfondos_txt.append(f"{nombre or f'Trasfondo {i + 1}'}: {valor}")
    lineas.append(f"**Trasfondos:** {'  ·  '.join(trasfondos_txt) if trasfondos_txt else '*(ninguno)*'}  ")

    virtudes_txt = "  ·  ".join(f"{v}: {ventajas_valores['Virtudes'][v]}" for v in ventajas_valores["Virtudes"])
    lineas.append(f"**Virtudes:** {virtudes_txt}  ")
    lineas.append("---")

    base_hum = ventajas_valores["Virtudes"]["Conciencia"] + ventajas_valores["Virtudes"]["Autocontrol"]
    humanidad = base_hum + mejoras_derivados.get("Humanidad", 0)
    fdv = ventajas_valores["Virtudes"]["Coraje"]
    lineas.append("### Rasgos Derivados")
    lineas.append(f"**Humanidad:** {humanidad} / 10  |  **Fuerza de Voluntad:** {fdv} / 10  ")

    if fase_creacion["estado"] == "gratuitos":
        lineas.append("---")
        lineas.append(f"**Puntos Gratuitos Restantes:** {puntos_gratuitos.get('restantes', 15)}")

    return "\n\n".join(lineas)

def mostrar_resumen():
    texto = generar_texto_resumen()
    if referencias_ui.get("resumen_markdown"): referencias_ui["resumen_markdown"].set_content(texto)
    if referencias_ui.get("resumen_dialog"): referencias_ui["resumen_dialog"].open()


# ==========================================
# 4. ESTILOS GRÁFICOS Y AMBIENTACIÓN 
# ==========================================
ui.dark_mode().enable()

ui.add_head_html('''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=EB+Garamond:wght@400;700&display=swap');
        
        body { background-color: #0a0a0a; background-image: radial-gradient(circle at center, #1a1a1a 0%, #050505 100%); font-family: 'EB Garamond', serif; color: #d4d4d8; }
        .titulo-gotico { font-family: 'Cinzel', serif; text-shadow: 2px 2px 5px #000000; }
        .tarjeta-vampiro { background: linear-gradient(145deg, #1c1c1c, #121212) !important; border: 1px solid #7f1d1d !important; box-shadow: 0 6px 15px rgba(153, 27, 27, 0.15) !important; border-radius: 8px; }
        .panel-lateral { background-color: rgba(20, 20, 20, 0.8) !important; border-left: 2px solid #7f1d1d; box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.8); }
        .q-tab { color: #71717a; }
        .q-tab--active { color: #dc2626 !important; font-weight: bold; }
        .q-tab-panel { background-color: transparent !important; }
    </style>
''')

# ==========================================
# 5. INTERFAZ GRÁFICA PRINCIPAL
# ==========================================
ui.page_title('Vampiro V20 - Creador de Personajes')

with ui.row().classes('w-full justify-center items-center py-6 bg-black border-b-2 border-red-900 shadow-2xl'):
    with ui.column().classes('items-center gap-0'):
        ui.label('VAMPIRO').classes('text-5xl text-red-700 titulo-gotico tracking-widest')
        ui.label('LA MASCARADA').classes('text-xl text-gray-500 titulo-gotico tracking-[0.3em]')

with ui.row().classes('w-full h-screen no-wrap p-6 gap-6'):
    with ui.column().classes('w-2/3'):
        with ui.tabs().classes('w-full border-b border-gray-800') as tabs:
            tab_concepto = ui.tab('1. Concepto').classes('titulo-gotico text-lg')
            tab_atributos = ui.tab('2. Atributos').classes('titulo-gotico text-lg')
            tab_habilidades = ui.tab('3. Habilidades').classes('titulo-gotico text-lg')
            tab_ventajas = ui.tab('4. Ventajas').classes('titulo-gotico text-lg')
            tab_gratuitos = ui.tab('5. Gratuitos').classes('titulo-gotico text-lg text-yellow-700').disable()

        with ui.tab_panels(tabs, value=tab_concepto).classes('w-full mt-4'):
            
            with ui.tab_panel(tab_concepto):
                with ui.row().classes('w-full gap-8 justify-center tarjeta-vampiro p-8'):
                    with ui.column():
                        ui.input('Nombre:').bind_value(datos_concepto, 'Nombre').classes('w-48')
                        ui.input('Jugador:').bind_value(datos_concepto, 'Jugador').classes('w-48')
                        ui.input('Crónica:').bind_value(datos_concepto, 'Crónica').classes('w-48')
                    with ui.column():
                        arquetipos = ["Ansioso", "Arquitecto", "Autócrata", "Bizarro", "Bribón", "Bufón", "Capitalista", "Celebrante", "Competidor", "Conformista", "Creador", "Cuidador", "Defensor", "Director", "Enigma", "Fanático", "Galán", "Gurú", "Juez", "Mártir", "Monstruo", "Niño", "Pedagogo", "Penitente", "Perfeccionista", "Rebelde", "Sádico", "Sobreviviente", "Solitario", "Tradicionalista", "Visionario"]
                        ui.select(arquetipos, label='Naturaleza:', on_change=lambda e: actualizar_guia_desplegable(e, "Naturaleza")).bind_value(datos_concepto, 'Naturaleza').classes('w-48')
                        ui.select(arquetipos, label='Conducta:', on_change=lambda e: actualizar_guia_desplegable(e, "Conducta")).bind_value(datos_concepto, 'Conducta').classes('w-48')
                        ui.input('Concepto:').bind_value(datos_concepto, 'Concepto').classes('w-48').on('focus', lambda: referencias_ui["texto_guia"].set_text("CONCEPTO\n\nEl Concepto es un resumen de quién era tu personaje antes del Abrazo (su vida mortal). Es el ancla de su Humanidad.") if referencias_ui.get("texto_guia") else None)
                    with ui.column():
                        clanes = ['Assamita', 'Brujah', 'Gangrel', 'Giovanni', 'Lasombra', 'Malkavian', 'Nosferatu', 'Ravnos', 'Seguidores de Set', 'Toreador', 'Tremere', 'Tzimisce', 'Ventrue']
                        sel_clan = ui.select(clanes, label='Clan:', on_change=actualizar_guia_clan).classes('w-48')
                        referencias_ui["clan_select"] = sel_clan
                        # CÓDIGO ACTUALIZADO: El selector de generación ahora dispara la automatización
                        generaciones = ["13ª Generación", "12ª Generación", "11ª Generación", "10ª Generación", "9ª Generación", "8ª Generación"]
                        ui.select(generaciones, label='Generación:', on_change=actualizar_generacion).bind_value(datos_concepto, 'Generación').classes('w-48')
                        ui.input('Sire:').bind_value(datos_concepto, 'Sire').classes('w-48').on('focus', lambda: referencias_ui["texto_guia"].set_text("SIRE\n\nEl Sire es el vampiro que te dio el Abrazo y te convirtió. Es tu maestro y el responsable de tus acciones.") if referencias_ui.get("texto_guia") else None)
                         
                        # NUEVO: Campo dinámico para la debilidad del clan
                        input_deb = ui.input('Debilidad:').bind_value(datos_concepto, 'Detalle_Debilidad').classes('w-48')
                        input_deb.set_visibility(False) # Oculto por defecto
                        referencias_ui["input_debilidad"] = input_deb # Guardamos la referencia para mostrarlo luego    
                                                              
            with ui.tab_panel(tab_atributos):
                with ui.row().classes('w-full justify-around'):
                    opciones_base = ['Primario (7 pts)', 'Secundario (5 pts)', 'Terciario (3 pts)']
                    
                    for cat_nombre, attrs in atributos.items():
                        with ui.card().classes('w-64 tarjeta-vampiro p-4'):
                            ui.label(cat_nombre).classes('text-xl text-red-600 titulo-gotico mb-1 border-b border-red-900 w-full pb-1')
                            lbl_contador = ui.label('').classes('text-sm mb-2 text-gray-400')
                            labels_contadores_attr[cat_nombre] = lbl_contador
                            
                            sel = ui.select(opciones_base, label='Prioridad', on_change=lambda e, c=cat_nombre: cambiar_prioridad(e, c)) \
                                    .classes('w-full mb-4').props('clearable')
                            selects_prioridad[cat_nombre] = sel
                            
                            for attr_name in attrs.keys():
                                with ui.row().classes('items-center justify-between w-full no-wrap mb-1'):
                                    ui.label(attr_name).classes('w-20 text-md text-gray-300 cursor-help') \
                                        .on('mouseenter', lambda e, a=attr_name: actualizar_guia_atributo(a))
                                    dots_container = ui.row().classes('no-wrap items-center gap-0')
                                    contenedores_atributos[attr_name] = dots_container 
                                    renderizar_puntos(dots_container, cat_nombre, attr_name)

            with ui.tab_panel(tab_habilidades):
                with ui.row().classes('w-full justify-around items-start'):
                    opciones_base_hab = ['Primario (13 pts)', 'Secundario (9 pts)', 'Terciario (5 pts)']
                    
                    for grupo_nombre, lista_habs in habilidades.items():
                        with ui.card().classes('w-[30%] tarjeta-vampiro p-4 min-w-[280px]'):
                            ui.label(grupo_nombre).classes('text-xl text-red-600 titulo-gotico mb-1 border-b border-red-900 w-full pb-1')
                            lbl_contador_hab = ui.label('').classes('text-sm mb-2 text-gray-400')
                            labels_contadores_hab[grupo_nombre] = lbl_contador_hab
                            
                            sel_hab = ui.select(opciones_base_hab, label='Prioridad', on_change=lambda e, c=grupo_nombre: cambiar_prioridad_hab(e, c)) \
                                        .classes('w-full mb-4').props('clearable')
                            selects_prioridad_hab[grupo_nombre] = sel_hab

                            for hab_name in lista_habs:
                                with ui.row().classes('items-center justify-between w-full no-wrap mb-1'):
                                    ui.label(hab_name).classes('w-24 text-sm text-gray-300 cursor-help shrink-0') \
                                        .on('mouseenter', lambda e, h=hab_name: actualizar_guia_habilidad(h))
                                    dots_container = ui.row().classes('no-wrap items-center gap-0 flex-grow')
                                    contenedores_habilidades[hab_name] = dots_container
                                    renderizar_puntos_hab(dots_container, grupo_nombre, hab_name)

            with ui.tab_panel(tab_ventajas):
                with ui.row().classes('w-full justify-around items-start'):
                    with ui.card().classes('w-72 tarjeta-vampiro p-4'):
                        ui.label("Disciplinas (3 pts)").classes('text-xl text-red-600 titulo-gotico mb-2 border-b border-red-900 w-full pb-1 cursor-help') \
                            .on('mouseenter', lambda: actualizar_guia_ventaja("Disciplinas"))
                        
                        # Creamos un puente gráfico para poder acceder a los selectores desde otras funciones
                        if "selectores_disciplinas" not in referencias_ui:
                            referencias_ui["selectores_disciplinas"] = []
                        else:
                            referencias_ui["selectores_disciplinas"].clear()

                        for i in range(3):
                            with ui.row().classes('items-center justify-between w-full no-wrap mb-2'):
                                
                                # NUEVO COMPONENTE: Un selector predictivo que admite texto libre
                                sel_disc = ui.select(
                                    options=[], 
                                    with_input=True, 
                                    new_value_mode='add-unique', 
                                    label=f'Disciplina {i+1}'
                                ).bind_value(nombres_ventajas["Disciplinas"], str(i)).classes('w-32 text-xs')
                                
                                referencias_ui["selectores_disciplinas"].append(sel_disc)
                                
                                dots_container = ui.row().classes('no-wrap items-center gap-0')
                                contenedores_ventajas[f"Disciplinas_{i}"] = dots_container
                                renderizar_puntos_ventajas(dots_container, "Disciplinas", i)
                    
                    # CÓDIGO ACTUALIZADO: Tarjeta de Trasfondos con referencias visuales
                    with ui.card().classes('w-72 tarjeta-vampiro p-4'):
                        ui.label("Trasfondos (5 pts)").classes('text-xl text-red-600 titulo-gotico mb-2 border-b border-red-900 w-full pb-1 cursor-help') \
                            .on('mouseenter', lambda: actualizar_guia_ventaja("Trasfondos"))
                            
                        # Creamos un puente gráfico para las cajas de texto de los Trasfondos
                        if "inputs_trasfondos" not in referencias_ui:
                            referencias_ui["inputs_trasfondos"] = []
                        else:
                            referencias_ui["inputs_trasfondos"].clear()
                            
                        for i in range(5):
                            with ui.row().classes('items-center justify-between w-full no-wrap mb-1'):
                                inp_trasfondo = ui.input(placeholder=f'Trasfondo {i+1}').bind_value(nombres_ventajas["Trasfondos"], str(i)).classes('w-28 text-sm')
                                referencias_ui["inputs_trasfondos"].append(inp_trasfondo)
                                
                                dots_container = ui.row().classes('no-wrap items-center gap-0')
                                contenedores_ventajas[f"Trasfondos_{i}"] = dots_container
                                renderizar_puntos_ventajas(dots_container, "Trasfondos", i)
                                
                    with ui.card().classes('w-72 tarjeta-vampiro p-4'):
                        ui.label("Virtudes (7 pts)").classes('text-xl text-red-600 titulo-gotico mb-2 border-b border-red-900 w-full pb-1')
                        for virtud in ["Conciencia", "Autocontrol", "Coraje"]:
                            with ui.row().classes('items-center justify-between w-full no-wrap mb-4'):
                                ui.label(virtud).classes('w-28 text-md text-gray-300 cursor-help') \
                                    .on('mouseenter', lambda e, v=virtud: actualizar_guia_ventaja(v))
                                dots_container = ui.row().classes('no-wrap items-center gap-0')
                                contenedores_ventajas[f"Virtudes_{virtud}"] = dots_container
                                renderizar_puntos_ventajas(dots_container, "Virtudes", virtud)

                with ui.row().classes('w-full justify-around mt-8'):
                    with ui.card().classes('w-[45%] tarjeta-vampiro p-4 items-center'):
                        ui.label("Humanidad").classes('text-2xl text-red-600 titulo-gotico mb-2 cursor-help') \
                            .on('mouseenter', lambda: actualizar_guia_ventaja("Humanidad"))
                        cont_hum = ui.row().classes('no-wrap items-center gap-0')
                        contenedores_derivados["Humanidad"] = cont_hum
                        
                    with ui.card().classes('w-[45%] tarjeta-vampiro p-4 items-center'):
                        ui.label("Fuerza de Voluntad").classes('text-2xl text-red-600 titulo-gotico mb-2 cursor-help') \
                            .on('mouseenter', lambda: actualizar_guia_ventaja("Fuerza de Voluntad"))
                        cont_fdv = ui.row().classes('no-wrap items-center gap-0')
                        contenedores_derivados["Fuerza de Voluntad"] = cont_fdv
                        
                actualizar_derivados()
                
                with ui.row().classes('w-full justify-center mt-12'):
                    ui.button('VALIDAR FICHA Y CONTINUAR', on_click=lambda: validar_ficha_base(tabs, tab_gratuitos)) \
                        .classes('bg-red-900 text-white font-bold py-3 px-8 rounded-sm hover:bg-red-700 transition-colors titulo-gotico text-xl shadow-lg')
                        
            with ui.tab_panel(tab_gratuitos):
                with ui.column().classes('w-full items-center tarjeta-vampiro p-10'):
                    ui.label("LA SANGRE SE AFIANZA").classes('text-3xl text-red-600 titulo-gotico mb-4')
                    ui.label("Tu ficha base ha sido bloqueada y auditada con éxito. Ahora dispones de 15 Puntos Gratuitos para personalizar a tu personaje saltándote las restricciones iniciales. Vuelve a las pestañas anteriores para gastarlos haciendo clic en los puntos.").classes('text-lg text-gray-300 text-center mb-8')
                    label_puntos = ui.label(f'Puntos Gratuitos Restantes: {puntos_gratuitos.get("restantes", 15)}').classes('text-5xl text-yellow-600 titulo-gotico mb-8')
                    label_puntos_gratuitos["ui"] = label_puntos
                    
                    with ui.row().classes('w-full justify-around mt-6 border-t border-red-900 pt-8'):
                        with ui.column().classes('items-center'):
                            ui.label("TABLA DE COSTES").classes('text-xl text-gray-400 titulo-gotico mb-4 border-b border-gray-700 pb-1')
                            ui.label("• Atributos: 5 puntos por punto").classes('text-gray-300 text-lg')
                            ui.label("• Disciplinas: 7 puntos por punto").classes('text-gray-300 text-lg')
                            ui.label("• Habilidades: 2 puntos por punto").classes('text-gray-300 text-lg')
                            ui.label("• Virtudes: 2 puntos por punto").classes('text-gray-300 text-lg')
                            ui.label("• Humanidad: 2 puntos por punto").classes('text-gray-300 text-lg')
                            ui.label("• Trasfondos: 1 punto por punto").classes('text-gray-300 text-lg')
                            
                    with ui.row().classes('w-full justify-center mt-12'):
                        ui.button('GUARDAR PERSONAJE (JSON)', on_click=descargar_ficha) \
                            .classes('bg-green-900 text-white font-bold py-3 px-8 rounded-sm hover:bg-green-700 transition-colors titulo-gotico text-xl shadow-lg')
                            
        with ui.row().classes('w-full justify-between items-center mt-6 border-t border-red-900 pt-4'):
            ui.label('Gestión de Archivos').classes('text-gray-400 titulo-gotico text-xl')
            with ui.row().classes('items-center gap-4'):
                ui.button('📜 VER RESUMEN', on_click=mostrar_resumen) \
                    .classes('bg-gray-800 text-red-500 font-bold py-2 px-4 rounded-sm hover:bg-gray-700 transition-colors titulo-gotico')
                ui.upload(label='Cargar Ficha (.json)', auto_upload=True, on_upload=cargar_ficha).props('accept=".json"').classes('w-64 tarjeta-vampiro rounded-lg shadow-md')

    with ui.dialog() as resumen_dialog, ui.card().classes('tarjeta-vampiro p-6 w-[650px] max-w-full max-h-[85vh] overflow-y-auto'):
        ui.label('RESUMEN DE LA FICHA').classes('text-2xl text-red-600 titulo-gotico mb-4 border-b border-red-900 pb-2 w-full')
        resumen_markdown = ui.markdown('').classes('text-gray-200 w-full')
        with ui.row().classes('w-full justify-end mt-4'):
            ui.button('Cerrar', on_click=resumen_dialog.close) \
                .classes('bg-red-900 text-white font-bold py-2 px-6 rounded-sm hover:bg-red-700 transition-colors titulo-gotico')
    referencias_ui["resumen_dialog"] = resumen_dialog
    referencias_ui["resumen_markdown"] = resumen_markdown

    with ui.column().classes('w-1/3 panel-lateral p-6 rounded-lg h-full'):
        ui.label('LA BIBLIOTECA OSCURA').classes('text-2xl text-red-700 titulo-gotico mb-4 border-b border-red-900 pb-2 w-full text-center')
        texto_guia = ui.label('Bienvenido, Vástago.\n\nSelecciona opciones en tu hoja de personaje para desvelar los secretos de tu linaje y tu naturaleza.').classes('text-lg text-gray-300 whitespace-pre-line leading-relaxed')
        referencias_ui["texto_guia"] = texto_guia
    
ui.run()