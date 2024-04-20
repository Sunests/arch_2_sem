FROM python:3.12
WORKDIR /init

RUN pip install psycopg && pip install Faker && pip install pymongo

COPY . .

ENTRYPOINT ["bash", "-c", "python init.py"]