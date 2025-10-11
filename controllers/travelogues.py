from fastapi.encoders import jsonable_encoder
from config import db
from models.travoulage import Itinerary
from bson import ObjectId

collection = db["itineraries"]

async def create_itinerary(data: Itinerary):
    payload = jsonable_encoder(data, by_alias=True, exclude_none=True)  # exclude None fields
    result = await collection.insert_one(payload)
    payload["_id"] = str(result.inserted_id)  # set the inserted ID for response
    return payload


async def get_all_itineraries():
    items = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])
        items.append(doc)
    return items

async def get_itinerary(id: str):
    doc = await collection.find_one({"_id": ObjectId(id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc
