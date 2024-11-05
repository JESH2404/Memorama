import random

from flask import Flask, render_template, request, redirect, url_for, session

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

        return redirect(url_for('end'))

    if request.method == 'GET':
        result = session.get('result')

        if not result:
            return redirect(url_for('index'))

        return render_template('end.html', message=messages[result])


if __name__ == '__main__':
    app.run(debug=True)
