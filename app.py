import random
from src.controllers.usuario_controller import insertar_usuario, obtener_usuarios, borrar_usuario, actualizar_usuario
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = '123459384'  # Necesario para manejar sesiones

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

#


@app.route('/end', methods=['GET', 'POST'])
def end():
    if request.method == 'POST':
        data = request.get_json()
        result = data.get('status')
        session['result'] = result

        # Guardar el resultado en la base de datos
        nombre_usuario = session.get('nombre', 'Usuario Anónimo')
        puntuacion = session.get('score', 0)
        dificultad = session.get('difficulty', 'easy') #falta corregir estos gets ;D
        insertar_usuario(nombre_usuario, puntuacion, 0, dificultad)

        return redirect(url_for('end'))

    if request.method == 'GET':
        result = session.get('result')
        if not result:
            return redirect(url_for('index'))

        return render_template('end.html', message=messages[result])



@app.route('/usuarios', methods=['GET']) #Metodos crud para crear la tabla :D
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
