FROM python:3.8

RUN apt-get update -qq

RUN pip install --upgrade pip && \
    pip install flask && \
    pip install sqlalchemy && \
    pip install flask_login && \
    pip install flask_wtf && \
    pip install wtforms && \
    pip install flask_sqlalchemy

RUN mkdir /flask_app

WORKDIR /flask_app

COPY . /flask_app

ENTRYPOINT ["/bin/bash"]
