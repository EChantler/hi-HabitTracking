from pydantic import BaseModel

class UserRequest(BaseModel):
    name : str
    email : str

class UserResponse(UserRequest):
    name: str
    email: str
    api_key: str
  