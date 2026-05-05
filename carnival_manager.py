import customtkinter as ctk
import ingresoplayersSUD
import actualiplayersSUD
import topplayersSUD
import ingresoplayersCEN
import actualiplayersCEN
import topplayersCEN

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("The Midnight Carnival - Manager")
        self.geometry("600x1000")
        self.contenedor = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedor.pack(expand=True, fill="both")
        self.mostrar_menu_principal()

    def limpiar_pantalla(self):
        # limpia el contenedor, es para el cambio de pestañas
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_menu_principal(self):
        self.limpiar_pantalla()

        
        # Título principal
        self.label = ctk.CTkLabel(self.contenedor, text="CARNIVAL MANAGER", font=("Now", 24, "bold"))
        self.label.pack(pady=30)

        # Botones
        self.btn_registro = ctk.CTkButton(self.contenedor, text="Registrar Jugador Sudamerica", 
                                          command=self.mostrar_ingreso)
        self.btn_registro.pack(pady=15)

        self.btn_update = ctk.CTkButton(self.contenedor, text="Actualizar Puntos/Datos Sudamerica", 
                                        command=self.mostrar_actualizacion)
        self.btn_update.pack(pady=15)

        self.btn_img = ctk.CTkButton(self.contenedor, text="Generar Imagen Top 10 Sudamerica", 
                                     command=topplayersSUD.generar_ranking_imagen)
        self.btn_img.pack(pady=15)
        self.btn_registro = ctk.CTkButton(self.contenedor, text="Registrar Jugador Centroamerica", 
                                          command=self.mostrar_ingresoCEN)
        self.btn_registro.pack(pady=15)

        self.btn_update = ctk.CTkButton(self.contenedor, text="Actualizar Puntos/Datos Centroamerica", 
                                        command=self.mostrar_actualizacionCEN)
        self.btn_update.pack(pady=15)

        self.btn_img = ctk.CTkButton(self.contenedor, text="Generar Imagen Top 10 Centroamerica", 
                                     command=topplayersCEN.generar_ranking_imagenCEN)
        self.btn_img.pack(pady=15)

        self.btn_exit = ctk.CTkButton(self.contenedor, text="Salir", fg_color="red", hover_color="#8B0000",
                                      command=self.quit)
        self.btn_exit.pack(pady=40)
    def mostrar_ingreso(self):
        self.limpiar_pantalla()
        # llamada a la funcion
        ingresoplayersSUD.ejecutar_ingreso(self.contenedor, self.mostrar_menu_principal)

    def mostrar_actualizacion(self):
        self.limpiar_pantalla()
        actualiplayersSUD.ejecutar_actualizacion(self.contenedor, self.mostrar_menu_principal)
    def mostrar_ingresoCEN(self):
        self.limpiar_pantalla()
        ingresoplayersCEN.ejecutar_ingresoCEN(self.contenedor, self.mostrar_menu_principal)

    def mostrar_actualizacionCEN(self):
        self.limpiar_pantalla()
        actualiplayersCEN.ejecutar_actualizacionCEN(self.contenedor, self.mostrar_menu_principal)

if __name__ == "__main__":
    app = App()
    app.mainloop()