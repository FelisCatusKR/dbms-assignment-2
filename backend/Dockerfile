FROM python:3.7

RUN pip --disable-pip-version-check --no-cache-dir install \
    fastapi \
    uvicorn \
    sqlalchemy \
    psycopg2-binary

COPY app /app
