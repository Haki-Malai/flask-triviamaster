import unittest
import os

from app import create_app, db


class BaseTestCase(unittest.TestCase):

    data_retrieved = False

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            os.remove(self.app.config['SQLALCHEMY_DATABASE_URI']
                      .replace('sqlite:///', ''))