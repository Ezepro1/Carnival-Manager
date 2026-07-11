from PIL import Image, ImageDraw, ImageFont
import os
from tkinter import filedialog, Tk, messagebox
import sys

def obtener_ruta(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

CONFIG_TOP = {
    "SUD": {"archivo": "players.txt", "template": "archivos/template.jpg", "file": "CarnivalSUDTop10.png"},
    "CEN": {"archivo": "playersCEN.txt", "template": "archivos/templateCEN.jpg", "file": "CarnivalCENTop10.png"}
}

def generar_ranking_imagen(region="SUD"):
    conf = CONFIG_TOP[region]
    jugadores = []

    try:
        with open(conf["archivo"], "r", encoding="utf-8") as archivo:
            for linea in archivo:
                d = linea.strip().split(";")
                if len(d) >= 5:
                    jugadores.append({"nom": d[0], "pais": d[1], "pts": d[2], "team": d[3], "main": d[4]})
    except: return

    top10 = sorted(jugadores, key=lambda x: int(x['pts']), reverse=True)[:10]

    try:
        img = Image.open(obtener_ruta(conf["template"])).convert("RGBA")
        dibujo = ImageDraw.Draw(img)
        font_path = obtener_ruta("archivos/Now-Bold.otf")
        f_datos, f_pts = ImageFont.truetype(font_path, 25), ImageFont.truetype(font_path, 30)

        for i, j in enumerate(top10):
            y_c = 585 + (i * 74)
            try:
                pj = Image.open(obtener_ruta(f"archivos/imgpjs/{j['main']}.png")).convert("RGBA")
                
                # Redimensionado
                alto_pj = 70
                ancho_pj = int((alto_pj / pj.size[1]) * pj.size[0])
                pj = pj.resize((ancho_pj, alto_pj), Image.Resampling.LANCZOS)
                
                # --- EFECTO DESVANECER IZQUIERDA ---
                mask = Image.new("L", pj.size, 0)
                for x in range(pj.size[0]):
                    alpha = int(255 * (x / pj.size[0]))
                    for y in range(pj.size[1]):
                        mask.putpixel((x, y), alpha)
                pj.putalpha(mask)
                
                img.alpha_composite(pj, dest=(809 - pj.size[0], int(y_c - 35)))
            except: pass

            dibujo.text((180, y_c), j['team'].upper(), font=f_datos, fill="white", anchor="mm")
            dibujo.text((230, y_c), j['nom'].upper(), font=f_datos, fill="white", anchor="lm")
            dibujo.text((860, y_c), j['pais'].upper(), font=f_datos, fill="white", anchor="mm")
            dibujo.text((975, y_c), str(j['pts']), font=f_pts, fill="white", anchor="mm")

        root = Tk(); root.withdraw(); root.attributes("-topmost", True)
        ruta = filedialog.asksaveasfilename(defaultextension=".png", initialfile=conf["file"])
        if ruta:
            img.save(ruta)
            messagebox.showinfo("Éxito", "Ranking generado.")
        root.destroy()
    except Exception as e: print(f"Error: {e}")