from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal, Union
from uuid import UUID

# -------------------- ENUMS --------------------

Orientation = Literal["landscape", "portrait", "square"]
ContentBlockType = Literal[
    "text",
    "image",
    "quote",
    "tags",
    "videos",
    "budget_breakdown",
    "experiences",
    "gallery",
    "journey_route",
    "taste_memories",
    "travel_notes",
    "closing_quote",
    "related_itineraries",
    "related_travelogues"
]

# -------------------- BASE MODELS --------------------

class FocalPoint(BaseModel):
    x: float
    y: float

class CDNVariant(BaseModel):
    quality: int
    format: str
    resize: str
    max_width: int

class ImageAsset(BaseModel):
    image_url: HttpUrl
    alt_text: str
    blurhash: Optional[str] = None
    width: int
    height: int
    aspect_ratio: str
    focal_point: Optional[FocalPoint] = None
    mime_type: str
    size_bytes: int
    orientation: Orientation
    cdn_variant: Optional[CDNVariant] = None

class Author(BaseModel):
    name: str
    avatar: HttpUrl

class VideoItem(BaseModel):
    id: str
    title: str
    url: HttpUrl
    views: str
    creator: str
    thumbnail: HttpUrl
    duration_seconds: int

# -------------------- CONTENT BLOCKS --------------------

class TextBlock(BaseModel):
    type: Literal["text"]
    content: str
    style: Optional[Literal["body", "intro", "highlight"]] = None

class ImageBlock(BaseModel):
    type: Literal["image"]
    image: ImageAsset
    caption: Optional[str] = None

class QuoteBlock(BaseModel):
    type: Literal["quote"]
    content: str
    style: Optional[str] = None

class TagsBlock(BaseModel):
    type: Literal["tags"]
    items: List[str]

class VideosBlock(BaseModel):
    type: Literal["videos"]
    section_title: str
    source: str
    videos: List[VideoItem]

class BudgetBreakdownCategory(BaseModel):
    label: str
    amount: int

class BudgetBreakdownBlock(BaseModel):
    type: Literal["budget_breakdown"]
    title: str
    currency: str
    categories: List[BudgetBreakdownCategory]
    total: int
    show_chart: Optional[bool] = False

class ExperiencesBlock(BaseModel):
    type: Literal["experiences"]
    title: str
    items: List[dict]

class GalleryBlock(BaseModel):
    type: Literal["gallery"]
    title: str
    images: List[ImageAsset]

class JourneyRouteBlock(BaseModel):
    type: Literal["journey_route"]
    title: str
    stops: List[dict]

class TasteMemoriesBlock(BaseModel):
    type: Literal["taste_memories"]
    title: str
    foods: List[str]
    description: str

class TravelNoteItem(BaseModel):
    label: str
    content: str

class TravelNotesBlock(BaseModel):
    type: Literal["travel_notes"]
    title: str
    notes: List[TravelNoteItem]
    tags: Optional[List[str]] = None

class ClosingQuoteBlock(BaseModel):
    type: Literal["closing_quote"]
    content: str
    attribution: Optional[str] = None

class RelatedItineraryItem(BaseModel):
    id: str
    title: str
    author: str
    rating: float
    thumbnail: HttpUrl

class RelatedItinerariesBlock(BaseModel):
    type: Literal["related_itineraries"]
    title: str
    items: List[RelatedItineraryItem]

class RelatedTravelogueItem(BaseModel):
    id: str
    title: str
    category: str
    author: str
    read_time: str
    rating: float
    thumbnail: ImageAsset

class RelatedTraveloguesBlock(BaseModel):
    type: Literal["related_travelogues"]
    title: str
    items: List[RelatedTravelogueItem]

# -------------------- MAIN UNION BLOCK --------------------

ContentBlock = Union[
    TextBlock,
    ImageBlock,
    QuoteBlock,
    TagsBlock,
    VideosBlock,
    BudgetBreakdownBlock,
    ExperiencesBlock,
    GalleryBlock,
    JourneyRouteBlock,
    TasteMemoriesBlock,
    TravelNotesBlock,
    ClosingQuoteBlock,
    RelatedItinerariesBlock,
    RelatedTraveloguesBlock
]

# -------------------- MAIN TRAVELOGUE MODEL --------------------

class TravelogueFilters(BaseModel):
    duration_days: Optional[int] = None
    duration_range: Optional[str] = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    experiences: Optional[List[str]] = None
    perfect_for: Optional[List[str]] = None
    season: Optional[List[str]] = None
    region: Optional[str] = None
    travel_type: Optional[str] = None
    tags: Optional[List[str]] = None

class Travelogue(BaseModel):
    id: Optional[str] = None
    slug: str
    title: str
    subtitle: Optional[str] = None
    published_at: str
    author: Author
    categories: List[str]
    destinations: List[str]
    cover_image: ImageAsset
    content_blocks: List[ContentBlock]
    filter_keys: Optional[TravelogueFilters] = None

# -------------------- METRICS MODEL --------------------

class TravelogueMetrics(BaseModel):
    id: UUID
    date_key: str  # e.g. "TOTAL" or specific date
    views: int
    likes: int
    dislikes: int
    shares: int
    feedback: Optional[dict] = None
    updated_at: str
