import os

from flask import Flask
from flask_cors import CORS
from flask_redoc import Redoc
from flask_migrate import Migrate

from . import config
from .version import __version__

def create_app(config_name='DevelopmentConfig'):
    """Create application from config object.
    Args:
        config_name (string) Config instance name
    Returns:
        Flask Application with config instance scope
    """
    app = Flask(__name__)
    conf = config.get_settings(config_name)
    app.config.from_object(conf)
    app.config['REDOC'] = {
        'title': 'API SPEC',
        'spec_route': '/api/docs'
    }

    with app.app_context():
        CORS(app, resources={r"/*": {"origins": "*"}})
        _ = Redoc('./spec/openapi_finance.yaml', app)

        # DB
        from api_finance.models import db
        db.init_app(app)
        Migrate(app, db)

        # Setup blueprint
        from api_finance.blueprint import bp
        app.register_blueprint(bp)

    return app

app = create_app()

__all__ = (
    '__version__',
    'create_app',
)
