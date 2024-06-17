from typing import Annotated
from fastapi import APIRouter, Depends, Header
from fastapi.encoders import jsonable_encoder

# from app.api.auth import auth_scheme
from app.core.dtos.user import  UserRequest, UserResponse
from app.core.data.db import Session
from app.core.services.users import UsersService
from app.api.auth import api_key_auth, auth_scheme

router = APIRouter()

@router.post("")
async def create_user(user: UserRequest) -> UserResponse:
    session = Session()
    user_service = UsersService(session)
    # return await user_service.add_user(UserDto(name=user.name, email=user.email,api_key=user.apiKey))
    response = await user_service.add_user(user)
    return jsonable_encoder(response)

@router.get("")
async def get_user(user_id: int = Depends(api_key_auth)) -> UserResponse:
    with Session() as session:
        user_service = UsersService(session)
        return await user_service.get(user_id)

    
# @router.get("/{user_id}")
# async def get_user(user_id: int) -> UserResponse:
#     session = Session()
#     user_service = UsersService(session)
#     return await user_service.get(user_id)    

# @router.get("")
# async def get_all_users() -> list[str]:
#     session = Session()
#     user_service = UsersService(session)
#     return await user_service.get_all()
