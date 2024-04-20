from fastapi import APIRouter, Depends, HTTPException, status, Header
import jwt
from connectors.psql import PSQL
import psycopg
from models.user import UserModel
import hashlib
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta


router = APIRouter()

connection = PSQL(db_name="arch_db")


def get_current_user(token: str):
    try:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials")
    except jwt.DecodeError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials")
    return user_id


@router.get("/")
async def get_all_users(offset: int, limit: int, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    try:
        sql_query = f"SELECT * FROM users OFFSET {offset} LIMIT {limit}"
        cursor.execute(sql_query)
        result = cursor.fetchall()
        cursor.close()
    except Exception as e:
        print(e)
        cursor.close()
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.get("/search_by_name")
async def search_by_name(first_name: str = None, last_name: str = None, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    try:
        result = []
        if first_name and not last_name:
            sql_query = f"SELECT user_id, user_name, first_name, second_name, affiliation FROM users " \
                f"WHERE first_name LIKE '{first_name}%'"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()
        elif not first_name and last_name:
            sql_query = f"SELECT user_id, user_name, first_name, second_name, affiliation FROM users " \
                f"WHERE second_name LIKE '{last_name}%'"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()
        elif first_name and last_name:
            sql_query = f"SELECT user_id, user_name, first_name, second_name, affiliation FROM users " \
                f"WHERE first_name LIKE '{
                    first_name}%' AND second_name LIKE '{last_name}%'"
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()
        else:
            raise HTTPException(
                status_code=404, detail="Need first name or second name")
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Users not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        cursor.close()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search_by_username")
async def search_by_username(username, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    try:
        sql_query = f"""SELECT user_id, user_name, first_name, second_name, affiliation
                        FROM users
                        WHERE user_name LIKE '{username}%'"""
        cursor.execute(sql_query)
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException as e:
        cursor.close()
        raise e
    except Exception as e:
        print(e)
        cursor.close()
        raise e


@router.get("/get_user_details")
async def get_user_details(id: int, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    try:
        sql_query = f"SELECT user_id, user_name, first_name, second_name, affiliation FROM users "\
            "WHERE user_id = %s"
        cursor.execute(sql_query, (id,))
        result = cursor.fetchall()
        cursor.close()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except HTTPException as e:
        cursor.close()
        raise e
    except Exception as e:
        print(e)
        cursor.close()
        raise e


@router.post("/create_user")
async def create_user(new_user: UserModel, cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    try:
        hashed_password = hashlib.sha256(
            new_user.password.encode()).hexdigest()
        sql_query = "INSERT INTO users (user_name, first_name, second_name, affiliation, password) VALUES (%s, %s, %s, %s, %s) RETURNING user_id"
        data = (new_user.user_name, new_user.first_name,
                new_user.second_name, new_user.affiliation, hashed_password)
        cursor.execute(sql_query, data)
        user_id = cursor.fetchone()[0]
        cursor.connection.commit()
    except psycopg.errors.UniqueViolation:
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(status_code=400, detail=f"User with user name {
                            new_user.user_name} already exists")
    except Exception as e:
        print(type(e))
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(status_code=400, detail="Failed to create user")
    cursor.close()
    return {"user_id": user_id}


@router.put("/update_user")
async def update_user(user_id: int, updated_user: UserModel, cursor: psycopg.Cursor = Depends(connection.get_cursor), authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        token_id = get_current_user(authorization.credentials)
        print(token_id, user_id)
        if token_id != user_id:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials")
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
        cursor.close()
    except HTTPException as e:
        cursor.close()
        raise e
    except Exception as e:
        cursor.close()
        raise HTTPException(
            status_code=400, detail="Failed to update user, check your data")
    return {"message": f"User with id user_id successfully updated"}


@router.delete("/remove_user")
async def remove_user(user_id: int, cursor: psycopg.Cursor = Depends(connection.get_cursor), authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        token_id = get_current_user(authorization.credentials)
        print(token_id, user_id)
        if token_id != user_id:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials")
        sql_query = "DELETE FROM users WHERE user_id=%s"
        cursor.execute(sql_query, (user_id,))
        cursor.connection.commit()
        cursor.close()
    except HTTPException as e:
        cursor.close()
        raise e
    except Exception as e:
        print(e)
        cursor.connection.rollback()
        cursor.close()
        raise HTTPException(
            status_code=400, detail="Failed to remove user, check your data")

    return {"message": "successfully removed"}


@router.post("/auth")
async def login_for_access_token(credentials: HTTPBasicCredentials = Depends(HTTPBasic()), cursor: psycopg.Cursor = Depends(connection.get_cursor)):
    sql_query = f"SELECT user_id, password FROM users \n"
    sql_query += f"WHERE users.user_name = %s"
    cursor.execute(sql_query, (credentials.username,))
    result = cursor.fetchone()
    cursor.close()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Basic"},
        )
    hashed_password = hashlib.sha256(
        credentials.password.encode()).hexdigest()
    if hashed_password != result[1]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    to_encode = {"user_id": result[0]}
    expiration = datetime.now() + timedelta(minutes=20)
    to_encode.update({"exp": expiration})
    access_token = jwt.encode(to_encode, "secret_key",
                              algorithm="HS256")
    return {"access_token": access_token, "token_type": "bearer"}
