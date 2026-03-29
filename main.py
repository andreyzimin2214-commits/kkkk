from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key' # Нужен для работы сессий

# Структура вашей игры (Сюжет)
STORY = {
    'start': {
        'text': "Вы проснулись в холодной палате заброшенной больницы. Дверь приоткрыта. Что будете делать?",
        'choices': [
            {'text': "Выйти в коридор", 'next': 'corridor'},
            {'text': "Обыскать тумбочку", 'next': 'table'}
        ]
    },
    'corridor': {
        'text': "В коридоре темно, пахнет лекарствами. Слева слышны шаги, справа — лестница вниз.",
        'choices': [
            {'text': "Идти на лестницу", 'next': 'escape'},
            {'text': "Спрятаться в палате", 'next': 'start'}
        ]
    },
    'table': {
        'text': "В тумбочке вы нашли ржавый ключ! Теперь вы чувствуете себя увереннее.",
        'choices': [
            {'text': "Выйти в коридор с ключом", 'next': 'corridor_key'}
        ]
    },
    'corridor_key': {
        'text': "С ключом вы открываете черный ход и выбираетесь на свободу! ВЫ ПОБЕДИЛИ!",
        'choices': [
            {'text': "Играть снова", 'next': 'start'}
        ]
    },
    'escape': {
        'text': "Вы побежали по лестнице, но споткнулись. Санитары поймали вас... ИГРА ОКОНЧЕНА.",
        'choices': [
            {'text': "Попробовать снова", 'next': 'start'}
        ]
    }
}

@app.route('/')
def index():
    # Если игра только началась, ставим начальную сцену
    if 'scene' not in session:
        session['scene'] = 'start'
    
    scene_id = session['scene']
    scene_data = STORY.get(scene_id, STORY['start'])
    
    return render_template('index.html', scene=scene_data)

@app.route('/action', methods=['POST'])
def action():
    next_scene = request.form.get('next_scene')
    if next_scene in STORY:
        session['scene'] = next_scene
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
