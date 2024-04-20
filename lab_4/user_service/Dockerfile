FROM python:3.12
WORKDIR /conference_app

RUN pip install "fastapi[all]" psycopg pyjwt

COPY . /conference_app

ENTRYPOINT ["bash", "-c", "uvicorn main:app --port 8080 --host 0.0.0.0"]