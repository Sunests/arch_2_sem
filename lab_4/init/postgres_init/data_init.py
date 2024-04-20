from typing import List
import json
import psycopg
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
                self.conn = psycopg.connect(dbname=self.db_name, user=self.user,
                                            password=self.password, host=self.host, port=self.port)
                break
            except:
                print("Can't connect to postgres")
                time.sleep(1)

    def get_cursor(self) -> psycopg.Cursor:
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
        with open("./postgres_init/sql_script.sql", "r") as tables_creation_cript:
            cursor.execute(tables_creation_cript.read())

    @staticmethod
    def insert_data(db_name: str, table_name: str, data: List[dict]) -> List[int]:
        connector = PSQL(db_name=db_name)
        cursor = connector.get_cursor()
        cursor.connection.autocommit = True
        columns = data[0].keys()
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({
            placeholders}) RETURNING user_id"
        inserted_ids = []
        for row in data:
            values = [row[column] for column in columns]
            try:
                cursor.execute(sql, values)
                inserted_ids.append(cursor.fetchone()[0])
            except psycopg.Error as e:
                print(f"Error inserting row: {e}")
        return inserted_ids

    @staticmethod
    def init_database() -> List[int]:
        print("Initialize DB")
        db_name = "arch_db"
        PSQLManager.init_tables(db_name)
        with open("./postgres_init/init_data/users.json", "r") as users:
            users_json = (json.load(users))
            users_list = users_json["users"]
        users_ids = PSQLManager.insert_data(
            db_name=db_name, table_name="users", data=users_list)
        print("Postgress successfully inited")
        return users_ids
