FROM python:3.10.0-alpine

LABEL maintainer='slawomir.pawlik'

ENV PYTHONUNBUFFERED 1


COPY ./app /app
COPY ./pyproject.toml /app

WORKDIR /app
EXPOSE 8000
ARG DEV=false

RUN apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev && \
    apk add curl && \
    apk del .tmp-build-deps

RUN pip install pip --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --with main

RUN if [ $ARG == "true" ];  \
      then \
        RUN poetry install --with dev ; \
    fi
RUN adduser --disabled-password\
            --no-create-home \
            django-user

USER django-user
