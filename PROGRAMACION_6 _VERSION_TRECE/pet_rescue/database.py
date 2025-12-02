#CAMBIOS:

#1. Columna fecha_ingreso agregada automáticamente
#2. Migración de datos de columna imagen a imagen_url


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
        
        #tabla de animales - VERSIÓN COMPLETA CON TODAS LAS COLUMNAS NECESARIAS
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS animales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especie TEXT NOT NULL,
                edad TEXT NOT NULL,
                fecha_rescate TEXT NOT NULL,
                estado TEXT NOT NULL,
                vacunas TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                imagen TEXT,
                imagen_url TEXT,
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
        
        #asegurar que todas las columnas necesarias existan
        self._verificar_y_crear_columnas_faltantes()
        
        #insertar usuario demo si no existe
        self.cursor.execute('''
            INSERT OR IGNORE INTO usuarios (usuario, contraseña) 
            VALUES (?, ?)
        ''', ('admin', '1234'))
        
        self.conn.commit()
    
    def _verificar_y_crear_columnas_faltantes(self):
        """Verificar y crear columnas faltantes en la tabla animales"""
        try:
            #obtener información de columnas existentes
            self.cursor.execute("PRAGMA table_info(animales)")
            columnas_existentes = self.cursor.fetchall()
            nombres_columnas = [col[1] for col in columnas_existentes]
            
            #lista de columnas requeridas
            columnas_requeridas = [
                ('fecha_ingreso', 'TEXT NOT NULL DEFAULT CURRENT_DATE'),
                ('imagen_url', 'TEXT'),
                ('imagen', 'TEXT')
            ]
            
            #verificar y agregar columnas faltantes
            for columna, tipo in columnas_requeridas:
                if columna not in nombres_columnas:
                    try:
                        self.cursor.execute(f"ALTER TABLE animales ADD COLUMN {columna} {tipo}")
                    except:
                        #si falla, intentar sin la parte DEFAULT
                        tipo_simple = tipo.split('DEFAULT')[0].strip()
                        self.cursor.execute(f"ALTER TABLE animales ADD COLUMN {columna} {tipo_simple}")
            
            #migrar datos de 'imagen' a 'imagen_url' si es necesario
            if 'imagen' in nombres_columnas and 'imagen_url' in nombres_columnas:
                self.cursor.execute('''
                    UPDATE animales 
                    SET imagen_url = imagen 
                    WHERE (imagen_url IS NULL OR imagen_url = '') 
                    AND imagen IS NOT NULL AND imagen != ''
                ''')
            
            self.conn.commit()
            
        except Exception:
            #silenciar errores, continuar con la aplicación
            pass
    
    def execute_query(self, query, params=()):
        """Ejecutar consulta y retornar resultados"""
        try:
            self.cursor.execute(query, params)
            
            #para consultas SELECT (o PRAGMA que se comporta como SELECT)
            if query.strip().upper().startswith('SELECT') or query.strip().upper().startswith('PRAGMA'):
                return self.cursor.fetchall()
            else:
                self.conn.commit()
                return self.cursor.rowcount
                
        except Exception:
            #error silencioso, retornar None
            return None
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.conn:
            self.conn.close()