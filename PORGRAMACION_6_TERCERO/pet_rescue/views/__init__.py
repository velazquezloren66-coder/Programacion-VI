"""
Módulo de vistas para Pet Rescue
"""

from .login_view import LoginView
from .dashboard_view import DashboardView
from .animales_view import AnimalesView
from .adopciones_view import AdopcionesView
from .donaciones_view import DonacionesView
from .contacto_view import ContactoView


__all__ = [
    'LoginView',
    'DashboardView', 
    'AnimalesView',
    'AdopcionesView',
    'DonacionesView',
    'ContactoView'
]


# views/__init__.py
"""
Vistas de la aplicación Pet Rescue

Este módulo contiene todas las vistas de la aplicación:
- LoginView: Vista de inicio de sesión
- DashboardView: Vista principal del dashboard
- AnimalesView: Gestión de animales rescatados
- AdopcionesView: Sistema de adopciones
- DonacionesView: Registro de donaciones  
- ContactoView: Información de contacto
"""