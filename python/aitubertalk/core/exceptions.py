"""
Exception classes for AITuberTalk SDK
"""

from enum import Enum
from typing import Any, Optional


class ErrorCode(Enum):
    """Error codes for AITuberTalk SDK exceptions"""
    
    # Connection errors
    CONNECTION_FAILED = "CONNECTION_FAILED"
    CONNECTION_LOST = "CONNECTION_LOST"
    RECONNECTION_FAILED = "RECONNECTION_FAILED"
    
    # Authentication errors
    AUTH_FAILED = "AUTH_FAILED"
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    AUTH_INSUFFICIENT_PERMISSION = "AUTH_INSUFFICIENT_PERMISSION"
    
    # Room errors
    ROOM_NOT_FOUND = "ROOM_NOT_FOUND"
    ROOM_FULL = "ROOM_FULL"
    ROOM_ACCESS_DENIED = "ROOM_ACCESS_DENIED"
    
    # Floor errors
    FLOOR_DENIED = "FLOOR_DENIED"
    FLOOR_TIMEOUT = "FLOOR_TIMEOUT"
    FLOOR_CONFLICT = "FLOOR_CONFLICT"
    
    # Media errors
    MEDIA_DEVICE_NOT_FOUND = "MEDIA_DEVICE_NOT_FOUND"
    MEDIA_PERMISSION_DENIED = "MEDIA_PERMISSION_DENIED"
    MEDIA_TRACK_FAILED = "MEDIA_TRACK_FAILED"
    
    # Network errors
    NETWORK_ERROR = "NETWORK_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    
    # Unknown error
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class AITuberTalkError(Exception):
    """Base exception class for AITuberTalk SDK"""
    
    def __init__(
        self,
        code: ErrorCode,
        message: str,
        retryable: bool = False,
        details: Optional[Any] = None
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable
        self.details = details
        
    def __str__(self) -> str:
        return f"[{self.code.value}] {self.message}"
    
    def __repr__(self) -> str:
        return (
            f"AITuberTalkError(code={self.code.value}, "
            f"message='{self.message}', retryable={self.retryable})"
        )