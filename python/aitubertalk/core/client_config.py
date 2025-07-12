"""
Client configuration for AITuberTalk SDK
"""

from dataclasses import dataclass
from typing import Optional

from .retry_config import RetryConfig


@dataclass
class ClientConfig:
    """Configuration class for AITuberTalk client"""
    
    api_key: str
    region: str = "asia-northeast1"
    endpoint: Optional[str] = None
    timeout: int = 30000  # milliseconds
    retry_config: Optional[RetryConfig] = None
    log_level: str = "info"  # debug, info, warn, error
    auto_reconnect: bool = True
    
    def __post_init__(self) -> None:
        if self.retry_config is None:
            self.retry_config = RetryConfig()
            
        if self.endpoint is None:
            self.endpoint = f"https://api.aitubertalk.ai/{self.region}"