import unittest
import os

from app import create_app, db
from app.models import Game, Question, GameQuestion, Answer, Category


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.category = Category(name='History')
        self.question = Question(body='What year did World War I begin?',
                                 type='multiple',
                                 difficulty=2,
                                 category=self.category)
        self.answer1 = Answer(body='1914',
                              correct=True,
                              question=self.question)
        self.answer2 = Answer(body='1918',
                              correct=False,
                              question=self.question)
        self.game = Game(score=0)
        db.session.add_all([self.category,
                            self.question,
                            self.answer1,
                            self.answer2,
                            self.game])
        db.session.commit()
        self.game_question = GameQuestion(game=self.game,
                                          question=self.question)
        db.session.add(self.game_question)
        db.session.commit()

    def tearDown(self):
        with self.app_context:
            db.session.close()
            db.drop_all()
            os.remove(self.app.config['SQLALCHEMY_DATABASE_URI']
                      .replace('sqlite:///', ''))
        self.app_context.pop()