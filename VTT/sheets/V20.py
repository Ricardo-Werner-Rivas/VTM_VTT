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
    "Brujah": "Los Brujah son rebeldes, apasionados y violentos. Antaño fueron reyes filósofos en Cartago, pero hoy son conocidos por su furia y su lucha contra el orden establecido.\n\n• Disciplinas: Celeridad, Potencia, Presencia.\n• Debilidad: Su sangre hierve fácilmente; la dificultad para resistir el frenesí aumenta en 2.",
    "Nosferatu": "Los Nosferatu sufren la Maldición de Caín en su propia carne. El Abrazo los deforma monstruosamente. Aislados del resto, son los grandes espías y traficantes de secretos.\n\n• Disciplinas: Animalismo, Ofuscación, Potencia.\n• Debilidad: Apariencia cero (no puede subirse con puntos).",
    "Ventrue": "Los Ventrue son la realeza de los Condenados. Dirigen la Camarilla y valoran el linaje, el éxito corporativo y la influencia en la sociedad mortal.\n\n• Disciplinas: Dominación, Fortaleza, Presencia.\n• Debilidad: Gusto refinado. Solo pueden beber sangre de un tipo específico de mortal."
}

# --- FUNCIONES LÓGICAS ---
def actualizar_guia_clan(evento):
    clan = evento.value
    info = lore_clanes.get(clan, "Información de este clan no disponible aún.")
    texto_guia.set_text(f"CLAN {clan.upper()}\n\n{info}")

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


# --- INTERFAZ GRÁFICA ---
ui.page_title('Vampiro V20 - Creador de Personajes')

with ui.row().classes('w-full h-screen no-wrap p-4 bg-gray-50'):
    
    # Panel Izquierdo: Ficha (Ocupa 2/3 del ancho)
    with ui.column().classes('w-2/3'):
        with ui.tabs().classes('w-full') as tabs:
            tab_concepto = ui.tab('1. Concepto')
            tab_atributos = ui.tab('2. Atributos')
            tab_habilidades = ui.tab('3. Habilidades')
            tab_ventajas = ui.tab('4. Ventajas')

        with ui.tab_panels(tabs, value=tab_concepto).classes('w-full bg-white shadow-md rounded-b-lg border'):
            
            # PESTAÑA CONCEPTO
            with ui.tab_panel(tab_concepto):
                with ui.row().classes('w-full gap-8 justify-center'):
                    with ui.column():
                        ui.input('Nombre:').classes('w-48')
                        ui.input('Jugador:').classes('w-48')
                        ui.input('Crónica:').classes('w-48')
                    with ui.column():
                        ui.input('Naturaleza:').classes('w-48')
                        ui.input('Conducta:').classes('w-48')
                        ui.input('Concepto:').classes('w-48')
                    with ui.column():
                        clanes = ['Assamita', 'Brujah', 'Gangrel', 'Giovanni', 'Lasombra', 'Malkavian', 'Nosferatu', 'Ravnos', 'Seguidores de Set', 'Toreador', 'Tremere', 'Tzimisce', 'Ventrue']
                        ui.select(clanes, label='Clan:', on_change=actualizar_guia_clan).classes('w-48')
                        ui.input('Generación:').classes('w-48')
                        ui.input('Sire:').classes('w-48')

            # PESTAÑA ATRIBUTOS
            with ui.tab_panel(tab_atributos):
                with ui.row().classes('w-full justify-around'):
                    opciones_prio = ['Primario (7 pts)', 'Secundario (5 pts)', 'Terciario (3 pts)']
                    for cat_nombre, attrs in atributos.items():
                        with ui.card().classes('w-64'):
                            ui.label(cat_nombre).classes('text-xl font-bold mb-2')
                            
                            # Bind de la prioridad
                            ui.select(opciones_prio, label='Prioridad', on_change=lambda e, c=cat_nombre: prioridades_attr.update({c: e.value})).classes('w-full mb-4')
                            
                            for attr_name, val in attrs.items():
                                with ui.row().classes('items-center justify-between w-full no-wrap mb-1'):
                                    ui.label(attr_name).classes('w-20 text-sm')
                                    lbl_puntos = ui.label("●" * val + "○" * (5 - val)).classes('text-red-800 text-lg font-mono tracking-widest')
                                    with ui.row().classes('no-wrap gap-1'):
                                        ui.button('-', on_click=lambda e, c=cat_nombre, a=attr_name, l=lbl_puntos: modificar_atributos(c, a, -1, l)).props('dense size=sm color="grey"')
                                        ui.button('+', on_click=lambda e, c=cat_nombre, a=attr_name, l=lbl_puntos: modificar_atributos(c, a, 1, l)).props('dense size=sm color="grey"')

            # PESTAÑA HABILIDADES
            with ui.tab_panel(tab_habilidades):
                with ui.row().classes('w-full justify-around items-start'):
                    for grupo_nombre, lista_habs in habilidades.items():
                        with ui.card().classes('w-64'):
                            ui.label(grupo_nombre).classes('text-xl font-bold mb-2')
                            for hab_name in lista_habs:
                                with ui.row().classes('items-center justify-between w-full no-wrap mb-1'):
                                    ui.label(hab_name).classes('w-24 text-sm')
                                    ui.label("○○○○○").classes('text-red-800 text-lg font-mono tracking-widest')

            # PESTAÑA VENTAJAS
            with ui.tab_panel(tab_ventajas):
                ui.label('Espacio reservado para las Disciplinas, Trasfondos y Virtudes.').classes('text-lg')

    # Panel Derecho: Guía (Ocupa 1/3 del ancho)
    with ui.column().classes('w-1/3 bg-[#1e1e1e] p-6 rounded-lg shadow-inner text-gray-300 h-full'):
        ui.label('Guía de La Biblioteca Oscura').classes('text-2xl font-bold text-white mb-4 border-b border-gray-600 pb-2 w-full')
        texto_guia = ui.label('Bienvenido al creador de personajes.\n\nSelecciona opciones en la ficha para recibir ayuda e información sobre el trasfondo.').classes('text-base whitespace-pre-line')

# Iniciar la aplicación
ui.run()