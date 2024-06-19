
from fastapi import APIRouter
from app.core.data.db import Session

router = APIRouter()

@router.get("")
async def get() -> bool:
    session = Session()
    
    return True