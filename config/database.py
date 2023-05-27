from pymongo import mongo_client

from config.config import settings


def connect_db():
    database_url = (
        f"mongodb+srv://{settings.MONGO_USER}:{settings.MONGO_PASS}@parser.0dyse3y.mongodb.net/?retryWrites=true&w=majority",
    )
    client = mongo_client.MongoClient(database_url)
    db = client[settings.MONGO_DB]
    return db
