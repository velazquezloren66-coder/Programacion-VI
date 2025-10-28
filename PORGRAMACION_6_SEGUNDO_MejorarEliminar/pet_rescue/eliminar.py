#En esta segunda versión mini solo se cuenta con una vista de cómo debería verse el buen funcionamiento
#de la función eliminar en mi sistema, aquí implemento dos datos sencillos de prueba para 
#realizar la eliminación, la cual termina siendo un éxito.


import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = "Test Eliminar"
    page.padding = 50
    
    #conectar a la misma base de datos
    conn = sqlite3.connect('pet_rescue.db', check_same_thread=False)
    cursor = conn.cursor()
    
    #crear tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_animales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    ''')
    
    #insertar datos de prueba
    cursor.execute("DELETE FROM test_animales")
    cursor.execute("INSERT INTO test_animales (nombre) VALUES ('Perro Test')")
    cursor.execute("INSERT INTO test_animales (nombre) VALUES ('Gato Test')")
    conn.commit()
    
    #función para cargar datos
    def cargar_datos():
        cursor.execute("SELECT * FROM test_animales")
        animales = cursor.fetchall()
        
        tabla.rows.clear()
        for animal in animales:
            tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(animal[1])),
                    ft.DataCell(ft.Text(str(animal[0]))),
                    ft.DataCell(
                        ft.IconButton(
                            ft.Icons.DELETE,
                            on_click=lambda e, id=animal[0]: eliminar_animal(id)
                        )
                    ),
                ])
            )
        page.update()
    
    #función eliminar, pruebo con uno simple para ver si ya funciona con este
    def eliminar_animal(animal_id):
        print(f"Intentando eliminar animal ID: {animal_id}")
        
        try:
            cursor.execute("DELETE FROM test_animales WHERE id = ?", (animal_id,))
            conn.commit()
            print("✅ Eliminado en la base de datos")
            
            #mostrar mensaje
            page.snack_bar = ft.SnackBar(ft.Text("✅ Eliminado correctamente"))
            page.snack_bar.open = True
            
            #recargar tabla
            cargar_datos()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Error: {e}"))
            page.snack_bar.open = True
            page.update()
    
    #crear tabla
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Eliminar")),
        ],
        rows=[]
    )
    
    #cargar datos iniciales
    cargar_datos()
    
    page.add(
        ft.Text("TEST ELIMINAR - Haz clic en el icono de eliminar", size=20),
        ft.Container(height=20),
        tabla
    )

if __name__ == "__main__":
    ft.app(target=main)