import enum


class CompetitionStatus(str, enum.Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"


class SessionStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    APPROVED = "approved"  # утверждено главным судьей


class TypeEvents(str, enum.Enum):
    EVENTS_1 = "events_1"
    EVENTS_2 = "events_2"
