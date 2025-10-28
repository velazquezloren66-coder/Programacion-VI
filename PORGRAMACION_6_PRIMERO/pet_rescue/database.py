#Acá inicializa la base de datos SQLite del sistema PetRescue, creando cuatro tablas principales: 
#animales (registro de mascotas rescatadas), adoptantes (información de personas adoptantes), donantes 
#(gestión de contribuciones) y usuarios (control de acceso). Además, inserta datos de demostración incluyendo
#credenciales de prueba y animales ejemplo, estableciendo la estructura fundamental para el funcionamiento
#del sistema de gestión del refugio



import sqlite3

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.init_db()
    
    def init_db(self):
        """Inicializar base de datos SQLite"""
        self.conn = sqlite3.connect('pet_rescue.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        #tabla de animales
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS animales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especie TEXT NOT NULL,
                edad TEXT NOT NULL,
                fecha_rescate TEXT NOT NULL,
                estado TEXT NOT NULL,
                vacunas TEXT,
                descripcion TEXT,
                imagen TEXT
            )
        ''')
        
        #tabla de adoptantes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS adoptantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                contacto TEXT NOT NULL,
                direccion TEXT,
                email TEXT,
                fecha_adopcion TEXT NOT NULL,
                animal_id INTEGER,
                descripcion TEXT,
                FOREIGN KEY (animal_id) REFERENCES animales (id)
            )
        ''')
        
        #tabla de donantes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS donantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                contacto TEXT NOT NULL,
                tipo_donacion TEXT NOT NULL,
                monto REAL,
                descripcion TEXT,
                fecha_donacion TEXT NOT NULL
            )
        ''')
        
        #tabla de usuarios (para login)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL
            )
        ''')
        
        #insertar usuario demo si no existe
        self.cursor.execute('''
            INSERT OR IGNORE INTO usuarios (usuario, contraseña) 
            VALUES (?, ?)
        ''', ('admin', '1234'))
        
        #insertar algunos animales de ejemplo
        self.cursor.execute('''
            INSERT OR IGNORE INTO animales (nombre, especie, edad, fecha_rescate, estado, descripcion) 
            VALUES 
            ('Manchitas', 'Perro', '2 años', '15/08/2024', 'En adopción', 'Perro juguetón y cariñoso, le encanta correr en el parque'),
            ('Luna', 'Gato', '1 año', '20/09/2024', 'En adopción', 'Gata tranquila y amorosa, ideal para apartamento'),
            ('Rex', 'Perro', '3 años', '10/07/2024', 'En refugio', 'Perro guardián y leal, necesita espacio para correr')
        ''')
        
        self.conn.commit()
    
    def execute_query(self, query, params=()):
        """Ejecutar consulta y retornar resultados"""
        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return self.cursor.rowcount
        except Exception as e:
            print(f"Error en consulta: {e}")
            return None
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.conn:
            self.conn.close()