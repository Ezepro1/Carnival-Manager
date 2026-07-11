import customtkinter as ctk
from tkinter import messagebox, filedialog, Tk, colorchooser
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

CONFIG_TOP8 = {
    "SUD": {"archivo": "players.txt", "template": "archivos/template8.jpg", "file": "Top8_Sudamerica.png"},
    "CEN": {"archivo": "playersCEN.txt", "template": "archivos/template8CEN.jpg", "file": "Top8_Centroamerica.png"}
}

COLORES_PREDEFINIDOS = ["#FFD700", "#C0C0C0", "#CD7F32", "#A10000", "#A10000", "#00A100", "#00A100", "#0000A1"]

def ejecutar_top8(master_frame, callback_volver, region="SUD"):
    conf = CONFIG_TOP8[region]
    jugadores_db = []
    
    seleccionados = [ctk.StringVar(value="Seleccionar...") for _ in range(8)]
    twitters = [] 
    colores_borde1 = [ctk.StringVar(value=COLORES_PREDEFINIDOS[i]) for i in range(8)]
    colores_borde2 = [ctk.StringVar(value=COLORES_PREDEFINIDOS[i]) for i in range(8)]
    custom_imgs = [None for _ in range(8)] # Rutas de imágenes personalizadas
    botones_color1 = []
    botones_color2 = []

    def cargar_datos():
        nonlocal jugadores_db
        jugadores_db.clear()
        try:
            if os.path.exists(conf["archivo"]):
                with open(conf["archivo"], "r", encoding="utf-8") as f:
                    for linea in f:
                        d = linea.strip().split(";")
                        if len(d) >= 5:
                            jugadores_db.append({"nom": d[0], "team": d[3], "main": d[4], "pais": d[1]})
        except: pass

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def obtener_fuente_ajustada(dibujo, texto, max_ancho, ruta_f, tam_inicial):
        tam = tam_inicial
        fuente = ImageFont.truetype(ruta_f, tam)
        while dibujo.textbbox((0, 0), texto, font=fuente)[2] > max_ancho and tam > 18:
            tam -= 2
            fuente = ImageFont.truetype(ruta_f, tam)
        return fuente

    def crear_gradient_rect(ancho, alto, c1, c2):
        # Crea una imagen con gradiente vertical para el borde/franja
        base = Image.new('RGBA', (ancho, alto), c1)
        top = Image.new('RGBA', (ancho, alto), c2)
        mask = Image.new('L', (ancho, alto))
        mask_data = []
        for y in range(alto):
            mask_data.extend([int(255 * (y / alto))] * ancho)
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base

    def crear_imagen_pil():
        img = Image.open(obtener_ruta(conf["template"])).convert("RGBA")
        dibujo = ImageDraw.Draw(img)
        f_path = obtener_ruta("archivos/Now-Bold.otf")
        
        fuente_meta = ImageFont.truetype(f_path, 40)
        fuente_tw = ImageFont.truetype(f_path, 22)

        coords = [
            [35, 175, 665, 665], [725, 175, 350, 350], [1115, 175, 350, 350], [1505, 175, 350, 350],
            [725, 650, 260, 260], [1020, 650, 260, 260], [1315, 650, 260, 260], [1610, 650, 260, 260]
        ]
        ancho_borde = 12

        for i in range(8):
            nom_sel = seleccionados[i].get()
            if nom_sel == "Seleccionar..." and not custom_imgs[i]: continue
            
            # Datos del jugador (si existe en DB)
            jugador = next((j for j in jugadores_db if j["nom"] == nom_sel), {"nom": nom_sel, "team": "-", "main": "None", "pais": "arg"})
            x, y, w, h = coords[i]
            c1, c2 = hex_to_rgb(colores_borde1[i].get()), hex_to_rgb(colores_borde2[i].get())

            alto_franja = int(h * 0.22) if i == 0 else int(h * 0.30)
            
            # 1. Dibujar Borde y Franja (con gradiente si c1 != c2)
            if c1 == c2:
                dibujo.rectangle([x, y + h, x + w, y + h + alto_franja], fill=c1)
                rect_coords = [x - ancho_borde//2, y - ancho_borde//2, x + w + ancho_borde//2, y + h + alto_franja + ancho_borde//2]
                dibujo.rectangle(rect_coords, outline=c1, width=ancho_borde)
            else:
                grad_img = crear_gradient_rect(w + ancho_borde, h + alto_franja + ancho_borde, c1, c2)
                # Máscara para el borde y la franja
                mask_borde = Image.new('L', img.size, 0)
                d_mask = ImageDraw.Draw(mask_borde)
                # Dibujar el área de la franja y el borde en la máscara
                d_mask.rectangle([x, y + h, x + w, y + h + alto_franja], fill=255)
                d_mask.rectangle([x - ancho_borde//2, y - ancho_borde//2, x + w + ancho_borde//2, y + h + alto_franja + ancho_borde//2], outline=255, width=ancho_borde)
                img.paste(grad_img, (x - ancho_borde//2, y - ancho_borde//2), grad_img)
                # Limpiar el centro para que no tape el fondo (solo queremos el borde y la franja)
                # Volvemos a pegar el template original en el centro del cuadro
                centro = Image.open(obtener_ruta(conf["template"])).convert("RGBA").crop((x, y, x+w, y+h))
                img.paste(centro, (x, y))

            # 2. Imagen del Personaje o Custom
            try:
                path_img = custom_imgs[i] if custom_imgs[i] else obtener_ruta(f"archivos/imgpjstop8/{jugador['main']}.png")
                
                pj = Image.open(path_img).convert("RGBA")
                alto_pj = h - (ancho_borde * 2)
                pj = pj.resize((int(pj.size[0] * (alto_pj/pj.size[1])), alto_pj), Image.Resampling.LANCZOS)
                
                img.alpha_composite(pj, (x + (w - pj.size[0] - ancho_borde), y + ancho_borde))
            except: pass

            # 3. Bandera y Textos
            try:
                band = Image.open(obtener_ruta(f"archivos/banderas/{jugador['pais']}.png")).convert("RGBA").resize((60, 60))
                img.alpha_composite(band, (x + w - 85, y + 15))
            except: pass

            full_name = f"{jugador['team']}|{jugador['nom']}".upper() if jugador['team'] != "-" else jugador['nom'].upper()
            fuente_aj = obtener_fuente_ajustada(dibujo, full_name, w-40, f_path, 75 if i == 0 else 42)
            dibujo.text((x + 15, y + h + alto_franja - 45), full_name, font=fuente_aj, fill="white", anchor="ls")
            
            tw = twitters[i].get()
            if tw: dibujo.text((x + 20, y + h + alto_franja - 20), f"@{tw}", font=fuente_tw, fill="white", anchor="ls")

        dibujo.text((60, 30), entry_fecha.get().upper(), font=fuente_meta, fill="white")
        dibujo.text((1560, 30), f"{entry_part.get()} PARTICIPANTES", font=fuente_meta, fill="white")
        return img

    def actualizar_preview(*args):
        try:
            img_pil = crear_imagen_pil()
            ancho_pre = 800
            alto_pre = int((ancho_pre / 1920) * 1080)
            img_resized = img_pil.resize((ancho_pre, alto_pre), Image.Resampling.LANCZOS)
            img_ctk = ctk.CTkImage(light_image=img_resized, dark_image=img_resized, size=(ancho_pre, alto_pre))
            label_preview.configure(image=img_ctk, text="")
            label_preview.image = img_ctk
        except: pass

    def seleccionar_imagen_custom(idx):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            custom_imgs[idx] = ruta
            actualizar_preview()

    def guardar_final():
        img_pil = crear_imagen_pil()
        root = Tk(); root.withdraw(); root.attributes("-topmost", True)
        ruta = filedialog.asksaveasfilename(defaultextension=".png", initialfile=conf["file"])
        if ruta:
            img_pil.save(ruta)
            messagebox.showinfo("Éxito", "Imagen guardada.")
        root.destroy()

    def elegir_color(idx, num_boton):
        target = colores_borde1[idx] if num_boton == 1 else colores_borde2[idx]
        color = colorchooser.askcolor(color=target.get())
        if color[1]:
            target.set(color[1])
            if num_boton == 1: botones_color1[idx].configure(fg_color=color[1])
            else: botones_color2[idx].configure(fg_color=color[1])
            actualizar_preview()

    # --- ESTRUCTURA VISUAL ---
    cargar_datos()
    frame_superior = ctk.CTkScrollableFrame(master_frame, fg_color="transparent", height=400)
    frame_superior.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(frame_superior, text=f"CONFIGURACIÓN TOP 8 - {region}", font=("Now", 22, "bold")).pack(pady=10)
    grid_puestos = ctk.CTkFrame(frame_superior, fg_color="transparent")
    grid_puestos.pack()

    nombres_db = sorted([j["nom"] for j in jugadores_db])

    for i in range(8):
        f = ctk.CTkFrame(grid_puestos, fg_color="#1a1a1a")
        f.grid(row=i//2, column=i%2, padx=5, pady=5)
        ctk.CTkLabel(f, text=f"P{i+1}:", width=30).pack(side="left", padx=5)
        ctk.CTkOptionMenu(f, variable=seleccionados[i], values=nombres_db, width=120, command=actualizar_preview).pack(side="left", padx=2)
        tw_entry = ctk.CTkEntry(f, placeholder_text="Tw", width=80)
        tw_entry.pack(side="left", padx=2); twitters.append(tw_entry)
        tw_entry.bind("<KeyRelease>", actualizar_preview)
        
        # Selectores de Color (Dos para gradiente)
        btn_c1 = ctk.CTkButton(f, text="", width=20, height=20, fg_color=colores_borde1[i].get(), command=lambda idx=i: elegir_color(idx, 1))
        btn_c1.pack(side="left", padx=2); botones_color1.append(btn_c1)
        btn_c2 = ctk.CTkButton(f, text="", width=20, height=20, fg_color=colores_borde2[i].get(), command=lambda idx=i: elegir_color(idx, 2))
        btn_c2.pack(side="left", padx=2); botones_color2.append(btn_c2)
        
        # Botón para Imagen Custom
        ctk.CTkButton(f, text="Img", width=40, height=20, fg_color="#333", command=lambda idx=i: seleccionar_imagen_custom(idx)).pack(side="left", padx=2)

    f_info = ctk.CTkFrame(frame_superior, fg_color="#111"); f_info.pack(pady=15, fill="x", padx=40)
    entry_fecha = ctk.CTkEntry(f_info, placeholder_text="FECHA", width=150); entry_fecha.pack(side="left", padx=15, pady=10)
    entry_fecha.bind("<KeyRelease>", actualizar_preview)
    entry_part = ctk.CTkEntry(f_info, placeholder_text="PART.", width=80); entry_part.pack(side="left", padx=10)
    entry_part.bind("<KeyRelease>", actualizar_preview)
    
    ctk.CTkButton(f_info, text="GUARDAR PNG", fg_color="green", command=guardar_final).pack(side="right", padx=15)
    ctk.CTkButton(f_info, text="VOLVER", fg_color="#444", command=callback_volver).pack(side="right", padx=5)

    frame_inferior = ctk.CTkFrame(master_frame, fg_color="#0a0a0a", corner_radius=15)
    frame_inferior.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    label_preview = ctk.CTkLabel(frame_inferior, text="Selecciona un jugador para previsualizar")
    label_preview.pack(expand=True)

    actualizar_preview()