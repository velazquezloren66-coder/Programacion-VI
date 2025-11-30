#CAMBIOS:
#1.	Se validó que se completen los datos obligatoriamente en todos los campos.

#2.	Validación de solo aceptar los tipos de datos que correspondan en los inputs (solo int,
#solo str, o solo ambos y asi) en vista Donaciones.

#3.	Contar con un refresh (Actualizar vista) en vista Donaciones.

#4.	Contar con una tabla con todos los registros de las donaciones realizadas en vista Donaciones.

#5.	Que el conteo de dinero recaudado funcione correctamente en vista Donaciones.

#6.	Agregar una columna de descripción en la tabla de Donaciones en vista Donaciones.

#7.	Mensajes de éxito tanto al guardar, eliminar y editar los registros de la tabla de donaciones
#en vista Donaciones.



import flet as ft
import re
from datetime import datetime
from styles.colors import COLORS, crear_header, crear_card

class DonacionesView:
    def __init__(self, app):
        self.app = app
        self.db = app.db
        self.edit_id = None
        self.mensaje_error = None
        self.mensaje_exito = None
        self.mensaje_eliminacion = None  #nuevo mensaje específico para eliminaciones
        
    def build(self):
        #campos del formulario con validaciones
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
            label="Monto (₲) *", #con ₲ porque tratamos con guaranies
            expand=True, 
            visible=False,
            prefix_text="₲",
            on_change=self.validar_monto
        )
        
        self.descripcion_field = ft.TextField(
            label="Descripción (opcional)", 
            expand=True, 
            multiline=True,
            visible=False,
            on_change=self.validar_descripcion
        )
        
        #contenedor para mensaje de error
        self.mensaje_error = ft.Container(
            content=ft.Text("", color="white", weight=ft.FontWeight.BOLD, size=14),
            bgcolor="#F44336",
            padding=10,
            border_radius=5,
            visible=False,
            margin=ft.margin.only(bottom=10)
        )
        
        #contenedor para mensaje de éxito
        self.mensaje_exito = ft.Container(
            content=ft.Text("", color="white", weight=ft.FontWeight.BOLD, size=16),
            bgcolor="#4CAF50",
            padding=15,
            border_radius=8,
            visible=False,
            margin=ft.margin.only(bottom=10),
            alignment=ft.alignment.center
        )
        
        #contenedor para mensaje de eliminación (en la sección de tabla)
        self.mensaje_eliminacion = ft.Container(
            content=ft.Text("", color="white", weight=ft.FontWeight.BOLD, size=14),
            bgcolor="#2196F3",
            padding=10,
            border_radius=5,
            visible=False,
            margin=ft.margin.only(bottom=10),
            alignment=ft.alignment.center
        )
        
        #tabla de donaciones - CON COLUMNA DE DESCRIPCIÓN
        self.tabla_donaciones = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("Contacto")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Operaciones")),
            ],
            rows=[]
        )
        
        #evento para mostrar/ocultar campos según tipo de donación
        self.tipo_donacion.on_change = self.on_tipo_donacion_change
        
        #cargar datos iniciales
        self.cargar_donaciones()
        
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
                            ft.Text("❤️ TODO APORTE AYUDA, ¡DONÁ!", 
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
                            #TÍTULO CON BOTÓN REFRESH AL LADO
                            ft.Row([
                                ft.Text("📋 Registro del Donador", 
                                       size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(expand=True),
                                ft.ElevatedButton(
                                    "🔄 Actualizar Vista",
                                    on_click=self.refresh_vista,
                                    bgcolor=COLORS["primary"],
                                    color="white",
                                    icon=ft.Icons.REFRESH,
                                    height=40
                                )
                            ]),
                            ft.Text("* Campos obligatorios", size=12, color="gray", italic=True),
                            #mensaje de éxito
                            self.mensaje_exito,
                            #mensaje de error
                            self.mensaje_error,
                            ft.Row([self.nombre_field, self.apellido_field]),
                            ft.Row([self.contacto_field, self.tipo_donacion]),
                            self.monto_field,
                            self.descripcion_field,
                            ft.Container(height=20),
                            ft.Row([
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
                    
                    #estadísticas de donaciones
                    self._crear_estadisticas_donaciones(),
                    
                    #tabla de donaciones
                    crear_card(
                        ft.Column([
                            ft.Text("📋 Historial de Donaciones", 
                                   size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("Todas las donaciones registradas", 
                                   size=14, color=COLORS["text"]),
                            ft.Container(height=10),
                            #mensaje de eliminación exitosa - AHORA EN LA SECCIÓN DE TABLA
                            self.mensaje_eliminacion,
                            ft.Container(
                                content=ft.Column([self.tabla_donaciones], scroll=ft.ScrollMode.ALWAYS),
                                height=400,
                            )
                        ])
                    )
                ]),
                padding=20
            )
        ])
    
    #MÉTODOS DE VALIDACIÓN
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
    
    def validar_monto(self, e):
        """Validar que el monto sea un número válido para guaraníes"""
        valor = self.monto_field.value
        if valor:
            #permitir números con puntos como separadores de miles y sin puntos
            #eliminar puntos para validar que sea un número válido
            valor_limpio = valor.replace('.', '')
            
            if not re.match(r'^[\d\.]+$', valor):
                self.monto_field.error_text = "Solo se permiten números y puntos para separadores de miles"
                self.monto_field.border_color = "red"
            else:
                try:
                    #convertir a número (eliminar puntos primero)
                    monto = float(valor_limpio)
                    if monto <= 0:
                        self.monto_field.error_text = "El monto debe ser mayor a 0"
                        self.monto_field.border_color = "red"
                    else:
                        self.monto_field.error_text = None
                        self.monto_field.border_color = None
                except ValueError:
                    self.monto_field.error_text = "Monto inválido"
                    self.monto_field.border_color = "red"
        else:
            self.monto_field.error_text = None
            self.monto_field.border_color = None
        self.app.page.update()
    
    def validar_descripcion(self, e):
        """Validar descripción - solo caracteres permitidos"""
        valor = self.descripcion_field.value
        if valor:
            #permitir letras, números, espacios, acentos, comas, puntos y paréntesis
            if re.search(r'[!@#$%^&*_+=|<>?{}\[\]~;/\\]', valor):
                self.descripcion_field.error_text = "No se permiten caracteres especiales como !@#$%^&*_+= etc."
                self.descripcion_field.border_color = "red"
            elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\.,\(\)\-:]+$', valor):
                self.descripcion_field.error_text = "Solo se permiten letras, números, espacios, comas, puntos y guiones"
                self.descripcion_field.border_color = "red"
            else:
                #validar longitud máxima
                if len(valor) > 500:
                    self.descripcion_field.error_text = f"Máximo 500 caracteres ({len(valor)}/500)"
                    self.descripcion_field.border_color = "red"
                else:
                    self.descripcion_field.error_text = None
                    self.descripcion_field.border_color = None
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
        
        #validar tipo de donación
        if not self.tipo_donacion.value:
            return False, "❌ Debes seleccionar un TIPO DE DONACIÓN"
        
        #validar monto para donaciones en dinero
        if self.tipo_donacion.value == "Dinero":
            if not self.monto_field.value:
                return False, "❌ El campo MONTO es obligatorio para donaciones en dinero"
            if self.monto_field.error_text:
                return False, "❌ El campo MONTO tiene un formato inválido"
        
        #validar descripción
        if self.descripcion_field.error_text:
            return False, "❌ El campo DESCRIPCIÓN tiene un formato inválido"
        
        return True, "OK"
    
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
    
    def mostrar_eliminacion_exitosa(self, mensaje):
        """Mostrar mensaje de eliminación exitosa en la sección de tabla"""
        self.mensaje_eliminacion.content.value = mensaje
        self.mensaje_eliminacion.visible = True
        self.app.page.update()
    
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
    
    def cargar_donaciones(self):
        """Cargar la lista de donaciones desde la base de datos"""
        try:
            donaciones = self.db.execute_query("""
                SELECT id, nombre, apellido, contacto, tipo_donacion, monto, descripcion, fecha_donacion 
                FROM donantes 
                ORDER BY fecha_donacion DESC
            """)
            
            self.tabla_donaciones.rows.clear()
            
            if donaciones:
                for donacion in donaciones:
                    btn_editar = ft.IconButton(
                        ft.Icons.EDIT, 
                        icon_color=COLORS["primary"],
                        tooltip="Editar donación",
                        data=donacion[0],
                        on_click=self.editar_donacion_click
                    )
                    
                    btn_eliminar = ft.IconButton(
                        ft.Icons.DELETE, 
                        icon_color="#F44336",
                        tooltip="Eliminar donación",
                        data=donacion[0],
                        on_click=self.eliminar_donacion_click
                    )
                    
                    #formatear monto con separadores de miles para guaraníes
                    if donacion[5] and donacion[5] > 0:
                        monto_texto = f"₲{donacion[5]:,.0f}".replace(',', '.')
                    else:
                        monto_texto = "N/A"
                    
                    #truncar descripción si es muy larga para la tabla
                    descripcion = donacion[6] or "Sin descripción"
                    if len(descripcion) > 50:
                        descripcion = descripcion[:50] + "..."
                    
                    self.tabla_donaciones.rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(ft.Text(donacion[1])),  #nombre
                            ft.DataCell(ft.Text(donacion[2])),  #apellido
                            ft.DataCell(ft.Text(donacion[3])),  #contacto
                            ft.DataCell(ft.Text(donacion[4])),  #tipo Donación
                            ft.DataCell(ft.Text(monto_texto)),  #monto
                            ft.DataCell(ft.Text(descripcion, tooltip=donacion[6] or "")),  #descripción (con tooltip completo)
                            ft.DataCell(ft.Text(donacion[7])),  #fecha
                            ft.DataCell(ft.Row([btn_editar, btn_eliminar])),  #operaciones
                        ])
                    )
            else:
                self.tabla_donaciones.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text("No hay donaciones registradas", italic=True)),
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
            self.app.show_snackbar("Error al cargar las donaciones", "#F44336")
    
    def editar_donacion_click(self, e):
        """Manejar clic en botón editar"""
        donacion_id = e.control.data
        self.editar_donacion(donacion_id)
    
    def eliminar_donacion_click(self, e):
        """Manejar clic en botón eliminar"""
        donacion_id = e.control.data
        self.eliminar_donacion(donacion_id)
    
    def editar_donacion(self, donacion_id):
        """Cargar datos de la donación para editar"""
        try:
            donacion_data = self.db.execute_query("SELECT * FROM donantes WHERE id = ?", (donacion_id,))
            
            if donacion_data:
                donacion = donacion_data[0]
                
                #llenar el formulario con los datos de la donación
                self.nombre_field.value = donacion[1]  #nombre
                self.apellido_field.value = donacion[2]  #apellido
                self.contacto_field.value = donacion[3]  #contacto
                self.tipo_donacion.value = donacion[4]  #tipo_donacion
                
                #activar campos según tipo de donación
                self.on_tipo_donacion_change(None)
                
                if donacion[5]:  #monto
                    #formatear el monto con separadores de miles para mostrar en el campo
                    monto_formateado = f"{donacion[5]:,.0f}".replace(',', '.')
                    self.monto_field.value = monto_formateado
                
                self.descripcion_field.value = donacion[6] or ""  #descripción
                
                self.edit_id = donacion_id
                
                #mostrar mensaje en el formulario
                self.mostrar_exito("📝 MODO EDICIÓN ACTIVADO - Modifica los datos y guarda los cambios")
                
        except Exception as ex:
            self.mostrar_error(f"❌ Error al cargar datos: {str(ex)}")
    
    def eliminar_donacion(self, donacion_id):
        """Eliminar donación"""
        try:
            #obtener información de la donación
            donacion_data = self.db.execute_query("SELECT nombre, apellido FROM donantes WHERE id = ?", (donacion_id,))
            
            if not donacion_data:
                self.mostrar_error("❌ Donación no encontrada")
                return
            
            nombre_donante = f"{donacion_data[0][0]} {donacion_data[0][1]}"
            
            #eliminar la donación
            result = self.db.execute_query("DELETE FROM donantes WHERE id = ?", (donacion_id,))
            
            if result is not None and result > 0:
                #mostrar mensaje de éxito EN LA SECCIÓN DE TABLA
                self.mostrar_eliminacion_exitosa(f"🗑️ ELIMINADO CON ÉXITO: Donación de {nombre_donante} eliminada correctamente")
                
                #recargar datos
                self.cargar_donaciones()
                
                #ocultar el mensaje después de 5 segundos
                def ocultar_mensaje():
                    import time
                    time.sleep(5)
                    self.mensaje_eliminacion.visible = False
                    self.app.page.update()
                
                import threading
                threading.Thread(target=ocultar_mensaje, daemon=True).start()
                
            else:
                self.mostrar_error("❌ Error al eliminar la donación")
                
        except Exception as e:
            self.mostrar_error(f"❌ Error: {str(e)}")
    
    def guardar_donacion(self, e):
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
            #procesar monto - eliminar puntos para guardar como número
            if self.monto_field.value and self.tipo_donacion.value == "Dinero":
                monto_limpio = self.monto_field.value.replace('.', '')
                monto = float(monto_limpio)
            else:
                monto = 0.0
            
            if self.edit_id:
                #ACTUALIZAR DONACIÓN EXISTENTE
                result = self.db.execute_query(
                    """UPDATE donantes 
                    SET nombre=?, apellido=?, contacto=?, tipo_donacion=?, monto=?, descripcion=?
                    WHERE id=?""",
                    (self.nombre_field.value, self.apellido_field.value, self.contacto_field.value, 
                     self.tipo_donacion.value, monto, self.descripcion_field.value, self.edit_id)
                )
                
                #MENSAJE DE ÉXITO MEJORADO - EDITADO
                mensaje_exito = f"✅ ¡EDITADO CON ÉXITO! Donación de {self.nombre_field.value} {self.apellido_field.value} actualizada correctamente"
                
            else:
                #NUEVA DONACIÓN
                result = self.db.execute_query(
                    """INSERT INTO donantes (nombre, apellido, contacto, tipo_donacion, monto, descripcion, fecha_donacion) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (self.nombre_field.value, self.apellido_field.value, self.contacto_field.value, 
                     self.tipo_donacion.value, monto, self.descripcion_field.value,
                     datetime.now().strftime("%d/%m/%Y"))
                )
                
                #MENSAJE DE ÉXITO MEJORADO - GUARDADO
                mensaje_exito = f"✅ ¡GUARDADO CON ÉXITO! Donación de {self.nombre_field.value} {self.apellido_field.value} registrada correctamente"
            
            #MOSTRAR MENSAJE DE ÉXITO ANTES DE LIMPIAR
            self.mostrar_exito(mensaje_exito)
            
            #limpiar formulario PERO MANTENER EL MENSAJE
            self.limpiar_campos_sin_mensajes()
            
            #recargar datos
            self.cargar_donaciones()
            
            #mostrar también snackbar para mayor visibilidad
            if self.edit_id:
                self.app.show_snackbar("✅ ¡Donación editada con éxito!", "#4CAF50")
            else:
                self.app.show_snackbar("✅ ¡Donación guardada con éxito!", "#4CAF50")
            
        except Exception as ex:
            self.mostrar_error(f"❌ Error al registrar donación: {str(ex)}")
    
    def _crear_estadisticas_donaciones(self):
        try:
            #obtener estadísticas
            total_donaciones = self.db.execute_query("SELECT COUNT(*) FROM donantes")[0][0]
            total_dinero = self.db.execute_query("SELECT SUM(monto) FROM donantes WHERE monto > 0")[0][0] or 0
            
            tipos_donacion = self.db.execute_query(
                "SELECT tipo_donacion, COUNT(*) FROM donantes GROUP BY tipo_donacion"
            )
            
            #formatear el total de dinero con separadores de miles
            total_dinero_formateado = f"₲{total_dinero:,.0f}".replace(',', '.')
            
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
                                ft.Text(total_dinero_formateado, size=20, weight=ft.FontWeight.BOLD),
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
    
    def limpiar_campos_sin_mensajes(self):
        """Limpiar solo los campos del formulario sin afectar los mensajes"""
        self.nombre_field.value = ""
        self.nombre_field.error_text = None
        self.nombre_field.border_color = None
        
        self.apellido_field.value = ""
        self.apellido_field.error_text = None
        self.apellido_field.border_color = None
        
        self.contacto_field.value = ""
        self.contacto_field.error_text = None
        self.contacto_field.border_color = None
        
        self.tipo_donacion.value = ""
        self.monto_field.value = ""
        self.monto_field.error_text = None
        self.monto_field.border_color = None
        self.monto_field.visible = False
        
        self.descripcion_field.value = ""
        self.descripcion_field.error_text = None
        self.descripcion_field.border_color = None
        self.descripcion_field.visible = False
        
        self.edit_id = None
        
        #NO LIMPIAMOS LOS MENSAJES ACÁ
        self.app.page.update()
    
    def limpiar_formulario(self, e=None):
        """Limpiar formulario completamente incluyendo mensajes"""
        self.limpiar_campos_sin_mensajes()
        
        #ahora sí limpia los mensajes
        self.mensaje_error.visible = False
        self.mensaje_exito.visible = False
        self.app.page.update()
    
    def refresh_vista(self, e=None):
        """Recargar la vista completa para mostrar cambios actualizados"""
        #mostrar mensaje de carga
        self.app.show_snackbar("🔄 Actualizando vista...", "#2196F3")
        
        #recargar la vista de donaciones
        self.app.show_view("donaciones")