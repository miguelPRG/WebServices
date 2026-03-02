from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import test_database_connection, init_database
from routes.userRoute import userRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    if await test_database_connection():
        print("Conexão com MongoDB bem-sucedida. Inicializando banco de dados...")
        if await init_database():
            print("Base de dados inicializada com sucesso.")
    yield

app = FastAPI(
    title="Meu Projeto API",
    tags=["Web Services"],
    lifespan=lifespan,
)

app.include_router(userRouter)

@app.get("/", tags=["Root"], description="Returns a greeting message")
def read_root():
    return {"Hello": "World"}
