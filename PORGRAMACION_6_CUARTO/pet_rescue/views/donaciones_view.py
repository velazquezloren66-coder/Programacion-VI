#Sigue sin ser completamente funcional, pero la idea es que permita contactar al whatsapp a 
#la fundación, así tambien posiblemente llamarlos y hasta ver la ubicación del lugar, además de
#ya de por sí proporcionar datos sobre la ubicación y demás en esta vista


#no hay validación de completar todos los campos obligatorios, no guarda la donación y por 
#tanto no queda registrado.


import flet as ft
from datetime import datetime
from styles.colors import COLORS, crear_header, crear_card

class DonacionesView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
        
    def build(self):
        #campos del formulario
        self.nombre_field = ft.TextField(label="Nombre", expand=True)
        self.apellido_field = ft.TextField(label="Apellido", expand=True)
        self.contacto_field = ft.TextField(label="Contacto", expand=True)
        
        self.tipo_donacion = ft.Dropdown(
            label="Tipo de donación *",
            options=[
                ft.dropdown.Option("Alimento"),
                ft.dropdown.Option("Dinero"),
                ft.dropdown.Option("Medicamentos"),
                ft.dropdown.Option("Juguetes"),
                ft.dropdown.Option("Otros")
            ],
            expand=True
        )
        
        self.monto_field = ft.TextField(
            label="Monto ($)", 
            expand=True, 
            visible=False,
            prefix_text="$"
        )
        
        self.descripcion_field = ft.TextField(
            label="Descripción (opcional)", 
            expand=True, 
            multiline=True,
            visible=False
        )
        
        #evento para mostrar/ocultar campos según tipo de donación
        self.tipo_donacion.on_change = self.on_tipo_donacion_change
        
        return ft.Column([
            crear_header("Donaciones"),
            
            ft.Container(
                content=ft.Column([
                    #navegación
                    ft.Row([
                        ft.ElevatedButton(
                            "← Volver al Inicio", 
                            on_click=lambda _: self.app.show_view("dashboard")
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "🚪 Cerrar Sesión",
                            on_click=self.app.cerrar_sesion,
                            bgcolor="#F44336",
                            color="white",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=15
                            )
                        )
                    ]),
                    
                    ft.Container(height=20),
                    
                    #mensaje inspirador
                    crear_card(
                        ft.Column([
                            ft.Text("❤️ TODO APORTE AYUDA, ¡DONA!", 
                                   size=22, weight=ft.FontWeight.BOLD, 
                                   color=COLORS["accent"], text_align=ft.TextAlign.CENTER),
                            ft.Container(height=15),
                            ft.Text(
                                "Cada donación que recibimos se transforma en alimento, refugio y "
                                "esperanza para cientos de animales que hoy viven en las calles. "
                                "Con tu ayuda, podemos rescatar, cuidar y encontrar hogares amorosos "
                                "para perros y gatos que solo necesitan una segunda oportunidad. "
                                "Ningún aporte es pequeño cuando se da con el corazón.",
                                size=14,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=15),
                            ft.Row([
                                ft.Icon(ft.Icons.FAVORITE, size=30, color=COLORS["secondary"]),
                                ft.Icon(ft.Icons.EMOJI_NATURE, size=30, color=COLORS["primary"]),
                                ft.Icon(ft.Icons.HEART_BROKEN, size=30, color=COLORS["accent"]),
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ]),
                        padding=30
                    ),
                    
                    #formulario de donación
                    crear_card(
                        ft.Column([
                            ft.Text("📋 Registro del Donador", 
                                   size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([self.nombre_field, self.apellido_field]),
                            ft.Row([self.contacto_field, self.tipo_donacion]),
                            self.monto_field,
                            self.descripcion_field,
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                "💰 REGISTRAR DONACIÓN",
                                on_click=self.guardar_donacion,
                                bgcolor=COLORS["primary"],
                                color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=15),
                                    padding=25
                                ),
                                expand=True
                            )
                        ])
                    ),
                    
                    #estadísticas de donaciones
                    self._crear_estadisticas_donaciones()
                ]),
                padding=20
            )
        ])
    
    def on_tipo_donacion_change(self, e):
        #mostrar monto solo para donaciones en dinero
        self.monto_field.visible = (self.tipo_donacion.value == "Dinero")
        
        #mostrar descripción para otros tipos de donación
        self.descripcion_field.visible = (self.tipo_donacion.value in ["Alimento", "Medicamentos", "Juguetes", "Otros"])
        
        if self.descripcion_field.visible:
            if self.tipo_donacion.value == "Alimento":
                self.descripcion_field.label = "Describe el tipo de alimento (ej: croquetas para perro adulto)"
            elif self.tipo_donacion.value == "Medicamentos":
                self.descripcion_field.label = "Describe los medicamentos (ej: antiparasitarios, vacunas)"
            elif self.tipo_donacion.value == "Juguetes":
                self.descripcion_field.label = "Describe los juguetes"
            else:
                self.descripcion_field.label = "Describe tu donación"
        
        if hasattr(self.app, 'page'):
            self.app.page.update()
    
    def guardar_donacion(self, e):
        if not all([self.nombre_field.value, self.apellido_field.value, 
                   self.contacto_field.value, self.tipo_donacion.value]):
            self.app.show_snackbar("Los campos marcados con * son obligatorios")
            return
        
        if self.tipo_donacion.value == "Dinero" and not self.monto_field.value:
            self.app.show_snackbar("Para donación en dinero debe especificar el monto")
            return
        
        try:
            monto = float(self.monto_field.value) if self.monto_field.value and self.monto_field.value else 0.0
            
            self.db.execute_query(
                """INSERT INTO donantes (nombre, apellido, contacto, tipo_donacion, monto, descripcion, fecha_donacion) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (self.nombre_field.value, self.apellido_field.value, self.contacto_field.value, 
                 self.tipo_donacion.value, monto, self.descripcion_field.value,
                 datetime.now().strftime("%d/%m/%Y"))
            )
            
            mensaje = self._get_mensaje_agradecimiento(self.tipo_donacion.value)
            self.app.show_snackbar(mensaje)
            self.limpiar_formulario()
            
        except ValueError:
            self.app.show_snackbar("El monto debe ser un número válido")
        except Exception as ex:
            self.app.show_snackbar(f"Error al registrar donación: {str(ex)}")
    
    def _get_mensaje_agradecimiento(self, tipo_donacion):
        mensajes = {
            "Dinero": "¡Donación monetaria registrada! 💰 Gracias por tu generosidad.",
            "Alimento": "¡Donación de alimento registrada! 🍖 Los animalitos te lo agradecen.",
            "Medicamentos": "¡Donación de medicamentos registrada! 💊 Ayudas a mantenerlos saludables.",
            "Juguetes": "¡Donación de juguetes registrada! 🎾 Los animalitos se divertirán mucho.",
            "Otros": "¡Donación registrada! ❤️ Gracias por tu valioso aporte."
        }
        return mensajes.get(tipo_donacion, "¡Donación registrada con éxito! Gracias por tu ayuda ❤️")
    
    def _crear_estadisticas_donaciones(self):
        try:
            #obtener estadísticas
            total_donaciones = self.db.execute_query("SELECT COUNT(*) FROM donantes")[0][0]
            total_dinero = self.db.execute_query("SELECT SUM(monto) FROM donantes WHERE monto > 0")[0][0] or 0
            
            tipos_donacion = self.db.execute_query(
                "SELECT tipo_donacion, COUNT(*) FROM donantes GROUP BY tipo_donacion"
            )
            
            return crear_card(
                ft.Column([
                    ft.Text("📊 Estadísticas de Donaciones", size=18, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(str(total_donaciones), size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("Total Donaciones", size=12)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=15,
                            bgcolor=COLORS["background"],
                            border_radius=10,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text(f"${total_dinero:,.2f}", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text("Total Recaudado", size=12)
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=15,
                            bgcolor=COLORS["background"],
                            border_radius=10,
                            expand=True
                        ),
                    ]),
                    ft.Container(height=10),
                    ft.Text("Distribución por tipo:", size=14, weight=ft.FontWeight.BOLD),
                    *[ft.Text(f"• {tipo[0]}: {tipo[1]}", size=12) for tipo in tipos_donacion]
                ])
            )
        except:
            return ft.Container()  #retorna contenedor vacío si hay error
    
    def limpiar_formulario(self):
        self.nombre_field.value = ""
        self.apellido_field.value = ""
        self.contacto_field.value = ""
        self.tipo_donacion.value = ""
        self.monto_field.value = ""
        self.descripcion_field.value = ""
        self.monto_field.visible = False
        self.descripcion_field.visible = False
        if hasattr(self.app, 'page'):
            self.app.page.update()