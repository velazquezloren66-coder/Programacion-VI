#Aquí le permite al administrador registrar al adoptante, sus datos y demás, hasta elegir directemente a qué
#animalito se llevará consigo a casa

#no hay validación de completar todos los campos obligatorios y tampoco hay mensaje de confirmación o error 
#de la realización de la adopción.



import flet as ft
from styles.colors import COLORS, crear_header, crear_card

class AdopcionesView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
        
    def build(self):
        #campos del formulario de adopción
        self.nombre_field = ft.TextField(label="Nombre", expand=True)
        self.apellido_field = ft.TextField(label="Apellido", expand=True)
        self.contacto_field = ft.TextField(label="Contacto", expand=True)
        self.direccion_field = ft.TextField(label="Dirección", expand=True)
        self.email_field = ft.TextField(label="Email", expand=True)
        self.fecha_field = ft.TextField(
            label="Fecha de adopción (dd/mm/aaaa)", 
            expand=True,
            value=self._get_current_date()
        )
        
        #dropdown para seleccionar animal
        self.animal_field = ft.Dropdown(
            label="Se va conmigo *",
            hint_text="Selecciona un animal",
            options=[],
            expand=True
        )
        
        #cargar animales disponibles para adopción
        self.cargar_animales_adopcion()
        
        return ft.Column([
            crear_header("Adopciones"),
            
            ft.Container(
                content=ft.Column([
                    #navegación
                    ft.Row([
                        ft.ElevatedButton(
                            "← Volver al Inicio", 
                            on_click=lambda _: self.app.show_view("dashboard")
                        )
                    ]),
                    
                    ft.Container(height=20),
                    
                    #información de animales disponibles
                    crear_card(
                        ft.Column([
                            ft.Text("🐾 Animales Disponibles para Adopción", 
                                   size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Conoce a nuestros amiguitos que buscan un hogar amoroso", 
                                   size=14, color=COLORS["text"]),
                            ft.Container(height=10),
                            self._crear_lista_animales()
                        ])
                    ),
                    
                    #formulario de adopción
                    crear_card(
                        ft.Column([
                            ft.Text("📝 Registra al Adoptante", 
                                   size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([self.nombre_field, self.apellido_field]),
                            ft.Row([self.contacto_field, self.email_field]),
                            ft.Row([self.direccion_field, self.fecha_field]),
                            self.animal_field,
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                "🏠 VAMOS A CASA",
                                on_click=self.guardar_adopcion,
                                bgcolor=COLORS["accent"],
                                color="white",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=15),
                                    padding=25
                                ),
                                expand=True
                            )
                        ])
                    )
                ]),
                padding=20
            )
        ])
    
    def _get_current_date(self):
        from datetime import datetime
        return datetime.now().strftime("%d/%m/%Y")
    
    def cargar_animales_adopcion(self):
        animales = self.db.execute_query(
            "SELECT id, nombre, especie, edad FROM animales WHERE estado = 'En adopción'"
        )
        self.animal_field.options.clear()
        
        for animal in animales:
            self.animal_field.options.append(
                ft.dropdown.Option(
                    key=str(animal[0]),
                    text=f"🐕 {animal[1]} - {animal[2]} ({animal[3]})" if animal[2] == "Perro" else f"🐈 {animal[1]} - {animal[2]} ({animal[3]})"
                )
            )
        
        if hasattr(self.app, 'page'):
            self.app.page.update()
    
    def _crear_lista_animales(self):
        animales = self.db.execute_query(
            "SELECT nombre, especie, edad, descripcion FROM animales WHERE estado = 'En adopción'"
        )
        
        if not animales:
            return ft.Text("No hay animales disponibles para adopción en este momento.", 
                          color=COLORS["text"], italic=True)
        
        contenedores = []
        for animal in animales:
            icono = "🐕" if animal[1] == "Perro" else "🐈"
            contenedores.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"{icono} {animal[0]}", 
                                   weight=ft.FontWeight.BOLD, size=16),
                            ft.Text(f"{animal[1]} • {animal[2]}", 
                                   color=COLORS["text"], size=12)
                        ]),
                        ft.Text(animal[3] or "Busca un hogar cálido y una familia responsable.", 
                              size=12, color=COLORS["text"]),
                    ]),
                    padding=15,
                    bgcolor=COLORS["background"],
                    border_radius=10,
                    margin=ft.margin.only(bottom=10)
                )
            )
        
        return ft.Column(contenedores, scroll=ft.ScrollMode.ADAPTIVE)
    
    def guardar_adopcion(self, e):
        if not all([self.nombre_field.value, self.apellido_field.value, 
                   self.contacto_field.value, self.animal_field.value]):
            self.app.show_snackbar("Los campos marcados con * son obligatorios")
            return
        
        try:
            #registrar adoptante
            self.db.execute_query(
                """INSERT INTO adoptantes (nombre, apellido, contacto, direccion, email, fecha_adopcion, animal_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (self.nombre_field.value, self.apellido_field.value, self.contacto_field.value, 
                 self.direccion_field.value, self.email_field.value, self.fecha_field.value, 
                 int(self.animal_field.value))
            )
            
            #actualizar estado del animal
            self.db.execute_query(
                "UPDATE animales SET estado = 'Adoptado' WHERE id = ?",
                (int(self.animal_field.value),)
            )
            
            self.app.show_snackbar("¡Adopción registrada! ❤️ El animal ahora aparece como adoptado.")
            self.limpiar_formulario()
            self.cargar_animales_adopcion()
            
        except Exception as ex:
            self.app.show_snackbar(f"Error al registrar adopción: {str(ex)}")
    
    def limpiar_formulario(self):
        self.nombre_field.value = ""
        self.apellido_field.value = ""
        self.contacto_field.value = ""
        self.direccion_field.value = ""
        self.email_field.value = ""
        self.fecha_field.value = self._get_current_date()
        self.animal_field.value = ""
        if hasattr(self.app, 'page'):
            self.app.page.update()