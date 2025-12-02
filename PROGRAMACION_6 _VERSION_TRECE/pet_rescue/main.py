#CAMBIOS:

# Utilizamos la librería de python: Pillow (PIL moderno) - Procesamiento de imágenes
#Se usa para: 
# 1. Generar placeholder automático cuando no existe img/placeholder.png
# 2. Procesar imágenes subidas por usuarios
# 3. Manejar diferentes formatos de imagen (JPG, PNG, GIF)
#Instalación: pip install Pillow


import flet as ft
from database import Database
from views import (
    LoginView, 
    DashboardView, 
    AnimalesView, 
    AdopcionesView, 
    DonacionesView, 
    ContactoView,
)
from views.publico_view import PublicoView
from views.contacto_publico_view import ContactoPublicoView

class PetRescueApp:
    def __init__(self):
        self.db = Database()
        self.current_view = "login"
        self.page = None
        
        #verificar estructura de tabla al iniciar
        self._verificar_estructura_tabla()
        
    def _verificar_estructura_tabla(self):
        """Verificar la estructura de la tabla animales"""
        try:
            #obtener información de columnas
            self.db.cursor.execute("PRAGMA table_info(animales)")
            columnas = self.db.cursor.fetchall()
            
            #ver cuántos registros hay
            self.db.cursor.execute("SELECT COUNT(*) FROM animales")
            cantidad = self.db.cursor.fetchone()
            
            #ver algunos datos de ejemplo (si existen)
            self.db.cursor.execute("SELECT * FROM animales LIMIT 3")
            datos = self.db.cursor.fetchall()
                
        except Exception as e:
            #solo registrar error en caso de falla crítica
            import traceback
            traceback.print_exc()
    
    def main(self, page: ft.Page):
        #configuración de la ventana
        page.window.width = 1200
        page.window.height = 800
        page.window.min_width = 800
        page.window.min_height = 600
        page.window.resizable = True
        page.window.title = "Pet Rescue - Transformando rescates en segundas oportunidades"
        
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
            "contacto": ContactoView(self),
            "publico": PublicoView(self),
            "contacto_publico": ContactoPublicoView(self)
        }
        
        #mostrar vista inicial
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
            #fallback a login si hay error
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
            pass  #silenciar errores del snackbar

def main(page: ft.Page):
    #crear estructura de carpetas si no existe
    import os
    os.makedirs("img/animales", exist_ok=True)
    
    #verificar placeholder
    if not os.path.exists("img/placeholder.png"):
        #crear un placeholder simple si no existe usando Pillow
        try:
            from PIL import Image, ImageDraw #Importar módulos específicos de Pillow
            #Image: para crear y manipular imágenes
            #ImageDraw: para dibujar texto y formas en imágenes
            
            #crear imagen de 200x150 píxeles (tamaño estándar para preview)
            img = Image.new('RGB', (200, 150), color='#f0f0f0')
            #configurar texto con color gris medio
            draw = ImageDraw.Draw(img)
            draw.text((50, 60), "Sin imagen", fill='#999999')
            #guardar como PNG (formato con compresión sin pérdida)
            img.save("img/placeholder.png")
        except ImportError:
            #Si Pillow no está instalado, la aplicación funcionará pero sin placeholder automático
            #Con Pillow no instalado - funcionalidad limitada pero aplicación funciona
            #Las imágenes placeholder no se generarán automáticamente
            pass
        except Exception:
            #Error al crear placeholder, continuar sin él
            pass
    
    app = PetRescueApp()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main)