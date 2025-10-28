#aquí prácticamente veo unas tarjetas en la parte superior de la vista que se nos presenta al iniciar sesión,
#en esas tarjetas se visualizan según cómo se van realizando las adopciones y demás, mostrando la cantidad de
#animales adoptados y así. Y no se puede ingresar a estos, solo son una aclaración rápida por así decirlo
#de lo que está sucediendo


#Tanto en la Vista Animales rescatados y Adopciones se van guardando bien cuando se realizan las adopciones,
#se comunican bien, pero aún así hay ciertos errores al cambiar su estado a En refugio nuevamente y no
#se actualiza la cantidad de adoptados en las diferentes tarjetas correspondientes.



import flet as ft
from styles.colors import COLORS, crear_header, crear_boton

class DashboardView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
    
    def build(self):
        #obtener estadísticas
        total_animales = self.db.execute_query("SELECT COUNT(*) FROM animales")[0][0]
        en_adopcion = self.db.execute_query("SELECT COUNT(*) FROM animales WHERE estado = 'En adopción'")[0][0]
        adopciones = self.db.execute_query("SELECT COUNT(*) FROM adoptantes")[0][0]
        donaciones = self.db.execute_query("SELECT COUNT(*) FROM donantes")[0][0]

        return ft.Column([
            crear_header("Bienvenido a Pet Rescue"),
            
            ft.Container(
                content=ft.Column([
                    ft.Text("Transformando rescates en segundas oportunidades", 
                           size=18, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
                    ft.Container(height=20),
                    
                    #tarjetas de estadísticas
                    ft.Row([
                        self._crear_tarjeta_estadistica(
                            str(total_animales), "Animales Rescatados", ft.Icons.PETS, COLORS["primary"]
                        ),
                        self._crear_tarjeta_estadistica(
                            str(en_adopcion), "En Adopción", ft.Icons.FAVORITE, COLORS["secondary"]
                        ),
                        self._crear_tarjeta_estadistica(
                            str(adopciones), "Adopciones", ft.Icons.HOME, COLORS["accent"]
                        ),
                        self._crear_tarjeta_estadistica(
                            str(donaciones), "Donaciones", ft.Icons.ATTACH_MONEY, COLORS["primary"]
                        ),
                    ]),
                    
                    ft.Container(height=30),
                    
                    #botones principales
                    ft.Row([
                        crear_boton("Adopciones", ft.Icons.FAVORITE_BORDER, 
                                   lambda _: self.app.show_view("adopciones")),
                        crear_boton("Donaciones", ft.Icons.ATTACH_MONEY, 
                                   lambda _: self.app.show_view("donaciones")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.Row([
                        crear_boton("Animales Rescatados", ft.Icons.PETS, 
                                   lambda _: self.app.show_view("animales")),
                        crear_boton("Contacto", ft.Icons.CONTACT_PHONE, 
                                   lambda _: self.app.show_view("contacto")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    
                    ft.Container(height=20),
                    ft.Text(
                        "Conoce a nuestros amiguitos peludos que buscan un hogar. "
                        "Ayudamos a llegar a más animalitos que necesitan de nuestra ayuda.",
                        size=14, color=COLORS["text"], text_align=ft.TextAlign.CENTER
                    )
                    
                ]),
                padding=20
            )
        ])
    
    def _crear_tarjeta_estadistica(self, valor, titulo, icono, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icono, size=30, color=color),
                ft.Text(valor, size=20, weight=ft.FontWeight.BOLD),
                ft.Text(titulo, size=12, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15,
            bgcolor=COLORS["card"],
            border_radius=10,
            expand=True,
            margin=5
        )