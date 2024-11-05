# src/controllers/usuario_controller.py
from src.database.db_sqlite import get_connection
from src.models.Usuario import Usuario

def insertar_usuario(nombre, puntuacion, tiempo, dificultad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO usuario (nombre, puntuacion, tiempo, dificultad) VALUES (?, ?, ?, ?)',
        (nombre, puntuacion, tiempo, dificultad)
    )
    conn.commit()
    cursor.close()

def obtener_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuario')
    usuarios_data = cursor.fetchall()
    usuarios = [Usuario(row['nombre'], row['puntuacion'], row['tiempo'], row['dificultad']) for row in usuarios_data]
    cursor.close()
    return usuarios

def borrar_usuario(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuario WHERE id = ?', (id_usuario,))
    conn.commit()
    cursor.close()

def actualizar_usuario(id_usuario, nombre, puntuacion, tiempo, dificultad):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE usuario SET nombre = ?, puntuacion = ?, tiempo = ?, dificultad = ? WHERE id = ?',
        (nombre, puntuacion, tiempo, dificultad, id_usuario)
    )
    conn.commit()
    cursor.close()
