from app import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    answers = db.relationship('Answer', back_populates='question')
    category = db.relationship('Category', back_populates='questions')

    def __repr__(self):
        return "<Question %r>" % self.body


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(128), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    question = db.relationship('Question', back_populates='answers')

    def __repr__(self):
        return "<Answer %r>" % self.body


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    questions = db.relationship('Question', back_populates='category')

    def __repr__(self):
        return "<Category %r>" % self.name