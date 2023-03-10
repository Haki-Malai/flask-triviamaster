from flask import render_template, current_app, request, redirect, url_for, \
    flash

from app import db
from app.main import bp
from app.models import Category, Game


@bp.route('/')
def index():
    return render_template(
        'index.html',
        config=current_app.config,
        categories=Category.query.order_by(Category.name).all())


@bp.route('/category_game/<int:category_id>')
@bp.route('/game')
def start_game(category_id=None):
    """Start a new game
    Creates a new game and redirects to the game page.
    """
    game = Game()
    db.session.add(game)
    game.generate_questions(
        num_questions=current_app.config['QUESTIONS_PER_GAME'],
        category_id=category_id)
    db.session.commit()
    return redirect(url_for('main.show_game', game_id=game.id))


@bp.route('/game/<int:game_id>')
def show_game(game_id):
    """Show the game page
    If the game is finished, redirects to the results page.
    """
    game = Game.query.get(game_id)
    if not game:
        return redirect(url_for('main.index'))
    if game.finished:
        return redirect(url_for('main.game_results', game_id=game.id))
    return render_template(
        'game.html',
        config=current_app.config,
        game=game,
        game_question=game.next_question(),
        categories=Category.query.order_by(Category.name).all())


@bp.route('/game/<int:game_id>', methods=['POST'])
def play_game(game_id):
    """Play the game
    If the game is finished, redirects to the results page.
    """
    game = Game.query.get(game_id)
    if not game:
        return redirect(url_for('main.index'))
    question_id = request.form.get('question_id')
    answer_id = request.form.get('answer_id')
    if game.answer_question(question_id, answer_id):
        flash('Correct!', 'success')
    else:
        flash('Incorrect!', 'danger')
    db.session.commit()
    return redirect(url_for('main.play_game', game_id=game.id))


@bp.route('/game/<int:game_id>/results')
def game_results(game_id):
    """Show the game results
    If the game is not finished, redirects to the game page.
    """
    game = Game.query.get(game_id)
    if not game:
        return redirect(url_for('main.index'))
    if not game.finished:
        return redirect(url_for('main.play_game', game_id=game.id))
    return render_template(
        'results.html',
        config=current_app.config,
        game=game,
        categories=Category.query.order_by(Category.name).all())