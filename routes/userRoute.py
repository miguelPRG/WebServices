from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.userModel import UserCreate, UserLogin
import database
from pwdlib import PasswordHash
from datetime import datetime
from controller.jwtValidation import generate_jwt

userRouter = APIRouter(prefix="/user", tags=["User"])
password_hash = PasswordHash.recommended()

@userRouter.post("/register", description="Create a new user")
async def create_user(user: UserCreate):
    if database.user_collection is None:
        raise HTTPException(status_code=500, detail="Base de dados não inicializada")

    existing_user = await database.user_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Já existe um utilizador com esse email")

    user_dict = user.model_dump()
    user_dict["password"] = password_hash.hash(user.password)
    data = datetime.now()
    user_dict["created_at"] = data
    user_dict["updated_at"] = data
    user_dict["last_login"] = None

    try:
        await database.user_collection.insert_one(user_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar utilizador: {str(e)}")

    return {"message": "Utilizador criado com sucesso"}

@userRouter.post("/login", description="Authenticate a user")
async def login_user(user: UserLogin):
    if database.user_collection is None:
        raise HTTPException(status_code=500, detail="Base de dados não inicializada")

    existing_user = await database.user_collection.find_one({"email": user.email})

    if not existing_user or not password_hash.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Email ou password inválidos")

    jwt_token = generate_jwt(str(existing_user["_id"]))

    await database.user_collection.update_one(
        {"_id": existing_user["_id"]},
        {"$set": {"last_login": datetime.now()}}
    )

    response = JSONResponse(content={"message": "Login bem-sucedido"})
    response.set_cookie(
        key="token",
        value=jwt_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=24 * 3600
    )
    return response