import sqlite3

# Crear o conectar a la base de datos SQLite3
conn = sqlite3.connect('database.db')

cursor = conn.cursor()

# Crear tabla para almacenar configuraciones generales del sistema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        config_name TEXT NOT NULL UNIQUE,
        config_value TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Crear tabla para almacenar la información de los sensores
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_name TEXT NOT NULL,
        sensor_type TEXT NOT NULL,
        location TEXT,
        unit TEXT NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Crear tabla para almacenar los valores históricos de los sensores
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id INTEGER NOT NULL,
        value REAL NOT NULL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(sensor_id) REFERENCES sensors(id)
    )
''')

# Crear un índice para optimizar consultas basadas en sensor_id y recorded_at
cursor.execute('CREATE INDEX IF NOT EXISTS idx_sensor_data_sensor_id ON sensor_data(sensor_id)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_sensor_data_recorded_at ON sensor_data(recorded_at)')

# Cerrar la conexión a la base de datos
conn.close()


print(f"Base de datos creada exitosamente")
