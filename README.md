# flask-image-rec [![Build Status](https://travis-ci.com/cheukky/flask-image-rec.svg?branch=master)](https://travis-ci.com/cheukky/flask-image-rec)
This goal of this project is to create a web app that allows users to upload pictures of Gundam faces and get a reasonably accurate prediction back

## Pages
### Index
Allows user to upload picture of subject

### Result
Gives user the prediction and allows user to confirm or deny it

### Training
Gives user the chance to apply correct label to image, which is then saved to database and used in subsequent training sets

### Thanks
Allows user to start again

## Usage
Using Python3:

Required to have Python3 installed.

1. Create and activate virtualenv, then populate the environment with the requisite packages
```shell
pip install -r requirements.txt
```

2. Then run the app
```shell
export FLASK_APP=app
flask run
```
Accessible at http://localhost:5000

To Stop:
```
Press CTRL+C
```

Using Docker:

Required to have Docker installed

```shell
docker build -t cheukky/flaskapp .
docker run --rm -p 8888:5000 --name flaskapp cheukky/flaskapp
```
Accessible at http://192.168.99.100:8888/

To Stop:
```shell
docker stop flaskapp
```
