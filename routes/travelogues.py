from fastapi import APIRouter
from models.travoulage import Itinerary
from controllers.travelogues import create_itinerary, get_all_itineraries

router = APIRouter(prefix="/itineraries", tags=["Itineraries"])

@router.post("/")
async def create(data: Itinerary):
    return await create_itinerary(data)  # call the function directly

@router.get("/")
async def get_all():
    return await get_all_itineraries()  # call the function directly
