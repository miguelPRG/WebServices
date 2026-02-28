from fastapi import APIRouter
from models.userModel import User

userRouter = APIRouter(prefix="/users", tags=["Users"])

@userRouter.post("/", description="Create a new user")
async def create_user(user: User):
    pass
