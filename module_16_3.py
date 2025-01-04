from fastapi import FastAPI, Path, HTTPException
from typing import Annotated

app = FastAPI()
users = {'1': 'Имя: Example, возраст: 18'}


@app.get("/users")
async def get_all_messages() -> dict:
    return users


@app.post("/user/{username}/{age}")
async def create_message(
        username: Annotated[str, Path(min_length=1, max_length=20, description="Enter username", example="Dmit")],
        age: int = Path(ge=1, le=100, description="Enter age", example=18)) -> dict:
    user_id = str(int(max(users, key=int)) + 1)
    message = f"Имя: {username}, возраст: {age}"
    users[user_id] = message
    return {"message": f"User {user_id} is registered"}


@app.put("/user/{user_id}/{username}/{age}")
async def update_message(
        username: Annotated[str, Path(min_length=1, max_length=20, description="Enter username", example="Dmit")],
        age: int = Path(ge=1, le=100, description="Enter age", example=18),
        user_id: int = Path(ge=0)) -> dict:
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"The user {user_id} is updated"}


@app.delete('/user/{user_id}')
async def delete_user(user_id: str) -> str:
    if user_id in users:
        users.pop(user_id)
        return f'Пользователь {user_id} удалён'
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
