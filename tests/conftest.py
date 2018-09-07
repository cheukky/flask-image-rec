import pytest
import os
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

    dirPath = "data/uploads/"
    fileList = os.listdir(dirPath)
    for fileName in fileList:
        if fileName != 'test.jpg' and fileName != '.gitignore':
            os.remove(dirPath+"/"+fileName)
    #
    # # close and remove the temporary database
    # os.close(db_fd)
    # os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
