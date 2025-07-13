"""
Room management module for AITuberTalk SDK
"""

import asyncio
from typing import List, Optional, TYPE_CHECKING
from uuid import uuid4
from datetime import datetime

from ..core.exceptions import AITuberTalkError, ErrorCode
from .types import (
    Room, CreateRoomConfig, ParticipantConfig, JoinResult, 
    Participant, RoomFilter, AITuberConfig
)

if TYPE_CHECKING:
    from ..client import AITuberTalkClient


class RoomModule:
    """
    Room management module for creating, joining, and managing rooms
    """
    
    def __init__(self, client: "AITuberTalkClient") -> None:
        self._client = client
        self._current_room: Optional[Room] = None
        self._current_participant: Optional[Participant] = None
        
    async def create(self, config: CreateRoomConfig) -> Room:
        """
        Create a new room
        
        Args:
            config: Room configuration
            
        Returns:
            Created room information
            
        Raises:
            AITuberTalkError: If room creation fails
        """
        try:
            self._client.logger.info(f"Creating room: {config.name}")
            
            # Validate max_aitubers
            if config.max_aitubers > 10:
                raise ValueError("Maximum AITubers cannot exceed 10")
            
            # TODO: Implement actual API call to create room
            
            # Simulate API call
            await asyncio.sleep(0.1)
            
            # Get current user
            current_user = self._client.auth.get_current_user()
            if not current_user:
                raise AITuberTalkError(
                    code=ErrorCode.AUTH_FAILED,
                    message="Must be authenticated to create room",
                    retryable=False
                )
            
            # Mock room creation
            room = Room(
                id=str(uuid4()),
                name=config.name,
                description=config.description,
                owner_id=current_user.uid,
                participants=[],
                max_aitubers=config.max_aitubers,
                is_public=config.is_public,
                created_at=datetime.now()
            )
            
            self._client.logger.info(f"Successfully created room: {room.id}")
            return room
            
        except AITuberTalkError:
            raise
        except Exception as e:
            self._client.logger.error(f"Room creation failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.UNKNOWN_ERROR,
                message=f"Failed to create room: {e}",
                retryable=True
            )
    
    async def list(self, filter_options: Optional[RoomFilter] = None) -> List[Room]:
        """
        Get list of available rooms
        
        Args:
            filter_options: Optional filtering criteria
            
        Returns:
            List of rooms matching the filter
            
        Raises:
            AITuberTalkError: If listing fails
        """
        try:
            self._client.logger.info("Listing available rooms")
            
            # TODO: Implement actual API call to list rooms
            
            # Simulate API call
            await asyncio.sleep(0.1)
            
            # Mock room list
            mock_rooms = [
                Room(
                    id="room-1",
                    name="AI Chat Room",
                    description="General AI discussion",
                    owner_id="user-1",
                    max_aitubers=5,
                    is_public=True,
                    created_at=datetime.now()
                ),
                Room(
                    id="room-2", 
                    name="Private Discussion",
                    description="Private room for team",
                    owner_id="user-2",
                    max_aitubers=3,
                    is_public=False,
                    created_at=datetime.now()
                )
            ]
            
            # Apply filters if provided
            if filter_options:
                filtered_rooms = []
                for room in mock_rooms:
                    if filter_options.is_public is not None and room.is_public != filter_options.is_public:
                        continue
                    if filter_options.owner_id and room.owner_id != filter_options.owner_id:
                        continue
                    if filter_options.name_contains and filter_options.name_contains.lower() not in room.name.lower():
                        continue
                    filtered_rooms.append(room)
                
                return filtered_rooms[:filter_options.max_results]
            
            self._client.logger.info(f"Found {len(mock_rooms)} rooms")
            return mock_rooms
            
        except Exception as e:
            self._client.logger.error(f"Room listing failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.NETWORK_ERROR,
                message=f"Failed to list rooms: {e}",
                retryable=True
            )
    
    async def get(self, room_id: str) -> Room:
        """
        Get detailed information about a specific room
        
        Args:
            room_id: Room identifier
            
        Returns:
            Room information
            
        Raises:
            AITuberTalkError: If room is not found or access fails
        """
        try:
            self._client.logger.info(f"Getting room details: {room_id}")
            
            # TODO: Implement actual API call to get room details
            
            # Simulate API call
            await asyncio.sleep(0.1)
            
            # Mock room retrieval
            if room_id == "room-not-found":
                raise AITuberTalkError(
                    code=ErrorCode.ROOM_NOT_FOUND,
                    message=f"Room {room_id} not found",
                    retryable=False
                )
            
            room = Room(
                id=room_id,
                name="Test Room",
                description="Test room description",
                owner_id="owner-123",
                participants=[],
                max_aitubers=5,
                is_public=True,
                created_at=datetime.now()
            )
            
            self._client.logger.info(f"Retrieved room: {room.name}")
            return room
            
        except AITuberTalkError:
            raise
        except Exception as e:
            self._client.logger.error(f"Room retrieval failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.NETWORK_ERROR,
                message=f"Failed to get room: {e}",
                retryable=True
            )
    
    async def join(self, room_id: str, participant_config: ParticipantConfig) -> JoinResult:
        """
        Join a room as a participant
        
        Args:
            room_id: Room to join
            participant_config: Participant configuration
            
        Returns:
            Join result with room info and LiveKit token
            
        Raises:
            AITuberTalkError: If join fails
        """
        try:
            self._client.logger.info(f"Joining room {room_id} as {participant_config.name}")
            
            # Get current user
            current_user = self._client.auth.get_current_user()
            if not current_user:
                raise AITuberTalkError(
                    code=ErrorCode.AUTH_FAILED,
                    message="Must be authenticated to join room",
                    retryable=False
                )
            
            # TODO: Implement actual API call to join room
            
            # Simulate API call
            await asyncio.sleep(0.2)
            
            # Mock room join
            room = await self.get(room_id)
            
            # Check if room is full (for AITubers)
            if participant_config.type == "aituber":
                aituber_count = sum(1 for p in room.participants if p.type == "aituber")
                if aituber_count >= room.max_aitubers:
                    raise AITuberTalkError(
                        code=ErrorCode.ROOM_FULL,
                        message=f"Room has reached maximum AITuber limit ({room.max_aitubers})",
                        retryable=False
                    )
            
            # Create participant
            participant = Participant(
                id=str(uuid4()),
                type=participant_config.type,
                name=participant_config.name,
                user_id=current_user.uid if participant_config.type == "human" else None,
                aituber_config=participant_config.aituber_config,
                joined_at=datetime.now(),
                is_active=True
            )
            
            # Mock LiveKit token
            livekit_token = f"lkt_{room_id}_{participant.id}_mock_token"
            
            # Update current room and participant
            self._current_room = room
            self._current_participant = participant
            
            join_result = JoinResult(
                room=room,
                participant=participant,
                livekit_token=livekit_token
            )
            
            # Emit room joined event
            from ..core.events import SystemEvent
            self._client._emit_event(SystemEvent.ROOM_JOINED.value, room, participant)
            
            self._client.logger.info(f"Successfully joined room: {room.name}")
            return join_result
            
        except AITuberTalkError:
            raise
        except Exception as e:
            self._client.logger.error(f"Room join failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.UNKNOWN_ERROR,
                message=f"Failed to join room: {e}",
                retryable=True
            )
    
    async def leave(self) -> None:
        """
        Leave the current room
        
        Raises:
            AITuberTalkError: If not in a room or leave fails
        """
        try:
            if not self._current_room:
                raise AITuberTalkError(
                    code=ErrorCode.ROOM_NOT_FOUND,
                    message="Not currently in a room",
                    retryable=False
                )
            
            self._client.logger.info(f"Leaving room: {self._current_room.name}")
            
            # TODO: Implement actual API call to leave room
            
            # Simulate API call
            await asyncio.sleep(0.1)
            
            # Store room info for event
            left_room = self._current_room
            left_participant = self._current_participant
            
            # Clear current room and participant
            self._current_room = None
            self._current_participant = None
            
            # Emit room left event
            from ..core.events import SystemEvent
            self._client._emit_event(SystemEvent.ROOM_LEFT.value, left_room, left_participant)
            
            self._client.logger.info("Successfully left room")
            
        except AITuberTalkError:
            raise
        except Exception as e:
            self._client.logger.error(f"Room leave failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.UNKNOWN_ERROR,
                message=f"Failed to leave room: {e}",
                retryable=True
            )
    
    def get_current_room(self) -> Optional[Room]:
        """
        Get current room information
        
        Returns:
            Current room or None if not in a room
        """
        return self._current_room
    
    def get_current_participant(self) -> Optional[Participant]:
        """
        Get current participant information
        
        Returns:
            Current participant or None if not in a room
        """
        return self._current_participant