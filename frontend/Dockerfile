FROM python:3.7

RUN pip --disable-pip-version-check --no-cache-dir install \
    flask \
    gunicorn

COPY app /app
