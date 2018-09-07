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
