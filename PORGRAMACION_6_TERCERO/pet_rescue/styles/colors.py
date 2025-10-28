import flet as ft

#la paleta de colores según el diseño de Pet Rescue
COLORS = {
    "primary": "#4CAF50",      #verde menta
    "secondary": "#9C27B0",    #morado
    "accent": "#FF9800",       #naranja
    "background": "#FFF8E1",   #beige claro
    "card": "#FFFFFF",
    "text": "#333333",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "error": "#F44336"
}

def crear_boton(texto, icono, on_click, color=COLORS["primary"], expand=False):
    """Crear botón estilizado"""
    return ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row([
                ft.Icon(icono, color="white"),
                ft.Text(texto, color="white", weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER),
            on_click=on_click,
            bgcolor=color,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20
            ),
            expand=expand
        ),
        margin=10,
        width=200 if not expand else None
    )

def crear_header(titulo):
    """Crear encabezado estilizado"""
    return ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.PETS, color=COLORS["primary"], size=32),
            ft.Text(titulo, size=24, weight=ft.FontWeight.BOLD, color=COLORS["text"]),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        bgcolor=COLORS["card"],
        margin=ft.margin.only(bottom=10),
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=5, color=COLORS["secondary"] + "20")
    )

def crear_card(content, padding=20):
    """Crear tarjeta estilizada"""
    return ft.Card(
        content=ft.Container(
            content=content,
            padding=padding
        ),
        margin=ft.margin.only(bottom=20)
    )