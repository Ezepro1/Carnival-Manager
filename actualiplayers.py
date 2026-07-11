import customtkinter as ctk
from tkinter import messagebox
from datos import PJS
from PIL import Image, ImageDraw, ImageFont
import os
import sys

def obtener_ruta(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

CONFIG_ACTUALI = {
    "SUD": {
        "archivo": "players.txt",
        "default_pais": "Argentina",
        "banderas": {"Argentina": "arg", "Uruguay": "uru", "Paraguay": "par", "Bolivia": "bol", "Chile": "chi", "Brasil": "br", "Peru": "per", "China": "chn"}
        #china agregada especialmente para un jugador
    },
    "CEN": {
        "archivo": "playersCEN.txt",
        "default_pais": "Venezuela",
        "banderas": {
            "Venezuela": "ven", "Colombia": "col", "Ecuador": "ecu", "Guyana": "guy", "Surinam": "sur", 
            "Guayana Francesa": "guf", "Panamá": "pan", "Costa Rica": "cri", "Nicaragua": "nic", 
            "Honduras": "hon", "Guatemala": "gua", "México": "mex", "Puerto Rico": "pri", 
            "Rep. Dominicana": "dom", "Trinidad y Tobago": "tto","Antigua y Barbuda": "atg",
            "Bahamas": "bhs","Barbados": "brb","Cuba": "cub","Dominica": "dma","Granada": "grd",
            "Haití": "hti","Jamaica": "jam","Santa Lucía": "lca",
            "San Vicente y las Granadinas": "vct","El Salvador": "slv", "Belice": "blz"
        } # "San Cristóbal y Nieves": "kna" no encontre una buena bandera para añadir
    }
}

def ejecutar_actualizacion(master_frame, callback_volver, region="SUD"):
    conf = CONFIG_ACTUALI[region]
    BANDERAS_REVERSO = {v: k for k, v in conf["banderas"].items()}
    jugadores = []
    seleccionado = {"nombre": None} 

    pais_actual = ctk.StringVar(value=conf["default_pais"])
    lista_paises_visible = False

    def cargar_icono_bandera(codigo, size=(30, 20)):
        try:
            path = obtener_ruta(f"archivos/banderas/{codigo}.png")
            img = Image.open(path).convert("RGBA")
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except: return None

    def toggle_menu_paises():
        nonlocal lista_paises_visible
        if lista_paises_visible:
            frame_lista_desplegable.place_forget()
            lista_paises_visible = False
        else:
            x = btn_selector_pais.winfo_x() + col1.winfo_x()
            y = btn_selector_pais.winfo_y() + col1.winfo_y() + 35
            frame_lista_desplegable.place(x=x, y=y)
            frame_lista_desplegable.lift()
            lista_paises_visible = True

    def seleccionar_pais(nombre):
        pais_actual.set(nombre)
        codigo = conf["banderas"].get(nombre)
        btn_selector_pais.configure(text=f"  {nombre}", image=cargar_icono_bandera(codigo))
        frame_lista_desplegable.place_forget()
        nonlocal lista_paises_visible
        lista_paises_visible = False
        actualizar_preview()

    def cargar_archivo():
        nonlocal jugadores
        nueva_lista = []
        try:
            if os.path.exists(conf["archivo"]):
                with open(conf["archivo"], "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if not linea: continue
                        d = linea.split(";")
                        if len(d) >= 5:
                            while len(d) < 7: d.append("")
                            nueva_lista.append({
                                "nom": d[0], "pais": d[1], "pts": d[2],
                                "team": d[3], "main": d[4], "sub1": d[5], "sub2": d[6]
                            })
                jugadores = nueva_lista
        except Exception as e: print(f"Error al cargar: {e}")

    def dibujar_lista(lista_nombres):
        for b in botones_lista: b.destroy()
        botones_lista.clear()
        for nombre in lista_nombres:
            btn = ctk.CTkButton(frame_scroll, text=nombre, fg_color="transparent", anchor="w", 
                                command=lambda n=nombre: seleccionar_jugador(n))
            btn.pack(fill="x", padx=5, pady=2)
            botones_lista.append(btn)

    def filtrar_jugadores(event=None):
        termino = entry_busqueda.get().lower()
        filtrados = [j["nom"] for j in jugadores if termino in j["nom"].lower()]
        dibujar_lista(sorted(filtrados, key=str.lower))

    def seleccionar_jugador(nombre):
        seleccionado["nombre"] = nombre
        jugador = next((j for j in jugadores if j["nom"] == nombre), None)
        if jugador:
            entry_nom.delete(0, 'end'); entry_nom.insert(0, jugador["nom"])
            entry_pts.delete(0, 'end'); entry_pts.insert(0, str(jugador["pts"]))
            entry_team.delete(0, 'end'); entry_team.insert(0, "" if jugador["team"] == "-" else jugador["team"])
            combo_main.set(jugador["main"])
            combo_sub1.set(jugador["sub1"]); combo_sub2.set(jugador["sub2"])
            nombre_pais = BANDERAS_REVERSO.get(jugador["pais"], conf["default_pais"])
            seleccionar_pais(nombre_pais)

    def actualizar_preview(*args):
        preview_canvas = Image.new("RGBA", (800, 160), (255, 255, 255, 0))
        draw = ImageDraw.Draw(preview_canvas)
        centro_y = 80
        try:
            f_path = obtener_ruta("archivos/Now-Bold.otf")
            fuente, fuente_rank = ImageFont.truetype(f_path, 45), ImageFont.truetype(f_path, 55)
        except: fuente = ImageFont.load_default(); fuente_rank = fuente

        draw.rectangle([0, 40, 100, 120], fill="#ff3131")
        draw.rectangle([100, 40, 650, 120], fill="#000000")
        draw.text((50, centro_y), entry_pts.get().upper() or "0", font=fuente_rank, fill="white", anchor="mm")
        
        team, nom = entry_team.get().upper(), entry_nom.get().upper()
        draw.text((120, centro_y), f"{team}  {nom}" if team else nom, font=fuente, fill="white", anchor="lm")

        try:
            pj_img = Image.open(obtener_ruta(f"archivos/imgpjs/{combo_main.get()}.png")).convert("RGBA")
            alto_pj = 85
            ratio = alto_pj / pj_img.size[1]
            pj_img = pj_img.resize((int(pj_img.size[0] * ratio), alto_pj), Image.Resampling.LANCZOS)
            
            # --- EFECTO DESVANECER IZQUIERDA ---
            mask = Image.new("L", pj_img.size, 0)
            for x in range(pj_img.size[0]):
                alpha = int(255 * (x / pj_img.size[0]))
                for y in range(pj_img.size[1]):
                    mask.putpixel((x, y), alpha)
            pj_img.putalpha(mask)
            
            preview_canvas.alpha_composite(pj_img, (225, int(centro_y - (alto_pj // 2))))
            
            cod_pais = conf["banderas"].get(pais_actual.get())
            bandera = Image.open(obtener_ruta(f"archivos/banderas/{cod_pais}.png")).convert("RGBA").resize((80, 80))
            preview_canvas.alpha_composite(bandera, (670, 40))
        except: pass

        img_ctk = ctk.CTkImage(light_image=preview_canvas, dark_image=preview_canvas, size=(400, 80))
        label_preview.configure(image=img_ctk)

    def guardar_cambios():
        if not seleccionado["nombre"]: return
        for j in jugadores:
            if j["nom"] == seleccionado["nombre"]:
                j["nom"], j["pts"] = entry_nom.get().strip(), entry_pts.get().strip()
                j["pais"] = conf["banderas"].get(pais_actual.get())
                j["team"] = entry_team.get().strip() or "-"
                j["main"], j["sub1"], j["sub2"] = combo_main.get(), combo_sub1.get(), combo_sub2.get()
                break
        try:
            with open(conf["archivo"], "w", encoding="utf-8") as f:
                for j in jugadores:
                    f.write(f"{j['nom']};{j['pais']};{j['pts']};{j['team']};{j['main']};{j['sub1']};{j['sub2']}\n")
            messagebox.showinfo("Éxito", "Cambios guardados.")
            refrescar_buscador(entry_nom.get().strip())
        except Exception as e: messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def eliminar_jugador():
        if not seleccionado["nombre"]: return
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {seleccionado['nombre']}?"):
            jugadores[:] = [j for j in jugadores if j["nom"] != seleccionado["nombre"]]
            try:
                with open(conf["archivo"], "w", encoding="utf-8") as f:
                    for j in jugadores:
                        f.write(f"{j['nom']};{j['pais']};{j['pts']};{j['team']};{j['main']};{j['sub1']};{j['sub2']}\n")
                messagebox.showinfo("Éxito", "Jugador eliminado.")
                refrescar_buscador()
            except Exception as e: messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def refrescar_buscador(nombre_a_seleccionar=None):
        cargar_archivo()
        filtrar_jugadores()
        if nombre_a_seleccionar: seleccionar_jugador(nombre_a_seleccionar)
        elif jugadores: seleccionar_jugador(jugadores[0]["nom"])

    # --- DISEÑO VISUAL ---
    ctk.CTkLabel(master_frame, text=f"EDITAR JUGADOR - {region}", font=("Now", 24, "bold")).pack(pady=20)
    frame_main = ctk.CTkFrame(master_frame, fg_color="transparent")
    frame_main.pack(expand=True, fill="both", padx=20)

    # COLUMNA IZQUIERDA
    frame_lista = ctk.CTkFrame(frame_main, fg_color="transparent", width=250)
    frame_lista.pack(side="left", fill="y", padx=(0, 30))
    entry_busqueda = ctk.CTkEntry(frame_lista, placeholder_text="Filtrar...", width=220)
    entry_busqueda.pack(pady=(0, 10)); entry_busqueda.bind("<KeyRelease>", filtrar_jugadores)
    botones_lista = []
    frame_scroll = ctk.CTkScrollableFrame(frame_lista, width=220, height=550, label_text="Lista de Jugadores")
    frame_scroll.pack(expand=True, fill="both")

    # COLUMNA DERECHA
    frame_edicion = ctk.CTkFrame(frame_main, fg_color="transparent")
    frame_edicion.pack(side="left", expand=True, fill="both")
    label_preview = ctk.CTkLabel(frame_edicion, text="")
    label_preview.pack(pady=(0, 20))
    frame_form = ctk.CTkFrame(frame_edicion, fg_color="transparent")
    frame_form.pack()

    # FORM COL 1
    col1 = ctk.CTkFrame(frame_form, fg_color="transparent")
    col1.pack(side="left", padx=20)
    ctk.CTkLabel(col1, text="Nombre:").pack(anchor="w")
    entry_nom = ctk.CTkEntry(col1, width=320); entry_nom.pack(pady=(0, 10))
    ctk.CTkLabel(col1, text="Team (Opcional):").pack(anchor="w")
    entry_team = ctk.CTkEntry(col1, width=320); entry_team.pack(pady=(0, 10))
    ctk.CTkLabel(col1, text="Puntos Totales:").pack(anchor="w")
    entry_pts = ctk.CTkEntry(col1, width=320); entry_pts.pack(pady=(0, 10))
    ctk.CTkLabel(col1, text="País:").pack(anchor="w")
    btn_selector_pais = ctk.CTkButton(col1, text=f"  {conf['default_pais']}", image=cargar_icono_bandera(conf["banderas"][conf["default_pais"]]), compound="left", width=320, height=35, anchor="w", fg_color="#1f538d", hover_color="#14375e", command=toggle_menu_paises)
    btn_selector_pais.pack(pady=(0, 10))

    frame_lista_desplegable = ctk.CTkScrollableFrame(frame_edicion, width=300, height=200, fg_color="#2b2b2b", border_color="#555", border_width=1)
    for nombre_pais, codigo in conf["banderas"].items():
        img_bandera = cargar_icono_bandera(codigo)
        ctk.CTkButton(frame_lista_desplegable, text=f"  {nombre_pais}", image=img_bandera, compound="left", fg_color="transparent", text_color="white", hover_color="#444", anchor="w", command=lambda p=nombre_pais: seleccionar_pais(p)).pack(fill="x", padx=5, pady=2)

    # FORM COL 2
    col2 = ctk.CTkFrame(frame_form, fg_color="transparent")
    col2.pack(side="left", padx=20, anchor="n") 
    ctk.CTkLabel(col2, text="Main:").pack(anchor="w")
    combo_main = ctk.CTkOptionMenu(col2, values=PJS, width=320, command=actualizar_preview)
    combo_main.pack(pady=(0, 10))
    ctk.CTkLabel(col2, text="Personajes Secundarios:").pack(anchor="w")
    f_subs = ctk.CTkFrame(col2, fg_color="transparent")
    f_subs.pack()
    combo_sub1 = ctk.CTkOptionMenu(f_subs, values=[""] + PJS, width=155, command=actualizar_preview); combo_sub1.pack(side="left", padx=(0, 10))
    combo_sub2 = ctk.CTkOptionMenu(f_subs, values=[""] + PJS, width=155, command=actualizar_preview); combo_sub2.pack(side="left")

    # BOTONES
    frame_botones = ctk.CTkFrame(frame_edicion, fg_color="transparent")
    frame_botones.pack(pady=40)
    ctk.CTkButton(frame_botones, text="GUARDAR CAMBIOS", fg_color="#b30000", hover_color="#800000", width=200, height=35, command=guardar_cambios).grid(row=0, column=0, padx=10, pady=10)
    ctk.CTkButton(frame_botones, text="ELIMINAR JUGADOR", fg_color="#444444", hover_color="#8b0000", width=200, height=35, command=eliminar_jugador).grid(row=0, column=1, padx=10, pady=10)
    ctk.CTkButton(frame_botones, text="REFRESCAR VISTA PREVIA", fg_color="#555555", width=200, height=35, command=actualizar_preview).grid(row=1, column=0, padx=10, pady=10)
    ctk.CTkButton(frame_botones, text="← VOLVER AL MENÚ", fg_color="#2b2b2b", width=200, height=35, command=callback_volver).grid(row=1, column=1, padx=10, pady=10)

    refrescar_buscador()