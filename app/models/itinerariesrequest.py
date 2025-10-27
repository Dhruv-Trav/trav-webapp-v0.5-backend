from typing import List, Optional, Dict
from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import date, datetime
from enum import Enum


# =====================================================
# ENUMS
# =====================================================

class PriorityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Visibility(str, Enum):
    internal = "internal"
    requester_visible = "requester_visible"


class Status(str, Enum):
    new = "new"
    under_review = "under_review"
    approved = "approved"
    rejected = "rejected"


class Role(str, Enum):
    admin = "Admin"
    editor = "Editor"
    reviewer = "Reviewer"
    contributor = "Contributor"
    viewer = "Viewer"


# =====================================================
# COMMON MODELS
# =====================================================

class Person(BaseModel):
    id: str
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    verified: Optional[bool] = None
    total_trips: Optional[int] = None


class DateRange(BaseModel):
    from_date: date
    to_date: date


class Budget(BaseModel):
    min: float
    max: float
    currency: str


class SpecialRequirements(BaseModel):
    dietary: Optional[List[str]] = []
    accessibility: Optional[str] = None
    interests: Optional[List[str]] = []


class Attachment(BaseModel):
    name: str
    url: HttpUrl
    mime_type: str
    size_bytes: int


class Timeline(BaseModel):
    submitted_at: datetime
    assigned_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None


class WorkflowMeta(BaseModel):
    review_deadline: datetime
    escalation_threshold: str
    sla_hours: int


# =====================================================
# MAIN ENTITY: ITINERARY REQUEST
# =====================================================

class ItineraryRequest(BaseModel):
    id: str
    type: str = "itinerary_request"
    requester: Person

    destinations: List[str]
    categories: List[str]

    duration: Dict[str, int]  # {"days": 7, "nights": 6}
    preferred_dates: DateRange
    notes: Optional[str] = None
    budget: Budget
    group_size: int

    accommodation: Optional[str] = None
    transportation: Optional[str] = None
    special_requirements: Optional[SpecialRequirements] = None

    priority_level: PriorityLevel
    tags: Optional[List[str]] = []

    status: Status
    assigned_to: Optional[Person] = None
    stage: Optional[str] = None

    attachments: Optional[List[Attachment]] = []
    timeline: Timeline
    workflow_meta: WorkflowMeta


# =====================================================
# COMMENTS
# =====================================================

class RequestComment(BaseModel):
    id: str
    request_id: str
    author: Person
    content: str
    attachments: Optional[List[Attachment]] = []
    mentions: Optional[List[str]] = []
    created_at: datetime
    visibility: Visibility


# =====================================================
# ACTIVITY LOG (IMMUTABLE)
# =====================================================

class RequestActivityLog(BaseModel):
    id: str
    request_id: str
    actor: Person
    action: str
    from_status: Optional[Status] = None
    to_status: Optional[Status] = None
    timestamp: datetime
    meta: Optional[Dict] = {}


# =====================================================
# METRICS (AGGREGATED)
# =====================================================

class RequestMetrics(BaseModel):
    id: str
    request_id: str
    total_comments: int
    total_assignments: int
    status_history: Dict[str, int]
    avg_response_time_hours: float
    total_handling_time_hours: float
    review_iterations: int
    engagement_score: float
    updated_at: datetime


# =====================================================
# TEAM PERFORMANCE
# =====================================================

class TeamPerformance(BaseModel):
    id: str
    user_id: str
    name: str
    requests_handled: int
    avg_response_time_hours: float
    approval_rate: float
    last_active: datetime


# =====================================================
# APPROVAL QUEUE
# =====================================================

class ApprovalQueue(BaseModel):
    id: str
    content_type: str
    content_id: str
    assigned_reviewer: Person
    status: Status
    priority: PriorityLevel
    preflight_score: int
    review_guidelines: Dict[str, str]
    last_updated: datetime


# =====================================================
# USER MANAGEMENT
# =====================================================

class TeamMember(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Role
    status: str
    last_active: datetime
    requests_handled: int
    assigned_tasks: int


class Permission(BaseModel):
    create: bool
    edit: bool
    review: bool
    publish: bool
    manage_users: bool
    system_admin: bool


class UserManagement(BaseModel):
    team_members: List[TeamMember]
    role_distribution: Dict[str, int]
    permissions_matrix: Dict[Role, Permission]
    recent_activity: List[Dict]
    metrics: Dict[str, int]
