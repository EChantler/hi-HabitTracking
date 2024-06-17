

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.core.data.db import Session
from app.core.services.users import UsersService

auth_scheme = APIKeyHeader(name="x-key")  # use token authentication


async def api_key_auth(api_key: str = Depends(auth_scheme)):
    session = Session()
    users_service = UsersService(session)
    user_id = await users_service.get_with_api_key(api_key)
    if(user_id is not None):
        return user_id
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )
        

