from tests.base_test_case import BaseTestCase

from app import db
from app.models import Question, Category


class TestQuestion(BaseTestCase):
    def test_create_question(self):
        # Create a category
        category = Category(name="Test Category")
        db.session.add(category)
        db.session.commit()

        # Create a question
        question = Question(body="Test Question", type="multiple choice", difficulty=1, category=category)
        db.session.add(question)
        db.session.commit()

        # Retrieve the question from the database
        retrieved_question = Question.query.filter_by(id=question.id).first()

        # Make sure the retrieved question matches the created question
        self.assertEqual(retrieved_question.body, "Test Question")
        self.assertEqual(retrieved_question.type, "multiple choice")
        self.assertEqual(retrieved_question.difficulty, 1)
        self.assertEqual(retrieved_question.category, category)

        # Delete the question and category from the database
        db.session.delete(question)
        db.session.delete(category)
        db.session.commit()