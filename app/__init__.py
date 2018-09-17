from flask import Flask, render_template, flash, redirect, request, url_for
import os
from werkzeug.utils import secure_filename
import random
from flask import send_from_directory
from app import ml_functions as ml, configs
import numpy as np


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in configs.ALLOWED_EXTENSIONS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = configs.UPLOAD_FOLDER
    app.config['MODEL_LOC'] = configs.MODEL_LOC
    app.config['DATASET_LOC'] = configs.DATASET_LOC
    app.model = ml.load_saved_model(app.config['MODEL_LOC'])

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

        url = random.choice(configs.images)
        return render_template('index.html', url=url)

    @app.route('/result/<filename>', methods=('GET', 'POST'))
    def result(filename):
        if request.method == 'POST':
            if "yes" in request.form:
                return redirect(url_for('thanks'))
            elif "no" in request.form:
                return redirect(url_for('training'))
        img = ml.parse_image(app.config['UPLOAD_FOLDER'] + "/" + filename)
        pred, prob, _ = ml.predict_image(img, app.model)
        return render_template('result.html', filename=filename,
                               prediction=pred, probability=prob)

    @app.route('/uploads/<filename>')
    def send_file(filename):
        return send_from_directory('../'+app.config['UPLOAD_FOLDER'], filename)

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
