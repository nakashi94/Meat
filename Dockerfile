FROM python:3.8

RUN apt-get update -qq

RUN pip install --upgrade pip && \
    pip install flask

RUN mkdir /flask_app

WORKDIR /flask_app

COPY . /flask_app

ENTRYPOINT ["/bin/bash"]
