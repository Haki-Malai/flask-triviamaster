from flask import render_template, current_app, request, redirect, url_for, \
    flash

from app import db
from app.main import bp
from app.models import Category, Question, Game


@bp.route('/')
def index():
    return render_template(
        'index.html',
        config=current_app.config,
        categories=Category.query.order_by(Category.name).all())


@bp.route('/game')
def start_game():
    game = Game()
    db.session.add(game)
    game.generate_questions()
    db.session.commit()
    return redirect(url_for('main.show_game', game_id=game.id))


@bp.route('/game/<int:game_id>')
def show_game(game_id):
    return render_template(
        'game.html',
        config=current_app.config,
        game=Game.query.get(game_id),
        question=Game.query.get(game_id).next_question(),
        categories=Category.query.order_by(Category.name).all())


@bp.route('/game/<int:game_id>', methods=['POST'])
def play_game(game_id):
    game = Game.query.get(game_id)
    question_id = request.form.get('question_id')
    answer_id = request.form.get('answer_id')
    if game.answer_question(question_id, answer_id):
        flash('Correct!', 'success')
    else:
        flash('Incorrect!', 'danger')
    db.session.commit()
    return redirect(url_for('main.play_game', game_id=game.id))