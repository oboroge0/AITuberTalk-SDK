"""
Retry configuration for AITuberTalk SDK
"""

from dataclasses import dataclass


@dataclass
class RetryConfig:
    """Configuration for retry mechanisms"""
    
    max_attempts: int = 3
    initial_delay: int = 1000  # milliseconds
    max_delay: int = 10000  # milliseconds
    backoff_multiplier: float = 2.0