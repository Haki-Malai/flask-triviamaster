from tests.base_test_case import BaseTestCase
from unittest.mock import patch, Mock

from app.retrieve_data import retrieve_data
from app.models import Question, Answer


class TestDatabase(BaseTestCase):

    def test_retrieve_data(self):
        # Create a mock response object for the requests.get() function
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "category": "General Knowledge",
                    "type": "multiple",
                    "difficulty": "easy",
                    "question": "What is the capital of France?",
                    "correct_answer": "Paris",
                    "incorrect_answers": [
                        "Marseille",
                        "Lyon",
                        "Toulouse"
                    ]
                }
            ]
        }
        # Patch the requests.get() function with the mock response object        
        with patch('requests.get', return_value=mock_response):
            retrieve_data(amount=1, silent=True)
        # Check if the database has been initialized correctly
        question = Question.query.filter_by(
            body='What is the capital of France?').first()
        self.assertIsNotNone(question)
        self.assertEqual(question.difficulty, 1)
        # Check if the category has been created
        answers = Answer.query.filter_by(question_id=question.id).all()
        self.assertEqual(len(answers), 4)
        self.assertIn('Paris', [a.body for a in answers])
        self.assertNotIn('Rome', [a.body for a in answers])