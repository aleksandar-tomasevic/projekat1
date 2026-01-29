from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, AnyUrl
from pymongo import MongoClient
from bson import ObjectId

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')    
    MONGO_URI: AnyUrl
    DB_NAME: str 
    COLLECTION_NAME: str 

class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str

class PostPatch(BaseModel):
    userId: int | None = None
    id: int | None = None
    title: str | None = None
    body: str | None = None

settings = Settings()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient(str(settings.MONGO_URI))
db = client[settings.DB_NAME]
collection = db[settings.COLLECTION_NAME]

@app.get("/posts")
def get_posts(userId: int = None,title:str=None):
    query = {}
    if userId is not None:
        query["userId"] = userId
    if title is not None:
        query["title"] = title

    posts = list(collection.find(query, {"_id": 0}))
    return posts

@app.get("/posts/{obj_id}")
def get_post(obj_id: str):
    post = collection.find_one({"_id": ObjectId(obj_id)})
    if post:
        post["_id"] = str(post["_id"])
        return post
    else:
        return {"message": "Post nije pronadjen"}, 404

@app.post("/posts")
def create_post(post: Post):
    result = collection.insert_one(post.model_dump())
    return {"message": "Post je uspjesno kreiran"} 

@app.delete("/posts/{obj_id}")
def delete_post(obj_id: str):
    result = collection.delete_one({"_id": ObjectId(obj_id)})
    if result.deleted_count == 1:
        return {"message": "Post je uspjesno obrisan"}
    else:
        return {"message": "Post nije pronadjen"}, 404
    
@app.put("/posts/{obj_id}")
def update_post(obj_id: str, post: Post):
    post = collection.find_one({"_id": ObjectId(obj_id)}, {"_id": 0})
    if result.matched_count == 1:
        collection.update_one({"_id": ObjectId(obj_id)}, {"$set": post.model_dump()})
        return {"message": "Post je uspjesno azuriran"}
    else:
        return {"message": "Post nije pronadjen"}, 404

@app.patch("/posts/{obj_id}")
def patch_post(obj_id: str, post: PostPatch):
    result = collection.update_one({"_id": ObjectId(obj_id)}, {"$set": post.model_dump(exclude_unset=True)})
    if result.matched_count == 1:
        return {"message": "Post je uspjesno zakrpljen ;)"}
    else:
        return {"message": "Post nije pronadjen"}, 404

    