from fastapi import APIRouter
from app.models.itineraries import Itinerary
from app.controllers.itineraries import (
    create_itinerary,
    get_all_itineraries,
    get_itinerary,
    update_itinerary,
    delete_itinerary,
)

# Use a distinct prefix to avoid clashing with existing /itineraries routes
router = APIRouter(prefix="/itineraries", tags=["Itineraries v2"])

@router.post("")
@router.post("/")
async def create(data: Itinerary):
    return await create_itinerary(data)

@router.get("")
@router.get("/")
async def get_all():
    return await get_all_itineraries()

@router.get("/{id}")
async def get_one(id: str):
    return await get_itinerary(id)

@router.put("/{id}")
async def update(id: str, data: dict):
    return await update_itinerary(id, data)

@router.delete("/{id}")
async def delete(id: str):
    return await delete_itinerary(id)