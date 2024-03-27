from fastapi import APIRouter, Depends
from connectors.psql import PSQL
import psycopg2
from models.user import UserModel
import hashlib

router = APIRouter()

connection = PSQL(db_name="arch_db")


@router.get("/search_by_name")
async def search_by_name(first_name: str, last_name: str, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    sql_query = f"SELECT user_id, user_name, first_name, second_name, affiliation FROM users " \
        f"WHERE first_name LIKE '{
            first_name}%' AND second_name LIKE '{last_name}%'"
    cursor.execute(sql_query)
    return cursor.fetchall()


@router.get("/search_by_username")
async def search_by_username(username, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    sql_query = f"""SELECT user_id, user_name, first_name, second_name, affiliation
                    FROM users
                    WHERE user_name LIKE '{username}%'"""
    cursor.execute(sql_query)
    return cursor.fetchone()


@router.get("/get_user_details")
async def get_user_details(id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    sql_query = f"SELECT user_id, user_name, first_name, second_name, affiliation FROM users "\
        f"WHERE user_id = {id}"
    cursor.execute(sql_query)
    result = cursor.fetchall()
    return result


@router.post("/create_user")
async def create_user(new_user: UserModel, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        hashed_password = hashlib.sha256(
            new_user.password.encode()).hexdigest()
        sql_query = "INSERT INTO users (user_name, first_name, second_name, affiliation, password) VALUES (%s, %s, %s, %s, %s)"
        data = (new_user.user_name, new_user.first_name,
                new_user.second_name, new_user.affiliation, hashed_password)
        cursor.execute(sql_query, data)
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        return {"error": "Failed to create user"}, 500
    return {}, 200


@router.put("/update_user")
async def update_user(user_id: int, updated_user: UserModel, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        if updated_user.password:
            updated_user.password = hashlib.sha256(
                updated_user.password.encode()).hexdigest()
        updated_user_dict = UserModel.model_dump(
            updated_user, exclude_none=True)
        columns_to_update = ', '.join(
            [f"{key} = %s" for key in updated_user_dict.keys()])
        sql_query = f"UPDATE users SET {columns_to_update} WHERE user_id = %s"
        values = list(updated_user_dict.values())
        cursor.execute(sql_query, values + [user_id])
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        return {"error": "Failed to update user"}, 500
    return {}, 200


@router.delete("/remove_user")
async def remove_user(user_id: int, cursor: psycopg2.extensions.cursor = Depends(connection.get_cursor)):
    try:
        sql_query = "DELETE FROM users WHERE user_id=%s"
        cursor.execute(sql_query, (user_id,))
        cursor.connection.commit()
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        return {"error": "Failed to remove user"}, 500
    return {}, 200
