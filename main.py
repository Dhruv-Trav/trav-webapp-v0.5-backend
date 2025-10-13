from fastapi import FastAPI
from routes.travelogues import router as itinerary_router
from routes.itineraries import router as itineraries_v2_router

app = FastAPI(title="Itinerary CMS")

app.include_router(itinerary_router)
app.include_router(itineraries_v2_router)
