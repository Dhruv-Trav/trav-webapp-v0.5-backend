from fastapi import FastAPI
from routes.travelogues import router as itinerary_router

app = FastAPI(title="Itinerary CMS")

app.include_router(itinerary_router)
