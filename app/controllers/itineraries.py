from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from app.config import db
from app.models.itineraries import TripPlan

collection = db["trip_plans"]

async def create_trip_plan(data: TripPlan):
    payload = jsonable_encoder(data, by_alias=True, exclude_none=True)
    result = await collection.insert_one(payload)
    payload["_id"] = str(result.inserted_id)
    return payload

async def get_all_trip_plans():
    items = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])
        items.append(doc)
    return items

async def get_trip_plan(id: str):
    doc = await collection.find_one({"_id": ObjectId(id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

async def update_trip_plan(id: str, data: TripPlan):
    payload = jsonable_encoder(data, by_alias=True, exclude_none=True)
    await collection.update_one({"_id": ObjectId(id)}, {"$set": payload})
    doc = await collection.find_one({"_id": ObjectId(id)})
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

async def delete_trip_plan(id: str):
    res = await collection.delete_one({"_id": ObjectId(id)})
    return {"deleted": res.deleted_count == 1}