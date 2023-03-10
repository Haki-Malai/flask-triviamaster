import click
from html import unescape
from flask import Blueprint

from app import db

bp = Blueprint('cli', __name__)


@bp.cli.command('init')
@click.option('--amount', default=10, help='Number of questions to fetch. Max 50.')
@click.option('--drop', is_flag=True, help='Drop all tables before initializing.')
def init(amount, drop):
    """Initialize the database.
    """
    import requests
    from app.models import Question, Answer, Category

    # Drop all tables if drop flag is set
    if drop:
        db.drop_all()
        db.create_all()

    # Fetch questions from Open Trivia DB API
    response = requests.get(f'https://opentdb.com/api.php?amount={amount}')
    data = response.json()["results"]
    difficulty = {'easy': 1, 'medium': 2, 'hard': 3}

    for item in data:
        # Create category if not exists
        category_name = unescape(item['category'])
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

        question = Question(
            body=unescape(item['question']),
            type=int(item['type'] == 'boolean'),
            difficulty=difficulty[item['difficulty']],
            category_id=category.id
        )
        db.session.add(question)
        db.session.commit()

        # Create incorrect answers
        for i in range(len(item['incorrect_answers'])):
            incorect_answer = Answer(
                body=unescape(item['incorrect_answers'][i]),
                correct=False,
                question_id=question.id
            )
            db.session.add(incorect_answer)

        # Create correct answer
        correct_answer = Answer(
            body=unescape(item['correct_answer']),
            correct=True,
            question_id=question.id
        )
        db.session.add(correct_answer)
        db.session.commit()

    click.echo('Initialized the database.')