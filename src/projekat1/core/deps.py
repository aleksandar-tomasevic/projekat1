from projekat1.core.db import db
from projekat1.core.config import settings
from fastapi import Depends
from projekat1.repos.posts import PostRepository
from projekat1.services.posts import PostService

def get_post_repo() -> PostRepository:
    return PostRepository(db=db, collection_name=settings.COLLECTION_NAME)

def get_post_service(repo: PostRepository = Depends(get_post_repo)) -> PostService:
    return PostService(post_repo=repo)
