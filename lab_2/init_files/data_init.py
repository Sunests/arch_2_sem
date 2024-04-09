import psycopg2.extras
from typing import List
import psycopg2.extras
import json

import psycopg2
import time


class PSQL:

    def __init__(self, db_name: str = 'postgres') -> None:
        self.db_name = db_name
        self.user = 'sunestss'
        self.password = 'sunestss'
        self.host = 'postgres'
        self.port = '5432'
        while True:
            try:
                self.conn = psycopg2.connect(dbname=self.db_name, user=self.user,
                                             password=self.password, host=self.host, port=self.port)
                break

            except:
                print("Can't connect to postgres")
                time.sleep(1)

    def get_cursor(self) -> psycopg2.extensions.cursor:
        self.cur = self.conn.cursor()
        return self.cur

    def close_connection(self):
        self.cur.close()
        if self.conn:
            self.conn.close()


class PSQLManager:

    @staticmethod
    def init_tables(db_name: str):
        connector: PSQL = PSQL(db_name=db_name)
        cursor = connector.get_cursor()
        cursor.connection.autocommit = True
        with open("./sql_script.sql", "r") as tables_creation_cript:
            cursor.execute(tables_creation_cript.read())

    @staticmethod
    def insert_data(db_name: str, table_name: str, data: List[dict]):
        connector = PSQL(db_name=db_name)
        cursor = connector.get_cursor()
        cursor.connection.autocommit = True
        columns = data[0].keys()
        columns_str = ", ".join(columns)
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES %s"
        data_to_insert = [[i[column] for column in columns] for i in data]
        psycopg2.extras.execute_values(cursor, sql, data_to_insert)

    @staticmethod
    def init_database():
        print("Initialize DB")
        db_name = "arch_db"
        PSQLManager.init_tables(db_name)
        with open("./init_data/users.json", "r") as users:
            users_json = (json.load(users))
            users_list = users_json["users"]
        PSQLManager.insert_data(
            db_name=db_name, table_name="users", data=users_list)


PSQLManager.init_database()
print("Successful initializing")
