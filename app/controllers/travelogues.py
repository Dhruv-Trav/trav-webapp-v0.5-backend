# controllers/travelogues.py
from fastapi.encoders import jsonable_encoder
from app.config import db
from app.models.travoulage import Travelogue
from pymongo import ReturnDocument

collection = db["travelogues"]

async def _next_travelogue_id() -> str:
    doc = await db["counters"].find_one_and_update(
        {"_id": "travelogues_seq"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    seq = int(doc.get("seq", 1))
    return f"tl-{seq:03d}"

async def create_travelogue(data: Travelogue):
    payload = jsonable_encoder(data, by_alias=True, exclude_none=True)  # exclude None fields
    if not payload.get("id"):
        payload["id"] = await _next_travelogue_id()
    result = await collection.insert_one(payload)
    payload["_id"] = str(result.inserted_id)  # set the inserted ID for response
    return payload

async def get_all_travelogues():
    items = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])  # keep Mongo id as string in responses
        items.append(doc)
    return items

async def get_travelogue(id: str):
    doc = await collection.find_one({"id": id})
    if doc:
        doc["_id"] = str(doc["_id"])  # normalize for response
    return doc

async def update_travelogogue_filter(id: str):
    return {"id": id}

async def update_travelogogue_return(doc):
    if doc:
        doc["_id"] = str(doc["_id"])  # normalize for response
    return doc

async def update_travelogue(id: str, data: dict):
    update_doc = {"$set": jsonable_encoder(data, by_alias=True, exclude_none=True)}  # exclude None fields
    await collection.update_one(await update_travelogogue_filter(id), update_doc)
    doc = await collection.find_one(await update_travelogogue_filter(id))
    return await update_travelogogue_return(doc)

async def delete_travelogue(id: str):
    result = await collection.delete_one({"id": id})
    return {"deleted": result.deleted_count == 1}