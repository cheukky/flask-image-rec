# flask-image-rec
This goal of this project is to create a web app that allows users to upload pictures of Gundam faces and get a reasonably accurate prediction back

## Index
Allows user to upload picture of subject

## Result
Gives user the prediction and allows user to confirm or deny it

## Training
Gives user the chance to apply correct label to image, which is then saved to database and used in subsequent training sets

## Thanks
Allows user to start again


Run Flask app:
```shell
export FLASK_APP=app.py
flask run
```

To Stop:
Press CTRL+C

Run Dockerfile:
```shell
docker build -t cheukky/flaskapp .
docker run --rm -p 8888:5000 --name flaskapp cheukky/flaskapp
```

To Stop:
```shell
docker stop flaskapp
```
