"""
Type definitions for dialogue control module
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class FloorToken:
    """Token representing floor access permission"""
    room_id: str
    participant_id: str
    granted_at: datetime
    expires_at: datetime
    max_duration: int  # seconds


@dataclass
class SpeakOptions:
    """Options for speech synthesis"""
    target_aituber: Optional[str] = None
    emotion: str = "neutral"  # neutral, happy, sad, excited, angry
    speed: float = 1.0  # 0.5-2.0


@dataclass
class QueuedParticipant:
    """Participant waiting in floor queue"""
    participant_id: str
    priority: int
    queued_at: datetime


@dataclass
class FloorState:
    """Current state of the floor system"""
    current_holder: Optional[str]
    state: str  # idle, thinking, preparing, speaking, cooldown
    queue: List[QueuedParticipant]
    last_state_change: datetime


@dataclass
class Message:
    """Chat message in the room"""
    id: str
    sender_id: str
    sender_name: str
    content: str
    target_aituber: Optional[str] = None
    timestamp: Optional[datetime] = None
    message_type: str = "text"  # text, system, ai_response