# routes/travelogues.py
from fastapi import APIRouter
from app.models.travoulage import Travelogue
from app.controllers.travelogues import (
    create_travelogue,
    get_all_travelogues,
    get_travelogue,
    update_travelogue,
    delete_travelogue,
)

router = APIRouter(prefix="/travoulage", tags=["Travoulage"]) 

@router.post("/")
async def create(data: Travelogue):
    return await create_travelogue(data)  # call the function directly

@router.get("/")
async def get_all():
    return await get_all_travelogues()  # call the function directly

@router.get("/{id}")
async def get_one(id: str):
    return await get_travelogue(id)  # call the function directly

@router.put("/{id}")
async def update(id: str, data: dict):
    return await update_travelogue(id, data)  # call the function directly

@router.delete("/{id}")
async def delete(id: str):
    return await delete_travelogue(id)  # call the function directly