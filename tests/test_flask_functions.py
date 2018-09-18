from io import BytesIO
from PIL import Image
import os


def create_test_image():
    file = BytesIO()
    image = Image.new('RGB', size=(50, 50), color=(0, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


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
    rv = client.post('/', data={'file': (BytesIO(create_test_image().read()),
                                         'test.png') },
                     follow_redirects=True)
    assert b'Result' in rv.data


def test_index_submit_correct2(client):
    """Test index page submit right type."""
    rv = client.post('/', data={'file': (BytesIO(create_test_image().read()),
                                         'test.jpg') },
                     follow_redirects=True)
    assert b'Result' in rv.data


def test_index_submit_correct3(client):
    """Test index page submit right type."""
    rv = client.post('/', data={'file': (BytesIO(create_test_image().read()),
                                         'test.jpeg') },
                     follow_redirects=True)
    assert b'Result' in rv.data


def test_result_yes(client):
    """Test result page yes button."""
    filename = "test.jpg"
    IMG_ARRAY_LOC = 'data/uploads' + "/" + filename + ".npz"
    if(os.path.isfile(IMG_ARRAY_LOC)):
        os.remove(IMG_ARRAY_LOC)
    rv = client.post('/result/'+filename, data=dict(yes='Yes'),
                     follow_redirects=True)
    assert b'Thanks' in rv.data


def test_result_no(client):
    """Test result page no button."""
    rv = client.post('/result/test.jpg', data=dict(no='No'),
                     follow_redirects=True)
    assert b'Training' in rv.data


def test_thanks_again(client):
    """Test thanks page start again button."""
    rv = client.post('/thanks/test10.jpg&&10', data=dict(again='Start Again'),
                     follow_redirects=True)
    assert b'Upload' in rv.data


def test_training_confirm(client):
    """Test training page confirm button."""
    rv = client.post('/training/test10.jpg', data=dict(confirm='Confirm', labels="Strike Gundam"),
                     follow_redirects=True)
    assert b'Thanks' in rv.data
