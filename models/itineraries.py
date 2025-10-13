from pydantic import BaseModel, Field, HttpUrl, conint
from typing import List, Optional
from enum import Enum
from datetime import datetime


# ─── Existing Enums ─────────────────────────────────────────────────────────────
class TripType(str, Enum):
    food = "Food"
    pilgrimage = "Pilgrimage"
    trek = "Trek"
    culture = "Culture"
    spiritual = "Spiritual"
    adventure = "Adventure"


class Season(str, Enum):
    SPRING_SUMMER = "Spring/Summer"
    MONSOON = "Monsoon"
    AUTUMN = "Autumn"
    WINTER = "Winter"


class IconType(str, Enum):
    FOOD = "food"
    TREK = "trek"
    CULTURE = "culture"
    SPIRITUAL = "spiritual"


# ─── Models from You (Merged) ─────────────────────────────────────────────────
class TripHighlight(BaseModel):
    icon: IconType
    title: str
    description: str
    background_color: str = Field(..., description="Hex color code for card background")


class BestTimeToVisit(BaseModel):
    months: str = Field(..., description="e.g., 'April - June'")
    season: Season
    weather_description: str
    temperature_range: str = Field(..., description="e.g., '15-25°C'")
    icon_type: str = Field(..., description="check, warning, or snowflake")
    card_background: str = Field(..., description="Hex color for card background")


class ItineraryDay(BaseModel):
        day_title: str
        activities: List[str] = []
        notes: Optional[str] = None
        images: List[HttpUrl] = []


class HowToReachItem(BaseModel):
    mode: str
    description: str
    icon: Optional[str] = None


# ─── FINAL MASTER SCHEMA ─────────────────────────────────────────────────────—
class TripPlan(BaseModel):
    # Hero Metadata
    trip_title: str
    cover_image: Optional[HttpUrl] = None
    days: conint(ge=0)
    nights: conint(ge=0)
    trip_type: List[TripType] = []
    best_season: List[Season] = []
    destinations: List[str] = []

    # Itinerary
    itinerary: List[ItineraryDay] = []

    # Do's & Don'ts
    dos: List[str] = []
    donts: List[str] = []

    # Travel Help
    how_to_reach: List[HowToReachItem] = []

    # Gallery & Notes
    trip_gallery: List[HttpUrl] = []
    travel_notes: List[str] = []

    # ✅ Newly Added from Your Snippet
    highlights: List[TripHighlight]
    best_times: List[BestTimeToVisit]

    # Metadata
    draft_saved: bool = True
    last_saved: Optional[datetime] = None
