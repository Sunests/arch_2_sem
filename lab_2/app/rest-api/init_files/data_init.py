import psycopg2.extras
from connectors.psql import PSQL
from typing import List
import psycopg2.extras
import json


class PSQLManager:

    @staticmethod
    def init_tables(db_name: str):
        connector: PSQL = PSQL(db_name=db_name)
        cursor = connector.get_cursor()
        cursor.connection.autocommit = True
        with open("./init_files/sql_script.sql", "r") as tables_creation_cript:
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
        with open("./init_files/init_data/users.json", "r") as users:
            users_json = (json.load(users))
            users_list = users_json["users"]
        PSQLManager.insert_data(
            db_name=db_name, table_name="users", data=users_list)
