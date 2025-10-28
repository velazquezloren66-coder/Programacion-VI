#mi vista de animales rescatados donde ademas de registrar a un nuevo animalito, tambien se puede aditar
#o eliminar uno de ellos, o más. Así también se tiene disponible un filtro donde se puede elegir qué animales
#ver segun su estado, ya sea: adoptado, en adopcion o en refugio


#el botón de limpiar los inputs y la opción de eliminar registros YA funcionan. Se guarda todo correctamente,
#pero a la hora de editar no hay mensaje de confirmación, y al eliminar (que YA funciona) tampoco hay mensaje.
#Buscar por estado funciona bien.


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
                #ft.dropdown.Option("Adoptado")
            ],
            expand=True
        )
        self.vacunas_field = ft.TextField(label="Vacunas", expand=True, multiline=True)
        self.descripcion_field = ft.TextField(label="Descripción", expand=True, multiline=True)
        
        #botones
        btn_guardar = ft.ElevatedButton(
            "💾 Guardar", 
            on_click=self.guardar_animal,
            bgcolor=COLORS["primary"],
            color="white"
        )
        
        btn_limpiar = ft.ElevatedButton(
            "🔄 Limpiar", 
            on_click=lambda e: self.limpiar_formulario(),
            bgcolor=COLORS["secondary"],
            color="white"
        )
        
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
                        ),
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
                    
                    #formulario
                    crear_card(
                        ft.Column([
                            ft.Text("Registrar Animal Rescatado", size=18, weight=ft.FontWeight.BOLD),
                            ft.Row([self.nombre_field, self.especie_field, self.edad_field]),
                            ft.Row([self.fecha_field, self.estado_field]),
                            self.vacunas_field,
                            self.descripcion_field,
                            ft.Row([btn_guardar, btn_limpiar])
                        ])
                    ),
                    
                    #tabla
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
        try:
            filtro = self.filtro_estado.value
            if filtro and filtro != "Todos":
                query = "SELECT * FROM animales WHERE estado = ? ORDER BY fecha_rescate DESC"
                params = (filtro,)
            else:
                query = "SELECT * FROM animales ORDER BY fecha_rescate DESC"
                params = ()
            
            animales = self.db.execute_query(query, params)
            self.tabla_animales.rows.clear()
            
            if animales:
                for animal in animales:
                    #crear botones de editar y eliminar para cada animal
                    btn_editar = ft.IconButton(
                        ft.Icons.EDIT, 
                        icon_color=COLORS["primary"],
                        tooltip="Editar animal",
                        data=animal[0],  #guardar ID en data
                        on_click=self.editar_animal_click
                    )
                    
                    btn_eliminar = ft.IconButton(
                        ft.Icons.DELETE, 
                        icon_color="#F44336",
                        tooltip="Eliminar animal",
                        data=animal[0],  #guardar ID en data
                        on_click=self.eliminar_animal_click
                    )
                    
                    self.tabla_animales.rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(animal[1])),
                            ft.DataCell(ft.Text(animal[2])),
                            ft.DataCell(ft.Text(animal[3])),
                            ft.DataCell(ft.Text(animal[4])),
                            ft.DataCell(ft.Text(animal[5])),
                            ft.DataCell(ft.Row([btn_editar, btn_eliminar])),
                        ])
                    )
            else:
                #mostrar mensaje si no hay animales
                self.tabla_animales.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text("No hay animales registrados", italic=True)),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ])
                )
                
            self.app.page.update()
            
        except Exception as e:
            print(f"Error al cargar animales: {e}")
            self.app.show_snackbar("Error al cargar los animales", "#F44336")
    
    def editar_animal_click(self, e):
        """Manejador de clic para editar"""
        animal_id = e.control.data
        self.editar_animal(animal_id)
    
    def eliminar_animal_click(self, e):
        """Manejador de clic para eliminar"""
        animal_id = e.control.data
        self.eliminar_animal(animal_id)
    
    def eliminar_animal(self, animal_id):
        """Eliminar animal con mensajes en la vista"""
        try:
            #obtener datos del animal
            animal_data = self.db.execute_query("SELECT nombre, estado FROM animales WHERE id = ?", (animal_id,))
            
            if not animal_data:
                self.app.show_snackbar("❌ Animal no encontrado", "#F44336")
                return
                
            nombre_animal = animal_data[0][0]
            estado_animal = animal_data[0][1]
            
            if estado_animal == "Adoptado":
                self.app.show_snackbar("❌ No se puede eliminar un animal adoptado", "#F44336")
                return
            
            #eliminar el animal
            result = self.db.execute_query("DELETE FROM animales WHERE id = ?", (animal_id,))
            
            if result is not None and result > 0:
                self.app.show_snackbar(f"✅ '{nombre_animal}' eliminado correctamente", "#4CAF50")
                self.cargar_animales()  #recargar la tabla
            else:
                self.app.show_snackbar("❌ Error al eliminar el animal", "#F44336")
                
        except Exception as e:
            self.app.show_snackbar(f"❌ Error: {str(e)}", "#F44336")
    
    def guardar_animal(self, e):
        try:
            if not all([self.nombre_field.value, self.especie_field.value, 
                       self.edad_field.value, self.fecha_field.value, self.estado_field.value]):
                self.app.show_snackbar("❌ Todos los campos son obligatorios", "#F44336")
                return
            
            if self.edit_id:
                #actualizar
                result = self.db.execute_query(
                    """UPDATE animales SET nombre=?, especie=?, edad=?, fecha_rescate=?, estado=?, 
                    vacunas=?, descripcion=? WHERE id=?""",
                    (self.nombre_field.value, self.especie_field.value, self.edad_field.value, 
                     self.fecha_field.value, self.estado_field.value, self.vacunas_field.value, 
                     self.descripcion_field.value, self.edit_id)
                )
                if result is not None:
                    self.app.show_snackbar("✅ Animal actualizado correctamente", "#4CAF50")
                else:
                    self.app.show_snackbar("❌ Error al actualizar el animal", "#F44336")
            else:
                #insertar
                result = self.db.execute_query(
                    """INSERT INTO animales (nombre, especie, edad, fecha_rescate, estado, vacunas, descripcion) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (self.nombre_field.value, self.especie_field.value, self.edad_field.value, 
                     self.fecha_field.value, self.estado_field.value, self.vacunas_field.value, 
                     self.descripcion_field.value)
                )
                if result is not None:
                    self.app.show_snackbar("✅ Animal registrado correctamente", "#4CAF50")
                else:
                    self.app.show_snackbar("❌ Error al registrar el animal", "#F44336")
            
            self.limpiar_formulario()
            self.cargar_animales()
            
        except Exception as ex:
            self.app.show_snackbar(f"❌ Error: {str(ex)}", "#F44336")
    
    def editar_animal(self, id):
        try:
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
                self.app.show_snackbar("📝 Modo edición activado", "#2196F3")
                self.app.page.update()
                
        except Exception as ex:
            self.app.show_snackbar(f"❌ Error al cargar datos: {str(ex)}", "#F44336")
    
    def limpiar_formulario(self):
        """Limpiar formulario"""
        self.nombre_field.value = ""
        self.especie_field.value = ""
        self.edad_field.value = ""
        self.fecha_field.value = ""
        self.estado_field.value = ""
        self.vacunas_field.value = ""
        self.descripcion_field.value = ""
        self.edit_id = None
        self.app.page.update()