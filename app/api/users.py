from fastapi import APIRouter

from app.core.dtos.user import  UserRequest, UserResponse
from app.core.data.db import Session
from app.core.services.users import UsersService

router = APIRouter()

@router.post("")
async def create_user(user: UserRequest) -> UserResponse:
    session = Session()
    user_service = UsersService(session)
    # return await user_service.add_user(UserDto(name=user.name, email=user.email,api_key=user.apiKey))
    response = await user_service.add_user(user)
    return response
@router.get("/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    session = Session()
    user_service = UsersService(session)
    return await user_service.get(user_id)    

@router.get("")
async def get_all_users() -> list[str]:
    session = Session()
    user_service = UsersService(session)
    return await user_service.get_all()
