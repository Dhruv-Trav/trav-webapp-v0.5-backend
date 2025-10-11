from pydantic import BaseModel, HttpUrl, Field, validator
from typing import List, Union, Optional, Literal
from datetime import datetime

# --- Content Block Types ---

class ParagraphBlock(BaseModel):
    type: Literal["paragraph"] = "paragraph"
    text: str

class QuoteBlock(BaseModel):
    type: Literal["quote"] = "quote"
    text: str

class ImageBlock(BaseModel):
    type: Literal["image"] = "image"
    url: HttpUrl
    alt_text: str
    caption: Optional[str] = None

class YouTubeBlock(BaseModel):
    type: Literal["youtube"] = "youtube"
    url: HttpUrl
    title: Optional[str] = None

class PhotoGridBlock(BaseModel):
    type: Literal["photo_grid"] = "photo_grid"
    images: List[ImageBlock]

ContentBlock = Union[ParagraphBlock, QuoteBlock, ImageBlock, YouTubeBlock, PhotoGridBlock]


# --- Cover Image ---

class CoverImage(BaseModel):
    url: HttpUrl
    alt_text: str


# --- Main Itinerary Schema ---

class Itinerary(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    version: int = 1
    status: Literal["draft", "in_review", "published", "archived"] = "draft"
    
    title: str = Field(..., max_length=120)
    subtitle: str = Field(..., max_length=160)
    slug: str
    
    cover_image: CoverImage
    categories: List[str]
    destinations: List[str]
    content_blocks: List[ContentBlock]
    
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @validator("slug")
    def slug_format(cls, v):
        return v.lower().replace(" ", "-")
