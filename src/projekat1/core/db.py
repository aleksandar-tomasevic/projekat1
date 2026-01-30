from pymongo import MongoClient
from .config import settings

client = MongoClient(str(settings.MONGO_URI))
db = client[settings.DB_NAME]
collection = db[settings.COLLECTION_NAME]