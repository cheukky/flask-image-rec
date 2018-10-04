# our base image
FROM tensorflow/tensorflow:1.10.0

#RUN apk add --no-cache --virtual .build-deps build-base python3-dev freetype-dev libpng-dev openblas-dev

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/
RUN pip install --no-cache-dir -r /usr/src/requirements.txt

# copy files required for the app to run
COPY /. /usr/src/

# tell the port number the container should expose
EXPOSE 5000

# run the application
WORKDIR /usr/src
ENV FLASK_APP app
CMD ["flask", "run", "--host=0.0.0.0"]
