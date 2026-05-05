import customtkinter as ctk
from tkinter import messagebox
from datos import PAISES, PJS


BANDERAS_DISPLAY = {
    "Argentina": "arg",
    "Uruguay": "uru",
    "Paraguay": "par",
    "Bolivia": "bol",
    "Chile": "chi",
    "Brasil": "bra",
    "Peru": "per"
}

def ejecutar_ingreso(master_frame, callback_volver):

    def guardar_datos(): #guardado de datos
        nom = entry_nom.get().strip()
        pais_emoji = combo_pais.get()
        pais_codigo = BANDERAS_DISPLAY.get(pais_emoji)
        pts = entry_pts.get()
        team = entry_team.get().strip() or "-"
        main = combo_main.get()
        sub1 = combo_sub1.get()
        sub2 = combo_sub2.get()

        if not nom:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return
        
        try:
            pts = int(pts)
        except ValueError:
            messagebox.showerror("Error", "Los puntos deben ser un número.")
            return

        nombres_existentes = [] # por si hay nombres que ya existen
        try:
            with open("players.txt", "r") as f:
                for linea in f:
                    nombres_existentes.append(linea.split(";")[0].lower())
        except FileNotFoundError: pass

        if nom.lower() in nombres_existentes:
            messagebox.showerror("Error", f"El nombre '{nom}' ya está registrado.")
            return

        # --- GUARDAR ---
        with open("players.txt", "a") as f:
            f.write(f"{nom};{pais_codigo};{pts};{team};{main};{sub1};{sub2}\n")
        
        messagebox.showinfo("Éxito", f"¡Jugador {nom} guardado correctamente!")

        # --- LIMPIAR CAMPOS PARA EL SIGUIENTE ---
        entry_nom.delete(0, 'end')
        entry_team.delete(0, 'end')
        entry_pts.delete(0, 'end')
        entry_pts.insert(0, "0")
        
        # Opcional: Resetear
        combo_sub1.set("")
        combo_sub2.set("")
        
        #el foco de escritura
        entry_nom.focus()

    # --- DISEÑO VISUAL ---
    ctk.CTkLabel(master_frame, text="NUEVO COMPETIDOR", font=("Now", 20, "bold")).pack(pady=20)
    entry_nom = ctk.CTkEntry(master_frame, width=250)
    entry_nom.pack(pady=5)

    ctk.CTkLabel(master_frame, text="Nombre del Jugador:").pack()
    ctk.CTkLabel(master_frame, text="País:").pack()
    combo_pais = ctk.CTkOptionMenu(master_frame, values=list(BANDERAS_DISPLAY.keys()), width=250)
    combo_pais.pack(pady=5)

    ctk.CTkLabel(master_frame, text="Puntos iniciales:").pack()
    entry_pts = ctk.CTkEntry(master_frame, width=250)
    entry_pts.insert(0, "0")
    entry_pts.pack(pady=5)

    ctk.CTkLabel(master_frame, text="Team (Opcional):").pack()
    entry_team = ctk.CTkEntry(master_frame, width=250, placeholder_text="Ej: BTG")
    entry_team.pack(pady=5)

    ctk.CTkLabel(master_frame, text="Personaje Principal:").pack()
    combo_main = ctk.CTkOptionMenu(master_frame, values=PJS, width=250)
    combo_main.pack(pady=5)

    ctk.CTkLabel(master_frame, text="Secundario (Opcional):").pack()
    combo_sub1 = ctk.CTkOptionMenu(master_frame, values=[""] + PJS, width=250)
    combo_sub1.pack(pady=5)

    ctk.CTkLabel(master_frame, text="Terciario (Opcional):").pack()
    combo_sub2 = ctk.CTkOptionMenu(master_frame, values=[""] + PJS, width=250)
    combo_sub2.pack(pady=5)

    btn_guardar = ctk.CTkButton(master_frame, text="GUARDAR JUGADOR", fg_color="green", hover_color="darkgreen", command=guardar_datos)
    btn_guardar.pack(pady=30)

    btn_volver = ctk.CTkButton(master_frame, text="← Volver al Menú", fg_color="gray", 
                               command=callback_volver)
    btn_volver.pack(pady=10)