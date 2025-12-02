#Agregamos las vistas ContactoPublicoView y PublicoView que estaban en
#archivos separados pero no estaban siendo incluidas en el módulo principal de vistas.

"""
Módulo de vistas para Pet Rescue
"""

from .login_view import LoginView
from .dashboard_view import DashboardView
from .animales_view import AnimalesView
from .adopciones_view import AdopcionesView
from .donaciones_view import DonacionesView
from .contacto_view import ContactoView
from .contacto_publico_view import ContactoPublicoView 
from .publico_view import PublicoView  


__all__ = [
    'LoginView',
    'DashboardView', 
    'AnimalesView',
    'AdopcionesView',
    'DonacionesView',
    'ContactoView',
    'ContactoPublicoView', 
    'PublicoView'  
]



#views/__init__.py
"""
Vistas de la aplicación Pet Rescue

Este módulo contiene todas las vistas de la aplicación:
- LoginView: Vista de inicio de sesión
- DashboardView: Vista principal del dashboard
- AnimalesView: Gestión de animales rescatados
- AdopcionesView: Sistema de adopciones
- DonacionesView: Registro de donaciones  
- ContactoView: Información de contacto
- ContactoPublicoView: Formulario de contacto para el público
- PublicoView: Vista pública de la aplicación
"""


