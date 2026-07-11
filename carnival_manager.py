import customtkinter as ctk
import actualiplayers
import topplayers
import ingresoplayers
import creadortop8

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("The Midnight Carnival - Manager")
        self.after(0, lambda: self.state('zoomed'))
        self.minsize(800, 600)
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(expand=True, fill="both")
        self.mostrar_menu_principal()

    def limpiar_pantalla(self):
        # limpia el contenedor, es para el cambio de pestañas
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self):
        self.limpiar_pantalla()


        frame_columnas = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        frame_columnas.pack(expand=True, fill="both", padx=50)
        
        # Título principal
        frame_sud = ctk.CTkFrame(frame_columnas, fg_color="#1a1a1a", corner_radius=15)
        frame_sud.pack(side="left", expand=True, fill="both", padx=20, pady=20)

        # Sudamerica

        ctk.CTkLabel(frame_sud, text="SUDAMÉRICA", font=("Now", 20, "bold"), text_color="#00a8ff").pack(pady=(20, 30))

        self.btn_reg_sud = ctk.CTkButton(frame_sud, text="Registrar Jugador", width=250, height=40,
                                         fg_color="#005c8a", hover_color="#003d5c",
                                         command=lambda: self.mostrar_ingreso("SUD"))
        self.btn_reg_sud.pack(pady=15)

        self.btn_upd_sud = ctk.CTkButton(frame_sud, text="Actualizar Puntos/Datos", width=250, height=40,
                                         fg_color="#005c8a", hover_color="#003d5c",
                                         command=lambda: self.abrir_actuali("SUD"))
        self.btn_upd_sud.pack(pady=15)

        #self.btn_img_sud = ctk.CTkButton(frame_sud, text="Top 8 imagen", width=250, height=40,
        #                                 fg_color="#005c8a", hover_color="#003d5c",
        #                                 command=lambda: self.abrir_top8("SUD"))
        #self.btn_img_sud.pack(pady=15)

        self.btn_img_sud = ctk.CTkButton(frame_sud, text="Generar Imagen Top 10", width=250, height=40,
                                         fg_color="#005c8a", hover_color="#003d5c",
                                         command=lambda: topplayers.generar_ranking_imagen("SUD"))
        self.btn_img_sud.pack(pady=15)

        # CENTROAMÉRICA
        frame_cen = ctk.CTkFrame(frame_columnas, fg_color="#1a1a1a",  corner_radius=15)
        # side="right" lo tira a la derecha
        frame_cen.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame_cen, text="CENTROAMÉRICA", font=("Now", 20, "bold"), text_color="#ff5e00").pack(pady=(20, 30))

        self.btn_reg_cen = ctk.CTkButton(frame_cen, text="Registrar Jugador", width=250, height=40,
                                         fg_color="#a83c00", hover_color="#7a2b00",
                                         command=lambda: self.mostrar_ingreso("CEN"))
        self.btn_reg_cen.pack(pady=15)

        self.btn_upd_cen = ctk.CTkButton(frame_cen, text="Actualizar Puntos/Datos", width=250, height=40,
                                         fg_color="#a83c00", hover_color="#7a2b00",
                                         command=lambda: self.abrir_actuali("CEN"))
        self.btn_upd_cen.pack(pady=15)

        #self.btn_img_cen = ctk.CTkButton(frame_cen, text="Top 8 imagen", width=250, height=40,
        #                                 fg_color="#a83c00", hover_color="#7a2b00",
        #                                 command=lambda: self.abrir_top8("CEN"))
        #self.btn_img_cen.pack(pady=15)

        self.btn_img_cen = ctk.CTkButton(frame_cen, text="Generar Imagen Top 10", width=250, height=40,
                                         fg_color="#a83c00", hover_color="#7a2b00",
                                         command=lambda: topplayers.generar_ranking_imagen("CEN"))
        self.btn_img_cen.pack(pady=15)

        #SAlir
        self.btn_exit = ctk.CTkButton(self.contenedor, text="SALIR", width=200, height=40, 
                                      fg_color="#b30000", hover_color="#800000",
                                      command=self.quit)
        self.btn_exit.pack(pady=(20, 50))
    def mostrar_ingreso(self, region):
        self.limpiar_pantalla()
        ingresoplayers.ejecutar_ingreso(self.contenedor, self.mostrar_menu_principal, region)

    def abrir_actuali(self, region):
     self.limpiar_pantalla()
     actualiplayers.ejecutar_actualizacion(self.contenedor, self.mostrar_menu_principal, region)

    def abrir_top8(self, region):
     self.limpiar_pantalla()
     creadortop8.ejecutar_top8(self.contenedor, self.mostrar_menu_principal, region)

if __name__ == "__main__":
    app = App()
    app.mainloop()