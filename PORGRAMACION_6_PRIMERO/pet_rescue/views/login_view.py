#lo primero que le aparecerá al admin o usuario donde le permite iniciar sesión con los datos correspondientes,
#y si los datos no están completos o están mal debería de dar un mensaje sobre ello, lo cual aquí aún
#no está implementado



import flet as ft
from styles.colors import COLORS, crear_card

class LoginView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
    
    def build(self):
        usuario_field = ft.TextField(
            label="Usuario", 
            prefix_icon=ft.Icons.PERSON,
            border_radius=10,
            expand=True
        )
        
        password_field = ft.TextField(
            label="Contraseña", 
            password=True, 
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            border_radius=10,
            expand=True
        )

        def ingresar(e):
            usuario = usuario_field.value
            contraseña = password_field.value
            
            result = self.db.execute_query(
                "SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?", 
                (usuario, contraseña)
            )
            
            if result:
                self.app.show_view("dashboard")
            else:
                self.app.show_snackbar("Usuario o contraseña incorrectos")

        return ft.Container(
            content=ft.Column([
                ft.Container(height=50),
                ft.Icon(ft.Icons.PETS, size=80, color=COLORS["primary"]),
                ft.Text("PET RESCUE", size=32, weight=ft.FontWeight.BOLD, color=COLORS["primary"]),
                ft.Text("Transformando rescates en segundas oportunidades", 
                       size=16, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
                ft.Container(height=30),
                
                crear_card(
                    ft.Column([
                        ft.Text("INICIA SESIÓN", size=20, weight=ft.FontWeight.BOLD, 
                               text_align=ft.TextAlign.CENTER),
                        ft.Container(height=20),
                        usuario_field,
                        password_field,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "INGRESAR",
                            on_click=ingresar,
                            bgcolor=COLORS["primary"],
                            color="white",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=20
                            ),
                            expand=True
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
            padding=20
        )