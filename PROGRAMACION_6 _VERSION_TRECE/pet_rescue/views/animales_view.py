#CAMBIOS:

#1. AGREGADO: Campo para subir imágenes de animalitos: creé una nueva carpeta en mi carpeta del
#proyecto general llamado img para almacenar la carpeta "animales" donde irán las imágenes de
#las cédulas de los animalitos en vista animales_view.py (donde el admin cargará las imágenes
#al ir guardando o editando ciertos datos que se requieran).

#2. Indicador visual en tabla (✅ verde con imagen, ❌ rojo sin imagen).

#3. Gestión automática de imágenes en carpeta img/animales/

#4. "✓" verde en negrita cuando hay imagen

#5. "⚠️" naranja si archivo de imagen no existe

#6. Mejor ajuste de imagen en contenedor

#7. Placeholder automático con Pillow

#8. Imagen se mantiene al editar sin cambios

#9. Validaciones mejoradas para todos los campos

#10. Eliminación segura de imágenes al borrar animal 

import flet as ft
import re
import os
import shutil
from datetime import datetime
from styles.colors import COLORS, crear_header, crear_card

class AnimalesView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.edit_id = None
        self.mensaje_error = None
        self.img_folder = "img/animales"
        
        #se crea carpeta si no existe
        os.makedirs(self.img_folder, exist_ok=True)
        
    def build(self):
        #FilePicker para subir imágenes
        self.file_picker = ft.FilePicker(on_result=self._subir_imagen)
        self.app.page.overlay.append(self.file_picker)
        
        #campos del formulario con validaciones
        self.nombre_field = ft.TextField(
            label="Nombre", 
            expand=True,
            on_change=self.validar_nombre
        )
        
        self.especie_field = ft.Dropdown(
            label="Especie",
            options=[
                ft.dropdown.Option("Perro"),
                ft.dropdown.Option("Gato"),
                ft.dropdown.Option("Otro")
            ],
            expand=True
        )
        
        self.edad_field = ft.TextField(
            label="Edad (ej: 2 años, 8 meses)", 
            expand=True,
            on_change=self.validar_edad
        )
        
        self.fecha_field = ft.TextField(
            label="Fecha de rescate (dd/mm/aaaa)", 
            expand=True,
            on_change=self.validar_fecha
        )
        
        #estado field - opciones básicas para nuevo registro
        self.estado_field = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("En refugio"),
                ft.dropdown.Option("En adopción"), 
            ],
            expand=True
        )
        
        self.vacunas_field = ft.TextField(
            label="Vacunas *", 
            expand=True, 
            multiline=True,
            on_change=self.validar_vacunas
        )
        
        self.descripcion_field = ft.TextField(
            label="Descripción *", 
            expand=True, 
            multiline=True,
            on_change=self.validar_descripcion
        )
        
        #Preview de imagen - MEJORADO: Contenedor con mejor ajuste
        self.img_preview = ft.Image(
            src="img/placeholder.png",
            width=200,
            height=150,
            fit=ft.ImageFit.COVER,
            border_radius=8
        )
        
        self.current_image_path = None
        
        #contenedor para mensajes de error
        self.mensaje_error = ft.Container(
            content=ft.Text("", color="white", weight=ft.FontWeight.BOLD, size=14),
            bgcolor="#F44336",
            padding=10,
            border_radius=5,
            visible=False,
            margin=ft.margin.only(bottom=10)
        )
        
        #contenedor para mensajes de éxito
        self.mensaje_exito = ft.Container(
            content=ft.Text("", color="white", weight=ft.FontWeight.BOLD, size=16),
            bgcolor="#4CAF50",
            padding=15,
            border_radius=8,
            visible=False,
            margin=ft.margin.only(bottom=10),
            alignment=ft.alignment.center
        )
        
        #botones
        btn_guardar = ft.ElevatedButton(
            "💾 Guardar", 
            on_click=self.guardar_animal,
            bgcolor=COLORS["primary"],
            color="white"
        )
        
        btn_limpiar = ft.ElevatedButton(
            "🔄 Limpiar", 
            on_click=self.limpiar_formulario,
            bgcolor=COLORS["secondary"],
            color="white"
        )
        
        #botón de refresh
        btn_refresh = ft.ElevatedButton(
            "🔄 Actualizar Vista",
            on_click=self.refresh_vista,
            bgcolor=COLORS["primary"],
            color="white",
            icon=ft.Icons.REFRESH
        )
        
        #tabla de animales - AGREGADAS COLUMNAS DE VACUNAS, DESCRIPCIÓN Y IMAGEN
        self.tabla_animales = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Especie")),
                ft.DataColumn(ft.Text("Edad")),
                ft.DataColumn(ft.Text("Fecha Rescate")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Vacunas")),  #NUEVA COLUMNA
                ft.DataColumn(ft.Text("Descripción")),  #NUEVA COLUMNA
                ft.DataColumn(ft.Text("Imagen")),  #NUEVA COLUMNA PARA IMAGEN
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
                            ft.Text("* Campos obligatorios", size=12, color="gray", italic=True),
                            #mensaje de éxito
                            self.mensaje_exito,
                            #mensaje de error
                            self.mensaje_error,
                            
                            #primera fila: datos básicos
                            ft.Row([self.nombre_field, self.especie_field, self.edad_field]),
                            ft.Row([self.fecha_field, self.estado_field]),
                            
                            #segunda fila: imagen y campos grandes
                            ft.Row([
                                #columna izquierda: imagen - MEJORADO: Contenedor flexible
                                ft.Column([
                                    ft.Text("🖼️ Imagen del Animal", size=14, weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=self.img_preview,
                                        alignment=ft.alignment.center,
                                        padding=10,
                                        bgcolor="#f8f9fa",
                                        border_radius=10,
                                        border=ft.border.all(2, COLORS["secondary"]),
                                        width=220,  #Ancho fijo para el contenedor
                                        height=170  #Alto fijo para el contenedor
                                    ),
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "📁 Subir Imagen",
                                            on_click=lambda _: self.file_picker.pick_files(
                                                allow_multiple=False,
                                                allowed_extensions=["jpg", "jpeg", "png", "gif"]
                                            ),
                                            icon=ft.Icons.UPLOAD_FILE,
                                            width=120
                                        ),
                                        ft.ElevatedButton(
                                            "Quitar",
                                            on_click=self._quitar_imagen,
                                            icon=ft.Icons.DELETE,
                                            bgcolor="#F44336",
                                            color="white",
                                            width=100
                                        )
                                    ], alignment=ft.MainAxisAlignment.CENTER)
                                ], expand=1),
                                
                                #columna derecha: vacunas y descripción
                                ft.Column([
                                    self.vacunas_field,
                                    ft.Container(height=10),
                                    self.descripcion_field
                                ], expand=2)
                            ]),
                            
                            #agregué el botón de refresh al lado de limpiar
                            ft.Row([
                                btn_guardar,
                                btn_limpiar,
                                btn_refresh
                            ])
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
    
    def _subir_imagen(self, e: ft.FilePickerResultEvent):
        """Manejar subida de imagen"""
        if e.files:
            file = e.files[0]
            
            try:
                #generar nombre único para la imagen
                import time
                timestamp = int(time.time())
                file_extension = file.name.split('.')[-1].lower()
                
                #nombre basado en ID o 'new'
                base_name = f"animal_{self.edit_id or 'new'}_{timestamp}"
                filename = f"{base_name}.{file_extension}"
                file_path = os.path.join(self.img_folder, filename)
                
                #copiar archivo
                shutil.copy(file.path, file_path)
                
                #actualizar preview - MEJORADO: Asegurar que la imagen se vea bien
                self.img_preview.src = file_path
                self.img_preview.fit = ft.ImageFit.COVER  # Asegurar que cubra el espacio
                self.current_image_path = filename  # Solo guardamos el nombre del archivo
                
                #forzar actualización de la página
                self.img_preview.update()
                self.app.page.update()
                self.app.show_snackbar("✅ Imagen subida correctamente")
                
            except Exception as ex:
                self.app.show_snackbar(f"❌ Error al subir imagen: {str(ex)}", "#F44336")
    
    def _quitar_imagen(self, e):
        """Quitar imagen del formulario (solo visualmente)"""
        self.img_preview.src = "img/placeholder.png"
        self.img_preview.fit = ft.ImageFit.COVER
        
        #MODIFICADO: Solo resetear current_image_path si NO estamos editando
        #si estamos editando, mantener la referencia pero mostrar placeholder
        if not self.edit_id:
            self.current_image_path = None
        #si estamos editando, current_image_path se establecerá a None temporalmente
        #pero en guardar_animal recuperaremos la imagen original de la base de datos
        
        self.img_preview.update()
        self.app.page.update()
        self.app.show_snackbar("Imagen removida del formulario (no de la base de datos)")
    
    def refresh_vista(self, e=None):
        """Recargar la vista completa para mostrar cambios actualizados y limpiar filtros"""
        #mostrar mensaje de carga
        self.app.show_snackbar("🔄 Actualizando vista...", "#2196F3")
        
        #limpiar los combo boxes de filtro
        self.filtro_estado.value = None
        
        #recargar la vista de animales
        self.app.show_view("animales")
    
    #MÉTODOS DE VALIDACIÓN
    def validar_nombre(self, e):
        """Validar que el nombre solo contenga letras y espacios"""
        valor = self.nombre_field.value
        if valor:
            #permitir solo letras, espacios y algunos caracteres especiales comunes en nombres
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\.]+$', valor):
                self.nombre_field.error_text = "Solo se permiten letras, espacios y guiones"
                self.nombre_field.border_color = "red"
            else:
                self.nombre_field.error_text = None
                self.nombre_field.border_color = None
        else:
            self.nombre_field.error_text = None
            self.nombre_field.border_color = None
        self.app.page.update()
    
    def validar_edad(self, e):
        """Validar que la edad contenga letras y números pero no guiones ni caracteres especiales"""
        valor = self.edad_field.value
        if valor:
            #permitir letras, números, espacios y acentos, pero no guiones ni caracteres especiales
            if re.search(r'[-!@#$%^&*()_+=|<>?{}\[\]~;/]', valor):
                self.edad_field.error_text = "No se permiten guiones ni caracteres especiales"
                self.edad_field.border_color = "red"
            elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s]+$', valor):
                self.edad_field.error_text = "Solo se permiten letras, números y espacios"
                self.edad_field.border_color = "red"
            else:
                #validar longitud máxima
                if len(valor) > 20:
                    self.edad_field.error_text = "Máximo 20 caracteres"
                    self.edad_field.border_color = "red"
                else:
                    self.edad_field.error_text = None
                    self.edad_field.border_color = None
        else:
            self.edad_field.error_text = None
            self.edad_field.border_color = None
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
    
    def validar_vacunas(self, e):
        """Validar campo de vacunas - obligatorio y solo caracteres permitidos"""
        valor = self.vacunas_field.value
        if not valor or valor.strip() == "":
            self.vacunas_field.error_text = "❌ Este campo es obligatorio"
            self.vacunas_field.border_color = "red"
        else:
            #permitir letras, números, espacios, acentos, comas, puntos y paréntesis
            if re.search(r'[!@#$%^&*_+=|<>?{}\[\]~;/\\]', valor):
                self.vacunas_field.error_text = "No se permiten caracteres especiales como !@#$%^&*_+= etc."
                self.vacunas_field.border_color = "red"
            elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\.,\(\)\-:]+$', valor):
                self.vacunas_field.error_text = "Solo se permiten letras, números, espacios, comas, puntos y guiones"
                self.vacunas_field.border_color = "red"
            else:
                #validar longitud máxima
                if len(valor) > 500:
                    self.vacunas_field.error_text = f"Máximo 500 caracteres ({len(valor)}/500)"
                    self.vacunas_field.border_color = "red"
                else:
                    self.vacunas_field.error_text = None
                    self.vacunas_field.border_color = None
        self.app.page.update()
    
    def validar_descripcion(self, e):
        """Validar campo de descripción - obligatorio y solo caracteres permitidos"""
        valor = self.descripcion_field.value
        if not valor or valor.strip() == "":
            self.descripcion_field.error_text = "❌ Este campo es obligatorio"
            self.descripcion_field.border_color = "red"
        else:
            #permitir letras, números, espacios, acentos, comas, puntos y paréntesis
            if re.search(r'[!@#$%^&*_+=|<>?{}\[\]~;/\\]', valor):
                self.descripcion_field.error_text = "No se permiten caracteres especiales como !@#$%^&*_+= etc."
                self.descripcion_field.border_color = "red"
            elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\.,\(\)\-:]+$', valor):
                self.descripcion_field.error_text = "Solo se permiten letras, números, espacios, comas, puntos y guiones"
                self.descripcion_field.border_color = "red"
            else:
                #validar longitud máxima
                if len(valor) > 1000:
                    self.descripcion_field.error_text = f"Máximo 1000 caracteres ({len(valor)}/1000)"
                    self.descripcion_field.border_color = "red"
                else:
                    self.descripcion_field.error_text = None
                    self.descripcion_field.border_color = None
        self.app.page.update()
    
    def validar_formulario_completo(self):
        """Validar todos los campos del formulario antes de guardar"""
        #validar nombre
        if not self.nombre_field.value:
            return False, "❌ El campo NOMBRE es obligatorio"
        
        if self.nombre_field.error_text:
            return False, "❌ El campo NOMBRE tiene un formato inválido"
        
        #validar especie
        if not self.especie_field.value:
            return False, "❌ Debes seleccionar una ESPECIE"
        
        #validar edad
        if not self.edad_field.value:
            return False, "❌ El campo EDAD es obligatorio"
        
        if self.edad_field.error_text:
            return False, "❌ El campo EDAD tiene un formato inválido"
        
        #validar fecha
        if not self.fecha_field.value:
            return False, "❌ El campo FECHA DE RESCATE es obligatorio"
        
        if self.fecha_field.error_text:
            return False, "❌ El campo FECHA tiene un formato inválido"
        
        #validar estado
        if not self.estado_field.value:
            return False, "❌ Debes seleccionar un ESTADO"
        
        #validar vacunas (OBLIGATORIO)
        if not self.vacunas_field.value or self.vacunas_field.value.strip() == "":
            return False, "❌ El campo VACUNAS es obligatorio"
        
        if self.vacunas_field.error_text:
            return False, "❌ El campo VACUNAS tiene un formato inválido"
        
        #validar descripción (OBLIGATORIO)
        if not self.descripcion_field.value or self.descripcion_field.value.strip() == "":
            return False, "❌ El campo DESCRIPCIÓN es obligatorio"
        
        if self.descripcion_field.error_text:
            return False, "❌ El campo DESCRIPCIÓN tiene un formato inválido"
        
        return True, "OK"
    
    def mostrar_exito(self, mensaje):
        """Mostrar mensaje de éxito en el formulario"""
        self.mensaje_exito.content.value = mensaje
        self.mensaje_exito.visible = True
        self.mensaje_error.visible = False
        self.app.page.update()
    
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
                    btn_editar = ft.IconButton(
                        ft.Icons.EDIT, 
                        icon_color=COLORS["primary"],
                        tooltip="Editar animal",
                        data=animal[0],
                        on_click=self.editar_animal_click
                    )
                    
                    #botón eliminar en gris si estado es "Adoptado"
                    estado_animal = animal[5]  # posición 5: estado
                    puede_eliminar = estado_animal != "Adoptado"
                    
                    btn_eliminar = ft.IconButton(
                        ft.Icons.DELETE, 
                        icon_color="#F44336" if puede_eliminar else "#CCCCCC",
                        tooltip="Eliminar animal" if puede_eliminar else "No se puede eliminar un animal adoptado",
                        data=animal[0],
                        on_click=self.eliminar_animal_click,
                        disabled=not puede_eliminar
                    )
                    
                    #MEJORADO: Buscar imagen en ambas columnas posibles
                    tiene_imagen = ft.Text("❌", color="#F44336")  # Por defecto X roja
                    
                    #buscar en imagen_url (columna 9) primero
                    imagen_url = None
                    if len(animal) > 9 and animal[9]:
                        imagen_url = animal[9]
                    #si no hay en imagen_url, buscar en imagen (columna 8)
                    elif len(animal) > 8 and animal[8]:
                        imagen_url = animal[8]
                    
                    if imagen_url and imagen_url != "":
                        #verificar si el archivo realmente existe
                        img_path = os.path.join(self.img_folder, imagen_url)
                        if os.path.exists(img_path):
                            tiene_imagen = ft.Text("✅", color="#4CAF50", weight=ft.FontWeight.BOLD)  # Verde y en negrita
                        else:
                            tiene_imagen = ft.Text("⚠️", color="#FF9800", tooltip="Archivo no encontrado")  # Naranja con advertencia
                    
                    self.tabla_animales.rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(animal[1])),  #Nombre
                            ft.DataCell(ft.Text(animal[2])),  #Especie
                            ft.DataCell(ft.Text(animal[3])),  #Edad
                            ft.DataCell(ft.Text(animal[4])),  #Fecha Rescate
                            ft.DataCell(ft.Text(estado_animal)),  #Estado
                            ft.DataCell(ft.Text(animal[6] or "")),  #Vacunas
                            ft.DataCell(ft.Text(animal[7] or "")),  #Descripción
                            ft.DataCell(tiene_imagen),  #Imagen - ahora con color
                            ft.DataCell(ft.Row([btn_editar, btn_eliminar])),  #Operaciones
                        ])
                    )
            else:
                self.tabla_animales.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text("No hay animales registrados", italic=True)),
                        ft.DataCell(ft.Text("")),
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
            print(f"Error al cargar animales: {e}")
            import traceback
            traceback.print_exc()
            self.app.show_snackbar(f"Error al cargar los animales: {str(e)}", "#F44336")
    
    def editar_animal_click(self, e):
        animal_id = e.control.data
        self.editar_animal(animal_id)
    
    def eliminar_animal_click(self, e):
        animal_id = e.control.data
        self.eliminar_animal(animal_id)
    
    def eliminar_animal(self, animal_id):
        try:
            animal_data = self.db.execute_query("SELECT nombre, estado, imagen_url FROM animales WHERE id = ?", (animal_id,))
            
            if not animal_data:
                self.app.show_snackbar("❌ Animal no encontrado", "#F44336")
                return
                
            nombre_animal = animal_data[0][0]
            estado_animal = animal_data[0][1]
            #buscar en ambas columnas posibles
            imagen_url = None
            if len(animal_data[0]) > 2 and animal_data[0][2]:
                imagen_url = animal_data[0][2]  #imagen_url
            elif len(animal_data[0]) > 3 and animal_data[0][3]:
                imagen_url = animal_data[0][3]  #imagen (si existe)
            
            if estado_animal == "Adoptado":
                self.app.show_snackbar("❌ No se puede eliminar un animal adoptado", "#F44336")
                return
            
            #eliminar imagen si existe
            if imagen_url:
                img_path = os.path.join(self.img_folder, imagen_url)
                if os.path.exists(img_path):
                    os.remove(img_path)
            
            result = self.db.execute_query("DELETE FROM animales WHERE id = ?", (animal_id,))
            
            if result is not None and result > 0:
                self.mostrar_exito(f"✅ '{nombre_animal}' ELIMINADO CORRECTAMENTE")
                self.cargar_animales()
                self.app.show_snackbar("💡 Usa '🔄 Actualizar Vista' para ver todos los cambios", "#2196F3")
            else:
                self.app.show_snackbar("❌ Error al eliminar el animal", "#F44336")
                
        except Exception as e:
            self.app.show_snackbar(f"❌ Error: {str(e)}", "#F44336")
    
    def guardar_animal(self, e):
        """Guardar o actualizar animal"""
        #ocultar mensajes al intentar guardar de nuevo
        self.mensaje_error.visible = False
        self.mensaje_exito.visible = False
        self.app.page.update()
        
        #validar todos los campos
        es_valido, mensaje_error = self.validar_formulario_completo()
        if not es_valido:
            self.mostrar_error(mensaje_error)
            return
        
        try:
            #preparar fecha actual para fecha_ingreso
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            
            if self.edit_id:
                #MODIFICADO: Si estamos editando, obtener la imagen actual primero
                imagen_a_guardar = self.current_image_path
                
                #si no hay nueva imagen (current_image_path es None), obtener la imagen existente
                if imagen_a_guardar is None:
                    animal_data = self.db.execute_query(
                        "SELECT imagen_url, imagen FROM animales WHERE id = ?", 
                        (self.edit_id,)
                    )
                    if animal_data:
                        #buscar en ambas columnas posibles
                        if animal_data[0][0]:  #imagen_url
                            imagen_a_guardar = animal_data[0][0]
                        elif len(animal_data[0]) > 1 and animal_data[0][1]:  #imagen
                            imagen_a_guardar = animal_data[0][1]
                
                #si hay una nueva imagen, eliminar la anterior si existe
                if self.current_image_path and self.current_image_path != imagen_a_guardar:
                    animal_data = self.db.execute_query(
                        "SELECT imagen_url, imagen FROM animales WHERE id = ?", 
                        (self.edit_id,)
                    )
                    if animal_data:
                        imagen_anterior = None
                        if animal_data[0][0]:  #imagen_url
                            imagen_anterior = animal_data[0][0]
                        elif len(animal_data[0]) > 1 and animal_data[0][1]:  #imagen
                            imagen_anterior = animal_data[0][1]
                        
                        if imagen_anterior and imagen_anterior != self.current_image_path:
                            old_img_path = os.path.join(self.img_folder, imagen_anterior)
                            if os.path.exists(old_img_path):
                                os.remove(old_img_path)
                
                #UPDATE con imagen_url
                result = self.db.execute_query(
                    """UPDATE animales SET nombre=?, especie=?, edad=?, fecha_rescate=?, estado=?, 
                    vacunas=?, descripcion=?, imagen_url=? WHERE id=?""",
                    (self.nombre_field.value, self.especie_field.value, self.edad_field.value, 
                    self.fecha_field.value, self.estado_field.value, self.vacunas_field.value, 
                    self.descripcion_field.value, imagen_a_guardar, self.edit_id)
                )
                if result is not None:
                    self.mostrar_exito("✅ ANIMALITO ACTUALIZADO CORRECTAMENTE")
                    self.app.show_snackbar("✅ Animal actualizado correctamente", "#4CAF50")
                    self.limpiar_campos_sin_mensajes()
                    self.cargar_animales()
                    self.app.show_snackbar("💡 Usa '🔄 Actualizar Vista' para ver todos los cambios", "#2196F3")
                else:
                    self.app.show_snackbar("❌ Error al actualizar el animal", "#F44336")
            else:
                #INSERT para nuevo animal
                result = self.db.execute_query(
                    """INSERT INTO animales 
                    (nombre, especie, edad, fecha_rescate, estado, vacunas, descripcion, imagen_url, fecha_ingreso) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (self.nombre_field.value, self.especie_field.value, self.edad_field.value, 
                    self.fecha_field.value, self.estado_field.value, self.vacunas_field.value, 
                    self.descripcion_field.value, self.current_image_path, fecha_actual)
                )
                if result is not None:
                    self.mostrar_exito("✅ ANIMALITO REGISTRADO CORRECTAMENTE")
                    self.app.show_snackbar("✅ Animal registrado correctamente", "#4CAF50")
                    self.limpiar_campos_sin_mensajes()
                    self.cargar_animales()
                    self.app.show_snackbar("💡 Usa '🔄 Actualizar Vista' para ver todos los cambios", "#2196F3")
                else:
                    self.app.show_snackbar("❌ Error al registrar el animal", "#F44336")
            
        except Exception as ex:
            self.app.show_snackbar(f"❌ Error: {str(ex)}", "#F44336")
    
    def limpiar_campos_sin_mensajes(self):
        """Limpiar solo los campos sin afectar los mensajes"""
        self.nombre_field.value = ""
        self.nombre_field.error_text = None
        self.nombre_field.border_color = None
        
        self.especie_field.value = ""
        
        self.edad_field.value = ""
        self.edad_field.error_text = None
        self.edad_field.border_color = None
        
        self.fecha_field.value = ""
        self.fecha_field.error_text = None
        self.fecha_field.border_color = None
        
        #al limpiar, restablecer las opciones básicas del estado (sin "Adoptado")
        self.estado_field.options = [
            ft.dropdown.Option("En refugio"),
            ft.dropdown.Option("En adopción"), 
        ]
        self.estado_field.value = ""
        
        self.vacunas_field.value = ""
        self.vacunas_field.error_text = None
        self.vacunas_field.border_color = None
        
        self.descripcion_field.value = ""
        self.descripcion_field.error_text = None
        self.descripcion_field.border_color = None
        
        #limpiar imagen
        self.img_preview.src = "img/placeholder.png"
        self.img_preview.fit = ft.ImageFit.COVER
        self.current_image_path = None
        
        self.edit_id = None
        self.app.page.update()
    
    def mostrar_error(self, mensaje):
        """Mostrar mensaje de error en el formulario"""
        self.mensaje_error.content.value = mensaje
        self.mensaje_error.visible = True
        self.mensaje_exito.visible = False
        self.app.page.update()
    
    def editar_animal(self, id):
        try:
            animales = self.db.execute_query("SELECT * FROM animales WHERE id = ?", (id,))
            if animales:
                animal = animales[0]
                self.nombre_field.value = animal[1]
                self.especie_field.value = animal[2]
                self.edad_field.value = animal[3]
                self.fecha_field.value = animal[4]
                
                #configurar opciones del estado según si ya está adoptado
                estado_actual = animal[5]
                
                if estado_actual == "Adoptado":
                    self.estado_field.options = [
                        ft.dropdown.Option("En refugio"),
                        ft.dropdown.Option("En adopción"),
                        ft.dropdown.Option("Adoptado")
                    ]
                else:
                    self.estado_field.options = [
                        ft.dropdown.Option("En refugio"),
                        ft.dropdown.Option("En adopción"),
                    ]
                
                self.estado_field.value = estado_actual
                self.vacunas_field.value = animal[6] or ""
                self.descripcion_field.value = animal[7] or ""
                
                #MEJORADO: Buscar imagen en ambas columnas
                imagen_url = None
                if len(animal) > 9 and animal[9]:
                    imagen_url = animal[9]  #imagen_url (columna 9)
                elif len(animal) > 8 and animal[8]:
                    imagen_url = animal[8]  #imagen (columna 8)
                
                if imagen_url:
                    self.current_image_path = imagen_url  #GUARDAR LA REFERENCIA
                    img_path = os.path.join(self.img_folder, imagen_url)
                    if os.path.exists(img_path):
                        self.img_preview.src = img_path
                        self.img_preview.fit = ft.ImageFit.COVER
                    else:
                        self.img_preview.src = "img/placeholder.png"
                        #MODIFICADO: Mantener current_image_path aunque el archivo no exista
                        #para que se guarde en la base de datos
                else:
                    self.img_preview.src = "img/placeholder.png"
                    self.current_image_path = None
                
                self.edit_id = id
                #ocultar mensajes al editar
                self.mensaje_error.visible = False
                self.mensaje_exito.visible = False
                self.app.show_snackbar("📝 Modo edición activado", "#2196F3")
                self.app.page.update()
                
        except Exception as ex:
            self.app.show_snackbar(f"❌ Error al cargar datos: {str(ex)}", "#F44336")
    
    def limpiar_formulario(self, e=None):
        """Limpiar formulario completamente"""
        self.limpiar_campos_sin_mensajes()
        #ocultar mensajes al limpiar
        self.mensaje_error.visible = False
        self.mensaje_exito.visible = False
        self.app.page.update()