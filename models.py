from pydantic import BaseModel, Field
from typing import List

class UserProfile(BaseModel):
    preferences: List[str] = Field(
        description="Explicit likes, dislikes, and favorites (e.g., 'Likes sushi', 'Hates traffic')."
    )
    emotional_patterns: List[str] = Field(
        description="Recurring moods, triggers, and psychological states (e.g., 'Anxious about work')."
    )
    facts: List[str] = Field(
        description="Hard facts: names, locations, job titles, dates, pets."
    )

class ChatMessage(BaseModel):
    role: str
    content: str