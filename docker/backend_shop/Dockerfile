FROM python:latest as python_base

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
    # env lang
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # dockerize:
    DOCKERIZE_VERSION=v0.6.1

RUN apt-get update

# Install system dependencies
#RUN apt-get -y install
#    libpq-dev \
#    python-dev

# Install python dependencies
RUN pip install -U --no-cache-dir pip \
    && pip install --no-cache-dir pipenv

# Copy only requirements, to cache them in docker layer:
WORKDIR /pysetup

COPY ./shop/Pipfile ./shop/Pipfile.lock /pysetup/

# Project initialization:
RUN pipenv install --dev --system


FROM python_base as development_build

# Installing `dockerize` utility:
# https://github.com/jwilder/dockerize
RUN wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && rm "dockerize-alpine-linux-amd64-${DOCKERIZE_VERSION}.tar.gz"

# This is a special case. We need to run this script as an entry point:
COPY ./docker/backend_shop/docker-entrypoint.sh ./docker/backend_shop/wait-for-command.sh ./docker/backend_shop/runserver.sh /
RUN chmod +x /docker-entrypoint.sh /wait-for-command.sh /runserver.sh

# This dir will become the mountpoint of development code:
WORKDIR /code

ENTRYPOINT ["/docker-entrypoint.sh"]
