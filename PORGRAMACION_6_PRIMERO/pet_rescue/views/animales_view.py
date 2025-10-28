#mi vista de animales rescatados donde ademas de registrar a un nuevo animalito, tambien se puede aditar
#o eliminar uno de ellos, o más. Así también se tiene disponible un filtro donde se puede elegir qué animales
# ver segun su estado, ya sea: adoptado, en adopcion o en refugio


#el botón de limpiar los inputs y la opción de eliminar no funcionan. Se guarda todo correctamente pero a la 
#hora de editar no hay mensaje de confirmación, y al eliminar (ya que no funciona) tampoco hay mensaje. Buscar
#por estado funciona bien.


import flet as ft
from styles.colors import COLORS, crear_header, crear_card

class AnimalesView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.edit_id = None
        
    def build(self):
        #campos del formulario
        self.nombre_field = ft.TextField(label="Nombre", expand=True)
        self.especie_field = ft.Dropdown(
            label="Especie",
            options=[
                ft.dropdown.Option("Perro"),
                ft.dropdown.Option("Gato"),
                ft.dropdown.Option("Otro")
            ],
            expand=True
        )
        self.edad_field = ft.TextField(label="Edad", expand=True)
        self.fecha_field = ft.TextField(label="Fecha de rescate (dd/mm/aaaa)", expand=True)
        self.estado_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("En refugio"),
                ft.dropdown.Option("En adopción"), 
                ft.dropdown.Option("Adoptado")
            ],
            expand=True
        )
        self.vacunas_field = ft.TextField(label="Vacunas", expand=True, multiline=True)
        self.descripcion_field = ft.TextField(label="Descripción", expand=True, multiline=True)
        
        #tabla de animales
        self.tabla_animales = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Especie")),
                ft.DataColumn(ft.Text("Edad")),
                ft.DataColumn(ft.Text("Fecha Rescate")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Operaciones")),
            ],
            rows=[]
        )
        
        #filtro por estado
        self.filtro_estado = ft.Dropdown(
            label="Buscar por estado",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("En refugio"),
                ft.dropdown.Option("En adopción"),
                ft.dropdown.Option("Adoptado")
            ],
            on_change=lambda e: self.cargar_animales(),
            width=200
        )
        
        #cargar datos iniciales
        self.cargar_animales()
        
        return ft.Column([
            crear_header("Animales Rescatados"),
            
            ft.Container(
                content=ft.Column([
                    #filtro y navegación
                    ft.Row([
                        self.filtro_estado,
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "← Volver al Inicio", 
                            on_click=lambda _: self.app.show_view("dashboard")
                        )
                    ]),
                    
                    ft.Container(height=20),
                    
                    #mi formulario
                    crear_card(
                        ft.Column([
                            ft.Text("Registrar Animal Rescatado", size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([self.nombre_field, self.especie_field, self.edad_field]),
                            ft.Row([self.fecha_field, self.estado_field]),
                            self.vacunas_field,
                            self.descripcion_field,
                            ft.Row([
                                ft.ElevatedButton(
                                    "Registrar", 
                                    on_click=self.guardar_animal,
                                    bgcolor=COLORS["primary"],
                                    color="white"
                                ),
                                ft.ElevatedButton(
                                    "Limpiar", 
                                    on_click=self.limpiar_formulario,
                                    bgcolor=COLORS["secondary"],
                                    color="white"
                                )
                            ])
                        ])
                    ),
                    
                    #la tabla
                    crear_card(
                        ft.Column([
                            ft.Text("Animales Registrados", size=18, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Column([self.tabla_animales], scroll=ft.ScrollMode.ALWAYS),
                                height=400,
                            )
                        ])
                    )
                ]),
                padding=20
            )
        ])
    
    def cargar_animales(self):
        filtro = self.filtro_estado.value
        if filtro and filtro != "Todos":
            query = "SELECT * FROM animales WHERE estado = ? ORDER BY fecha_rescate DESC"
            params = (filtro,)
        else:
            query = "SELECT * FROM animales ORDER BY fecha_rescate DESC"
            params = ()
        
        animales = self.db.execute_query(query, params)
        self.tabla_animales.rows.clear()
        
        for animal in animales:
            self.tabla_animales.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(animal[1])),
                    ft.DataCell(ft.Text(animal[2])),
                    ft.DataCell(ft.Text(animal[3])),
                    ft.DataCell(ft.Text(animal[4])),
                    ft.DataCell(ft.Text(animal[5])),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(ft.Icons.EDIT, on_click=lambda e, id=animal[0]: self.editar_animal(id)),
                            ft.IconButton(ft.Icons.DELETE, on_click=lambda e, id=animal[0]: self.eliminar_animal(id)),
                        ])
                    ),
                ])
            )
        self.app.page.update()
    
    def guardar_animal(self, e):
        if not all([self.nombre_field.value, self.especie_field.value, 
                   self.edad_field.value, self.fecha_field.value, self.estado_field.value]):
            self.app.show_snackbar("Todos los campos son obligatorios")
            return
        
        if self.edit_id:
            #actualizar
            self.db.execute_query(
                """UPDATE animales SET nombre=?, especie=?, edad=?, fecha_rescate=?, estado=?, 
                vacunas=?, descripcion=? WHERE id=?""",
                (self.nombre_field.value, self.especie_field.value, self.edad_field.value, 
                 self.fecha_field.value, self.estado_field.value, self.vacunas_field.value, 
                 self.descripcion_field.value, self.edit_id)
            )
            mensaje = "Animal actualizado correctamente!"
        else:
            #insertar
            self.db.execute_query(
                """INSERT INTO animales (nombre, especie, edad, fecha_rescate, estado, vacunas, descripcion) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (self.nombre_field.value, self.especie_field.value, self.edad_field.value, 
                 self.fecha_field.value, self.estado_field.value, self.vacunas_field.value, 
                 self.descripcion_field.value)
            )
            mensaje = "Animal registrado correctamente!"
        
        self.app.show_snackbar(mensaje)
        self.limpiar_formulario()
        self.cargar_animales()
    
    def editar_animal(self, id):
        animales = self.db.execute_query("SELECT * FROM animales WHERE id = ?", (id,))
        if animales:
            animal = animales[0]
            self.nombre_field.value = animal[1]
            self.especie_field.value = animal[2]
            self.edad_field.value = animal[3]
            self.fecha_field.value = animal[4]
            self.estado_field.value = animal[5]
            self.vacunas_field.value = animal[6] or ""
            self.descripcion_field.value = animal[7] or ""
            self.edit_id = id
            self.app.page.update()
    
    def eliminar_animal(self, id):
        def confirmar_eliminar(e):
            self.db.execute_query("DELETE FROM animales WHERE id=?", (id,))
            self.cargar_animales()
            self.app.page.dialog.open = False
            self.app.page.update()
            self.app.show_snackbar("Animal eliminado")
        
        self.app.page.dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text("¿Estás seguro de eliminar este animal?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(self.app.page.dialog, 'open', False)),
                ft.TextButton("Eliminar", on_click=confirmar_eliminar),
            ]
        )
        self.app.page.dialog.open = True
        self.app.page.update()
    
    def limpiar_formulario(self):
        self.nombre_field.value = ""
        self.especie_field.value = ""
        self.edad_field.value = ""
        self.fecha_field.value = ""
        self.estado_field.value = ""
        self.vacunas_field.value = ""
        self.descripcion_field.value = ""
        self.edit_id = None
        self.app.page.update()