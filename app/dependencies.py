from motor.motor_asyncio import AsyncIOMotorClient
from app.adapters.db_adapter import MongoDBAdapter
from app.adapters.auth_adapter import JWTAdapter
from app.config import Config


client = AsyncIOMotorClient(Config.MONGODB_URL)
db = client.user_service
collection = db.get_collection("users")
db_adapter = MongoDBAdapter(collection=collection)

def get_db_adapter():
    """
    Gibt den globalen Datenbankadapter zurück.
    """
    return db_adapter

jwt_adapter = JWTAdapter(
    secret_key=Config.SECRET_KEY,
    algorithm=Config.ALGORITHM,
    expire_minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
)

def get_jwt_adapter():
    """
    Gibt den JWT-Adapter zurück.
    """
    return jwt_adapter