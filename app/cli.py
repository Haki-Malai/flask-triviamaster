import click
from flask import Blueprint

bp = Blueprint('cli', __name__)


@bp.cli.command('init')
def init():
    click.echo('Initialized the database.')