#Validación de solo aceptar los tipos de datos que correspondan en los inputs (solo int,
# solo str, o solo ambos y así) en vista Adopciones

#Validaciones básicas de campos obligatorios del formulario de Registrar Adoptante



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
            content=ft.Text("", color="white", weight=ft.FontWeight.BOLD, size=14),
            bgcolor="#4CAF50",
            padding=10,
            border_radius=5,
            visible=False,
            margin=ft.margin.only(bottom=10)
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
                            ft.Text("* Campos obligatorios", size=12, color="gray", italic=True),
                            #mensaje de error
                            self.mensaje_error,
                            ft.Row([self.nombre_field, self.apellido_field]),
                            ft.Row([self.contacto_field, self.email_field]),
                            ft.Row([self.direccion_field, self.fecha_field]),
                            self.animal_field,
                            ft.Container(height=20),
                            #mensaje de éxito
                            self.mensaje_exito,
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
    
    #AQUÍ LO QUE AGREGUÉ, MIS MÉTODOS DE VALIDACIÓN
    
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
    
    #y mis demás métodos existentes
    
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
            
            #MOSTRAR MENSAJE DE ÉXITO EN EL FORMULARIO
            self.mostrar_exito(f"✅ ADOPCIÓN REALIZADA CON ÉXITO! {nombre_animal} tiene un nuevo hogar 🏠")
            
            #limpiar formulario PERO mantener el mensaje de éxito
            self.limpiar_formulario_sin_mensajes()
            self.cargar_animales_adopcion()
            
        except Exception as ex:
            self.mostrar_error(f"❌ Error al registrar adopción: {str(ex)}")

    def limpiar_formulario_sin_mensajes(self):
        """Limpiar formulario pero mantener los mensajes"""
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
        
        self.animal_field.value = ""
        
        #NO ocultar mensajes aquí
        if hasattr(self.app, 'page'):
            self.app.page.update()