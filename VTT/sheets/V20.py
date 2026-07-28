from nicegui import ui

# --- BASE DE DATOS Y ESTADO ---
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

prioridades_attr = {"Físicos": None, "Sociales": None, "Mentales": None}
habilidades_valores = {
    "Talentos": {h: 0 for h in habilidades["Talentos"]},
    "Técnicas": {h: 0 for h in habilidades["Técnicas"]},
    "Conocimientos": {h: 0 for h in habilidades["Conocimientos"]}
}
prioridades_hab = {"Talentos": None, "Técnicas": None, "Conocimientos": None}
selects_prioridad_hab = {}
contenedores_habilidades = {}
clan_seleccionado = {"nombre": None}
contenedores_atributos = {}
selects_prioridad = {}

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
    # Generaciones
    "13ª Generación": "La generación más común para neonatos. \n• Capacidad de Sangre: 10\n• Puntos por turno: 1\n• Coste: 0 puntos de Trasfondo.",
    "12ª Generación": "Tu sangre es un poco más fuerte. \n• Capacidad de Sangre: 11\n• Puntos por turno: 1\n• Coste: 1 punto de Trasfondo (Generación).",
    "11ª Generación": "Un paso más cerca de Caín. \n• Capacidad de Sangre: 12\n• Puntos por turno: 1\n• Coste: 2 puntos de Trasfondo (Generación).",
    "10ª Generación": "Tu sangre empieza a ser respetable. \n• Capacidad de Sangre: 13\n• Puntos por turno: 1\n• Coste: 3 puntos de Trasfondo (Generación).",
    "9ª Generación": "Sangre poderosa. \n• Capacidad de Sangre: 14\n• Puntos por turno: 2\n• Coste: 4 puntos de Trasfondo (Generación).",
    "8ª Generación": "El límite para un personaje inicial. Eres notablemente poderoso. \n• Capacidad de Sangre: 15\n• Puntos por turno: 3\n• Coste: 5 puntos de Trasfondo (Generación).",

    # Arquetipos de Personalidad
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
    # Talentos
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

    # Técnicas
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

    # Conocimientos
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

# --- FUNCIONES LÓGICAS ---
def actualizar_guia_clan(evento):
    clan = evento.value
    clan_seleccionado["nombre"] = clan
    
    # Regla especial: Maldición de los Nosferatu
    if clan == "Nosferatu":
        atributos["Sociales"]["Apariencia"] = 0
        if "Apariencia" in contenedores_atributos:
            renderizar_puntos(contenedores_atributos["Apariencia"], "Sociales", "Apariencia")
    elif atributos["Sociales"]["Apariencia"] == 0:
        # Si elegimos otro clan y estábamos en 0, devolvemos el punto base
        atributos["Sociales"]["Apariencia"] = 1
        if "Apariencia" in contenedores_atributos:
            renderizar_puntos(contenedores_atributos["Apariencia"], "Sociales", "Apariencia")

    info = lore_clanes.get(clan, "Información de este clan no disponible aún.")
    texto_guia.set_text(f"CLAN {clan.upper()}\n\n{info}")

def actualizar_guia_desplegable(evento, categoria):
    seleccion = evento.value
    info_general = lore_conceptos.get(categoria, "")
    info_especifica = lore_opciones_concepto.get(seleccion, "Información no disponible.")
    texto_combinado = f"{categoria.upper()}\n\n{info_general}\n\n{'='*30}\n\n{seleccion.upper()}\n\n{info_especifica}"
    texto_guia.set_text(texto_combinado)

def cambiar_prioridad(evento, categoria_actual):
    nueva_prioridad = evento.value
    
    # Si el usuario borra la selección
    if not nueva_prioridad:
        prioridades_attr[categoria_actual] = None
        return

    # Si otra categoría ya tiene esta prioridad, se la quitamos automáticamente
    for cat, select in selects_prioridad.items():
        if cat != categoria_actual and select.value == nueva_prioridad:
            select.value = None # Vaciamos el desplegable de la otra categoría
            prioridades_attr[cat] = None
            ui.notify(f"La prioridad '{nueva_prioridad}' se ha movido de {cat} a {categoria_actual}.", type='info')

    # Guardamos la nueva selección
    prioridades_attr[categoria_actual] = nueva_prioridad

def intentar_cambiar_puntos(categoria, atributo, nuevo_valor, container):
    # Bloqueo absoluto para Nosferatu
    if clan_seleccionado["nombre"] == "Nosferatu" and atributo == "Apariencia":
        ui.notify("La maldición Nosferatu impide aumentar la Apariencia.", type='negative')
        return

    prio_texto = prioridades_attr[categoria]
    if not prio_texto:
        ui.notify(f"Selecciona primero una prioridad para los atributos {categoria}.", type='warning')
        return

    max_pts = 7 if "7" in prio_texto else (5 if "5" in prio_texto else 3)
    old_value = atributos[categoria][atributo]
    delta = nuevo_valor - old_value
    
    if delta == 0: return
        
    if delta > 0:
        # Usamos max(0, ...) para que la Apariencia 0 del Nosferatu no rompa la matemática sumando puntos negativos
        gastados = sum(max(0, atributos[categoria][a] - 1) for a in atributos[categoria])
        if gastados + delta > max_pts:
            ui.notify(f"Límite de {max_pts} alcanzado en {categoria}.", type='info')
            return
    elif delta < 0:
        if nuevo_valor < 1:
            nuevo_valor = 1

    atributos[categoria][atributo] = nuevo_valor
    renderizar_puntos(container, categoria, atributo)

def renderizar_puntos(container, categoria, atributo):
    container.clear()
    valor = atributos[categoria][atributo]
    
    with container:
        for i in range(1, 6):
            dot_text = "●" if i <= valor else "○"
            ui.label(dot_text).classes(
                'text-red-700 text-2xl font-mono cursor-pointer mx-[1px] select-none hover:text-red-400 transition-colors'
            ).on('click', lambda e, cat=categoria, attr=atributo, nv=i, cont=container: intentar_cambiar_puntos(cat, attr, nv, cont))
            
def actualizar_guia_atributo(atributo):
    info = lore_atributos.get(atributo, "Información no disponible.")
    texto_guia.set_text(f"ATRIBUTO\n\n{info}")
    
def actualizar_guia_habilidad(habilidad):
    info = lore_habilidades.get(habilidad, "Información no disponible.")
    texto_guia.set_text(f"HABILIDAD\n\n{info}")

def cambiar_prioridad_hab(evento, categoria_actual):
    nueva_prioridad = evento.value
    if not nueva_prioridad:
        prioridades_hab[categoria_actual] = None
        return

    # Robo de prioridad automático
    for cat, select in selects_prioridad_hab.items():
        if cat != categoria_actual and select.value == nueva_prioridad:
            select.value = None
            prioridades_hab[cat] = None
            ui.notify(f"La prioridad '{nueva_prioridad}' se ha movido de {cat} a {categoria_actual}.", type='info')

    prioridades_hab[categoria_actual] = nueva_prioridad

def intentar_cambiar_puntos_hab(categoria, habilidad, nuevo_valor, container):
    prio_texto = prioridades_hab[categoria]
    if not prio_texto:
        ui.notify(f"Selecciona primero una prioridad para {categoria}.", type='warning')
        return

    # Leemos si son 13, 9 o 5 puntos
    max_pts = 13 if "13" in prio_texto else (9 if "9" in prio_texto else 5)
    
    old_value = habilidades_valores[categoria][habilidad]
    delta = nuevo_valor - old_value
    
    if delta == 0: return
        
    if delta > 0:
        # Regla estricta V20: Límite de 3 en creación inicial
        if nuevo_valor > 3:
            ui.notify("Regla V20: En esta fase, ninguna habilidad puede superar los 3 puntos.", type='negative')
            return
            
        gastados = sum(habilidades_valores[categoria].values())
        if gastados + delta > max_pts:
            ui.notify(f"Límite de {max_pts} alcanzado en {categoria}.", type='info')
            return
    elif delta < 0:
        if nuevo_valor < 0:
            nuevo_valor = 0 # Las habilidades sí pueden quedarse en 0

    habilidades_valores[categoria][habilidad] = nuevo_valor
    renderizar_puntos_hab(container, categoria, habilidad)

def renderizar_puntos_hab(container, categoria, habilidad):
    container.clear()
    valor = habilidades_valores[categoria][habilidad]
    
    with container:
        for i in range(1, 6):
            dot_text = "●" if i <= valor else "○"
            # Fuente un poco más pequeña que los atributos para que quepan bien las 10 filas
            ui.label(dot_text).classes(
                'text-red-700 text-xl font-mono cursor-pointer mx-[1px] select-none hover:text-red-400 transition-colors'
            ).on('click', lambda e, cat=categoria, hab=habilidad, nv=i, cont=container: intentar_cambiar_puntos_hab(cat, hab, nv, cont))

# --- ESTILOS GRÁFICOS Y AMBIENTACIÓN ---
ui.dark_mode().enable()

ui.add_head_html('''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=EB+Garamond:wght@400;700&display=swap');
        
        body {
            background-color: #0a0a0a;
            background-image: radial-gradient(circle at center, #1a1a1a 0%, #050505 100%);
            font-family: 'EB Garamond', serif;
            color: #d4d4d8;
        }
        .titulo-gotico {
            font-family: 'Cinzel', serif;
            text-shadow: 2px 2px 5px #000000;
        }
        .tarjeta-vampiro {
            background: linear-gradient(145deg, #1c1c1c, #121212) !important;
            border: 1px solid #7f1d1d !important;
            box-shadow: 0 6px 15px rgba(153, 27, 27, 0.15) !important;
            border-radius: 8px;
        }
        .panel-lateral {
            background-color: rgba(20, 20, 20, 0.8) !important;
            border-left: 2px solid #7f1d1d;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.8);
        }
        .q-tab { color: #71717a; }
        .q-tab--active { color: #dc2626 !important; font-weight: bold; }
        .q-tab-panel { background-color: transparent !important; }
    </style>
''')

# --- INTERFAZ GRÁFICA ---
ui.page_title('Vampiro V20 - Creador de Personajes')

# Cabecera inmersiva
with ui.row().classes('w-full justify-center items-center py-6 bg-black border-b-2 border-red-900 shadow-2xl'):
    with ui.column().classes('items-center gap-0'):
        ui.label('VAMPIRO').classes('text-5xl text-red-700 titulo-gotico tracking-widest')
        ui.label('LA MASCARADA').classes('text-xl text-gray-500 titulo-gotico tracking-[0.3em]')

# Contenedor Principal de la App
with ui.row().classes('w-full h-screen no-wrap p-6 gap-6'):
    
    # Panel Izquierdo: Ficha (Ocupa 2/3 del ancho)
    with ui.column().classes('w-2/3'):
        with ui.tabs().classes('w-full border-b border-gray-800') as tabs:
            tab_concepto = ui.tab('1. Concepto').classes('titulo-gotico text-lg')
            tab_atributos = ui.tab('2. Atributos').classes('titulo-gotico text-lg')
            tab_habilidades = ui.tab('3. Habilidades').classes('titulo-gotico text-lg')
            tab_ventajas = ui.tab('4. Ventajas').classes('titulo-gotico text-lg')

        with ui.tab_panels(tabs, value=tab_concepto).classes('w-full mt-4'):
            
            # PESTAÑA CONCEPTO
            with ui.tab_panel(tab_concepto):
                with ui.row().classes('w-full gap-8 justify-center tarjeta-vampiro p-8'):
                    with ui.column():
                        ui.input('Nombre:').classes('w-48')
                        ui.input('Jugador:').classes('w-48')
                        ui.input('Crónica:').classes('w-48')
                    
                    with ui.column():
                        arquetipos = [
                            "Ansioso", "Arquitecto", "Autócrata", "Bizarro", "Bribón", "Bufón", 
                            "Capitalista", "Celebrante", "Competidor", "Conformista", "Creador", 
                            "Cuidador", "Defensor", "Director", "Enigma", "Fanático", "Galán", 
                            "Gurú", "Juez", "Mártir", "Monstruo", "Niño", "Pedagogo", "Penitente", 
                            "Perfeccionista", "Rebelde", "Sádico", "Sobreviviente", "Solitario", 
                            "Tradicionalista", "Visionario"
                        ]
                        
                        ui.select(arquetipos, label='Naturaleza:', on_change=lambda e: actualizar_guia_desplegable(e, "Naturaleza")).classes('w-48')
                        ui.select(arquetipos, label='Conducta:', on_change=lambda e: actualizar_guia_desplegable(e, "Conducta")).classes('w-48')
                        
                        ui.input('Concepto:').classes('w-48').on('focus', lambda: texto_guia.set_text("CONCEPTO\n\nEl Concepto es un resumen de quién era tu personaje antes del Abrazo (su vida mortal). Es el ancla de su Humanidad.\n\nEjemplos: 'Estudiante endeudado', 'Médico forense', 'Artista torturado', 'Policía corrupto'."))
                    
                    with ui.column():
                        clanes = ['Assamita', 'Brujah', 'Gangrel', 'Giovanni', 'Lasombra', 'Malkavian', 'Nosferatu', 'Ravnos', 'Seguidores de Set', 'Toreador', 'Tremere', 'Tzimisce', 'Ventrue']
                        ui.select(clanes, label='Clan:', on_change=actualizar_guia_clan).classes('w-48')
                        generaciones = ["13ª Generación", "12ª Generación", "11ª Generación", "10ª Generación", "9ª Generación", "8ª Generación"]
                        ui.select(generaciones, label='Generación:', on_change=lambda e: actualizar_guia_desplegable(e, "Generación")).classes('w-48')
                        ui.input('Sire:').classes('w-48').on('focus', lambda: texto_guia.set_text("SIRE\n\nEl Sire es el vampiro que te dio el Abrazo y te convirtió. Es tu maestro y el responsable de tus acciones."))

            # PESTAÑA ATRIBUTOS
            with ui.tab_panel(tab_atributos):
                with ui.row().classes('w-full justify-around'):
                    opciones_base = ['Primario (7 pts)', 'Secundario (5 pts)', 'Terciario (3 pts)']
                    
                    for cat_nombre, attrs in atributos.items():
                        with ui.card().classes('w-64 tarjeta-vampiro p-4'):
                            ui.label(cat_nombre).classes('text-xl text-red-600 titulo-gotico mb-2 border-b border-red-900 w-full pb-1')
                            
                            # Creador del desplegable limpio y simple
                            sel = ui.select(opciones_base, label='Prioridad', 
                                            on_change=lambda e, c=cat_nombre: cambiar_prioridad(e, c)) \
                                    .classes('w-full mb-4').props('clearable')
                            
                            selects_prioridad[cat_nombre] = sel
                            
                            for attr_name in attrs.keys():
                                with ui.row().classes('items-center justify-between w-full no-wrap mb-1'):
                                    ui.label(attr_name).classes('w-20 text-md text-gray-300 cursor-help') \
                                        .on('mouseenter', lambda e, a=attr_name: actualizar_guia_atributo(a))
                                    
                                    dots_container = ui.row().classes('no-wrap items-center gap-0')
                                    
                                    # Guardamos la referencia para poder modificarlo desde el Clan
                                    contenedores_atributos[attr_name] = dots_container 
                                    
                                    renderizar_puntos(dots_container, cat_nombre, attr_name)

            # PESTAÑA HABILIDADES
            with ui.tab_panel(tab_habilidades):
                with ui.row().classes('w-full justify-around items-start'):
                    opciones_base_hab = ['Primario (13 pts)', 'Secundario (9 pts)', 'Terciario (5 pts)']
                    
                    for grupo_nombre, lista_habs in habilidades.items():
                        with ui.card().classes('w-64 tarjeta-vampiro p-4'):
                            ui.label(grupo_nombre).classes('text-xl text-red-600 titulo-gotico mb-2 border-b border-red-900 w-full pb-1')
                            
                            # Selector de prioridad para habilidades
                            sel_hab = ui.select(opciones_base_hab, label='Prioridad',
                                                on_change=lambda e, c=grupo_nombre: cambiar_prioridad_hab(e, c)) \
                                        .classes('w-full mb-4').props('clearable')
                            
                            selects_prioridad_hab[grupo_nombre] = sel_hab

                            for hab_name in lista_habs:
                                with ui.row().classes('items-center justify-between w-full no-wrap mb-1'):
                                    
                                    # Nombre de la habilidad con evento de lectura al pasar el ratón
                                    ui.label(hab_name).classes('w-24 text-sm text-gray-300 cursor-help') \
                                        .on('mouseenter', lambda e, h=hab_name: actualizar_guia_habilidad(h))
                                    
                                    # Contenedor de los puntos interactivos (Empiezan vacíos en lugar de con 1)
                                    dots_container = ui.row().classes('no-wrap items-center gap-0')
                                    contenedores_habilidades[hab_name] = dots_container
                                    
                                    renderizar_puntos_hab(dots_container, grupo_nombre, hab_name)

            # PESTAÑA VENTAJAS
            with ui.tab_panel(tab_ventajas):
                with ui.card().classes('w-full tarjeta-vampiro p-8 items-center'):
                    ui.label('Espacio reservado para las Disciplinas, Trasfondos y Virtudes.').classes('text-lg text-gray-400 font-style: italic')

    # Panel Derecho: Guía del Narrador
    with ui.column().classes('w-1/3 panel-lateral p-6 rounded-lg h-full'):
        ui.label('LA BIBLIOTECA OSCURA').classes('text-2xl text-red-700 titulo-gotico mb-4 border-b border-red-900 pb-2 w-full text-center')
        texto_guia = ui.label('Bienvenido, Vástago.\n\nSelecciona opciones en tu hoja de personaje para desvelar los secretos de tu linaje y tu naturaleza.').classes('text-lg text-gray-300 whitespace-pre-line leading-relaxed')

ui.run()