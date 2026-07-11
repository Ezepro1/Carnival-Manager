import customtkinter as ctk
from tkinter import messagebox
from datos import PJS
import os

BANDERAS_SUD = {"Argentina": "arg", "Uruguay": "uru", "Paraguay": "par", "Bolivia": "bol", "Chile": "chi", "Brasil": "br", "Peru": "per", "China": "chn"}
BANDERAS_CEN = {
    "Venezuela": "ven", "Colombia": "col", "Ecuador": "ecu", "Guyana": "guy", "Surinam": "sur", 
            "Guayana Francesa": "guf", "Panamá": "pan", "Costa Rica": "cri", "Nicaragua": "nic", 
            "Honduras": "hon", "Guatemala": "gua", "México": "mex", "Puerto Rico": "pri", 
            "Rep. Dominicana": "dom", "Trinidad y Tobago": "tto","Antigua y Barbuda": "atg",
            "Bahamas": "bhs","Barbados": "brb","Cuba": "cub","Dominica": "dma","Granada": "grd",
            "Haití": "hti","Jamaica": "jam","Santa Lucía": "lca",
            "San Vicente y las Granadinas": "vct","El Salvador": "slv", "Belice": "blz"
}

def ejecutar_ingreso(master_frame, callback_volver, region="SUD"):
    #depende el boton saldra uno u otro
    if region == "SUD": 
         titulo, archivo, banderas = "NUEVO COMPETIDOR SUD", "players.txt", BANDERAS_SUD
    else:
        titulo, archivo, banderas = "NUEVO COMPETIDOR CEN", "playersCEN.txt", BANDERAS_CEN

    def guardar_datos():
        nom = entry_nom.get().strip().capitalize()
        pais_emoji = combo_pais.get()
        pais_codigo = banderas.get(pais_emoji)
        pts = entry_pts.get()
        team = entry_team.get().strip() or "-"
        main = combo_main.get()
        sub1 = combo_sub1.get()
        sub2 = combo_sub2.get()

        if not nom:
            messagebox.showerror("Error", "Nombre obligatorio")
            return
        nombres_existentes = []
        try:
            # Abrimos el archivo correspondiente (SUD o CEN) para leer
            if os.path.exists(archivo):
                with open(archivo, "r", encoding="utf-8") as f:
                    for linea in f:
                       
                        nombre_en_lista = linea.split(";")[0]
                        nombres_existentes.append(nombre_en_lista.lower())

            # Comparamos en minúsculas
            if nom.lower() in nombres_existentes:
                messagebox.showerror("Error", f"El jugador '{nom}' ya está registrado en {region}.")
                return
        except Exception as e:
            print(f"Error al verificar duplicados: {e}")
        try:
            with open(archivo, "a", encoding="utf-8") as f:
                f.write(f"{nom};{pais_codigo};{pts};{team};{main};{sub1};{sub2}\n")
            messagebox.showinfo("Éxito", f"Jugador {nom} guardado")
            entry_nom.delete(0, 'end')
            entry_nom.focus()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    # --- Interfaz (Compacta) ---
    ctk.CTkLabel(master_frame, text=titulo, font=("Now", 20, "bold")).pack(pady=20)
    entry_nom = ctk.CTkEntry(master_frame, width=250, placeholder_text="Nombre"); entry_nom.pack(pady=5)
    
    combo_pais = ctk.CTkOptionMenu(master_frame, values=list(banderas.keys()), width=250); combo_pais.pack(pady=5)
    entry_pts = ctk.CTkEntry(master_frame, width=250); entry_pts.insert(0, "0"); entry_pts.pack(pady=5)
    entry_team = ctk.CTkEntry(master_frame, width=250, placeholder_text="Team"); entry_team.pack(pady=5)
    
    combo_main = ctk.CTkOptionMenu(master_frame, values=PJS, width=250); combo_main.pack(pady=5)
    combo_sub1 = ctk.CTkOptionMenu(master_frame, values=[""] + PJS, width=250); combo_sub1.pack(pady=5)
    combo_sub2 = ctk.CTkOptionMenu(master_frame, values=[""] + PJS, width=250); combo_sub2.pack(pady=5)

    ctk.CTkButton(master_frame, text="GUARDAR", fg_color="green", command=guardar_datos).pack(pady=20)
    ctk.CTkButton(master_frame, text="VOLVER", fg_color="gray", command=callback_volver).pack()