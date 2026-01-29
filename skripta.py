import aiohttp
import asyncio
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, ValidationError, HttpUrl
from pymongo import MongoClient, UpdateOne

MONGO_URI = "mongodb://localhost:27018"
DB_NAME = "test_db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')    
    BASE_URL: HttpUrl

class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str
url = f"{Settings().BASE_URL}/posts"


async def fetch_posts():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    
    valid = []

    for item in data:
        try:
            post = Post(**item)
            valid.append(post.model_dump())
        except ValidationError as e:
            print(f"error sa {item['id']}: {e}")
    
    return valid

def main():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db["posts"]

    posts = asyncio.run(fetch_posts())

    operations = [
        UpdateOne({'id': post['id']}, {'$set': post}, upsert=True)
        for post in posts
    ]

    print(f"Inserting {len(operations)} posts...")
    if operations:
        result = collection.bulk_write(operations)
        print(f"Inserted: {result.upserted_count}, Modified: {result.modified_count}")
    else:
        print("Nema validnih.")

if __name__ == "__main__":
    main()
