import os
from dotenv import load_dotenv
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
from pymongo.errors import PyMongoError

load_dotenv()  # garante leitura do .env

MONGO_URI = os.getenv("MONGO_URL")
MONGO_DB_NAME = "Web"

if not MONGO_URI:
    raise RuntimeError("MONGO_URL não foi carregada do .env")

client: AsyncIOMotorClient | None = None
db: AsyncIOMotorDatabase | None = None

# Exportáveis para outros ficheiros
user_collection: AsyncIOMotorCollection | None = None
sala_collection: AsyncIOMotorCollection | None = None
user_sala_collection: AsyncIOMotorCollection | None = None


async def test_database_connection(uri: str | None = None) -> bool:
    mongo_uri = uri or MONGO_URI
    local_client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
    try:
        await local_client.admin.command("ping")
        return True
    except PyMongoError as e:
        print("Erro ao conectar ao MongoDB: ", str(e))
        return False
    finally:
        local_client.close()


async def init_database(uri: str | None = None, db_name: str | None = None) -> bool:
    global client, db, user_collection, sala_collection, user_sala_collection

    mongo_uri = uri or MONGO_URI
    mongo_db_name = db_name or MONGO_DB_NAME

    tmp_client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
    try:
        await tmp_client.admin.command("ping")
        client = tmp_client
        db = client[mongo_db_name]

        user_collection = db["users"]
        sala_collection = db["salas"]
        user_sala_collection = db["user_salas"]
        return True
    except PyMongoError:
        tmp_client.close()
        client = None
        db = None
        user_collection = None
        sala_collection = None
        user_sala_collection = None
        return False
