from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal, Dict
from datetime import datetime

# ─── Image Types ─────────────────────────────────────────────────────────────
class FocalPoint(BaseModel):
    x: float
    y: float


class ImageAsset(BaseModel):
    image_url: HttpUrl
    alt_text: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    aspect_ratio: Optional[str] = None
    focal_point: Optional[FocalPoint] = None
    mime_type: Optional[str] = None
    orientation: Optional[Literal["landscape", "portrait", "square"]] = None


# ─── Day Plans ───────────────────────────────────────────────────────────────
class Activity(BaseModel):
    id: Optional[str] = None
    time: Optional[str] = None
    title: str
    subtitle: Optional[str] = None
    type: Optional[str] = None  # arrival | transfer | activity | temple visit
    location: Optional[str] = None
    distance_km: Optional[float] = None  # can represent meters too (frontend uses numeric)
    duration_minutes: Optional[int] = None
    # save only UI icon key (e.g., 'plane', 'car', 'trek', 'hotel', 'food', 'camera')
    icon: Optional[str] = None
    # CHANGED: align with frontend multi-tag input
    activitytags: Optional[List[str]] = None
    activity_images: List[ImageAsset] = []  # optional images for this activity


class DayImage(BaseModel):
    image_url: HttpUrl
    alt_text: Optional[str] = None
    sort_order: Optional[int] = None


class DayPlan(BaseModel):
    day: int
    title: str
    activities: List[Activity] = []
    day_images: List[DayImage] = []
    notes: Optional[str] = None


# ─── Sections ────────────────────────────────────────────────────────────────
class DoAndDonts(BaseModel):
    # Frontend sends only strings; UI uses common check/cross icons
    dos: List[str] = []
    donts: List[str] = []


# How to Reach as a list of modes (icon/color keys + title/description)
# EXTENDED: include 'bicycle' and 'ship' to match UI usage
TravelIconKey = Literal["plane", "train", "bus", "car", "bicycle", "ship"]
TravelColorKey = Literal["blue", "green", "orange", "purple"]


class TravelMode(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    icon: TravelIconKey
    color: TravelColorKey


class HowToReach(BaseModel):
    modes: List[TravelMode] = []


# Trip gallery
class TripGalleryItem(BaseModel):
    id: Optional[str] = None
    image_url: HttpUrl
    caption: Optional[str] = None
    uploaded_at: Optional[datetime] = None


# Budget and insights (unchanged)
class BudgetItem(BaseModel):
    item: str
    range: str


class LocalInsights(BaseModel):
    budget_planning: List[BudgetItem] = []
    connectivity: Optional[str] = None
    etiquette: List[str] = []


# Best time to visit aligned to frontend visuals
SeasonIconKey = Literal["sun", "rain", "wind", "snow"]  # extend as needed
IndicatorColorKey = Literal["bg-green-100", "bg-yellow-100", "bg-blue-100"]  # store key; UI maps to Tailwind


class BestTimeEntry(BaseModel):
    id: Optional[str] = None
    period: str             # e.g., "April - June"
    name: str               # e.g., "Spring/Summer"
    description: Optional[str] = None
    indicator_color: Optional[IndicatorColorKey] = None
    icon: Optional[SeasonIconKey] = None


class BestTimeToVisit(BaseModel):
    entries: List[BestTimeEntry] = []


# Filters (unchanged)
class Filters(BaseModel):
    duration_days: Optional[int] = None
    categories: Optional[List[str]] = None
    budget_tier: Optional[str] = None
    best_season: Optional[List[str]] = None
    perfect_for: Optional[List[str]] = None
    filter_keys: Optional[List[str]] = None


# ─── Route Map (unchanged) ───────────────────────────────────────────────────
class RouteStop(BaseModel):
    order: int
    name: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    type: Optional[str] = None  # stay | sight | food | activity | transport
    description: Optional[str] = None
    icon: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    duration_minutes: Optional[int] = None
    tags: Optional[List[str]] = None


class RouteDay(BaseModel):
    day: int
    title: str
    stops: List[RouteStop] = []


class RouteMap(BaseModel):
    interactive: Optional[bool] = None
    total_stops: Optional[int] = None
    map_center: Optional[Dict[str, float]] = None  # { lat, lng, zoom }
    days: List[RouteDay] = []


# ─── Metrics (unchanged) ─────────────────────────────────────────────────────
class ItineraryMetrics(BaseModel):
    id: str
    content_id: str
    date_key: str  # e.g., TOTAL or date
    views: int
    likes: int
    shares: Optional[int] = 0
    saves: Optional[int] = 0
    feedback_inspiring: Optional[int] = 0
    feedback_not_useful: Optional[int] = 0
    avg_read_time_seconds: Optional[int] = 0
    engagement_rate: Optional[float] = 0.0
    updated_at: str


# ─── Travel Notes updated to support UI type/color ───────────────────────────
NoteTypeKey = Literal["info", "warning", "tip"]


class TravelNote(BaseModel):
    id: Optional[str] = None
    text: str
    # store only the type key; UI maps to colors/icons
    type: NoteTypeKey


# ─── Getting Around (NEW) ────────────────────────────────────────────────────
class GettingAroundOption(BaseModel):
    id: Optional[str] = None
    title: str
    subtitle: Optional[str] = None
    price1_label: Optional[str] = None
    price1_value: Optional[str] = None
    price2_label: Optional[str] = None
    price2_value: Optional[str] = None
    note: Optional[str] = None
    icon: TravelIconKey
    color: TravelColorKey


class GettingAround(BaseModel):
    city: str
    options: List[GettingAroundOption] = []


# ─── MAIN ITINERARY MODEL ────────────────────────────────────────────────────
class Itinerary(BaseModel):
    id: Optional[str] = None  # e.g., itinerary_001
    version: Optional[int] = 1
    status: Optional[Literal["draft", "in_review", "published", "archived"]] = "draft"

    title: str
    subtitle: Optional[str] = None
    slug: Optional[str] = None

    cover_image: ImageAsset

    destinations: List[str]
    categories: List[str]
    duration_days: int
    budget_tier: Optional[str] = None
    best_season: List[str] = []
    perfect_for: List[str] = []

    # Day-wise plan aligned to UI (activities include icon key)
    daywise_plan: List[DayPlan] = []

    # Do's & Don'ts as plain strings
    do_and_donts: Optional[DoAndDonts] = None

    # How to reach aligned to UI (list of modes with keys)
    how_to_reach: Optional[HowToReach] = None

    # Trip gallery with id/url/caption/uploaded_at
    trip_gallery: List[TripGalleryItem] = []

    local_insights: Optional[LocalInsights] = None

    # Travel notes aligned to UI (type + text)
    travel_notes: List[TravelNote] = []

    # Highlights as simple strings (UI shows list)
    highlights: List[str] = []

    # Best time to visit aligned to UI entries
    best_time_to_visit: Optional[BestTimeToVisit] = None

    # NEW: Getting Around
    getting_around: Optional[GettingAround] = None

    created_at: Optional[str] = None
    last_updated: Optional[str] = None
    updated_by: Optional[str] = None
    deleted_at: Optional[str] = None

    filters: Optional[Filters] = None
    route_map: Optional[RouteMap] = None