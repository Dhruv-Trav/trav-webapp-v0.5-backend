from fastapi import APIRouter
from app.models.itineraries import TripPlan
from app.controllers.itineraries import (
    create_trip_plan,
    get_all_trip_plans,
    get_trip_plan,
    update_trip_plan,
    delete_trip_plan,
)

# Use a distinct prefix to avoid clashing with existing /itineraries routes
router = APIRouter(prefix="/itineraries-v2", tags=["Itineraries v2"])

@router.post("/")
async def create(data: TripPlan):
    return await create_trip_plan(data)

@router.get("/")
async def get_all():
    return await get_all_trip_plans()

@router.get("/{id}")
async def get_one(id: str):
    return await get_trip_plan(id)

@router.put("/{id}")
async def update(id: str, data: TripPlan):
    return await update_trip_plan(id, data)

@router.delete("/{id}")
async def delete(id: str):
    return await delete_trip_plan(id)