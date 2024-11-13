import random
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g

from src.controllers.usuario_controller import (
    insertar_usuario,
    obtener_usuarios,
    borrar_usuario,
    actualizar_usuario
)

app = Flask(__name__)
app.secret_key = '123459384'  # Necesario para manejar sesiones

DATABASE = "memoramaDB.db"

# Función para conectar a la base de datos
def get_db():
    """Conexión a la base de datos SQLite."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Permite acceder a los datos como diccionarios
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Cerrar conexión a la base de datos."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Definir las cartas para cada dificultad
difficulties = {
    'easy': ['imagen1.png', 'imagen2.png', 'imagen3.png'],
    'medium': ['imagen1.png', 'imagen2.png', 'imagen3.png', 'imagen4.png', 'imagen5.png', 'imagen6.png'],
    'hard': ['imagen1.png', 'imagen2.png', 'imagen3.png', 'imagen4.png', 'imagen5.png', 'imagen6.png',
             'imagen7.png', 'imagen8.png', 'imagen9.png', 'imagen10.png']
}

messages = {
    'win': "¡Felicidades! Has encontrado todos los pares.",
    'loss': "Lo siento, has perdido. Se acabaron tus intentos."
}

#tabla
@app.route('/')
def index():
    return render_template('difficulty.html')


@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        session['difficulty'] = difficulty

        cards = difficulties[difficulty] * 2  # Crear pares
        random.shuffle(cards)  # Mezclar las cartas

        session['cards'] = cards

        if difficulty == 'easy':
            session['score'] = 30
        elif difficulty == 'medium':
            session['score'] = 60
        elif difficulty == 'hard':
            session['score'] = 100

        return redirect(url_for('play'))
    return render_template('index.html', cards=session['cards'])


@app.route('/end', methods=['GET', 'POST'])
def end():
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombre', 'Anónimo')
        puntuacion = session.get('score', 0)
        dificultad = session.get('difficulty', 'easy')
        tiempo = session.get('count', 0)  # Aquí podrías calcular el tiempo de juego si lo tienes disponible.

        # Guardar en la base de datos
        db = get_db()
        db.execute(
            'INSERT INTO usuario (nombre, puntuacion, tiempo, difictultad) VALUES (?, ?, ?, ?)',
            (nombre_usuario, puntuacion, tiempo, dificultad)
        )
        db.commit()

        # Redirigir a la tabla de puntuaciones
        return redirect(url_for('show_scores'))

    if request.method == 'GET':
        result = session.get('result')
        if not result:
            return redirect(url_for('index'))

        return render_template('end.html', message=messages[result])

@app.route('/scores')
def show_scores():
    """Mostrar la tabla de puntuaciones."""
    db = get_db()
    cursor = db.execute(
        'SELECT id, nombre, puntuacion, tiempo, difictultad FROM usuario ORDER BY puntuacion DESC'
    )
    scores = cursor.fetchall()
    return render_template('scores.html', scores=scores)

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = obtener_usuarios()
    usuarios_json = [{"nombre": u.nombre, "puntuacion": u.puntuacion,
                      "tiempo": u.tiempo, "dificultad": u.dificultad} for u in usuarios]
    return jsonify(usuarios_json), 200


@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    insertar_usuario(data['nombre'], data.get('puntuacion', 0), data.get(
        'tiempo', 0), data.get('dificultad', 'easy'))
    return jsonify({"mensaje": "Usuario creado exitosamente"}), 201


@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    borrar_usuario(id_usuario)
    return jsonify({"mensaje": "Usuario eliminado exitosamente"}), 200


@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def modificar_usuario(id_usuario):
    data = request.get_json()
    actualizar_usuario(id_usuario, data['nombre'], data.get(
        'puntuacion', 0), data.get('tiempo', 0), data.get('dificultad', 'easy'))
    return jsonify({"mensaje": "Usuario actualizado exitosamente"}), 200


if __name__ == '__main__':
    app.run(debug=True)
