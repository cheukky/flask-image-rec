from io import BytesIO
import os


def test_index_submit_nofile(client):
    """Test index page submit no file."""
    rv = client.post('/', data=dict(upload='Upload'), follow_redirects=True)
    assert b'Choose a file' in rv.data


def test_index_submit_nofilename(client):
    """Test index page submit no filename."""
    rv = client.post('/', data={'file': (BytesIO(b'my file contents'),
                                         '') },
                     follow_redirects=True)
    assert b'Choose a file' in rv.data


def test_index_submit_wrongtype(client):
    """Test index page submit wrong type."""
    rv = client.post('/', data={'file': (BytesIO(b'my file contents'),
                                         'test_file.txt') },
                     follow_redirects=True)
    assert b'Wrong file type' in rv.data


def test_index_submit_wrongtype2(client):
    """Test index page submit wrong type."""
    rv = client.post('/', data={'file': (BytesIO(b'my file contents'),
                                         'test_file.pdf') },
                     follow_redirects=True)
    assert b'Wrong file type' in rv.data


def test_index_submit_correct(client):
    """Test index page submit right type."""
    rv = client.post('/', data={'file': (BytesIO(b'my file contents'),
                                         'test_file.png') },
                     follow_redirects=True)
    assert b'Result' in rv.data


def test_index_submit_correct2(client):
    """Test index page submit right type."""
    rv = client.post('/', data={'file': (BytesIO(b'my file contents'),
                                         'test_file.jpg') },
                     follow_redirects=True)
    assert b'Result' in rv.data


def test_index_submit_correct3(client):
    """Test index page submit right type."""
    rv = client.post('/', data={'file': (BytesIO(b'my file contents'),
                                         'test_file.jpeg') },
                     follow_redirects=True)
    assert b'Result' in rv.data


def test_result_yes(client):
    """Test result page yes button."""
    rv = client.post('/result/test.jpg', data=dict(yes='Yes'),
                     follow_redirects=True)
    assert b'Thanks' in rv.data


def test_result_no(client):
    """Test result page no button."""
    rv = client.post('/result/test.jpg', data=dict(no='No'),
                     follow_redirects=True)
    assert b'Training' in rv.data


def test_thanks_again(client):
    """Test thanks page start again button."""
    rv = client.post('/thanks', data=dict(again='Start Again'),
                     follow_redirects=True)
    assert b'Start Page' in rv.data


def test_training_confirm(client):
    """Test training page confirm button."""
    rv = client.post('/training', data=dict(confirm='Confirm'),
                     follow_redirects=True)
    assert b'Thanks' in rv.data
