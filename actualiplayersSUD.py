import customtkinter as ctk
from tkinter import messagebox
from datos import PAISES, PJS
from PIL import Image, ImageDraw, ImageFont
import os
import sys

def obtener_ruta(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa) #temas de usar pyinstaller

# Diccionarios para las banderas
BANDERAS_DISPLAY = {"Argentina": "arg", "Uruguay": "uru", "Paraguay": "par", "Bolivia": "bol", "Chile": "chi", "Brasil": "br", "Peru": "per"}
BANDERAS_REVERSO = {v: k for k, v in BANDERAS_DISPLAY.items()}

def ejecutar_actualizacion(master_frame, callback_volver):
    jugadores = []
    seleccionado = {"nombre": None} 
    
    def cargar_archivo():
        nonlocal jugadores
        nueva_lista = []
        try:
            # prevencion utf-8 con las banderas
            if os.path.exists("players.txt"):
                with open("players.txt", "r", encoding="utf-8") as f:
                    for linea in f:
                        linea = linea.strip()
                        if not linea: continue
                        d = linea.split(";")
                        # Si tiene al menos los 5 campos básicos (Nombre a Main)
                        if len(d) >= 5:
                            # Rellenamos subs vacíos si faltan para evitar errores
                            while len(d) < 7: d.append("")
                            nueva_lista.append({
                                "nom": d[0], "pais": d[1], "pts": d[2],
                                "team": d[3], "main": d[4], "sub1": d[5], "sub2": d[6]
                            })
                jugadores = nueva_lista # Solo actualizamos si la lectura fue exitosa
        except Exception as e:
            print(f"Error al cargar archivo: {e}")

    # --- LÓGICA DE LA LISTA CON SCROLL ---
    botones_lista = []
    def dibujar_lista(lista_nombres):
        for b in botones_lista: b.destroy()
        botones_lista.clear()
        for nombre in lista_nombres:
            btn = ctk.CTkButton(frame_scroll, text=nombre, fg_color="transparent", 
                                text_color="white", hover_color="#333333", 
                                anchor="w", command=lambda n=nombre: seleccionar_jugador(n))
            btn.pack(fill="x", padx=5, pady=2)
            botones_lista.append(btn)

    def filtrar_jugadores(event=None):
        termino = entry_busqueda.get().lower()
        filtrados = [j["nom"] for j in jugadores if termino in j["nom"].lower()]
        dibujar_lista(sorted(filtrados, key=str.lower))

    def seleccionar_jugador(nombre):
        seleccionado["nombre"] = nombre
        cargar_datos(nombre)

    def refrescar_buscador(nombre_a_seleccionar=None):
        cargar_archivo()
        filtrar_jugadores()
        if nombre_a_seleccionar:
            seleccionar_jugador(nombre_a_seleccionar)
        elif jugadores:
            seleccionar_jugador(jugadores[0]["nom"])

    # --- LÓGICA DE PREVIEW (CON RUTAS PARA EXE) ---
    def actualizar_preview(*args):
        preview_canvas = Image.new("RGBA", (800, 160), (255, 255, 255, 0))
        draw = ImageDraw.Draw(preview_canvas)
        y_barra, alto_barra = 40, 80
        centro_y = y_barra + (alto_barra // 2)

        try:
            f_path = obtener_ruta("archivos/Now-Bold.otf")
            fuente = ImageFont.truetype(f_path, 45)
            fuente_rank = ImageFont.truetype(f_path, 55)
        except:
            fuente = ImageFont.load_default()

        draw.rectangle([0, y_barra, 100, y_barra + alto_barra], fill="#ff3131")
        draw.rectangle([100, y_barra, 650, y_barra + alto_barra], fill="#000000")
        
        pts_txt = entry_pts.get().upper() or "0"
        draw.text((50, centro_y), pts_txt, font=fuente_rank, fill="white", anchor="mm")
        
        team_txt = entry_team.get().upper()
        nom_txt = entry_nom.get().upper()
        full_name = f"{team_txt}  {nom_txt}" if team_txt else nom_txt
        draw.text((120, centro_y), full_name, font=fuente, fill="white", anchor="lm")

        try:
            pj_nombre = combo_main.get()
            pj_path = obtener_ruta(f"archivos/imgpjs/{pj_nombre}.png")
            pj_img = Image.open(pj_path).convert("RGBA")
            alto_pj = 85 
            ratio = alto_pj / pj_img.size[1]
            pj_img = pj_img.resize((int(pj_img.size[0] * ratio), alto_pj), Image.Resampling.LANCZOS)
            
            mask = Image.new("L", pj_img.size, 0)
            for x in range(pj_img.size[0]):
                alpha = int(255 * (x / pj_img.size[0]))
                for y in range(pj_img.size[1]): mask.putpixel((x, y), alpha)
            pj_img.putalpha(mask)
            preview_canvas.alpha_composite(pj_img, (225, int(centro_y - (alto_pj // 2))))
        except: pass

        try:
            cod_pais = BANDERAS_DISPLAY.get(combo_pais.get())
            band_path = obtener_ruta(f"archivos/banderas/{cod_pais}.png")
            bandera = Image.open(band_path).convert("RGBA")
            bandera = bandera.resize((80, 80))
            preview_canvas.alpha_composite(bandera, (670, int(centro_y - 40)))
        except: pass

        img_ctk = ctk.CTkImage(light_image=preview_canvas, dark_image=preview_canvas, size=(400, 80))
        label_preview.configure(image=img_ctk)
        label_preview.image = img_ctk

    def cargar_datos(nombre_seleccionado):
        jugador = next((j for j in jugadores if j["nom"] == nombre_seleccionado), None)
        if jugador:
            entry_nom.delete(0, 'end'); entry_nom.insert(0, jugador["nom"])
            combo_pais.set(BANDERAS_REVERSO.get(jugador["pais"], "Argentina"))
            entry_pts.delete(0, 'end'); entry_pts.insert(0, str(jugador["pts"]))
            entry_team.delete(0, 'end')
            entry_team.insert(0, "" if jugador["team"] == "-" else jugador["team"])
            combo_main.set(jugador["main"])
            combo_sub1.set(jugador["sub1"]); combo_sub2.set(jugador["sub2"])
            actualizar_preview()

    def guardar_cambios():
        nombre_original = seleccionado["nombre"]
        nuevo_nom = entry_nom.get().strip() # Obtenemos el texto
        if not nuevo_nom: return

        # 1. Actualizamos la lista en memoria
        for j in jugadores:
            if j["nom"] == nombre_original:
                j["nom"] = nuevo_nom
                j["pais"] = BANDERAS_DISPLAY.get(combo_pais.get(), "arg")
                j["pts"] = entry_pts.get().strip()
                j["team"] = entry_team.get().strip() or "-"
                j["main"] = combo_main.get()
                j["sub1"] = combo_sub1.get()
                j["sub2"] = combo_sub2.get()
                break

        # 2. Guardamos al disco (UTF-8 es clave javier milei image meme)
        try:
            with open("players.txt", "w", encoding="utf-8") as f:
                for j in jugadores:
                    f.write(f"{j['nom']};{j['pais']};{j['pts']};{j['team']};{j['main']};{j['sub1']};{j['sub2']}\n")
            
            messagebox.showinfo("Éxito", f"¡Datos de {nuevo_nom} guardados!")
            refrescar_buscador(nuevo_nom) 
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

    def eliminar_jugador():
        nombre_original = seleccionado["nombre"]
        if not nombre_original: return
        
        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar a {nombre_original}?"):
            # Filtramos la lista
            jugadores[:] = [j for j in jugadores if j["nom"] != nombre_original]
            
            try:
                # Guardamos con la misma codificación
                with open("players.txt", "w", encoding="utf-8") as f:
                    for j in jugadores:
                        f.write(f"{j['nom']};{j['pais']};{j['pts']};{j['team']};{j['main']};{j['sub1']};{j['sub2']}\n")
                
                messagebox.showinfo("Éxito", "Jugador eliminado correctamente.")
                refrescar_buscador() #primero de la lista
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    # --- DISEÑO VISUAL ---
    ctk.CTkLabel(master_frame, text="EDITAR JUGADOR", font=("Now", 22, "bold")).pack(pady=10)

    # Buscador
    ctk.CTkLabel(master_frame, text="Buscar jugador:", text_color="cyan").pack()
    entry_busqueda = ctk.CTkEntry(master_frame, placeholder_text="Filtrar...", width=280)
    entry_busqueda.pack(pady=5); entry_busqueda.bind("<KeyRelease>", filtrar_jugadores)
    
    # Lista con Scroll
    frame_scroll = ctk.CTkScrollableFrame(master_frame, width=280, height=150, label_text="Lista de Jugadores")
    frame_scroll.pack(pady=5)

    # Vista Previa
    ctk.CTkLabel(master_frame, text="VISTA PREVIA EN VIVO:", font=("Now", 12, "italic"), text_color="gray").pack(pady=(10, 0))
    label_preview = ctk.CTkLabel(master_frame, text="")
    label_preview.pack(pady=5)

    # Campos del Formulario
    ctk.CTkLabel(master_frame, text="Nombre:").pack()
    entry_nom = ctk.CTkEntry(master_frame, width=280); entry_nom.pack()

    ctk.CTkLabel(master_frame, text="País:").pack()
    combo_pais = ctk.CTkOptionMenu(master_frame, values=list(BANDERAS_DISPLAY.keys()), width=280, command=actualizar_preview)
    combo_pais.pack()

    ctk.CTkLabel(master_frame, text="Puntos Totales:").pack()
    entry_pts = ctk.CTkEntry(master_frame, width=280); entry_pts.pack()

    ctk.CTkLabel(master_frame, text="Team (Opcional):").pack()
    entry_team = ctk.CTkEntry(master_frame, width=280); entry_team.pack()

    ctk.CTkLabel(master_frame, text="Main:").pack()
    combo_main = ctk.CTkOptionMenu(master_frame, values=PJS, width=280, command=actualizar_preview)
    combo_main.pack()

    ctk.CTkLabel(master_frame, text="Sub 1 / Sub 2:").pack()
    f_subs = ctk.CTkFrame(master_frame, fg_color="transparent")
    f_subs.pack()
    combo_sub1 = ctk.CTkOptionMenu(f_subs, values=[""] + PJS, width=135); combo_sub1.pack(side="left", padx=5)
    combo_sub2 = ctk.CTkOptionMenu(f_subs, values=[""] + PJS, width=135); combo_sub2.pack(side="left", padx=5)

    # --- BOTONES DE ACCIÓN ---
    ctk.CTkButton(master_frame, text="REFRESCAR VISTA PREVIA", fg_color="gray", command=actualizar_preview).pack(pady=10)
    ctk.CTkButton(master_frame, text="GUARDAR CAMBIOS", fg_color="#b30000", hover_color="#800000", command=guardar_cambios).pack(pady=5)
    ctk.CTkButton(master_frame, text="ELIMINAR JUGADOR", fg_color="#444444", hover_color="#8b0000", command=eliminar_jugador).pack(pady=5)
    ctk.CTkButton(master_frame, text="← Volver al Menú", fg_color="gray", command=callback_volver).pack(pady=10)

    # Carga inicial
    refrescar_buscador()