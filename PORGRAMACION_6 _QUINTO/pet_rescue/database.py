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
        
        # Tabla de usuarios (para login)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contraseña TEXT NOT NULL
            )
        ''')
        
        # Insertar usuario demo si no existe
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
                
        except Exception as e:
            return None
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.conn:
            self.conn.close()