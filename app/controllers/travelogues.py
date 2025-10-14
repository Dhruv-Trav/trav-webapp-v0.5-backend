# controllers/travelogues.py
from fastapi.encoders import jsonable_encoder
from app.config import db
from app.models.travoulage import Travelogue
from bson import ObjectId

collection = db["travelogues"]

async def create_travelogue(data: Travelogue):
    payload = jsonable_encoder(data, by_alias=True, exclude_none=True)  # exclude None fields
    result = await collection.insert_one(payload)
    payload["_id"] = str(result.inserted_id)  # set the inserted ID for response
    return payload

async def get_all_travelogues():
    items = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])
        items.append(doc)
    return items

async def get_travelogue(id: str):
    doc = await collection.find_one({"_id": ObjectId(id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

async def update_travelogue(id: str, data: dict):
    update_doc = {"$set": jsonable_encoder(data, by_alias=True, exclude_none=True)}  # exclude None fields
    await collection.update_one({"_id": ObjectId(id)}, update_doc)
    doc = await collection.find_one({"_id": ObjectId(id)})
    if doc:
        doc["_id"] = str(doc["_id"])  # set the inserted ID for response
    return doc

async def delete_travelogue(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    return {"deleted": result.deleted_count == 1}