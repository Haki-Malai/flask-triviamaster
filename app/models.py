from app import db


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, question, answer, difficulty, category, rating):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty
        self.category = category
        self.rating = rating

    def __repr__(self):
        return "<Question %r>" % self.question

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()