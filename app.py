import random

from flask import Flask, render_template, request

app = Flask(__name__)

# Definir las cartas para cada dificultad
difficulties = {
    'easy': ['imagen1.png', 'imagen2.png', 'imagen3.png'],
    'medium': ['imagen1.png', 'imagen2.png', 'imagen3.png', 'imagen4.png', 'imagen5.png', 'imagen6.png'],
    'hard': ['imagen1.png', 'imagen2.png', 'imagen3.png', 'imagen4.png', 'imagen5.png', 'imagen6.png',
             'imagen7.png', 'imagen8.png', 'imagen9.png', 'imagen10.png']
}


@app.route('/')
def index():
    return render_template('difficulty.html')


@app.route('/play', methods=['POST'])
def play():
    difficulty = request.form.get('difficulty')
    cards = difficulties[difficulty] * 2  # Crear pares
    random.shuffle(cards)  # Mezclar las cartas
    return render_template('index.html', cards=cards)


if __name__ == '__main__':
    app.run(debug=True)
