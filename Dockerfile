# our base image
FROM alpine:3.8

# Install python and pip
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/
RUN pip install --no-cache-dir -r /usr/src/requirements.txt

# copy files required for the app to run
COPY app/ /usr/src/app/

# tell the port number the container should expose
EXPOSE 5000

# run the application
WORKDIR /usr/src
ENV FLASK_APP app
CMD ["flask", "run", "--host=0.0.0.0"]
