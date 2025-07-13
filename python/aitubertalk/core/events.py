"""
Event system for AITuberTalk SDK
"""

from enum import Enum


class SystemEvent(Enum):
    """System events for AITuberTalk SDK"""
    
    # Connection related
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"
    RECONNECTED = "reconnected"
    
    # Authentication related
    AUTH_STATE_CHANGED = "auth-state-changed"
    
    # Room related
    ROOM_JOINED = "room-joined"
    ROOM_LEFT = "room-left"
    PARTICIPANT_JOINED = "participant-joined"
    PARTICIPANT_LEFT = "participant-left"
    
    # Floor related
    FLOOR_STATE_CHANGED = "floor-state-changed"
    FLOOR_GRANTED = "floor-granted"
    FLOOR_DENIED = "floor-denied"
    FLOOR_RELEASED = "floor-released"
    
    # Media related
    TRACK_PUBLISHED = "track-published"
    TRACK_UNPUBLISHED = "track-unpublished"
    TRACK_SUBSCRIBED = "track-subscribed"
    TRACK_UNSUBSCRIBED = "track-unsubscribed"
    QUALITY_CHANGED = "quality-changed"
    
    # Message related
    MESSAGE_RECEIVED = "message-received"
    AI_RESPONSE_GENERATED = "ai-response-generated"
    
    # Error related
    ERROR = "error"
    WARNING = "warning"