import flet as ft
from styles.colors import COLORS, crear_header, crear_card

class PublicoView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
    
    def build(self):
        # Crear un GridView para mostrar los animalitos en cards
        self.grid_animales = ft.GridView(
            expand=1,
            runs_count=3,
            max_extent=320,  # Un poco más ancho para mejor formato
            child_aspect_ratio=0.7,  # Mejor proporción para cédulas
            spacing=15,
            run_spacing=15,
        )
        
        self.cargar_animales_publico()
        
        return ft.Column([
            crear_header("🐾 Animalitos en Busca de Hogar"),
            
            ft.Container(
                content=ft.Column([
                    # Barra de navegación
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
                    
                    # Mensaje inspirador
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
                    
                    # Grid de animalitos
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
                                height=600,
                            )
                        ])
                    )
                ]),
                padding=20
            )
        ])
    
    def cargar_animales_publico(self):
        """Cargar animales disponibles para adopción - SOLO 'En adopcion'"""
        try:
            print("🔍 Cargando animales EN ADOPCIÓN...")
            
            # CONSULTA ESPECÍFICA: Solo animales con estado 'En adopcion'
            animales = self.db.execute_query("""
                SELECT id, nombre, especie, raza, edad, descripcion, imagen_url, estado 
                FROM animales 
                WHERE estado = 'En adopcion'
                ORDER BY fecha_ingreso DESC
            """)
            
            print(f"✅ Animales en adopción encontrados: {len(animales) if animales else 0}")
            
            self.grid_animales.controls.clear()
            
            if animales and len(animales) > 0:
                print(f"🎯 Mostrando {len(animales)} animales EN ADOPCIÓN")
                
                for animal in animales:
                    print(f"🐾 Cédula para: {animal[1]}")
                    
                    # Crear la cédula con formato mejorado
                    card_animal = self._crear_cedula_animal(animal)
                    self.grid_animales.controls.append(card_animal)
            else:
                print("❌ No hay animales con estado 'En adopcion'")
                # Mensaje cuando no hay animales en adopción
                self.grid_animales.controls.append(
                    ft.Container(
                        content=crear_card(
                            ft.Column([
                                ft.Icon(ft.Icons.PETS, size=50, color=COLORS["secondary"]),
                                ft.Text("No hay animalitos disponibles", 
                                       size=16, weight=ft.FontWeight.BOLD),
                                ft.Text("Actualmente no tenemos animalitos buscando hogar", 
                                       size=12, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
                                ft.Text("¡Vuelve pronto!", 
                                       size=12, color=COLORS["accent"], text_align=ft.TextAlign.CENTER),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=30
                        ),
                        width=400
                    )
                )
                
            self.app.page.update()
            
        except Exception as e:
            print(f"❌ Error al cargar animales públicos: {e}")
            # Mostrar mensaje de error
            self.grid_animales.controls.append(
                ft.Container(
                    content=crear_card(
                        ft.Column([
                            ft.Icon(ft.Icons.ERROR, size=50, color="#F44336"),
                            ft.Text("Error al cargar los animalitos", 
                                   size=16, weight=ft.FontWeight.BOLD, color="#F44336"),
                            ft.Text(f"Error: {str(e)}", 
                                   size=10, color=COLORS["text"], text_align=ft.TextAlign.CENTER),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=30
                    ),
                    width=400
                )
            )
    
    def _crear_cedula_animal(self, animal):
        """Crear una cédula con formato atractivo para cada animal"""
        
        # Crear el contenido de la cédula
        contenido_cedula = ft.Column([
            # HEADER DE LA CÉDULA - Nombre y especie
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        animal[1],  # nombre
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLORS["primary"],
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        animal[2],  # especie
                        size=14,
                        color=COLORS["text"],
                        text_align=ft.TextAlign.CENTER
                    ),
                ]),
                bgcolor=COLORS["background"],
                padding=10,
                border_radius=ft.border_radius.only(top_left=10, top_right=10)
            ),
            
            # IMAGEN - Placeholder con diseño de cédula
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.PETS, size=60, color=COLORS["secondary"]),
                            ft.Text("IMAGEN AQUÍ", 
                                   size=14, 
                                   weight=ft.FontWeight.BOLD,
                                   color=COLORS["text"]),
                            ft.Text("🐾", size=20)
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        width=280,
                        height=180,
                        bgcolor="#f8f9fa",
                        border_radius=8,
                        border=ft.border.all(2, COLORS["secondary"])
                    )
                ]),
                alignment=ft.alignment.center,
                padding=15
            ),
            
            # INFORMACIÓN BÁSICA
            ft.Container(
                content=ft.Column([
                    # Fila: Edad y Raza
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("EDAD", size=10, color="gray", weight=ft.FontWeight.BOLD),
                                ft.Text(animal[4] or "No especificada", size=12, weight=ft.FontWeight.BOLD),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True
                        ),
                        ft.VerticalDivider(width=1, color=COLORS["background"]),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("RAZA", size=10, color="gray", weight=ft.FontWeight.BOLD),
                                ft.Text(animal[3] or "Mixta", size=12, weight=ft.FontWeight.BOLD),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            expand=True
                        ),
                    ]),
                    
                    ft.Container(height=10),
                    
                    # Estado destacado
                    ft.Container(
                        content=ft.Text(
                            "🏠 BUSCA HOGAR 🏠",
                            size=12,
                            color="white",
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER
                        ),
                        bgcolor="#4CAF50",
                        padding=ft.padding.symmetric(horizontal=15, vertical=8),
                        border_radius=20,
                        alignment=ft.alignment.center
                    ),
                ]),
                padding=ft.padding.symmetric(horizontal=15)
            ),
            
            ft.Container(height=10),
            
            # DESCRIPCIÓN
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "📝 Sobre mí:",
                        size=12,
                        color=COLORS["primary"],
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(height=5),
                    ft.Text(
                        animal[5] or "Este animalito está buscando un hogar lleno de amor y cuidados.",
                        size=11,
                        color=COLORS["text"],
                        text_align=ft.TextAlign.CENTER
                    ),
                ]),
                padding=ft.padding.symmetric(horizontal=15)
            ),
            
            ft.Container(height=15),
            
            # BOTÓN DE CONTACTO
            ft.Container(
                content=ft.ElevatedButton(
                    "💖 Me interesa adoptar",
                    on_click=lambda e, animal_id=animal[0]: self.contactar_por_animal(animal_id),
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
            
            # FOOTER DE LA CÉDULA
            ft.Container(
                content=ft.Text(
                    "ID: " + str(animal[0]),
                    size=9,
                    color="gray",
                    text_align=ft.TextAlign.CENTER
                ),
                padding=5,
                bgcolor=COLORS["background"],
                border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
            )
        ])
        
        # Envolver en un contenedor con ancho fijo y luego en crear_card
        return ft.Container(
            content=crear_card(
                contenido_cedula,
                padding=0  # Sin padding interno para mejor control
            ),
            width=300
        )
    
    def contactar_por_animal(self, animal_id):
        """Redirigir a la vista de contacto cuando se interesan por un animal"""
        self.app.show_view("contacto_publico")
    
    def contar_animales(self):
        """Contar total de animales EN ADOPCIÓN"""
        try:
            resultado = self.db.execute_query("""
                SELECT COUNT(*) FROM animales 
                WHERE estado = 'En adopcion'
            """)
            return resultado[0][0] if resultado else 0
        except Exception as e:
            print(f"Error contando animales: {e}")
            return 0
    
    def refresh_vista(self, e=None):
        """Recargar la vista"""
        self.cargar_animales_publico()
        self.app.show_snackbar("🔄 Vista actualizada", "#2196F3")