"""
Type definitions for room management module
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class CreateRoomConfig:
    """Configuration for creating a new room"""
    name: str
    description: Optional[str] = None
    max_aitubers: int = 5  # Default: 5, Max: 10
    is_public: bool = False


@dataclass
class AITuberConfig:
    """Configuration for AI Tuber participants"""
    model_id: str
    personality: Optional[str] = None
    voice_id: Optional[str] = None


@dataclass
class ParticipantConfig:
    """Configuration for room participants"""
    type: str  # "human" or "aituber"
    name: str
    aituber_config: Optional[AITuberConfig] = None


@dataclass
class Participant:
    """Room participant information"""
    id: str
    type: str  # "human" or "aituber"
    name: str
    user_id: Optional[str] = None
    aituber_config: Optional[AITuberConfig] = None
    joined_at: Optional[datetime] = None
    is_active: bool = True


@dataclass
class Room:
    """Room information"""
    id: str
    name: str
    description: Optional[str]
    owner_id: str
    participants: List[Participant] = field(default_factory=list)
    max_aitubers: int = 5
    is_public: bool = False
    created_at: Optional[datetime] = None


@dataclass
class JoinResult:
    """Result of joining a room"""
    room: Room
    participant: Participant
    livekit_token: str


@dataclass
class RoomFilter:
    """Filter options for room listing"""
    is_public: Optional[bool] = None
    owner_id: Optional[str] = None
    name_contains: Optional[str] = None
    max_results: int = 50