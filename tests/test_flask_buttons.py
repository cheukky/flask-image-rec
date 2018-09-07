def test_index_submit(client):
    """Test index page submit."""
    rv = client.post('/', data=dict(upload='Upload'), follow_redirects=True)
    assert b'Result' in rv.data


def test_result_yes(client):
    """Test result page yes button."""
    rv = client.post('/result', data=dict(yes='Yes'), follow_redirects=True)
    assert b'Thanks' in rv.data


def test_result_no(client):
    """Test result page no button."""
    rv = client.post('/result', data=dict(no='No'), follow_redirects=True)
    assert b'Training' in rv.data


def test_thanks_again(client):
    """Test thanks page start again button."""
    rv = client.post('/thanks', data=dict(again='Start Again'), follow_redirects=True)
    assert b'Start Page' in rv.data


def test_training_confirm(client):
    """Test training page confirm button."""
    rv = client.post('/training', data=dict(confirm='Confirm'), follow_redirects=True)
    assert b'Thanks' in rv.data
