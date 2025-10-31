import flet as ft
import webbrowser
from styles.colors import COLORS, crear_header, crear_card

class ContactoView:
    def __init__(self, app):
        self.app = app
        
    def build(self):
        return ft.Column([
            crear_header("Contáctanos"),
            
            ft.Container(
                content=ft.Column([
                    # Navegación
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
                    
                    ft.Container(height=30),
                    
                    # Tarjeta principal de contacto
                    crear_card(
                        ft.Column([
                            ft.Text("📍 ESTAMOS CERCA DE TI", 
                                   size=22, weight=ft.FontWeight.BOLD,
                                   color=COLORS["primary"], text_align=ft.TextAlign.CENTER),
                            ft.Text(
                                "Aquí puedes observar nuestros horarios y ubicación, "
                                "o consúltanos directamente por WhatsApp",
                                size=14, 
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=30),
                            
                            # Información de contacto
                            ft.Row([
                                self._crear_tarjeta_info(
                                    ft.Icons.ACCESS_TIME,
                                    "HORARIOS",
                                    "Lunes a Viernes\n08:00 - 11:00\n13:00 - 18:00\n\nSábados\n09:00 - 13:00",
                                    COLORS["accent"]
                                ),
                                self._crear_tarjeta_info(
                                    ft.Icons.LOCATION_ON,
                                    "DÓNDE ESTAMOS", 
                                    "Caacupé\nEligio Ayala c/ Ayala Solis\nAl costado de la Basílica",
                                    COLORS["secondary"]
                                ),
                            ]),
                            
                            ft.Container(height=20),
                            
                            # Información adicional
                            ft.Row([
                                self._crear_tarjeta_info(
                                    ft.Icons.PHONE,
                                    "TELÉFONO",
                                    "+595 972 283280",
                                    COLORS["primary"]
                                ),
                                self._crear_tarjeta_info(
                                    ft.Icons.EMAIL,
                                    "CORREO",
                                    "petrescuepy@gmail.com",
                                    COLORS["accent"]
                                ),
                            ]),
                            
                            ft.Container(height=30),
                            
                            # Botones de acción
                            ft.Row([
                                ft.ElevatedButton(
                                    "📞 LLAMAR AHORA",
                                    on_click=lambda _: self.llamar_telefono(),
                                    bgcolor=COLORS["primary"],
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        padding=20
                                    ),
                                    expand=True
                                ),
                                ft.ElevatedButton(
                                    "💬 WHATSAPP",
                                    on_click=lambda _: self.abrir_whatsapp(),
                                    bgcolor="#25D366",
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        padding=20
                                    ),
                                    expand=True
                                ),
                            ]),
                            
                            ft.Container(height=20),
                            
                            # Mapa o imagen de ubicación (placeholder)
                            ft.Container(
                                content=ft.Column([
                                    ft.Icon(ft.Icons.MAP, size=50, color=COLORS["text"]),
                                    ft.Text("Mapa de Ubicación", size=16, weight=ft.FontWeight.BOLD),
                                    ft.Text(
                                        "Estamos ubicados en el corazón de la ciudad, "
                                        "fácilmente accesible por transporte público.",
                                        size=12,
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    ft.Container(height=10),
                                    ft.ElevatedButton(
                                        "🗺️ VER EN GOOGLE MAPS",
                                        on_click=lambda _: self.abrir_maps(),
                                        bgcolor=COLORS["secondary"],
                                        color="white"
                                    )
                                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                padding=30,
                                bgcolor=COLORS["background"],
                                border_radius=10
                            ),
                            
                            ft.Container(height=20),
                            
                            # Mensaje final
                            ft.Container(
                                content=ft.Text(
                                    "¡No dudes en contactarnos! Estamos aquí para ayudarte "
                                    "y responder cualquier pregunta sobre adopciones, donaciones "
                                    "o cómo puedes ayudar a nuestros animalitos.",
                                    size=14,
                                    text_align=ft.TextAlign.CENTER,
                                    color=COLORS["text"]
                                ),
                                padding=20,
                                bgcolor=COLORS["card"],
                                border_radius=10
                            )
                        ]),
                        padding=30
                    )
                ]),
                padding=20
            )
        ])
    
    def _crear_tarjeta_info(self, icono, titulo, contenido, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icono, size=35, color=color),
                ft.Container(height=10),
                ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(height=5),
                ft.Text(contenido, size=12, text_align=ft.TextAlign.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=COLORS["card"],
            border_radius=10,
            expand=True,
            margin=5
        )
    
    def abrir_whatsapp(self):
        """Abrir WhatsApp con número predefinido"""
        numero = "+595972283280" 
        mensaje = "Hola, me interesa obtener más información sobre Pet Rescue"
        url = f"https://wa.me/{numero}?text={mensaje}"
        webbrowser.open(url)
        self.app.show_snackbar("¡Abriendo WhatsApp! 💬")
    
    def llamar_telefono(self):
        """Simular llamada telefónica"""
        self.app.show_snackbar("📞 Llamando al +595 972 283280...")
    
    def abrir_maps(self):
        """Abrir Google Maps con la ubicación"""
        url = "https://www.google.com/maps/search/?api=1&query=Pet+Rescue+Animal+Shelter"
        webbrowser.open(url)
        self.app.show_snackbar("🗺️ Abriendo Google Maps...")