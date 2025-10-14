from fastapi import FastAPI
from app.routes.travelogues import router as travelogues_router
from app.routes.itineraries import router as itineraries_v2_router

app = FastAPI(title="Itinerary CMS")

app.include_router(travelogues_router)
app.include_router(itineraries_v2_router)