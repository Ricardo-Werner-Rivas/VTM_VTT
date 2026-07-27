from nicegui import ui

# --- BASE DE DATOS Y ESTADO ---
atributos = {
    "Físicos": {"Fuerza": 1, "Destreza": 1, "Resistencia": 1},
    "Sociales": {"Carisma": 1, "Manipulación": 1, "Apariencia": 1},
    "Mentales": {"Percepción": 1, "Inteligencia": 1, "Astucia": 1}
}
prioridades_attr = {"Físicos": None, "Sociales": None, "Mentales": None}

habilidades = {
    "Talentos": ["Alerta", "Atletismo", "Callejeo", "Consciencia", "Empatía", "Expresión", "Intimidación", "Liderazgo", "Pelea", "Subterfugio"],
    "Técnicas": ["Armas de Fuego", "Artesanía", "Conducir", "Etiqueta", "Interpretación", "Latrocinio", "Pelea con Armas", "Sigilo", "Supervivencia", "T.c. Animales"],
    "Conocimientos": ["Academicismo", "Ciencias", "Finanzas", "Informática", "Investigación", "Leyes", "Medicina", "Ocultismo", "Política", "Tecnología"]
}

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
    
    "Toreador": "Artistas, seductores y hedonistas. Se obsesionan con la belleza y la cultura humana, siendo el clan más integrado en la alta sociedad mortal.\n\n• Disciplinas: Auspex, Celeridad, Presencia.\n• Debilidad: Pueden quedar extasiados al contemplar algo verdaderamente hermoso (una obra de arte, una persona, un amanecer), perdiendo la noción del entorno.",
    
    "Tremere": "Un clan de hechiceros de la sangre y antiguos magos que robaron la inmortalidad. Son estrictos, organizados y sumamente desconfiados con los demás clanes.\n\n• Disciplinas: Auspex, Dominación, Taumaturgia.\n• Debilidad: Su sangre está muy controlada. Todos los neófitos dan un paso hacia el Vínculo de Sangre con el consejo gobernante de los Siete al ser Abrazados.",
    
    "Tzimisce": "Eruditos inhumanos, monstruosos y maestros de la carne. Consideran que han superado los límites humanos y moldean los cuerpos de sus víctimas (y los suyos propios) a su antojo.\n\n• Disciplinas: Animalismo, Auspex, Vicisitud.\n• Debilidad: Apego a su tierra. Deben descansar rodeados de al menos dos puñados de tierra de un lugar importante para ellos (normalmente donde nacieron o fueron Abrazados).",
    
    "Ventrue": "Los Ventrue son la realeza de los Condenados. Dirigen la Camarilla y valoran el linaje, el éxito corporativo y la influencia en la sociedad mortal por encima de todo.\n\n• Disciplinas: Dominación, Fortaleza, Presencia.\n• Debilidad: Gusto refinado y exclusivo. Solo pueden beber sangre de un tipo específico de mortal (ej. mujeres jóvenes, sacerdotes, policías)."
}

lore_conceptos = {
    "Naturaleza": "La Naturaleza es el verdadero 'yo' de tu personaje, su personalidad más profunda y auténtica. En términos de juego, recuperas puntos de Fuerza de Voluntad cuando actúas de acuerdo a tu Naturaleza.\n\nEjemplos: Arquitecto, Autócrata, Bribón, Director, Mártir, Monstruo, Sobreviviente.",
    
    "Conducta": "La Conducta es la máscara o fachada que tu vampiro presenta al mundo. Es cómo te perciben los demás. En la traicionera sociedad de la Estirpe, mostrar tu verdadera Naturaleza es peligroso, por lo que la Conducta suele ser diferente.",
    
    "Concepto": "El Concepto es un resumen de quién era tu personaje antes del Abrazo (su vida mortal). Es el ancla de su Humanidad.\n\nEjemplos: 'Policía corrupto', 'Estudiante endeudado', 'Artista torturado', 'Heredero arruinado'.",
    
    "Generación": "La Generación indica a qué distancia está tu vampiro de Caín, el Primero. Los jugadores suelen empezar en la 13ª Generación. Cuanto más baja es (ej: 10ª u 8ª), más poderosa es tu sangre, pero para ello debes comprar el Trasfondo 'Generación'.",
    
    "Sire": "El Sire es el vampiro que te dio el Abrazo y te convirtió. En la Camarilla, tu Sire es tu maestro y responsable legal de tus acciones hasta que te presenta formalmente al Príncipe de la ciudad."
}

lore_opciones_concepto = {
    # Arquetipos (Sirven para Naturaleza y Conducta)
    "Arquitecto": "Tu sentido de la vida es construir un legado. Recuperas 1 punto de Fuerza de Voluntad cuando estableces algo de importancia o valor duradero.",
    "Autócrata": "Necesitas tener el control absoluto de la situación. Recuperas 1 punto de Fuerza de Voluntad cuando consigues el control sobre un grupo o una crisis.",
    "Bribón": "Solo te importas tú mismo. Recuperas 1 punto de Fuerza de Voluntad cuando tu actitud egoísta te salva de perder algo o te proporciona una ventaja.",
    "Director": "Odias el caos y amas el orden. Recuperas 1 punto de Fuerza de Voluntad cuando logras liderar a un grupo y completar una tarea difícil.",
    "Mártir": "Sufres por los demás. Recuperas 1 punto de Fuerza de Voluntad cuando te sacrificas de forma genuina por otro o por un ideal de forma perjudicial para ti.",
    "Monstruo": "Has abrazado la Bestia interior. Recuperas 1 punto de Fuerza de Voluntad cuando realizas un acto verdaderamente atroz sin mostrar remordimientos.",
    "Sobreviviente": "Nada puede acabar contigo. Recuperas 1 punto de Fuerza de Voluntad cuando sobrevives a una situación que amenazaba tu existencia mediante tu astucia o resistencia.",
    
    # Generaciones
    "13ª Generación": "La generación más común para neonatos. \n• Capacidad de Sangre: 10\n• Puntos por turno: 1\n• Coste: 0 puntos de Trasfondo.",
    "12ª Generación": "Tu sangre es un poco más fuerte. \n• Capacidad de Sangre: 11\n• Puntos por turno: 1\n• Coste: 1 punto de Trasfondo (Generación).",
    "11ª Generación": "Un paso más cerca de Caín. \n• Capacidad de Sangre: 12\n• Puntos por turno: 1\n• Coste: 2 puntos de Trasfondo (Generación).",
    "10ª Generación": "Tu sangre empieza a ser respetable. \n• Capacidad de Sangre: 13\n• Puntos por turno: 1\n• Coste: 3 puntos de Trasfondo (Generación).",
    "9ª Generación": "Sangre poderosa. \n• Capacidad de Sangre: 14\n• Puntos por turno: 2\n• Coste: 4 puntos de Trasfondo (Generación).",
    "8ª Generación": "El límite para un personaje inicial. Eres notablemente poderoso. \n• Capacidad de Sangre: 15\n• Puntos por turno: 3\n• Coste: 5 puntos de Trasfondo (Generación)."
}

# --- FUNCIONES LÓGICAS ---
def actualizar_guia_clan(evento):
    clan = evento.value
    info = lore_clanes.get(clan, "Información de este clan no disponible aún.")
    texto_guia.set_text(f"CLAN {clan.upper()}\n\n{info}")
    
def actualizar_guia_desplegable(evento, categoria):
    seleccion = evento.value
    
    # 1. Buscamos qué significa la categoría en general (ej: qué es la Naturaleza)
    info_general = lore_conceptos.get(categoria, "")
    
    # 2. Buscamos qué hace la opción elegida (ej: el arquetipo Arquitecto)
    info_especifica = lore_opciones_concepto.get(seleccion, "Información no disponible.")
    
    # 3. Construimos el texto combinando ambas con una separación clara
    texto_combinado = f"{categoria.upper()}\n\n{info_general}\n\n{'='*30}\n\n{seleccion.upper()}\n\n{info_especifica}"
    
    # 4. Actualizamos el panel lateral
    texto_guia.set_text(texto_combinado)
    
def actualizar_guia_concepto(campo):
    info = lore_conceptos.get(campo, "")
    if info:
        texto_guia.set_text(f"{campo.upper()}\n\n{info}")

def modificar_atributos(categoria, atributo, delta, label_puntos):
    prio = prioridades_attr[categoria]
    if not prio:
        ui.notify(f"Selecciona primero una prioridad para la categoría {categoria}.", type='warning')
        return

    # Extraer el máximo de puntos de la selección (7, 5 o 3)
    max_pts = 7 if "7" in prio else (5 if "5" in prio else 3)
    
    # Calcular gastados restando 1 (el punto base gratuito)
    gastados = sum(atributos[categoria][a] - 1 for a in atributos[categoria])
    valor_actual = atributos[categoria][atributo]
    nuevo_valor = valor_actual + delta

    # Validaciones matemáticas
    if delta > 0: # Sumar
        if gastados >= max_pts:
            ui.notify(f"Límite de {max_pts} puntos alcanzado en {categoria}.", type='info')
            return
        if nuevo_valor > 5:
            return
    elif delta < 0: # Restar
        if nuevo_valor < 1:
            return

    # Aplicar cambios al estado y a la interfaz
    atributos[categoria][atributo] = nuevo_valor
    label_puntos.set_text("●" * nuevo_valor + "○" * (5 - nuevo_valor))


# --- ESTILOS GRÁFICOS Y AMBIENTACIÓN ---

# 1. Forzar el Modo Oscuro nativo
ui.dark_mode().enable()

# 2. Inyectar CSS personalizado para fuentes góticas y texturas
ui.add_head_html('''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=EB+Garamond:wght@400;700&display=swap');
        
        body {
            /* Fondo oscuro profundo con un ligero degradado radial */
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
            border: 1px solid #7f1d1d !important; /* Borde rojo sangre oscuro */
            box-shadow: 0 6px 15px rgba(153, 27, 27, 0.15) !important;
            border-radius: 8px;
        }
        .panel-lateral {
            background-color: rgba(20, 20, 20, 0.8) !important;
            border-left: 2px solid #7f1d1d;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.8);
        }
        /* Personalizar el aspecto de las pestañas de NiceGUI/Quasar */
        .q-tab { color: #71717a; }
        .q-tab--active { color: #dc2626 !important; font-weight: bold; }
        .q-tab-panel { background-color: transparent !important; }
    </style>
''')

# --- INTERFAZ GRÁFICA ---
ui.page_title('Vampiro V20 - Creador de Personajes')

# Cabecera inmersiva
with ui.row().classes('w-full justify-center items-center py-6 bg-black border-b-2 border-red-900 shadow-2xl'):
    # Si descargas el logo de V20, quita el '#' de la siguiente línea y pon la ruta a tu imagen:
    # ui.image('logo_v20.png').classes('w-32 mr-6') 
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
                        arquetipos = ["Arquitecto", "Autócrata", "Bribón", "Director", "Mártir", "Monstruo", "Sobreviviente"]
                        ui.select(arquetipos, label='Naturaleza:', on_change=lambda e: actualizar_guia_desplegable(e, "Naturaleza")).classes('w-48')
                        ui.select(arquetipos, label='Conducta:', on_change=lambda e: actualizar_guia_desplegable(e, "Conducta")).classes('w-48')
                        ui.input('Concepto:').classes('w-48').on('focus', lambda: texto_guia.set_text("CONCEPTO\n\nEl Concepto es un resumen de quién era tu personaje antes del Abrazo (su vida mortal). Es el ancla de su Humanidad.\n\nEjemplos: 'Policía corrupto', 'Estudiante endeudado', 'Artista torturado'."))
                    
                    with ui.column():
                        clanes = ['Assamita', 'Brujah', 'Gangrel', 'Giovanni', 'Lasombra', 'Malkavian', 'Nosferatu', 'Ravnos', 'Seguidores de Set', 'Toreador', 'Tremere', 'Tzimisce', 'Ventrue']
                        ui.select(clanes, label='Clan:', on_change=actualizar_guia_clan).classes('w-48')
                        generaciones = ["13ª Generación", "12ª Generación", "11ª Generación", "10ª Generación", "9ª Generación", "8ª Generación"]
                        ui.select(generaciones, label='Generación:', on_change=lambda e: actualizar_guia_desplegable(e, "Generación")).classes('w-48')
                        ui.input('Sire:').classes('w-48').on('focus', lambda: texto_guia.set_text("SIRE\n\nEl Sire es el vampiro que te dio el Abrazo y te convirtió. Es tu maestro y el responsable de tus acciones."))

            # PESTAÑA ATRIBUTOS
            with ui.tab_panel(tab_atributos):
                with ui.row().classes('w-full justify-around'):
                    opciones_prio = ['Primario (7 pts)', 'Secundario (5 pts)', 'Terciario (3 pts)']
                    for cat_nombre, attrs in atributos.items():
                        with ui.card().classes('w-64 tarjeta-vampiro p-4'):
                            ui.label(cat_nombre).classes('text-xl text-red-600 titulo-gotico mb-2 border-b border-red-900 w-full pb-1')
                            ui.select(opciones_prio, label='Prioridad', on_change=lambda e, c=cat_nombre: prioridades_attr.update({c: e.value})).classes('w-full mb-4')
                            
                            for attr_name, val in attrs.items():
                                with ui.row().classes('items-center justify-between w-full no-wrap mb-1'):
                                    ui.label(attr_name).classes('w-20 text-md text-gray-300')
                                    lbl_puntos = ui.label("●" * val + "○" * (5 - val)).classes('text-red-700 text-lg font-mono tracking-widest')
                                    with ui.row().classes('no-wrap gap-1'):
                                        ui.button('-', on_click=lambda e, c=cat_nombre, a=attr_name, l=lbl_puntos: modificar_atributos(c, a, -1, l)).props('dense size=sm color="dark"')
                                        ui.button('+', on_click=lambda e, c=cat_nombre, a=attr_name, l=lbl_puntos: modificar_atributos(c, a, 1, l)).props('dense size=sm color="dark"')

            # PESTAÑA HABILIDADES
            with ui.tab_panel(tab_habilidades):
                with ui.row().classes('w-full justify-around items-start'):
                    for grupo_nombre, lista_habs in habilidades.items():
                        with ui.card().classes('w-64 tarjeta-vampiro p-4'):
                            ui.label(grupo_nombre).classes('text-xl text-red-600 titulo-gotico mb-2 border-b border-red-900 w-full pb-1')
                            for hab_name in lista_habs:
                                with ui.row().classes('items-center justify-between w-full no-wrap mb-1'):
                                    ui.label(hab_name).classes('w-24 text-sm text-gray-300')
                                    ui.label("○○○○○").classes('text-red-700 text-lg font-mono tracking-widest')

            # PESTAÑA VENTAJAS
            with ui.tab_panel(tab_ventajas):
                with ui.card().classes('w-full tarjeta-vampiro p-8 items-center'):
                    ui.label('Espacio reservado para las Disciplinas, Trasfondos y Virtudes.').classes('text-lg text-gray-400 font-style: italic')

    # Panel Derecho: Guía del Narrador (Ocupa 1/3 del ancho)
    with ui.column().classes('w-1/3 panel-lateral p-6 rounded-lg h-full'):
        ui.label('LA BIBLIOTECA OSCURA').classes('text-2xl text-red-700 titulo-gotico mb-4 border-b border-red-900 pb-2 w-full text-center')
        texto_guia = ui.label('Bienvenido, Vástago.\n\nSelecciona opciones en tu hoja de personaje para desvelar los secretos de tu linaje y tu naturaleza.').classes('text-lg text-gray-300 whitespace-pre-line leading-relaxed')

ui.run()