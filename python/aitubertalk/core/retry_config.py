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

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be ≥ 1")
        if self.initial_delay < 0 or self.max_delay < 0:
            raise ValueError("Delays must be non-negative")
        if self.initial_delay > self.max_delay:
            raise ValueError("initial_delay must not exceed max_delay")
        if self.backoff_multiplier <= 0:
            raise ValueError("backoff_multiplier must be > 0")