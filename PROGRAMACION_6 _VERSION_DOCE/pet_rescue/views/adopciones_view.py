#CAMBIOS:

#1. Contar con una lista debajo del formulario de Adopciones donde se visualice a los adoptantes
#junto con el animalito que adoptaron (y se pueda editar y eliminar)

#2. Tambien el DashboardView de adopciones donde muestra el numero de animales adoptados,
#se adapta a lo que muestra mi lista de adoptados en mi vista de Adopciones

#3. Lograr que tambien se limpien los combo boxes en vista Adopciones con botones de refresh (Actualizar vista)
#tanto en la barra de navegación (junto a los otros botones) como debajo de la lista de animales disponibles
#para así visualizar bien los datos disponibles

#4. El botón de Limpiar funciona como debe limpiando los inputs

#5. Da mensajes de éxito al guardar, editar y eliminar


import flet as ft
import re
from datetime import datetime
from styles.colors import COLORS, crear_header, crear_card

class AdopcionesView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.mensaje_error = None
        self.mensaje_exito = None
        self.edit_id = None
        
    def build(self):
        #campos del formulario de adopción con validaciones
        self.nombre_field = ft.TextField(
            label="Nombre *", 
            expand=True,
            on_change=self.validar_nombre
        )
        self.apellido_field = ft.TextField(
            label="Apellido *", 
            expand=True,
            on_change=self.validar_apellido
        )
        self.contacto_field = ft.TextField(
            label="Contacto *", 
            expand=True,
            on_change=self.validar_contacto
        )
        self.direccion_field = ft.TextField(
            label="Dirección *", 
            expand=True,
            multiline=True,
            on_change=self.validar_direccion
        )
        self.email_field = ft.TextField(
            label="Email *", 
            expand=True,
            on_change=self.validar_email
        )
        self.fecha_field = ft.TextField(
            label="Fecha de adopción (dd/mm/aaaa) *", 
            expand=True,
            value=self._get_current_date(),
            on_change=self.validar_fecha
        )
        
        #dropdown para seleccionar animal
        self.animal_field = ft.Dropdown(
            label="Se va conmigo *",
            hint_text="Selecciona un animal",
            options=[],
            expand=True
        )
        
        #contenedor para mensaje de error - MEJORADO
        self.mensaje_error = ft.Container(
            content=ft.Text("", color="white", weight=ft.FontWeight.BOLD, size=14),
            bgcolor="#F44336",
            padding=10,
            border_radius=5,
            visible=False,
            margin=ft.margin.only(bottom=10)
        )
        
        #contenedor para mensaje de éxito - MEJORADO
        self.mensaje_exito = ft.Container(
            content=ft.Text("", color="white", weight=ft.FontWeight.BOLD, size=16),
            bgcolor="#4CAF50",
            padding=15,
            border_radius=8,
            visible=False,
            margin=ft.margin.only(bottom=10),
            alignment=ft.alignment.center
        )
        
        # BOTÓN DE REFRESH SIEMPRE VISIBLE
        self.btn_refresh = ft.ElevatedButton(
            "🔄 Actualizar Vista",
            on_click=self.refresh_vista,
            bgcolor=COLORS["primary"],
            color="white",
            icon=ft.Icons.REFRESH,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=15
            )
        )
        
        # NUEVA TABLA DE ADOPTANTES
        self.tabla_adoptantes = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Contacto")),
                ft.DataColumn(ft.Text("Email")),
                ft.DataColumn(ft.Text("Dirección")),
                ft.DataColumn(ft.Text("Fecha Adopción")),
                ft.DataColumn(ft.Text("Animal")),
                ft.DataColumn(ft.Text("Operaciones")),
            ],
            rows=[]
        )
        
        #cargar animales disponibles para adopción
        self.cargar_animales_adopcion()
        #cargar lista de adoptantes
        self.cargar_adoptantes()
        
        return ft.Column([
            crear_header("Adopciones"),
            
            ft.Container(
                content=ft.Column([
                    #navegación
                    ft.Row([
                        ft.ElevatedButton(
                            "← Volver al Inicio", 
                            on_click=lambda _: self.app.show_view("dashboard")
                        ),
                        ft.Container(expand=True),
                        # BOTÓN DE REFRESH EN LA BARRA DE NAVEGACIÓN TAMBIÉN
                        self.btn_refresh,
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
                    
                    #información de animales disponibles
                    crear_card(
                        ft.Column([
                            ft.Text("🐾 Animales Disponibles para Adopción", 
                                   size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Conoce a nuestros amiguitos que buscan un hogar amoroso", 
                                   size=14, color=COLORS["text"]),
                            ft.Container(height=10),
                            self._crear_lista_animales(),
                            # BOTÓN DE REFRESH DEBAJO DE LA LISTA TAMBIÉN
                            ft.Container(
                                content=ft.Row([
                                    self.btn_refresh,
                                ], alignment=ft.MainAxisAlignment.CENTER),
                                margin=ft.margin.only(top=10)
                            )
                        ])
                    ),
                    
                    #formulario de adopción
                    crear_card(
                        ft.Column([
                            ft.Text("📝 Registra al Adoptante", 
                                   size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("* Campos obligatorios", size=12, color="gray", italic=True),
                            #mensaje de éxito - MOVIDO ARRIBA DEL ERROR
                            self.mensaje_exito,
                            #mensaje de error
                            self.mensaje_error,
                            ft.Row([self.nombre_field, self.apellido_field]),
                            ft.Row([self.contacto_field, self.email_field]),
                            ft.Row([self.direccion_field, self.fecha_field]),
                            self.animal_field,
                            ft.Container(height=20),
                            ft.Row([
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
                                ),
                                ft.ElevatedButton(
                                    "🔄 Limpiar",
                                    on_click=self.limpiar_formulario,
                                    bgcolor=COLORS["secondary"],
                                    color="white",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=10),
                                        padding=20
                                    )
                                )
                            ])
                        ])
                    ),
                    
                    # NUEVA SECCIÓN: LISTA DE ADOPTANTES
                    crear_card(
                        ft.Column([
                            ft.Text("👥 Lista de Adoptantes", 
                                   size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Adoptantes registrados y sus mascotas", 
                                   size=14, color=COLORS["text"]),
                            ft.Container(height=10),
                            ft.Container(
                                content=ft.Column([self.tabla_adoptantes], scroll=ft.ScrollMode.ALWAYS),
                                height=400,
                            )
                        ])
                    )
                ]),
                padding=20
            )
        ])
    
    # MÉTODOS DE VALIDACIÓN (se mantienen igual)
    def validar_nombre(self, e):
        """Validar que el nombre solo contenga letras y espacios"""
        valor = self.nombre_field.value
        if valor:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', valor):
                self.nombre_field.error_text = "Solo se permiten letras y espacios"
                self.nombre_field.border_color = "red"
            else:
                self.nombre_field.error_text = None
                self.nombre_field.border_color = None
        else:
            self.nombre_field.error_text = None
            self.nombre_field.border_color = None
        self.app.page.update()
    
    def validar_apellido(self, e):
        """Validar que el apellido solo contenga letras y espacios"""
        valor = self.apellido_field.value
        if valor:
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', valor):
                self.apellido_field.error_text = "Solo se permiten letras y espacios"
                self.apellido_field.border_color = "red"
            else:
                self.apellido_field.error_text = None
                self.apellido_field.border_color = None
        else:
            self.apellido_field.error_text = None
            self.apellido_field.border_color = None
        self.app.page.update()
    
    def validar_contacto(self, e):
        """Validar que el contacto sea un número de teléfono válido"""
        valor = self.contacto_field.value
        if valor:
            #permitir números, espacios, paréntesis y guiones para formatos de teléfono
            if not re.match(r'^[\d\s\(\)\-+]+$', valor):
                self.contacto_field.error_text = "Solo se permiten números, espacios, () y -"
                self.contacto_field.border_color = "red"
            elif len(valor) < 8:
                self.contacto_field.error_text = "El contacto debe tener al menos 8 dígitos"
                self.contacto_field.border_color = "red"
            else:
                self.contacto_field.error_text = None
                self.contacto_field.border_color = None
        else:
            self.contacto_field.error_text = None
            self.contacto_field.border_color = None
        self.app.page.update()
    
    def validar_direccion(self, e):
        """Validar dirección - obligatorio y solo caracteres permitidos"""
        valor = self.direccion_field.value
        if not valor or valor.strip() == "":
            self.direccion_field.error_text = "❌ Este campo es obligatorio"
            self.direccion_field.border_color = "red"
        else:
            #permitir letras, números, espacios, acentos, comas, puntos, # y -
            if re.search(r'[!@$%^&*_+=|<>?{}\[\]~;/\\]', valor):
                self.direccion_field.error_text = "No se permiten caracteres especiales como !@$%^&*_+= etc."
                self.direccion_field.border_color = "red"
            elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\.,\(\)\-\#]+$', valor):
                self.direccion_field.error_text = "Solo letras, números, espacios, comas, puntos, # y -"
                self.direccion_field.border_color = "red"
            else:
                #validar longitud mínima
                if len(valor.strip()) < 10:
                    self.direccion_field.error_text = "La dirección debe ser más específica (mínimo 10 caracteres)"
                    self.direccion_field.border_color = "red"
                else:
                    self.direccion_field.error_text = None
                    self.direccion_field.border_color = None
        self.app.page.update()
    
    def validar_email(self, e):
        """Validar formato de email - obligatorio"""
        valor = self.email_field.value
        if not valor or valor.strip() == "":
            self.email_field.error_text = "❌ Este campo es obligatorio"
            self.email_field.border_color = "red"
        else:
            #validar formato básico de email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, valor):
                self.email_field.error_text = "Formato de email inválido (ej: usuario@dominio.com)"
                self.email_field.border_color = "red"
            else:
                self.email_field.error_text = None
                self.email_field.border_color = None
        self.app.page.update()
    
    def validar_fecha(self, e):
        """Validar formato de fecha dd/mm/aaaa"""
        valor = self.fecha_field.value
        if valor:
            #verificar formato básico con regex
            if not re.match(r'^\d{2}/\d{2}/\d{4}$', valor):
                self.fecha_field.error_text = "Formato debe ser dd/mm/aaaa"
                self.fecha_field.border_color = "red"
            else:
                try:
                    #verificar que sea una fecha válida
                    fecha_obj = datetime.strptime(valor, '%d/%m/%Y')
                    #verificar que no sea una fecha futura
                    if fecha_obj > datetime.now():
                        self.fecha_field.error_text = "La fecha no puede ser futura"
                        self.fecha_field.border_color = "red"
                    else:
                        self.fecha_field.error_text = None
                        self.fecha_field.border_color = None
                except ValueError:
                    self.fecha_field.error_text = "Fecha inválida"
                    self.fecha_field.border_color = "red"
        else:
            self.fecha_field.error_text = None
            self.fecha_field.border_color = None
        self.app.page.update()
    
    def validar_formulario_completo(self):
        """Validar todos los campos del formulario antes de guardar"""
        #validar nombre
        if not self.nombre_field.value:
            return False, "❌ El campo NOMBRE es obligatorio"
        if self.nombre_field.error_text:
            return False, "❌ El campo NOMBRE tiene un formato inválido"
        
        #validar apellido
        if not self.apellido_field.value:
            return False, "❌ El campo APELLIDO es obligatorio"
        if self.apellido_field.error_text:
            return False, "❌ El campo APELLIDO tiene un formato inválido"
        
        #validar contacto
        if not self.contacto_field.value:
            return False, "❌ El campo CONTACTO es obligatorio"
        if self.contacto_field.error_text:
            return False, "❌ El campo CONTACTO tiene un formato inválido"
        
        #validar dirección (OBLIGATORIO)
        if not self.direccion_field.value or self.direccion_field.value.strip() == "":
            return False, "❌ El campo DIRECCIÓN es obligatorio"
        if self.direccion_field.error_text:
            return False, "❌ El campo DIRECCIÓN tiene un formato inválido"
        
        #validar email (OBLIGATORIO)
        if not self.email_field.value or self.email_field.value.strip() == "":
            return False, "❌ El campo EMAIL es obligatorio"
        if self.email_field.error_text:
            return False, "❌ El campo EMAIL tiene un formato inválido"
        
        #validar fecha
        if not self.fecha_field.value:
            return False, "❌ El campo FECHA es obligatorio"
        if self.fecha_field.error_text:
            return False, "❌ El campo FECHA tiene un formato inválido"
        
        #validar animal
        if not self.animal_field.value:
            return False, "❌ Debes seleccionar un ANIMAL para adoptar"
        
        return True, "OK"
    
    # MÉTODOS EXISTENTES (se mantienen igual)
    def _get_current_date(self):
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
    
    def mostrar_error(self, mensaje):
        """Mostrar mensaje de error en el formulario"""
        self.mensaje_error.content.value = mensaje
        self.mensaje_error.visible = True
        self.mensaje_exito.visible = False
        self.app.page.update()
    
    def mostrar_exito(self, mensaje):
        """Mostrar mensaje de éxito en el formulario"""
        self.mensaje_exito.content.value = mensaje
        self.mensaje_exito.visible = True
        self.mensaje_error.visible = False
        self.app.page.update()
    
    # NUEVO: Método para refrescar la vista completa
    def refresh_vista(self, e=None):
        """Recargar la vista completa para mostrar cambios actualizados"""
        # Mostrar mensaje de carga
        self.app.show_snackbar("🔄 Actualizando vista...", "#2196F3")
        
        # Recargar la vista de adopciones
        self.app.show_view("adopciones")
    
    # NUEVOS MÉTODOS PARA LA LISTA DE ADOPTANTES
    def cargar_adoptantes(self):
        """Cargar la lista de adoptantes desde la base de datos"""
        try:
            adoptantes = self.db.execute_query("""
                SELECT a.id, a.nombre, a.apellido, a.contacto, a.email, a.direccion, 
                       a.fecha_adopcion, an.nombre as nombre_animal
                FROM adoptantes a
                LEFT JOIN animales an ON a.animal_id = an.id
                ORDER BY a.fecha_adopcion DESC
            """)
            
            self.tabla_adoptantes.rows.clear()
            
            if adoptantes:
                for adoptante in adoptantes:
                    btn_editar = ft.IconButton(
                        ft.Icons.EDIT, 
                        icon_color=COLORS["primary"],
                        tooltip="Editar adoptante",
                        data=adoptante[0],
                        on_click=self.editar_adoptante_click
                    )
                    
                    btn_eliminar = ft.IconButton(
                        ft.Icons.DELETE, 
                        icon_color="#F44336",
                        tooltip="Eliminar adoptante",
                        data=adoptante[0],
                        on_click=self.eliminar_adoptante_click
                    )
                    
                    self.tabla_adoptantes.rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(adoptante[1])),  # Nombre
                            ft.DataCell(ft.Text(adoptante[2])),  # Apellido
                            ft.DataCell(ft.Text(adoptante[3])),  # Contacto
                            ft.DataCell(ft.Text(adoptante[4])),  # Email
                            ft.DataCell(ft.Text(adoptante[5])),  # Dirección
                            ft.DataCell(ft.Text(adoptante[6])),  # Fecha Adopción
                            ft.DataCell(ft.Text(adoptante[7])),  # Nombre Animal
                            ft.DataCell(ft.Row([btn_editar, btn_eliminar])),  # Operaciones
                        ])
                    )
            else:
                self.tabla_adoptantes.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text("No hay adoptantes registrados", italic=True)),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ])
                )
                
            self.app.page.update()
            
        except Exception as e:
            self.app.show_snackbar("Error al cargar los adoptantes", "#F44336")
    
    def editar_adoptante_click(self, e):
        """Manejar clic en botón editar"""
        adoptante_id = e.control.data
        self.editar_adoptante(adoptante_id)
    
    def eliminar_adoptante_click(self, e):
        """Manejar clic en botón eliminar"""
        adoptante_id = e.control.data
        self.eliminar_adoptante(adoptante_id)
    
    def editar_adoptante(self, adoptante_id):
        """Cargar datos del adoptante para editar"""
        try:
            adoptante_data = self.db.execute_query("""
                SELECT a.*, an.id as animal_id 
                FROM adoptantes a 
                LEFT JOIN animales an ON a.animal_id = an.id 
                WHERE a.id = ?
            """, (adoptante_id,))
            
            if adoptante_data:
                adoptante = adoptante_data[0]
                
                # Llenar el formulario con los datos del adoptante
                self.nombre_field.value = adoptante[1]  # nombre
                self.apellido_field.value = adoptante[2]  # apellido
                self.contacto_field.value = adoptante[3]  # contacto
                self.email_field.value = adoptante[4]  # email
                self.direccion_field.value = adoptante[5]  # dirección
                self.fecha_field.value = adoptante[6]  # fecha_adopcion
                
                # Cargar animales incluyendo el actual
                self.cargar_animales_para_edicion(adoptante[7])  # animal_id
                
                self.edit_id = adoptante_id
                
                # Mostrar mensaje en el formulario (NO snackbar)
                self.mostrar_exito("📝 MODO EDICIÓN ACTIVADO - Modifica los datos y guarda los cambios")
                
        except Exception as ex:
            self.mostrar_error(f"❌ Error al cargar datos: {str(ex)}")
    
    def cargar_animales_para_edicion(self, animal_id_actual):
        """Cargar animales incluyendo el animal actual del adoptante"""
        # Animales en adopción + el animal actual (que ya está adoptado)
        animales = self.db.execute_query("""
            SELECT id, nombre, especie, edad, estado 
            FROM animales 
            WHERE estado = 'En adopción' OR id = ?
        """, (animal_id_actual,))
        
        self.animal_field.options.clear()
        
        for animal in animales:
            estado_texto = " (Adoptado)" if animal[4] == "Adoptado" else ""
            self.animal_field.options.append(
                ft.dropdown.Option(
                    key=str(animal[0]),
                    text=f"🐕 {animal[1]} - {animal[2]} ({animal[3]}){estado_texto}" if animal[2] == "Perro" else f"🐈 {animal[1]} - {animal[2]} ({animal[3]}){estado_texto}"
                )
            )
        
        # Establecer el animal actual
        self.animal_field.value = str(animal_id_actual)
        self.app.page.update()
    
    def eliminar_adoptante(self, adoptante_id):
        """Eliminar adoptante y liberar el animal"""
        try:
            # Obtener información del adoptante y su animal
            adoptante_data = self.db.execute_query("""
                SELECT a.nombre, a.apellido, a.animal_id, an.nombre as nombre_animal 
                FROM adoptantes a 
                LEFT JOIN animales an ON a.animal_id = an.id 
                WHERE a.id = ?
            """, (adoptante_id,))
            
            if not adoptante_data:
                self.mostrar_error("❌ Adoptante no encontrado")
                return
            
            nombre_adoptante = f"{adoptante_data[0][0]} {adoptante_data[0][1]}"
            animal_id = adoptante_data[0][2]
            nombre_animal = adoptante_data[0][3]
            
            # Eliminar el adoptante
            result = self.db.execute_query("DELETE FROM adoptantes WHERE id = ?", (adoptante_id,))
            
            if result is not None and result > 0:
                # Liberar el animal (cambiar estado a "En adopción")
                self.db.execute_query(
                    "UPDATE animales SET estado = 'En adopción' WHERE id = ?",
                    (animal_id,)
                )
                
                # Mostrar mensaje de éxito EN EL FORMULARIO
                self.mostrar_exito(f"✅ ADOPTANTE '{nombre_adoptante.upper()}' ELIMINADO - '{nombre_animal}' DISPONIBLE PARA ADOPCIÓN")
                
                # Mostrar mensaje para usar refresh
                self.app.show_snackbar("💡 Usa el botón '🔄 Actualizar Vista' para ver los cambios", "#2196F3")
                
            else:
                self.mostrar_error("❌ Error al eliminar el adoptante")
                
        except Exception as e:
            self.mostrar_error(f"❌ Error: {str(e)}")
    
    def guardar_adopcion(self, e):
        #ocultar mensajes anteriores
        self.mensaje_error.visible = False
        self.mensaje_exito.visible = False
        self.app.page.update()
        
        #validar todos los campos
        es_valido, mensaje_error = self.validar_formulario_completo()
        if not es_valido:
            self.mostrar_error(mensaje_error)
            return
        
        try:
            #obtener información del animal para el mensaje
            animal_data = self.db.execute_query(
                "SELECT nombre FROM animales WHERE id = ?", 
                (int(self.animal_field.value),)
            )
            nombre_animal = animal_data[0][0] if animal_data else "el animalito"
            
            if self.edit_id:
                # ACTUALIZAR ADOPTANTE EXISTENTE
                # Obtener el animal anterior
                adoptante_anterior = self.db.execute_query(
                    "SELECT animal_id FROM adoptantes WHERE id = ?", 
                    (self.edit_id,)
                )
                
                animal_id_anterior = adoptante_anterior[0][0] if adoptante_anterior else None
                animal_id_nuevo = int(self.animal_field.value)
                
                # Actualizar adoptante
                self.db.execute_query(
                    """UPDATE adoptantes 
                    SET nombre=?, apellido=?, contacto=?, direccion=?, email=?, fecha_adopcion=?, animal_id=?
                    WHERE id=?""",
                    (self.nombre_field.value, self.apellido_field.value, self.contacto_field.value, 
                     self.direccion_field.value, self.email_field.value, self.fecha_field.value, 
                     animal_id_nuevo, self.edit_id)
                )
                
                # Manejar cambios de animal
                if animal_id_anterior and animal_id_anterior != animal_id_nuevo:
                    # Liberar el animal anterior
                    self.db.execute_query(
                        "UPDATE animales SET estado = 'En adopción' WHERE id = ?",
                        (animal_id_anterior,)
                    )
                    # Adoptar el nuevo animal
                    self.db.execute_query(
                        "UPDATE animales SET estado = 'Adoptado' WHERE id = ?",
                        (animal_id_nuevo,)
                    )
                
                # MENSAJE DE ÉXITO MEJORADO
                self.mostrar_exito(f"✅ ADOPTANTE ACTUALIZADO CORRECTAMENTE! {nombre_animal.upper()} MANTIENE SU HOGAR 🏠")
                
            else:
                # NUEVO ADOPTANTE
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
                
                #MOSTRAR MENSAJE DE ÉXITO EN EL FORMULARIO - MEJORADO
                self.mostrar_exito(f"✅ ADOPCIÓN REGISTRADA CORRECTAMENTE! {nombre_animal.upper()} TIENE UN NUEVO HOGAR 🏠")
            
            #limpiar formulario PERO mantener el mensaje de éxito
            self.limpiar_campos_sin_mensajes()
            self.cargar_adoptantes()
            
            # Mostrar mensaje para usar refresh
            self.app.show_snackbar("💡 Usa el botón '🔄 Actualizar Vista' para ver los cambios actualizados", "#2196F3")
            
        except Exception as ex:
            self.mostrar_error(f"❌ Error al registrar adopción: {str(ex)}")

    def limpiar_campos_sin_mensajes(self):
        """Limpiar solo los campos sin afectar los mensajes"""
        self.nombre_field.value = ""
        self.nombre_field.error_text = None
        self.nombre_field.border_color = None
        
        self.apellido_field.value = ""
        self.apellido_field.error_text = None
        self.apellido_field.border_color = None
        
        self.contacto_field.value = ""
        self.contacto_field.error_text = None
        self.contacto_field.border_color = None
        
        self.direccion_field.value = ""
        self.direccion_field.error_text = None
        self.direccion_field.border_color = None
        
        self.email_field.value = ""
        self.email_field.error_text = None
        self.email_field.border_color = None
        
        self.fecha_field.value = self._get_current_date()
        self.fecha_field.error_text = None
        self.fecha_field.border_color = None
        
        # CORREGIDO: Limpiar correctamente el dropdown del animal
        self.animal_field.value = None  # Usar None en lugar de string vacío
        # Recargar las opciones para asegurar que se muestre el hint_text
        self.cargar_animales_adopcion()
        
        self.edit_id = None
        
        #NO ocultar mensajes aquí
        if hasattr(self.app, 'page'):
            self.app.page.update()
    
    def limpiar_formulario(self, e=None):
        """Limpiar formulario completamente"""
        self.limpiar_campos_sin_mensajes()
        #ocultar mensajes al limpiar
        self.mensaje_error.visible = False
        self.mensaje_exito.visible = False
        self.app.page.update()