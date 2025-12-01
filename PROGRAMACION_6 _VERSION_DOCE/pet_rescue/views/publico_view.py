import flet as ft
from styles.colors import COLORS, crear_header, crear_card

class PublicoView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
    
    def build(self):
        #crear un GridView para mostrar los animalitos en cards
        self.grid_animales = ft.GridView(
            expand=1,
            runs_count=3,
            max_extent=350,
            child_aspect_ratio=0.50, #ESTE es el que cambia la altura de las cedulas, cuando mas chico, es mayor el largor de la tarjeta
            spacing=15,
            run_spacing=15,
        )
        
        self.cargar_animales_publico()
        
        return ft.Column([
            crear_header("🐾 Animalitos en Busca de Hogar"),
            
            ft.Container(
                content=ft.Column([
                    #barra de navegación
                    ft.Row([
                        ft.ElevatedButton(
                            "← Volver al Inicio", 
                            on_click=lambda _: self.app.show_view("login"),
                            icon=ft.Icons.ARROW_BACK,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=10
                            )
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "📞 Contactar Asociación",
                            on_click=lambda _: self.app.show_view("contacto_publico"),
                            bgcolor=COLORS["primary"],
                            color="white",
                            icon=ft.Icons.CONTACT_PHONE,
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
                            ft.Text("❤️ DALES UNA SEGUNDA OPORTUNIDAD", 
                                   size=22, weight=ft.FontWeight.BOLD, 
                                   color=COLORS["accent"], text_align=ft.TextAlign.CENTER),
                            ft.Container(height=10),
                            ft.Text(
                                "Cada uno de estos animalitos tiene una historia de superación. "
                                "Han sido rescatados, rehabilitados y están listos para llenar "
                                "tu hogar de amor y alegría. ¡Conócelos!",
                                size=14,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Icon(ft.Icons.FAVORITE, size=25, color=COLORS["secondary"]),
                                ft.Icon(ft.Icons.PETS, size=25, color=COLORS["primary"]),
                                ft.Icon(ft.Icons.HOME, size=25, color=COLORS["accent"]),
                            ], alignment=ft.MainAxisAlignment.CENTER)
                        ]),
                        padding=25
                    ),
                    
                    ft.Container(height=20),
                    
                    #Grid de animalitos
                    crear_card(
                        ft.Column([
                            ft.Row([
                                ft.Text("📋 Nuestros Animalitos Disponibles", 
                                       size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    "🔄 Actualizar",
                                    on_click=self.refresh_vista,
                                    bgcolor=COLORS["primary"],
                                    color="white",
                                    icon=ft.Icons.REFRESH,
                                    height=40
                                )
                            ]),
                            ft.Container(height=10),
                            ft.Text(f"Total de animalitos buscando hogar: {self.contar_animales()}",
                                   size=14, color=COLORS["text"], weight=ft.FontWeight.BOLD),
                            ft.Container(height=15),
                            ft.Container(
                                content=self.grid_animales,
                                height=650, #altura/largor de la tarjeta que contiene todas las cedulas
                            )
                        ])
                    )
                ]),
                padding=20
            )
        ])
    
    def cargar_animales_publico(self):
        """Cargar animales disponibles para adopción"""
        try:
            query = """
                SELECT id, nombre, especie, edad, descripcion, estado 
                FROM animales 
                WHERE estado = 'En adopción'
            """
            
            animales = self.db.execute_query(query)
            
            self.grid_animales.controls.clear()
            
            if animales and len(animales) > 0:
                for animal in animales:
                    card_animal = self._crear_cedula_animal(animal)
                    self.grid_animales.controls.append(card_animal)
            else:
                self._mostrar_sin_animales()
                
            self.app.page.update()
            
        except Exception:
            self._mostrar_error("Error al cargar los animalitos")
    
    def _crear_cedula_animal(self, animal):
        """Crear una cédula para un animal individual"""
        animal_id = animal[0]
        nombre = animal[1]
        especie = animal[2]
        edad = animal[3]
        descripcion = animal[4]
        
        contenido = ft.Column([
            #Header con nombre
            ft.Container(
                content=ft.Text(
                    nombre,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=COLORS["primary"],
                    text_align=ft.TextAlign.CENTER
                ),
                bgcolor=COLORS["background"],
                padding=10,
                border_radius=ft.border_radius.only(top_left=10, top_right=10)
            ),
            
            #Área de IMAGEN AQUÍ
            ft.Container(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PETS, size=60, color=COLORS["secondary"]),
                        ft.Text(
                            "IMAGEN AQUÍ",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=COLORS["text"]
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center,
                    width=300,  
                    height=160,
                    bgcolor="#f8f9fa",
                    border_radius=8,
                    border=ft.border.all(2, COLORS["secondary"])
                ),
                alignment=ft.alignment.center,
                padding=15
            ),
            
            #información básica
            ft.Container(
                content=ft.Column([
                    #fila: Especie y Edad
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("ESPECIE", size=10, color="gray", weight=ft.FontWeight.BOLD),
                                ft.Text(especie, size=12, weight=ft.FontWeight.BOLD),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True
                        ),
                        ft.VerticalDivider(width=1, color=COLORS["background"]),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("EDAD", size=10, color="gray", weight=ft.FontWeight.BOLD),
                                ft.Text(str(edad), size=12, weight=ft.FontWeight.BOLD),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True
                        ),
                    ]),
                    
                    ft.Container(height=20),
                    
                    #descripción
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "📝 Sobre mí:",
                                size=12,
                                color=COLORS["primary"],
                                weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Container(height=5),
                            ft.Text(
                                descripcion[:100] + "..." if descripcion and len(descripcion) > 100 else (descripcion or "Sin descripción"),
                                size=11,
                                color=COLORS["text"],
                                text_align=ft.TextAlign.CENTER
                            ),
                        ]),
                        padding=ft.padding.symmetric(horizontal=10)
                    ),
                ]),
                padding=ft.padding.symmetric(horizontal=15)
            ),
            
            ft.Container(height=20),
            
            #botón de contacto
            ft.Container(
                content=ft.ElevatedButton(
                    "💖 Me interesa adoptar",
                    on_click=lambda e, aid=animal_id: self.contactar_por_animal(aid),
                    bgcolor=COLORS["accent"],
                    color="white",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=12
                    ),
                    expand=True
                ),
                padding=ft.padding.symmetric(horizontal=15)
            ),
        ])
        
        return ft.Container(
            content=crear_card(contenido, padding=0),
            width=300
        )
    
    def _mostrar_sin_animales(self):
        """Mostrar mensaje cuando no hay animales"""
        contenido = ft.Column([
            ft.Icon(ft.Icons.PETS, size=50, color=COLORS["secondary"]),
            ft.Text("No hay animalitos disponibles", 
                   size=16, weight=ft.FontWeight.BOLD),
            ft.Text("Los animalitos con estado 'En adopción' aparecerán aquí", 
                   size=12, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.grid_animales.controls.append(
            ft.Container(
                content=crear_card(contenido, padding=30),
                width=400
            )
        )
    
    def _mostrar_error(self, mensaje):
        """Mostrar error general"""
        contenido = ft.Column([
            ft.Icon(ft.Icons.ERROR, size=50, color="#F44336"),
            ft.Text("Error", size=16, weight=ft.FontWeight.BOLD, color="#F44336"),
            ft.Text(mensaje, size=12, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.grid_animales.controls.append(
            ft.Container(
                content=crear_card(contenido, padding=30),
                width=400
            )
        )
    
    def contactar_por_animal(self, animal_id):
        """Redirigir a la vista de contacto"""
        self.app.show_view("contacto_publico")
    
    def contar_animales(self):
        """Contar animales en adopción"""
        try:
            resultado = self.db.execute_query("SELECT COUNT(*) FROM animales WHERE estado = 'En adopción'")
            if resultado and len(resultado) > 0:
                return resultado[0][0]
            return 0
        except:
            return 0
    
    def refresh_vista(self, e=None):
        """Recargar la vista"""
        self.cargar_animales_publico()
        self.app.show_snackbar("🔄 Vista actualizada", "#2196F3")