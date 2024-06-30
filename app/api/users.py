from fastapi import APIRouter, Depends
from app.core.dtos.user import  UserRequest, UserResponse
from app.core.data.db import Session
from app.core.services.users import UsersService
from app.api.auth import api_key_auth

router = APIRouter()

@router.post("")
async def create_user(user: UserRequest) -> UserResponse:
    with Session() as session:
        user_service = UsersService(session)
        return await user_service.add_user(user)

@router.get("")
async def get_user(user_id: int = Depends(api_key_auth)) -> UserResponse:
    with Session() as session:
        user_service = UsersService(session)
        return await user_service.get(user_id)
