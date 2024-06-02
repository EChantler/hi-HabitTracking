from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel, EmailStr
from typing import Any

app = FastAPI()

@app.get("/users/header-sample")
def header_sample(apiKey: Annotated[str | None, Header()] = None):
    return {"ApiKey": apiKey}

@app.get("/users/register")
def register():
    return{success: True}

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user