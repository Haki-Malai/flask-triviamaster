from sqlalchemy.sql.expression import func

from app import db


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, default=0, nullable=False)
    game_questions = db.relationship('GameQuestion',
                                     back_populates='game',
                                     lazy='dynamic')

    def __repr__(self):
        return "<Game %r>" % self.id

    @property
    def questions(self):
        return [game_question.question for game_question in self.game_questions]

    @property
    def question_count(self):
        return self.game_questions.count()

    @property
    def answered_count(self):
        return self.game_questions.filter_by(answered=True).count()

    @property
    def progress(self):
        return self.answered_count / self.question_count * 100

    def next_question(self):
        for game_question in self.game_questions:
            if not game_question.answered:
                return game_question.question

    def generate_questions(self, num_questions=5, category_id=None):
        if category_id:
            query = Category.query.get(category_id).questions
        else:
            query = Question.query
        questions = query.order_by(func.random()).limit(num_questions).all()
        
        for question in questions:
            game_questions = GameQuestion(game_id=self.id,
                                          question_id=question.id)
            db.session.add(game_questions)

    def answer_question(self, question_id, answer_id):
        game_question = self.game_questions.filter_by(
            question_id=question_id).first()
        if game_question:
            game_question.answered = True
            if answer_id:
                answer = Answer.query.get(answer_id)
                if answer.correct:
                    self.score += 1
                    return True


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'),
                            nullable=False)

    answers = db.relationship('Answer', back_populates='question')
    category = db.relationship('Category', back_populates='questions')
    game_questions = db.relationship('GameQuestion',
                                     back_populates='question')

    def __repr__(self):
        return "<Question %r>" % self.body


class GameQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answered = db.Column(db.Boolean, default=False, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    question_id = db.Column(db.Integer,
                            db.ForeignKey('question.id'),
                            nullable=False)

    game = db.relationship('Game', back_populates='game_questions')
    question = db.relationship('Question', back_populates='game_questions')

    def __repr__(self):
        return "<GameQuestion %r>" % self.id


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(128), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer,
                            db.ForeignKey('question.id'),
                            nullable=False)

    question = db.relationship('Question', back_populates='answers')

    def __repr__(self):
        return "<Answer %r>" % self.body


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    questions = db.relationship('Question', back_populates='category')

    def __repr__(self):
            return "<Category %r>" % self.name