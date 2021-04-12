import click
from flask.cli import FlaskGroup

from . import app


def create_cli():
    """Define a Wrapper creation of Flask App in order to attach into flask click.
    Args:
         create_app (function) - Create app factory (Flask)
    """
    def create_cli_app():
        """Describe flask factory to create click command."""
        return app

    @click.group(cls=FlaskGroup, create_app=create_cli_app)
    def cli(**params):
        """Command line interface for api."""
        pass

    return cli


cli = create_cli()
