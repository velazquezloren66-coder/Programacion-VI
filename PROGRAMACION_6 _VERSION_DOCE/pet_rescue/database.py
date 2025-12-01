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
        
        #tabla de usuarios (para login)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL
            )
        ''')
        
        #tabla de animales
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS animales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especie TEXT NOT NULL,
                raza TEXT,
                edad TEXT NOT NULL,
                descripcion TEXT,
                imagen_url TEXT,
                estado TEXT NOT NULL,
                fecha_ingreso TEXT NOT NULL
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
        
        #tabla de adopciones
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS adopciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                animal_id INTEGER NOT NULL,
                adoptante_nombre TEXT NOT NULL,
                adoptante_contacto TEXT NOT NULL,
                fecha_adopcion TEXT NOT NULL,
                FOREIGN KEY (animal_id) REFERENCES animales (id)
            )
        ''')
        
        #insertar usuario demo si no existe
        self.cursor.execute('''
            INSERT OR IGNORE INTO usuarios (usuario, contraseña) 
            VALUES (?, ?)
        ''', ('loreadmin', 'larrymibb'))
        
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
                
        except Exception:
            return None
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.conn:
            self.conn.close()