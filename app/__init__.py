from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import config

db = SQLAlchemy()
mg = Migrate()


def create_app(config_name='default'):
    """Create an application instance using the app factory pattern.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Disable trailing slash
    app.url_map.strict_slashes = False

    # Initialize extensions
    db.init_app(app)
    mg.init_app(app, db)

    # Register blueprints
    from app.cli import bp as cli_bp
    app.register_blueprint(cli_bp)


    @app.shell_context_processor
    def make_shell_context():
        from app import models
        ctx = {'db': db}
        for attr in dir(models):
            model = getattr(models, attr)
            if hasattr(model, '__bases__') and \
                    db.Model in getattr(model, '__bases__'):
                ctx[attr] = model
        return ctx

    with app.app_context():
        db.create_all()

    return app