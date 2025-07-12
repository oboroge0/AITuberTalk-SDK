"""
Type definitions for authentication module
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """User information"""
    uid: str
    email: str
    display_name: Optional[str] = None
    photo_url: Optional[str] = None


@dataclass
class AuthResult:
    """Authentication result"""
    user: User
    token: str
    expires_at: datetime