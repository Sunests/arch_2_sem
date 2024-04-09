## FastAPI

This FastAPI application provides endpoints to manage users.

### Endpoints

#### Search By Name

- **URL:** `/users/search_by_name`
- **Method:** `GET`
- **Parameters:** `first_name`, `last_name`
- **Response Code:** `200 OK`

#### Search By Username

- **URL:** `/users/search_by_username`
- **Method:** `GET`
- **Parameters:** `username`
- **Response Code:** `200 OK`

#### Get User Details

- **URL:** `/users/get_user_details`
- **Method:** `GET`
- **Parameters:** `id`
- **Response Code:** `200 OK`

#### Create User

- **URL:** `/users/create_user`
- **Method:** `POST`
- **Response Code:** `200 OK`

#### Update User

- **URL:** `/users/update_user`
- **Method:** `PUT`
- **Parameters:** `user_id`
- **Response Code:** `200 OK`

#### Remove User

- **URL:** `/users/remove_user`
- **Method:** `DELETE`
- **Parameters:** `user_id`
- **Response Code:** `200 OK`

### Response Objects

- **UserModel:** Represents the structure of a user object.
- **ValidationError:** Represents validation error details.
- **HTTPValidationError:** Represents HTTP validation error details.

---