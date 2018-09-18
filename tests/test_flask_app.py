def test_index(client):
    """Test index page."""
    rv = client.get('/')
    assert b'Upload' in rv.data


def test_result(client):
    """Test result page."""
    rv = client.get('/result/test.jpg')
    assert b'Result' in rv.data


def test_thanks(client):
    """Test thanks page."""
    rv = client.get('/thanks/test10.jpg&&10')
    assert b'Thanks' in rv.data


def test_training(client):
    """Test training page."""
    rv = client.get('/training/test.jpg')
    assert b'Training' in rv.data
