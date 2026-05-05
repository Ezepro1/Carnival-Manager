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


def generar_ranking_imagenCEN():
    jugadores = []

    # 1. LEER DATOS (No usamos obtener_ruta aquí para que players.txt sea externo)
    try:
        with open("players.txtCEN", "r") as archivo:
            for linea in archivo:
                d = linea.strip().split(";")
                if len(d) >= 5:
                    jugadores.append({
                        "nom": d[0], "pais": d[1], "pts": d[2],
                        "team": d[3], "main": d[4]
                    })
    except FileNotFoundError:
        print("Error: No se encuentra players.txtCEN")
        return

    top10 = sorted(jugadores, key=lambda x: int(x['pts']), reverse=True)[:10]

    # 2. CONFIGURACIÓN DE IMAGEN
    try:
        template_path = obtener_ruta("archivos/templateCEN.jpg")
        img = Image.open(template_path).convert("RGBA")
        dibujo = ImageDraw.Draw(img)
        
        font_path = obtener_ruta("archivos/Now-Bold.otf") 
        fuente_datos = ImageFont.truetype(font_path, 25)
        fuente_puntos = ImageFont.truetype(font_path, 30)

        # Coordenadas
        y_inicial, salto_y = 585, 74 
        x_team, x_nombre, x_pj_derecha, x_pais, x_puntos = 180, 230, 809, 860, 975 

        # 4. DIBUJAR JUGADORES
        for i, j in enumerate(top10):
            y_centro = y_inicial + (i * salto_y)
            
            try:
                pj_path = obtener_ruta(f"archivos/imgpjs/{j['main']}.png")
                pj_img = Image.open(pj_path).convert("RGBA")
                
                alto_pj = 70
                ancho_pj = int((alto_pj / pj_img.size[1]) * pj_img.size[0])
                pj_img = pj_img.resize((ancho_pj, alto_pj), Image.Resampling.LANCZOS)
                
                mask = Image.new("L", pj_img.size, 0)
                for x in range(pj_img.size[0]):
                    alpha = int(255 * (x / pj_img.size[0]))
                    for y in range(pj_img.size[1]): mask.putpixel((x, y), alpha)
                pj_img.putalpha(mask)
                
                x_pj_final = x_pj_derecha - ancho_pj
                y_pj_final = int(y_centro - (alto_pj / 2))
                img.alpha_composite(pj_img, dest=(x_pj_final, y_pj_final))
            except: pass

            dibujo.text((x_team, y_centro), j['team'].upper(), font=fuente_datos, fill="white", anchor="mm")
            dibujo.text((x_nombre, y_centro), j['nom'].upper(), font=fuente_datos, fill="white", anchor="lm")
            dibujo.text((x_pais, y_centro), j['pais'].upper(), font=fuente_datos, fill="white", anchor="mm")
            dibujo.text((x_puntos, y_centro), str(j['pts']), font=fuente_puntos, fill="white", anchor="mm")

        # Diálogo de guardado
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        ruta_guardado = filedialog.asksaveasfilename(
            title="Selecciona dónde guardar el ranking",
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png"), ("Imagen JPG", "*.jpg")],
            initialfile="CarnivalCENTop10.png"
        )

        if ruta_guardado:
            if ruta_guardado.lower().endswith(".jpg"):
                img.convert("RGB").save(ruta_guardado)
            else:
                img.save(ruta_guardado)
            messagebox.showinfo("Éxito", "Imagen guardada correctamente.")
        
        root.destroy()

    except Exception as e:
        print(f"Error al procesar ranking: {e}")