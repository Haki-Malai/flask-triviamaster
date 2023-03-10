from flask import render_template, current_app

from app import db
from app.main import bp
from app.models import Category, Question


@bp.route('/')
def index():
    return render_template('index.html',
                           question=Question.query.first(),
                           config=current_app.config,
                           categories=Category.query.order_by(Category.name).all())