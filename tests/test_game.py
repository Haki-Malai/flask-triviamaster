from tests.base_test_case import BaseTestCase

from app.models import Question, GameQuestion, Answer, Game
from app import db


class TestModel(BaseTestCase):

    def test_game_model(self):
        # Check if the game has been initialized correctly
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.question_count, 1)
        self.assertEqual(self.game.answered_count, 0)
        self.assertFalse(self.game.finished)
        self.assertEqual(self.game.progress, 0)
        self.assertEqual(self.game.questions, [self.question])
        self.assertEqual(self.game.next_question().question,
                         self.question)
        self.game.answer_question(self.question.id,
                                            self.answer1.id)
        self.assertEqual(self.game.score, 1)
        self.assertEqual(self.game.answered_count, 1)
        self.assertTrue(self.game.finished)
        self.assertEqual(self.game.progress, 100)
        self.assertEqual(self.game.next_question(), None)

    def test_question_model(self):
        # Check if the question has been initialized correctly
        self.assertEqual(self.question.body,
                         'What year did World War I begin?')
        self.assertEqual(self.question.type, 'multiple')
        self.assertEqual(self.question.difficulty, 2)
        self.assertEqual(self.question.category, self.category)
        self.assertEqual(self.question.answers, [self.answer1, self.answer2])
        self.assertEqual(self.question.game_questions, [self.game_question])

    def test_game_question_model(self):
        # Check if the game_question has been initialized correctly
        self.assertEqual(self.game_question.game, self.game)
        self.assertEqual(self.game_question.question, self.question)
        self.assertEqual(self.game_question.answer_id, None)
        self.assertEqual(self.game_question.answer_correct, None)

    def test_answer_model(self):
        # Check if the answer has been initialized correctly
        self.assertEqual(self.answer1.body, '1914')
        self.assertEqual(self.answer1.correct, True)
        self.assertEqual(self.answer1.question, self.question)

    def test_category_model(self):
        # Check if the category has been initialized correctly
        self.assertEqual(self.category.name, 'History')
        self.assertEqual(self.category.questions.all(), [self.question])

    def test_next_question(self):
        # Create some questions and add them to the game
        q1 = Question(
            body="Question 1", type="type", difficulty=1, category_id=1)
        q2 = Question(
            body="Question 2", type="type", difficulty=2, category_id=1)
        q3 = Question(
            body="Question 3", type="type", difficulty=3, category_id=1)
        db.session.add_all([q1, q2, q3])
        # Create a new game
        self.game_test_next = Game()
        db.session.add(self.game_test_next)
        self.game_test_next.generate_questions(num_questions=3, category_id=1)
        db.session.commit()

        # Confirm next_question() returns the first question
        q = self.game_test_next.next_question()

        # Test next_question() after answering the first question
        game_question = GameQuestion.query.filter_by(
            game_id=self.game_test_next.id,
            question_id=q.question.id).first()
        game_question.answer_id = 1
        db.session.commit()
        q = self.game_test_next.next_question()
        self.assertEqual(q.question.body, "Question 2")

        # Answer 2nd question, test next_question() for 3rd question
        game_question = GameQuestion.query.filter_by(
            game_id=self.game_test_next.id,
            question_id=q.question.id).first()
        game_question.answer_id = 1
        db.session.commit()
        q = self.game_test_next.next_question()
        self.assertEqual(q.question.body, "Question 3")

        # Answer 3rd question and verify next_question() returns None
        game_question = GameQuestion.query.filter_by(
            game_id=self.game_test_next.id,
            question_id=q.question.id).first()
        game_question.answer_id = 1
        db.session.commit()
        q = self.game_test_next.next_question()
        self.assertIsNone(q)

    def test_answer_question(self):
        # Create a new game
        self.game_test_answer = Game()
        db.session.add(self.game_test_answer)
        self.game_test_answer.generate_questions(num_questions=3,
                                                 category_id=1)
        db.session.commit()

        # Create a question with two answers, one of which is correct
        q = Question(body="Question",
                     type="type",
                     difficulty=1,
                     category_id=1)
        a1 = Answer(body="Answer 1", correct=False, question=q)
        a2 = Answer(body="Answer 2", correct=True, question=q)
        db.session.add_all([q, a1, a2])
        db.session.commit()

        # Add the question to the game
        self.game_test_answer.generate_questions(num_questions=1,
                                                 category_id=1)

        # Answer incorrectly, score stays the same
        self.game_test_answer.answer_question(q.id, a1.id)
        self.assertEqual(self.game_test_answer.score, 0)

        # Answer correctly to increase the score by 1
        self.game_test_answer.answer_question(q.id, a2.id)
        db.session.commit()
        self.assertEqual(self.game_test_answer.score, 1)