from app import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    answers = db.relationship('Answer', back_populates='question')

    def __repr__(self):
        return "<Question %r>" % self.question

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(128), nullable=False)
    correct = db.Column(db.Boolean, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    question = db.relationship('Question', back_populates='answers')

    def __repr__(self):
        return "<Answer %r>" % self.answer