"""
Type definitions for dialogue control module
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
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


class FloorSystemState(Enum):
    """Possible states of the floor system"""
    IDLE = "idle"
    THINKING = "thinking"
    PREPARING = "preparing"
    SPEAKING = "speaking"
    COOLDOWN = "cooldown"


@dataclass
class FloorState:
    """Current state of the floor system"""
    current_holder: Optional[str]
    state: FloorSystemState
    queue: List[QueuedParticipant] = field(default_factory=list)
    last_state_change: datetime


class MessageType(Enum):
    """Types of messages in the chat"""
    TEXT = "text"
    SYSTEM = "system"
    AI_RESPONSE = "ai_response"


@dataclass
class Message:
    """Chat message in the room"""
    id: str
    sender_id: str
    sender_name: str
    content: str
    target_aituber: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    message_type: MessageType = MessageType.TEXT