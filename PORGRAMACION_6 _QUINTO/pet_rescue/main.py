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
        # Configuración de la ventana
        page.window.width = 1200
        page.window.height = 800
        page.window.min_width = 800
        page.window.min_height = 600
        page.window.resizable = True
        page.window.title = "Pet Rescue - Transformando rescates en segundas oportunidades"
        
        # Configuración de la página
        page.title = "Pet Rescue"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        page.bgcolor = "#f5f5f5"
        page.scroll = ft.ScrollMode.ADAPTIVE
        
        # Almacenar la página para acceso global
        self.page = page
        
        # Diccionario de vistas
        self.views = {
            "login": LoginView(self),
            "dashboard": DashboardView(self),
            "animales": AnimalesView(self),
            "adopciones": AdopcionesView(self),
            "donaciones": DonacionesView(self),
            "contacto": ContactoView(self)
        }
        
        # Mostrar vista inicial
        self.show_view("login")
    
    def cerrar_sesion(self, e=None):
        """Cerrar sesión y volver al login"""
        self.show_snackbar("Sesión cerrada correctamente")
        self.show_view("login")
    
    def show_view(self, view_name):
        """Cambiar entre vistas"""
        if view_name not in self.views:
            self.show_snackbar("Error: Vista no encontrada", "#F44336")
            return
            
        try:
            self.current_view = view_name
            self.page.controls.clear()
            
            view_content = self.views[view_name].build()
            
            self.page.add(view_content)
            self.page.update()
            
        except Exception as e:
            self.show_snackbar(f"Error al cargar {view_name}", "#F44336")
            # Fallback a login si hay error
            if view_name != "login":
                self.show_view("login")
    
    def show_snackbar(self, message, color=None):
        """Mostrar mensaje emergente"""
        try:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    message,
                    color="white",
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                bgcolor=color,
                duration=3000,
                show_close_icon=True
            )
            self.page.snack_bar.open = True
            self.page.update()
        except Exception:
            pass  # Silenciar errores del snackbar

def main(page: ft.Page):
    app = PetRescueApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)