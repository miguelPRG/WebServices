from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from database import test_database_connection, init_database
from routes.userRoute import userRouter
from routes.reservaRoute import reservaRouter
from controller.jwtValidation import validate_jwt  # ajusta o nome se no teu ficheiro for diferente

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

# Middleware para permitir CORS (Cross-Origin Resource Sharing). CORS é necessário para permitir que o frontend acesse a API, especialmente se estiverem em domínios diferentes.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # mete aqui o URL real do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PUBLIC_PATHS = {
    "/",
    "/user/register",
    "/docs",
    "/openapi.json",
    "/redoc",
}

@app.middleware("http")
async def jwt_cookie_middleware(request: Request, call_next):
    
    path = request.url.path

    # rotas públicas
    if path in PUBLIC_PATHS:
        return await call_next(request)

    token = request.cookies.get("token")
    if not token:
        return JSONResponse(status_code=401, content={"detail": "Não autenticado"})

    try:
        payload = validate_jwt(token)
        if not payload:
            return JSONResponse(status_code=401, content={"detail": "Token inválido"})
        request.state.user = payload
    except Exception:
        return JSONResponse(status_code=401, content={"detail": "Token inválido"})

    return await call_next(request)

# Rotas incluidas
app.include_router(userRouter)
app.include_router(reservaRouter)

@app.get("/", tags=["Root"], description="Returns a greeting message")
def read_root():
    return {"Hello": "World"}
