import pytest
# from flask_testing import TestCase
from app import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app({
        'TESTING': True,
        # 'DATABASE': db_path,
    })

    # # create the database and load test data
    # with app.app_context():
    #     init_db()
    #     get_db().executescript(_data_sql)

    yield app
    #
    # # close and remove the temporary database
    # os.close(db_fd)
    # os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_index(client):
    """Test index page."""

    rv = client.get('/')
    assert b'Start Page' in rv.data


def test_result(client):
    """Test result page."""

    rv = client.get('/result')
    assert b'Result' in rv.data


def test_thanks(client):
    """Test thanks page."""

    rv = client.get('/thanks')
    assert b'Thanks' in rv.data


def test_training(client):
    """Test training page."""

    rv = client.get('/training')
    assert b'Training' in rv.data
