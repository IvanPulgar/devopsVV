import os
import tempfile
import pytest
from app.app import create_app


@pytest.fixture
def app():
    """Fixture: crea una BD temporal para cada test y la destruye al terminar."""
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['DATABASE_PATH'] = db_path

    flask_app = create_app()
    flask_app.config['TESTING'] = True

    yield flask_app

    os.close(db_fd)
    os.unlink(db_path)
    os.environ.pop('DATABASE_PATH', None)


@pytest.fixture
def client(app):
    return app.test_client()
