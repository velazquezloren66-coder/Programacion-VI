import flet as ft
from styles.colors import COLORS, crear_card

class LoginView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
    
    def build(self):
        self.usuario_field = ft.TextField(
            label="Usuario", 
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            expand=True,
            autofocus=True
        )
        
        self.password_field = ft.TextField(
            label="Contraseña", 
            password=True, 
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            border_radius=10,
            expand=True
        )

        #mensaje de error que se mostrará dentro del formulario
        self.mensaje_error = ft.Container(
            content=ft.Text(
                "DATOS INCORRECTOS",
                color="white",
                weight=ft.FontWeight.BOLD,
                size=14,
                text_align=ft.TextAlign.CENTER
            ),
            bgcolor="#F44336",
            padding=10,
            border_radius=5,
            visible=False,
            margin=ft.margin.only(bottom=10)
        )

        def ingresar(e):
            usuario = self.usuario_field.value
            contraseña = self.password_field.value
            
            #ocultar mensaje de error al intentar nuevamente
            self.mensaje_error.visible = False
            
            #validar campos vacíos
            if not usuario or not contraseña:
                self.mensaje_error.content.value = "COMPLETE TODOS LOS CAMPOS"
                self.mensaje_error.bgcolor = "#FF9800"  # Naranja
                self.mensaje_error.visible = True
                self.app.page.update()
                return
            
            result = self.db.execute_query(
                "SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", 
                (usuario, contraseña)
            )
            
            if result and len(result) > 0:
                self.mensaje_error.visible = False
                self.app.show_view("dashboard")
            else:
                #mostrar mensaje de error en ROJO
                self.mensaje_error.content.value = "DATOS INCORRECTOS"
                self.mensaje_error.bgcolor = "#F44336"  # Rojo
                self.mensaje_error.visible = True
                self.app.page.update()

        #función para manejar Enter en los campos
        def on_enter(e):
            ingresar(e)

        #asignar evento Enter a los campos
        self.usuario_field.on_submit = on_enter
        self.password_field.on_submit = on_enter

        return ft.Container(
            content=ft.Column([
                ft.Container(height=50),
                ft.Icon(ft.Icons.PETS, size=80, color=COLORS["primary"]),
                ft.Text("PET RESCUE", size=32, weight=ft.FontWeight.BOLD, color=COLORS["primary"]),
                ft.Text("Sistema de Gestión Administrativa", 
                       size=16, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
                ft.Text("Transformando rescates en segundas oportunidades", 
                       size=14, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
                ft.Container(height=30),
                
                crear_card(
                    ft.Column([
                        ft.Text("INICIO DE SESIÓN", size=20, weight=ft.FontWeight.BOLD, 
                               text_align=ft.TextAlign.CENTER),
                        ft.Text("Acceso exclusivo para administradores", 
                               size=12, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
                        ft.Container(height=20),
                        self.usuario_field,
                        self.password_field,
                        
                        #mensaje de error integrado en el formulario
                        self.mensaje_error,
                        
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "🔐 INGRESAR",
                            on_click=ingresar,
                            bgcolor=COLORS["primary"],
                            color="white",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=20
                            ),
                            expand=True
                        ),
                        
                        # Separador
                        ft.Container(height=20),
                        ft.Divider(height=1, color=COLORS["secondary"]),
                        ft.Container(height=20),
                        
                        # Botón de acceso público
                        ft.Text("¿Quieres conocer nuestros animalitos?", 
                               size=14, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
                        ft.ElevatedButton(
                            "🐾 VER ANIMALITOS DISPONIBLES",
                            on_click=lambda _: self.app.show_view("publico"),
                            bgcolor=COLORS["secondary"],
                            color="white",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=15
                            ),
                            expand=True
                        ),
                        ft.Text("Acceso público sin registro", 
                               size=10, color="gray", text_align=ft.TextAlign.CENTER, italic=True),
                        
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            padding=20
        )