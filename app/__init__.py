from flask import Flask, render_template, flash, redirect, request, url_for
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from app import ml_functions as ml, configs
import numpy as np
import sys
from tensorflow import keras
from .decorators import asynch


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

    app.model = keras.models.load_model(app.config['MODEL_LOC'])
    app.model._make_predict_function()

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

        return render_template('index.html')

    @app.route('/result/<filename>', methods=('GET', 'POST'))
    def result(filename):
        img = ml.parse_image(app.config['UPLOAD_FOLDER'] + "/" + filename)

        IMG_ARRAY_LOC = app.config['UPLOAD_FOLDER'] + "/" + filename + ".npz"
        np.savez_compressed(IMG_ARRAY_LOC, new_img=img)

        pred, prob, array = ml.predict_image(img, app.model)
        ml.save_value_array(array, filename)

        if request.method == 'POST':
            if "yes" in request.form:
                return redirect(url_for('thanks',
                                        filename=filename,
                                        label=np.argmax(array)))
            elif "no" in request.form:
                return redirect(url_for('training', filename=filename))
            elif "restart" in request.form:
                return redirect(url_for('index'))

        return render_template('result.html', filename=filename,
                               prediction=pred, probability=prob)

    @app.route('/uploads/<filename>')
    def send_file(filename):
        return send_from_directory('../'+app.config['UPLOAD_FOLDER'], filename)

    @asynch
    def train_model(app, train_img, train_label):
        with app.app_context():
            np.savez_compressed(configs.DATASET_LOC, train_img=train_img,
                                train_label=train_label)
            app.model.fit(train_img, train_label, epochs=10)

    @app.route('/thanks/<filename>&&<label>', methods=('GET', 'POST'))
    def thanks(filename, label):
        if request.method == 'POST':
            if "again" in request.form:
                return redirect(url_for('index'))

        IMG_ARRAY_LOC = app.config['UPLOAD_FOLDER'] + "/" + filename + ".npz"
        if(os.path.isfile(IMG_ARRAY_LOC)):
            with np.load(IMG_ARRAY_LOC) as new_data:
                new_img = new_data['new_img']
            with np.load(configs.DATASET_LOC) as data:
                saved_train_img = data['train_img']
                saved_train_label = data['train_label']
            train_img, train_label = ml.add_training_data(new_img, label,
                                                          saved_train_img,
                                                          saved_train_label)
            train_model(app, train_img, train_label)
            os.remove(IMG_ARRAY_LOC)

        return render_template('thanks.html')

    @app.route('/training/<filename>', methods=('GET', 'POST'))
    def training(filename):
        if request.method == 'POST':
            if "confirm" in request.form:
                if 'labels' not in request.form:
                    flash('Choose a label')
                    return redirect(request.url)
                label = request.form['labels']
                if label == "default":
                    flash('Choose a label')
                    return redirect(request.url)
                else:
                    return redirect(url_for('thanks',
                                            filename=filename,
                                            label=configs.labels.index(label)))

            if "restart" in request.form:
                return redirect(url_for('index'))

        return render_template('training.html', labels=configs.labels[1:])

    @app.after_request
    def add_header(response):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response

    return app
