import click
from flask import Blueprint

from app.retrieve_data import retrieve_data
from config import Config

bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.command('get_data')
@click.option('--amount',
              default=Config.QUESTIONS_TO_RETRIEVE,
              help='Number of questions to fetch.')
@click.option('--drop',
              is_flag=True,
              help='Drop all tables before initializing.')
def get_data(amount=Config.QUESTIONS_TO_RETRIEVE, drop=False):
    """Fetch questions from Open Trivia DB API and initialize the database.
    """
    retrieve_data(amount, drop)


@bp.cli.command('test')
@click.option('--patern',
                default='*',
                help="Test file name patern. Default is 'test_*'.")
@click.option('--verbosity', default=2, type=int)
def test(patern, verbosity):
    """Run the tests.
    """
    import unittest
    patern = f'test_*{patern}*.py'
    tests = unittest.TestLoader().discover('tests', patern)
    unittest.TextTestRunner(verbosity=verbosity).run(tests)