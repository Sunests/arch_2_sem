FROM python:3.12
WORKDIR /init

RUN pip install psycopg2-binary

COPY . /init

ENTRYPOINT ["bash", "-c", "python3 data_init.py"]