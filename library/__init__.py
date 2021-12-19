"""Initialize Flask app."""
from flask import Flask
from pathlib import Path

import library.adapters.repository as repo
from library.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object("config.Config")
    data_path = Path("library") / "adapters" / "data"

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config["TEST_DATA_PATH"]

    # Instantiate MemoryRepository implementation & fill with books from JSON file
    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        # Register blueprints
        from .home import home

        app.register_blueprint(home.home_blueprint)

        from .books import books

        app.register_blueprint(books.books_blueprint)

        from .authentication import authentication

        app.register_blueprint(authentication.authentication_blueprint)

        from .utilities import utilities

        app.register_blueprint(utilities.utilities_blueprint)

    return app
