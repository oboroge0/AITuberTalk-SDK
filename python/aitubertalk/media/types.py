"""
Type definitions for media control module
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class AudioTrackOptions:
    """Options for creating audio tracks"""
    device_id: Optional[str] = None
    sample_rate: int = 44100
    channel_count: int = 2
    noise_suppression: bool = True
    echo_cancellation: bool = True


@dataclass
class VideoTrackOptions:
    """Options for creating video tracks"""
    device_id: Optional[str] = None
    width: int = 1280
    height: int = 720
    frame_rate: int = 30
    facing_mode: str = "user"  # "user" or "environment"


@dataclass
class PublishOptions:
    """Options for publishing tracks"""
    name: Optional[str] = None
    simulcast: bool = True
    dtx: bool = True  # Discontinuous transmission


@dataclass
class QualityProfile:
    """Media quality profile configuration"""
    name: str  # "high", "medium", "low", "audioOnly"
    video: Optional["VideoQuality"] = None
    audio: "AudioQuality" = None
    
    def __post_init__(self) -> None:
        if self.audio is None:
            self.audio = AudioQuality(
                sample_rate=44100,
                bitrate=96000,
                channels=2
            )


@dataclass
class VideoQuality:
    """Video quality settings"""
    width: int
    height: int
    frame_rate: int
    bitrate: int  # bits per second


@dataclass
class AudioQuality:
    """Audio quality settings"""
    sample_rate: int
    bitrate: int  # bits per second
    channels: int


class LocalTrack(ABC):
    """Base class for local media tracks"""
    
    def __init__(self, track_id: str, kind: str) -> None:
        self.track_id = track_id
        self.kind = kind  # "audio" or "video"
        self.enabled = True
        
    @abstractmethod
    def stop(self) -> None:
        """Stop the track"""
        pass
    
    @abstractmethod
    def mute(self) -> None:
        """Mute the track"""
        pass
    
    @abstractmethod
    def unmute(self) -> None:
        """Unmute the track"""
        pass


class LocalAudioTrack(LocalTrack):
    """Local audio track"""
    
    def __init__(self, track_id: str, options: AudioTrackOptions) -> None:
        super().__init__(track_id, "audio")
        self.options = options
        self._muted = False
        
    def stop(self) -> None:
        """Stop the audio track"""
        self.enabled = False
        
    def mute(self) -> None:
        """Mute the audio track"""
        self._muted = True
        
    def unmute(self) -> None:
        """Unmute the audio track"""
        self._muted = False
        
    @property
    def muted(self) -> bool:
        return self._muted


class LocalVideoTrack(LocalTrack):
    """Local video track"""
    
    def __init__(self, track_id: str, options: VideoTrackOptions) -> None:
        super().__init__(track_id, "video")
        self.options = options
        self._muted = False
        
    def stop(self) -> None:
        """Stop the video track"""
        self.enabled = False
        
    def mute(self) -> None:
        """Mute the video track"""
        self._muted = True
        
    def unmute(self) -> None:
        """Unmute the video track"""
        self._muted = False
        
    @property
    def muted(self) -> bool:
        return self._muted


class RemoteTrack(ABC):
    """Base class for remote media tracks"""
    
    def __init__(self, track_id: str, participant_id: str, kind: str) -> None:
        self.track_id = track_id
        self.participant_id = participant_id
        self.kind = kind  # "audio" or "video"
        self.enabled = True
        
    @abstractmethod
    def enable(self) -> None:
        """Enable the remote track"""
        pass
    
    @abstractmethod
    def disable(self) -> None:
        """Disable the remote track"""
        pass


class RemoteAudioTrack(RemoteTrack):
    """Remote audio track"""
    
    def __init__(self, track_id: str, participant_id: str) -> None:
        super().__init__(track_id, participant_id, "audio")
        
    def enable(self) -> None:
        """Enable the remote audio track"""
        self.enabled = True
        
    def disable(self) -> None:
        """Disable the remote audio track"""
        self.enabled = False


class RemoteVideoTrack(RemoteTrack):
    """Remote video track"""
    
    def __init__(self, track_id: str, participant_id: str) -> None:
        super().__init__(track_id, participant_id, "video")
        
    def enable(self) -> None:
        """Enable the remote video track"""
        self.enabled = True
        
    def disable(self) -> None:
        """Disable the remote video track"""
        self.enabled = False