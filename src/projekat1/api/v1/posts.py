from fastapi import APIRouter, Depends
from projekat1.core.deps import get_post_service
from projekat1.models.posts import PostCreate, PostPatch
from projekat1.services.posts import PostService

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("")
def get_posts(
    user_id: int | None = None,
    title: str | None = None,
    service: PostService = Depends(get_post_service),
):
    return service.list_posts(user_id=user_id, title=title)

@router.get("/{obj_id}")
def get_post(
    obj_id: str,
    service: PostService = Depends(get_post_service),
):
    return service.get_post(obj_id)

@router.post("")
def create_post(
    post: PostCreate,
    service: PostService = Depends(get_post_service),
):
    return service.create_post(post)

@router.delete("/{obj_id}")
def delete_post(
    obj_id: str,
    service: PostService = Depends(get_post_service),
):
    return service.delete_post(obj_id)

@router.put("/{obj_id}")
def update_post(
    obj_id: str,
    post: PostCreate,
    service: PostService = Depends(get_post_service),
):
    return service.update_post(obj_id, post)

@router.patch("/{obj_id}")
def patch_post(
    obj_id: str,
    post: PostPatch,
    service: PostService = Depends(get_post_service),
):
    return service.patch_post(obj_id, post)
