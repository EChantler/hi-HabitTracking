

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from app.core.data.db import Session, User



auth_scheme = APIKeyHeader(name="x-key")  # use token authentication


def api_key_auth(api_key: str = Depends(auth_scheme)):
    with Session() as session:
        user = session.query(User).filter(User.apiKey == api_key).first()
        print(f"User: {user}")
        if(user is not None):
            return user.id
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Forbidden"
            )
        

