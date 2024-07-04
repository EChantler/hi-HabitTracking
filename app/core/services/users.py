
from datetime import datetime
from app.core.data.db import User
from app.core.dtos.user import UserRequest, UserResponse
import secrets
import string

class UsersService:
    def __init__(self, session):
        self.session = session

    async def get(self, user_id:int):
        '''Get a specific user'''
        user = self.session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return UserResponse(name = user.name, email = user.email, api_key = user.apiKey)
    
    async def add_user(self, user_dto:UserRequest):
        '''Add a new user. Returns UserResponse with api_key'''
        api_key = self.__generate_api_key(10)
        user = User(name = user_dto.name, email = user_dto.email, apiKey = api_key , created_on_utc = datetime.now())
        self.session.add(user)
        self.session.commit()
        return UserResponse(name = user_dto.name, email = user_dto.email, api_key = api_key)
    
    def __generate_api_key(self, length):
        characters = string.ascii_letters + string.digits
        api_key = ''.join(secrets.choice(characters) for _ in range(length))
        return api_key
    
    async def get_with_api_key(self, api_key:string):
        '''Get a user's id by api_key. Returns None if not found'''
        user = self.session.query(User).filter(User.apiKey == api_key).first()
        if(user is not None):
            return user.id
        return None