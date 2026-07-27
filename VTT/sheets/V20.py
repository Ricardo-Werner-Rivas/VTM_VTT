import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class CreadorVampiro(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Vampiro V20 - Creador de Personajes")
        self.geometry("900x700")
        self.minsize(800, 600)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Diccionarios de datos
        self.atributos_vars = {}
        self.combos_prioridad_attr = {}
        
        # Categorías de Atributos
        self.categorias_atributos = {
            "Físicos": ["Fuerza", "Destreza", "Resistencia"],
            "Sociales": ["Carisma", "Manipulación", "Apariencia"],
            "Mentales": ["Percepción", "Inteligencia", "Astucia"]
        }

        self.crear_pestana_concepto()
        self.crear_pestana_atributos()
        self.crear_pestana_habilidades()
        self.crear_pestana_ventajas()

    def crear_pestana_concepto(self):
        frame_concepto = ttk.Frame(self.notebook)
        self.notebook.add(frame_concepto, text="1. Concepto")

        campos_izq = ["Nombre:", "Jugador:", "Crónica:"]
        campos_cen = ["Naturaleza:", "Conducta:", "Concepto:"]
        campos_der = ["Clan:", "Generación:", "Sire:"]

        for i, campo in enumerate(campos_izq):
            ttk.Label(frame_concepto, text=campo).grid(row=i, column=0, padx=10, pady=10, sticky="e")
            ttk.Entry(frame_concepto, width=25).grid(row=i, column=1, padx=10, pady=10)

        for i, campo in enumerate(campos_cen):
            ttk.Label(frame_concepto, text=campo).grid(row=i, column=2, padx=10, pady=10, sticky="e")
            ttk.Entry(frame_concepto, width=25).grid(row=i, column=3, padx=10, pady=10)

        for i, campo in enumerate(campos_der):
            ttk.Label(frame_concepto, text=campo).grid(row=i, column=4, padx=10, pady=10, sticky="e")
            if campo == "Clan:":
                clanes = ["Assamita", "Brujah", "Gangrel", "Giovanni", "Lasombra", 
                          "Malkavian", "Nosferatu", "Ravnos", "Seguidores de Set", 
                          "Toreador", "Tremere", "Tzimisce", "Ventrue"]
                combo_clan = ttk.Combobox(frame_concepto, values=clanes, state="readonly", width=22)
                combo_clan.grid(row=i, column=5, padx=10, pady=10)
            else:
                ttk.Entry(frame_concepto, width=25).grid(row=i, column=5, padx=10, pady=10)

    def crear_pestana_atributos(self):
        frame_atributos = ttk.Frame(self.notebook)
        self.notebook.add(frame_atributos, text="2. Atributos")

        prioridades = ["Primario (7 pts)", "Secundario (5 pts)", "Terciario (3 pts)"]

        for col_idx, (cat_nombre, attrs) in enumerate(self.categorias_atributos.items()):
            frame_cat = ttk.LabelFrame(frame_atributos, text=cat_nombre)
            frame_cat.grid(row=0, column=col_idx, padx=15, pady=15, sticky="n")

            ttk.Label(frame_cat, text="Prioridad:").grid(row=0, column=0, columnspan=4, pady=(5,0))
            combo_prio = ttk.Combobox(frame_cat, values=prioridades, state="readonly", width=17)
            combo_prio.grid(row=1, column=0, columnspan=4, pady=(0, 15))
            combo_prio.set("Seleccionar...")
            
            self.combos_prioridad_attr[cat_nombre] = combo_prio

            for row_idx, attr_name in enumerate(attrs, start=2):
                # Todos los atributos empiezan en 1
                self.atributos_vars[attr_name] = tk.IntVar(value=1) 
                
                ttk.Label(frame_cat, text=attr_name).grid(row=row_idx, column=0, padx=5, pady=5, sticky="w")
                lbl_puntos = ttk.Label(frame_cat, text="●○○○○", font=("Courier", 14), foreground="darkred")
                lbl_puntos.grid(row=row_idx, column=1, padx=5, pady=5)

                btn_menos = ttk.Button(frame_cat, text="-", width=2, 
                                       command=lambda a=attr_name, l=lbl_puntos, c=cat_nombre: self.modificar_atributos(a, -1, l, c))
                btn_menos.grid(row=row_idx, column=2, padx=2)

                btn_mas = ttk.Button(frame_cat, text="+", width=2, 
                                     command=lambda a=attr_name, l=lbl_puntos, c=cat_nombre: self.modificar_atributos(a, 1, l, c))
                btn_mas.grid(row=row_idx, column=3, padx=2)

    def modificar_atributos(self, atributo, delta, lbl_puntos, categoria):
        # 1. Validar la prioridad elegida
        seleccion = self.combos_prioridad_attr[categoria].get()
        if "7" in seleccion: max_pts = 7
        elif "5" in seleccion: max_pts = 5
        elif "3" in seleccion: max_pts = 3
        else:
            messagebox.showwarning("Atención", f"Selecciona primero una prioridad para los Atributos {categoria}.")
            return

        # 2. Calcular los puntos gastados sobre la base de 1
        gastados = sum(self.atributos_vars[a].get() - 1 for a in self.categorias_atributos[categoria])

        valor_actual = self.atributos_vars[atributo].get()
        nuevo_valor = valor_actual + delta

        # 3. Validar límites y avisar al usuario si llega al máximo
        if delta > 0: # Sumando
            if gastados >= max_pts:
                messagebox.showinfo("Límite alcanzado", f"Ya has repartido los {max_pts} puntos en los Atributos {categoria}.")
                return 
            if nuevo_valor > 5:
                return 
        elif delta < 0: # Restando
            if nuevo_valor < 1:
                return 

        # 4. Aplicar cambios visuales e internos
        self.atributos_vars[atributo].set(nuevo_valor)
        lbl_puntos.config(text="●" * nuevo_valor + "○" * (5 - nuevo_valor))

    def crear_pestana_habilidades(self):
        frame_habilidades = ttk.Frame(self.notebook)
        self.notebook.add(frame_habilidades, text="3. Habilidades")

        talentos = ["Alerta", "Atletismo", "Callejeo", "Consciencia", "Empatía", 
                    "Expresión", "Intimidación", "Liderazgo", "Pelea", "Subterfugio"]
        
        tecnicas = ["Armas de Fuego", "Artesanía", "Conducir", "Etiqueta", "Interpretación", 
                    "Latrocinio", "Pelea con Armas", "Sigilo", "Supervivencia", "T.c. Animales"]
        
        conocimientos = ["Academicismo", "Ciencias", "Finanzas", "Informática", "Investigación", 
                         "Leyes", "Medicina", "Ocultismo", "Política", "Tecnología"]

        grupos = {"Talentos": talentos, "Técnicas": tecnicas, "Conocimientos": conocimientos} 
        
        for col_idx, (nombre_grupo, habs) in enumerate(grupos.items()):
            frame_grupo = ttk.LabelFrame(frame_habilidades, text=nombre_grupo)
            frame_grupo.grid(row=0, column=col_idx, padx=15, pady=15, sticky="n")

            for row_idx, hab_name in enumerate(habs):
                ttk.Label(frame_grupo, text=hab_name).grid(row=row_idx, column=0, padx=5, pady=2, sticky="w")
                ttk.Label(frame_grupo, text="○○○○○", font=("Courier", 12), foreground="darkred").grid(row=row_idx, column=1, padx=5)

    def crear_pestana_ventajas(self):
        frame_ventajas = ttk.Frame(self.notebook)
        self.notebook.add(frame_ventajas, text="4. Ventajas y Rasgos")
        ttk.Label(frame_ventajas, text="Espacio reservado para las Disciplinas, Trasfondos y Virtudes.").pack(pady=20)

if __name__ == "__main__":
    app = CreadorVampiro()
    app.mainloop()