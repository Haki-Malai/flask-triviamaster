from tests.base_test_case import BaseTestCase

from app.models import Game, Question, GameQuestion, Answer, Category


class TestGame(BaseTestCase):

    def test_game_model(self):
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.question_count, 1)
        self.assertEqual(self.game.answered_count, 0)
        self.assertFalse(self.game.finished)
        self.assertEqual(self.game.progress, 0)
        self.assertEqual(self.game.questions, [self.question])
        self.assertEqual(self.game.next_question(), self.question)
        self.game.answer_question(self.question.id, self.answer1.id)
        self.assertEqual(self.game.score, 1)
        self.assertEqual(self.game.answered_count, 1)
        self.assertTrue(self.game.finished)
        self.assertEqual(self.game.progress, 100)
        self.assertEqual(self.game.next_question(), None)

    def test_question_model(self):
        self.assertEqual(self.question.body,
                         'What year did World War I begin?')
        self.assertEqual(self.question.type, 'multiple')
        self.assertEqual(self.question.difficulty, 2)
        self.assertEqual(self.question.category, self.category)
        self.assertEqual(self.question.answers, [self.answer1, self.answer2])
        self.assertEqual(self.question.game_questions, [self.game_question])

    def test_game_question_model(self):
        self.assertEqual(self.game_question.game, self.game)
        self.assertEqual(self.game_question.question, self.question)
        self.assertEqual(self.game_question.answer_id, None)
        self.assertEqual(self.game_question.answer_correct, None)

    def test_answer_model(self):
        self.assertEqual(self.answer1.body, '1914')
        self.assertEqual(self.answer1.correct, True)
        self.assertEqual(self.answer1.question, self.question)

    def test_category_model(self):
        self.assertEqual(self.category.name, 'History')
        self.assertEqual(self.category.questions.all(), [self.question])