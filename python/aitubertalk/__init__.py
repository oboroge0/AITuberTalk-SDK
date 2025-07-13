"""
AITuberTalk SDK for Python

A Python client library for the AITuberTalk platform, enabling developers
to easily integrate AI VTuber functionality into their applications.
"""

from .client import AITuberTalkClient
from .core.exceptions import AITuberTalkError, ErrorCode
from .core.events import SystemEvent

__version__ = "0.1.0"
__all__ = [
    "AITuberTalkClient",
    "AITuberTalkError", 
    "ErrorCode",
    "SystemEvent",
]