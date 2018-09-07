from flask import Flask, render_template, flash, redirect, request, url_for
import os
from werkzeug.utils import secure_filename
import random

UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# list of cat images
images = [
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26388-1381844103-11.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr01/15/9/anigif_enhanced-buzz-31540-1381844535-8.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26390-1381844163-18.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-1376-1381846217-0.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3391-1381844336-26.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-29111-1381845968-0.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3409-1381844582-13.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr02/15/9/anigif_enhanced-buzz-19667-1381844937-10.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26358-1381845043-13.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-18774-1381844645-6.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-25158-1381844793-0.gif",
    "http://img.buzzfeed.com/buzzfeed-static/static/2013-10/enhanced/webdr03/15/10/anigif_enhanced-buzz-11980-1381846269-1.gif"
    ]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    @app.route('/', methods=('GET', 'POST'))
    def index():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('Choose a file')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('Choose a file')
                return redirect(request.url)
            if not allowed_file(file.filename):
                flash('Wrong file type. Accepted extensions: .png, .jpg, .jpeg')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('result', filename=filename))

        url = random.choice(images)
        return render_template('index.html', url=url)

    from flask import send_from_directory

    @app.route('/result/<filename>', methods=('GET', 'POST'))
    def result(filename):
        if request.method == 'POST':
            if "yes" in request.form:
                return redirect(url_for('thanks'))
            elif "no" in request.form:
                return redirect(url_for('training'))
        return render_template('result.html', filename=filename)

    @app.route('/uploads/<filename>')
    def send_file(filename):
        return send_from_directory('../'+UPLOAD_FOLDER, filename)

    @app.route('/thanks', methods=('GET', 'POST'))
    def thanks():
        if request.method == 'POST':
            if "again" in request.form:
                return redirect(url_for('index'))

        url = "https://vignette.wikia.nocookie.net/gundam/images/a/a7/636723.jpg/revision/latest/scale-to-width-down/600?cb=20141018031606"
        return render_template('thanks.html', url=url)

    @app.route('/training', methods=('GET', 'POST'))
    def training():
        if request.method == 'POST':
            error = None
            if error is None:
                if "confirm" in request.form:
                    return redirect(url_for('thanks'))
            # remember to error if not one of the available labels
            # flash(error)

        url = "https://vignette.wikia.nocookie.net/gundam/images/9/93/00QanTSwordBitsBeam.jpg/revision/latest/scale-to-width-down/600?cb=20120921123309"
        return render_template('training.html', url=url)

    return app
