from projekat1.models.posts import PostCreate, PostPatch
from projekat1.repos.posts import PostRepository

class PostService:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def list_posts(self, user_id: int | None = None, title: str | None = None):
        return self.post_repo.list(user_id=user_id, title=title)

    def create_post(self, data: PostCreate):
        inserted_id = self.post_repo.create(data.model_dump())
        return {"message": "Post created successfully", "_id": inserted_id}

    def get_post(self, obj_id: str):
        post = self.post_repo.get_by_id(obj_id)
        if post is None:
            return {"message": "Post not found."}, 404
        return post

    def delete_post(self, obj_id: str):
        deleted = self.post_repo.delete_by_id(obj_id)
        if deleted != 1:
            return {"message": "Post not found."}, 404
        return {"message": "Post deleted successfully"}

    def update_post(self, obj_id: str, data: PostCreate):
        matched = self.post_repo.update_by_id(obj_id, data.model_dump())
        if matched != 1:
            return {"message": "Post not found."}, 404
        return {"message": "Post updated successfully"}

    def patch_post(self, obj_id: str, data: PostPatch):
        fields = data.model_dump(exclude_unset=True)
        matched = self.post_repo.patch_by_id(obj_id, fields)
        if matched != 1:
            return {"message": "Post not found."}, 404
        return {"message": "Post patched successfully"}
