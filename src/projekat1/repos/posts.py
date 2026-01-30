from __future__ import annotations

from typing import Any

from bson import ObjectId, errors as bson_errors

class PostRepository:
    def __init__(self, db, collection_name: str):
        self.collection = db[collection_name]

    def _serialize(self, doc: dict) -> dict:
        doc = dict(doc)
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        if "userId" in doc:
            doc["user_id"] = doc.pop("userId")
        return doc

    def _to_object_id(self, obj_id: str) -> ObjectId | None:
        try:
            return ObjectId(obj_id)
        except (bson_errors.InvalidId, TypeError):
            return None

    def _to_db(self, payload: dict) -> dict:
        data = dict(payload)
        if "user_id" in data:
            data["userId"] = data.pop("user_id")
        return data

    def list(self, user_id: int | None = None, title: str | None = None) -> list[dict]:
        query: dict[str, Any] = {}
        if user_id is not None:
            query["userId"] = user_id
        if title is not None:
            query["title"] = title

        posts = list(self.collection.find(query))
        return [self._serialize(p) for p in posts]

    def create(self, post: dict) -> str:
        result = self.collection.insert_one(self._to_db(post))
        return str(result.inserted_id)

    def get_by_id(self, obj_id: str) -> dict | None:
        object_id = self._to_object_id(obj_id)
        if object_id is None:
            return None
        doc = self.collection.find_one({"_id": object_id})
        if doc is None:
            return None
        return self._serialize(doc)

    def delete_by_id(self, obj_id: str) -> int:
        object_id = self._to_object_id(obj_id)
        if object_id is None:
            return 0
        result = self.collection.delete_one({"_id": object_id})
        return result.deleted_count

    def update_by_id(self, obj_id: str, post: dict) -> int:
        object_id = self._to_object_id(obj_id)
        if object_id is None:
            return 0
        result = self.collection.update_one({"_id": object_id}, {"$set": self._to_db(post)})
        return result.matched_count

    def patch_by_id(self, obj_id: str, fields: dict) -> int:
        object_id = self._to_object_id(obj_id)
        if object_id is None:
            return 0
        result = self.collection.update_one({"_id": object_id}, {"$set": self._to_db(fields)})
        return result.matched_count


