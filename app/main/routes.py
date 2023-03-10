from flask import render_template

from app import db
from app.main import bp
from app.models import Question


@bp.route('/')
def index():
    return render_template('index.html',
                           question=Question.query.first())