from fastapi.encoders import jsonable_encoder
from app.config import db
from app.models.itineraries import Itinerary
from pymongo import ReturnDocument
import re

collection = db["itineraries"]

def _slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")

async def _ensure_unique_slug(base_slug: str, exclude_id: str | None = None) -> str:
    slug = base_slug
    i = 2
    while True:
        query = {"slug": slug}
        if exclude_id:
            query["id"] = {"$ne": exclude_id}
        exists = await collection.find_one(query)
        if not exists:
            return slug
        slug = f"{base_slug}-{i}"
        i += 1

async def _next_itinerary_id() -> str:
    doc = await db["counters"].find_one_and_update(
        {"_id": "itineraries_seq"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    seq = int(doc.get("seq", 1))
    return f"itinerary_{seq:03d}"

async def create_itinerary(data: Itinerary):
    payload = jsonable_encoder(data, by_alias=True, exclude_none=True)
    if not payload.get("id"):
        payload["id"] = await _next_itinerary_id()
    if not payload.get("slug") and payload.get("title"):
        base_slug = _slugify(payload["title"]) or payload["id"]
        payload["slug"] = await _ensure_unique_slug(base_slug)
    result = await collection.insert_one(payload)
    payload["_id"] = str(result.inserted_id)
    return payload

async def get_all_itineraries():
    items = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])  # normalize
        items.append(doc)
    return items

async def get_itinerary(id: str):
    doc = await collection.find_one({"id": id})
    if doc:
        doc["_id"] = str(doc["_id"])  # normalize
    return doc

async def update_itinerary(id: str, data: dict):
    set_doc = jsonable_encoder(data, by_alias=True, exclude_none=True)
    if ("title" in set_doc) and (not set_doc.get("slug")):
        base_slug = _slugify(set_doc["title"]) if set_doc.get("title") else None
        if base_slug:
            set_doc["slug"] = await _ensure_unique_slug(base_slug, exclude_id=id)
    update_doc = {"$set": set_doc}
    await collection.update_one({"id": id}, update_doc)
    doc = await collection.find_one({"id": id})
    if doc:
        doc["_id"] = str(doc["_id"])  # normalize
    return doc

async def delete_itinerary(id: str):
    res = await collection.delete_one({"id": id})
    return {"deleted": res.deleted_count == 1}