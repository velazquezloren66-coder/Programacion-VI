#Acá se configura la aplicación principal PetRescue, definiendo las propiedades de la ventana 
#(tamaño, título, responsive) e inicializando el sistema de navegación entre vistas. Gestiona el cambio 
#entre diferentes pantallas (login, dashboard, animales, adopciones, etc.) y provee funciones globales
#como mostrar mensajes emergentes, estableciendo la estructura base de la interfaz gráfica de escritorio



import flet as ft
from database import Database
from views import (
    LoginView, 
    DashboardView, 
    AnimalesView, 
    AdopcionesView, 
    DonacionesView, 
    ContactoView
)

class PetRescueApp:
    def __init__(self):
        self.db = Database()
        self.current_view = "login"
        self.page = None
        
    def main(self, page: ft.Page):
        #configuración de la ventana - ESTA ES LA PARTE IMPORTANTE
        page.window.width = 1200
        page.window.height = 800
        page.window.min_width = 800
        page.window.min_height = 600
        page.window.resizable = True
        page.window.title = "Pet Rescue - Transformando rescates en segundas oportunidades"
        page.window.center()  #centrar la ventana
        
        #configuración de la página
        page.title = "Pet Rescue"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.bgcolor = "#f5f5f5"
        page.scroll = ft.ScrollMode.ADAPTIVE
        
        #almacenar la página para acceso global
        self.page = page
        
        #diccionario de vistas
        self.views = {
            "login": LoginView(self),
            "dashboard": DashboardView(self),
            "animales": AnimalesView(self),
            "adopciones": AdopcionesView(self),
            "donaciones": DonacionesView(self),
            "contacto": ContactoView(self)
        }
        
        #mostrar vista inicial
        self.show_view("login")
    
    def show_view(self, view_name):
        """Cambiar entre vistas"""
        if view_name not in self.views:
            print(f"Error: Vista '{view_name}' no encontrada")
            return
            
        self.current_view = view_name
        self.page.controls.clear()
        
        try:
            view_content = self.views[view_name].build()
            self.page.add(view_content)
            self.page.update()
        except Exception as e:
            print(f"Error al cargar vista {view_name}: {e}")
            #fallback a login si hay error
            if view_name != "login":
                self.show_view("login")
    
    def show_snackbar(self, message, color=None):
        """Mostrar mensaje emergente"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()

#ejecutar la aplicación
if __name__ == "__main__":
    #esta es la forma CORRECTA de configurar la ventana
    ft.app(
        target=lambda page: PetRescueApp().main(page),
        view=ft.FLET_APP  #para aplicación de escritorio
    )