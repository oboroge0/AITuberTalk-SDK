"""
Media control module for AITuberTalk SDK
"""

import asyncio
from typing import Callable, Dict, Optional, TYPE_CHECKING
from uuid import uuid4

from ..core.exceptions import AITuberTalkError, ErrorCode
from .types import (
    LocalAudioTrack, LocalVideoTrack, RemoteTrack, LocalTrack,
    AudioTrackOptions, VideoTrackOptions, PublishOptions, QualityProfile,
    VideoQuality, AudioQuality, RemoteAudioTrack, RemoteVideoTrack
)

if TYPE_CHECKING:
    from ..client import AITuberTalkClient


class MediaModule:
    """
    Media control module for managing audio/video streams
    """
    
    def __init__(self, client: "AITuberTalkClient") -> None:
        self._client = client
        self._published_tracks: Dict[str, LocalTrack] = {}
        self._subscribed_tracks: Dict[str, RemoteTrack] = {}
        self._current_quality: QualityProfile = self._get_default_quality_profile()
        self._track_published_callbacks: list = []
        self._track_subscribed_callbacks: list = []
        self._quality_changed_callbacks: list = []
        
    def _get_default_quality_profile(self) -> QualityProfile:
        """Get default quality profile"""
        return QualityProfile(
            name="medium",
            video=VideoQuality(
                width=1280,
                height=720,
                frame_rate=24,
                bitrate=1200000
            ),
            audio=AudioQuality(
                sample_rate=44100,
                bitrate=96000,
                channels=2
            )
        )
    
    async def create_audio_track(self, options: Optional[AudioTrackOptions] = None) -> LocalAudioTrack:
        """
        Create a local audio track
        
        Args:
            options: Audio track configuration options
            
        Returns:
            Created audio track
            
        Raises:
            AITuberTalkError: If track creation fails
        """
        try:
            if options is None:
                options = AudioTrackOptions()
                
            self._client.logger.info("Creating audio track")
            
            # TODO: Implement actual audio track creation using aiortc
            
            # Simulate track creation
            await asyncio.sleep(0.1)
            
            track_id = str(uuid4())
            audio_track = LocalAudioTrack(track_id, options)
            
            self._client.logger.info(f"Audio track created: {track_id}")
            return audio_track
            
        except Exception as e:
            self._client.logger.error(f"Audio track creation failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.MEDIA_TRACK_FAILED,
                message=f"Failed to create audio track: {e}",
                retryable=True
            )
    
    async def create_video_track(self, options: Optional[VideoTrackOptions] = None) -> LocalVideoTrack:
        """
        Create a local video track
        
        Args:
            options: Video track configuration options
            
        Returns:
            Created video track
            
        Raises:
            AITuberTalkError: If track creation fails
        """
        try:
            if options is None:
                options = VideoTrackOptions()
                
            self._client.logger.info("Creating video track")
            
            # TODO: Implement actual video track creation using aiortc
            
            # Simulate track creation
            await asyncio.sleep(0.2)
            
            track_id = str(uuid4())
            video_track = LocalVideoTrack(track_id, options)
            
            self._client.logger.info(f"Video track created: {track_id}")
            return video_track
            
        except Exception as e:
            self._client.logger.error(f"Video track creation failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.MEDIA_TRACK_FAILED,
                message=f"Failed to create video track: {e}",
                retryable=True
            )
    
    async def publish_track(self, track: LocalTrack, options: Optional[PublishOptions] = None) -> None:
        """
        Publish a local track to the room
        
        Args:
            track: Local track to publish
            options: Publishing options
            
        Raises:
            AITuberTalkError: If publishing fails
        """
        try:
            current_room = self._client.rooms.get_current_room()
            if not current_room:
                raise AITuberTalkError(
                    code=ErrorCode.ROOM_NOT_FOUND,
                    message="Must be in a room to publish tracks",
                    retryable=False
                )
            
            if options is None:
                options = PublishOptions()
                
            self._client.logger.info(f"Publishing {track.kind} track: {track.track_id}")
            
            # TODO: Implement actual track publishing using LiveKit
            
            # Simulate publishing
            await asyncio.sleep(0.1)
            
            # Store published track
            self._published_tracks[track.track_id] = track
            
            # Notify callbacks
            self._notify_track_published(track)
            
            # Emit system event
            from ..core.events import SystemEvent
            self._client._emit_event(SystemEvent.TRACK_PUBLISHED.value, track)
            
            self._client.logger.info(f"Successfully published {track.kind} track")
            
        except AITuberTalkError:
            raise
        except Exception as e:
            self._client.logger.error(f"Track publishing failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.MEDIA_TRACK_FAILED,
                message=f"Failed to publish track: {e}",
                retryable=True
            )
    
    async def unpublish_track(self, track: LocalTrack) -> None:
        """
        Unpublish a local track
        
        Args:
            track: Local track to unpublish
            
        Raises:
            AITuberTalkError: If unpublishing fails
        """
        try:
            self._client.logger.info(f"Unpublishing {track.kind} track: {track.track_id}")
            
            # TODO: Implement actual track unpublishing
            
            # Simulate unpublishing
            await asyncio.sleep(0.05)
            
            # Remove from published tracks
            if track.track_id in self._published_tracks:
                del self._published_tracks[track.track_id]
            
            # Stop the track
            track.stop()
            
            # Emit system event
            from ..core.events import SystemEvent
            self._client._emit_event(SystemEvent.TRACK_UNPUBLISHED.value, track)
            
            self._client.logger.info(f"Successfully unpublished {track.kind} track")
            
        except Exception as e:
            self._client.logger.error(f"Track unpublishing failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.MEDIA_TRACK_FAILED,
                message=f"Failed to unpublish track: {e}",
                retryable=True
            )
    
    async def subscribe_to_participant(self, participant_id: str, track_type: str) -> RemoteTrack:
        """
        Subscribe to a participant's track
        
        Args:
            participant_id: Participant to subscribe to
            track_type: "audio" or "video"
            
        Returns:
            Remote track for the participant
            
        Raises:
            AITuberTalkError: If subscription fails
        """
        try:
            current_room = self._client.rooms.get_current_room()
            if not current_room:
                raise AITuberTalkError(
                    code=ErrorCode.ROOM_NOT_FOUND,
                    message="Must be in a room to subscribe to tracks",
                    retryable=False
                )
            
            self._client.logger.info(f"Subscribing to {participant_id}'s {track_type} track")
            
            # TODO: Implement actual track subscription using LiveKit
            
            # Simulate subscription
            await asyncio.sleep(0.1)
            
            # Create remote track
            track_id = f"{participant_id}_{track_type}_{uuid4()}"
            
            if track_type == "audio":
                remote_track = RemoteAudioTrack(track_id, participant_id)
            elif track_type == "video":
                remote_track = RemoteVideoTrack(track_id, participant_id)
            else:
                raise ValueError(f"Invalid track type: {track_type}")
            
            # Store subscribed track
            self._subscribed_tracks[track_id] = remote_track
            
            # Notify callbacks
            self._notify_track_subscribed(remote_track)
            
            # Emit system event
            from ..core.events import SystemEvent
            self._client._emit_event(SystemEvent.TRACK_SUBSCRIBED.value, remote_track)
            
            self._client.logger.info(f"Successfully subscribed to {track_type} track")
            return remote_track
            
        except AITuberTalkError:
            raise
        except Exception as e:
            self._client.logger.error(f"Track subscription failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.MEDIA_TRACK_FAILED,
                message=f"Failed to subscribe to track: {e}",
                retryable=True
            )
    
    async def unsubscribe_from_participant(self, participant_id: str, track_type: str) -> None:
        """
        Unsubscribe from a participant's track
        
        Args:
            participant_id: Participant to unsubscribe from
            track_type: "audio" or "video"
            
        Raises:
            AITuberTalkError: If unsubscription fails
        """
        try:
            self._client.logger.info(f"Unsubscribing from {participant_id}'s {track_type} track")
            
            # TODO: Implement actual track unsubscription
            
            # Find and remove subscribed track
            tracks_to_remove = []
            for track_id, track in self._subscribed_tracks.items():
                if track.participant_id == participant_id and track.kind == track_type:
                    tracks_to_remove.append(track_id)
            
            for track_id in tracks_to_remove:
                track = self._subscribed_tracks[track_id]
                del self._subscribed_tracks[track_id]
                
                # Emit system event
                from ..core.events import SystemEvent
                self._client._emit_event(SystemEvent.TRACK_UNSUBSCRIBED.value, track)
            
            self._client.logger.info(f"Successfully unsubscribed from {track_type} track")
            
        except Exception as e:
            self._client.logger.error(f"Track unsubscription failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.MEDIA_TRACK_FAILED,
                message=f"Failed to unsubscribe from track: {e}",
                retryable=True
            )
    
    async def set_quality_profile(self, profile: QualityProfile) -> None:
        """
        Set media quality profile
        
        Args:
            profile: Quality profile to apply
            
        Raises:
            AITuberTalkError: If quality change fails
        """
        try:
            self._client.logger.info(f"Setting quality profile: {profile.name}")
            
            # TODO: Implement actual quality profile application
            
            # Simulate quality change
            await asyncio.sleep(0.1)
            
            # Update current quality
            self._current_quality = profile
            
            # Notify callbacks
            self._notify_quality_changed(profile)
            
            # Emit system event
            from ..core.events import SystemEvent
            self._client._emit_event(SystemEvent.QUALITY_CHANGED.value, profile)
            
            self._client.logger.info(f"Quality profile applied: {profile.name}")
            
        except Exception as e:
            self._client.logger.error(f"Quality profile change failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.MEDIA_TRACK_FAILED,
                message=f"Failed to set quality profile: {e}",
                retryable=True
            )
    
    def get_current_quality(self) -> QualityProfile:
        """
        Get current quality profile
        
        Returns:
            Current quality profile
        """
        return self._current_quality
    
    async def set_muted(self, track_type: str, muted: bool) -> None:
        """
        Mute or unmute local tracks
        
        Args:
            track_type: "audio" or "video"
            muted: True to mute, False to unmute
        """
        try:
            self._client.logger.info(f"{'Muting' if muted else 'Unmuting'} {track_type} tracks")
            
            for track in self._published_tracks.values():
                if track.kind == track_type:
                    if muted:
                        track.mute()
                    else:
                        track.unmute()
            
            self._client.logger.info(f"{track_type.capitalize()} tracks {'muted' if muted else 'unmuted'}")
            
        except Exception as e:
            self._client.logger.error(f"Mute operation failed: {e}")
    
    def is_muted(self, track_type: str) -> bool:
        """
        Check if local tracks are muted
        
        Args:
            track_type: "audio" or "video"
            
        Returns:
            True if any track of the type is muted
        """
        for track in self._published_tracks.values():
            if track.kind == track_type and hasattr(track, 'muted'):
                return track.muted
        return False
    
    def on_track_published(self, callback: Callable[[LocalTrack], None]) -> Callable[[], None]:
        """
        Register callback for track published events
        
        Args:
            callback: Function to call when track is published
            
        Returns:
            Unsubscribe function
        """
        self._track_published_callbacks.append(callback)
        
        def unsubscribe() -> None:
            if callback in self._track_published_callbacks:
                self._track_published_callbacks.remove(callback)
        
        return unsubscribe
    
    def on_track_subscribed(self, callback: Callable[[RemoteTrack], None]) -> Callable[[], None]:
        """
        Register callback for track subscribed events
        
        Args:
            callback: Function to call when track is subscribed
            
        Returns:
            Unsubscribe function
        """
        self._track_subscribed_callbacks.append(callback)
        
        def unsubscribe() -> None:
            if callback in self._track_subscribed_callbacks:
                self._track_subscribed_callbacks.remove(callback)
        
        return unsubscribe
    
    def on_quality_changed(self, callback: Callable[[QualityProfile], None]) -> Callable[[], None]:
        """
        Register callback for quality changed events
        
        Args:
            callback: Function to call when quality changes
            
        Returns:
            Unsubscribe function
        """
        self._quality_changed_callbacks.append(callback)
        
        def unsubscribe() -> None:
            if callback in self._quality_changed_callbacks:
                self._quality_changed_callbacks.remove(callback)
        
        return unsubscribe
    
    def _notify_track_published(self, track: LocalTrack) -> None:
        """Notify track published callbacks"""
        for callback in self._track_published_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(track))
                else:
                    callback(track)
            except Exception as e:
                self._client.logger.error(f"Error in track published callback: {e}")
    
    def _notify_track_subscribed(self, track: RemoteTrack) -> None:
        """Notify track subscribed callbacks"""
        for callback in self._track_subscribed_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(track))
                else:
                    callback(track)
            except Exception as e:
                self._client.logger.error(f"Error in track subscribed callback: {e}")
    
    def _notify_quality_changed(self, profile: QualityProfile) -> None:
        """Notify quality changed callbacks"""
        for callback in self._quality_changed_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(profile))
                else:
                    callback(profile)
            except Exception as e:
                self._client.logger.error(f"Error in quality changed callback: {e}")