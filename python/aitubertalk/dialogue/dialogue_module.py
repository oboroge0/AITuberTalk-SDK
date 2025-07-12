"""
Dialogue control module for AITuberTalk SDK
"""

import asyncio
from datetime import datetime, timedelta
from typing import Callable, Optional, TYPE_CHECKING
from uuid import uuid4

from ..core.exceptions import AITuberTalkError, ErrorCode
from .types import FloorToken, SpeakOptions, FloorState, QueuedParticipant, Message

if TYPE_CHECKING:
    from ..client import AITuberTalkClient


class DialogueModule:
    """
    Dialogue control module for managing floor access and speech
    """
    
    def __init__(self, client: "AITuberTalkClient") -> None:
        self._client = client
        self._current_floor_token: Optional[FloorToken] = None
        self._floor_state_callbacks: list = []
        self._floor_granted_callbacks: list = []
        self._floor_denied_callbacks: list = []
        self._message_received_callbacks: list = []
        
    async def request_floor(self, priority: int = 1) -> FloorToken:
        """
        Request floor access for speaking
        
        Args:
            priority: Request priority (higher = more priority)
            
        Returns:
            Floor token if granted immediately
            
        Raises:
            AITuberTalkError: If request fails or is denied
        """
        try:
            current_room = self._client.rooms.get_current_room()
            current_participant = self._client.rooms.get_current_participant()
            
            if not current_room or not current_participant:
                raise AITuberTalkError(
                    code=ErrorCode.FLOOR_DENIED,
                    message="Must be in a room to request floor",
                    retryable=False
                )
            
            self._client.logger.info(f"Requesting floor with priority {priority}")
            
            # TODO: Implement actual floor request API call
            
            # Simulate API call
            await asyncio.sleep(0.1)
            
            # Mock floor grant (in real implementation, this might be queued)
            floor_token = FloorToken(
                room_id=current_room.id,
                participant_id=current_participant.id,
                granted_at=datetime.now(),
                expires_at=datetime.now() + timedelta(seconds=30),
                max_duration=30
            )
            
            self._current_floor_token = floor_token
            
            # Notify floor granted callbacks
            self._notify_floor_granted(floor_token)
            
            self._client.logger.info("Floor access granted")
            return floor_token
            
        except AITuberTalkError:
            raise
        except Exception as e:
            self._client.logger.error(f"Floor request failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.FLOOR_DENIED,
                message=f"Failed to request floor: {e}",
                retryable=True
            )
    
    async def speak(self, text: str, options: Optional[SpeakOptions] = None) -> None:
        """
        Speak with current floor access
        
        Args:
            text: Text to speak
            options: Speech options
            
        Raises:
            AITuberTalkError: If not holding floor or speech fails
        """
        try:
            if not self._current_floor_token:
                raise AITuberTalkError(
                    code=ErrorCode.FLOOR_DENIED,
                    message="Must have floor access to speak",
                    retryable=False
                )
            
            # Check if token is still valid
            if datetime.now() > self._current_floor_token.expires_at:
                self._current_floor_token = None
                raise AITuberTalkError(
                    code=ErrorCode.FLOOR_TIMEOUT,
                    message="Floor token has expired",
                    retryable=True
                )
            
            if options is None:
                options = SpeakOptions()
            
            self._client.logger.info(f"Speaking: {text[:50]}{'...' if len(text) > 50 else ''}")
            
            # TODO: Implement actual speech synthesis and audio streaming
            
            # Simulate speech processing
            await asyncio.sleep(len(text) * 0.05)  # Simulate speech duration
            
            self._client.logger.info("Speech completed")
            
        except AITuberTalkError:
            raise
        except Exception as e:
            self._client.logger.error(f"Speech failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.UNKNOWN_ERROR,
                message=f"Failed to speak: {e}",
                retryable=True
            )
    
    async def release_floor(self) -> None:
        """
        Release current floor access
        """
        try:
            if not self._current_floor_token:
                self._client.logger.warning("No floor access to release")
                return
            
            self._client.logger.info("Releasing floor access")
            
            # TODO: Implement actual floor release API call
            
            # Simulate API call
            await asyncio.sleep(0.05)
            
            # Clear current token
            self._current_floor_token = None
            
            # Emit floor released event
            from ..core.events import SystemEvent
            self._client._emit_event(SystemEvent.FLOOR_RELEASED.value)
            
            self._client.logger.info("Floor access released")
            
        except Exception as e:
            self._client.logger.error(f"Floor release failed: {e}")
    
    async def send_message(self, message: str, target_aituber: Optional[str] = None) -> None:
        """
        Send a text message to the room
        
        Args:
            message: Message content
            target_aituber: Optional specific AITuber to target
            
        Raises:
            AITuberTalkError: If message sending fails
        """
        try:
            current_participant = self._client.rooms.get_current_participant()
            if not current_participant:
                raise AITuberTalkError(
                    code=ErrorCode.ROOM_NOT_FOUND,
                    message="Must be in a room to send messages",
                    retryable=False
                )
            
            self._client.logger.info(f"Sending message: {message[:50]}{'...' if len(message) > 50 else ''}")
            
            # TODO: Implement actual message sending API call
            
            # Simulate API call
            await asyncio.sleep(0.1)
            
            # Create message object
            msg = Message(
                id=str(uuid4()),
                sender_id=current_participant.id,
                sender_name=current_participant.name,
                content=message,
                target_aituber=target_aituber,
                timestamp=datetime.now(),
                message_type="text"
            )
            
            # Emit message received event (for own message)
            from ..core.events import SystemEvent
            self._client._emit_event(SystemEvent.MESSAGE_RECEIVED.value, msg)
            
            self._client.logger.info("Message sent successfully")
            
        except AITuberTalkError:
            raise
        except Exception as e:
            self._client.logger.error(f"Message sending failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.NETWORK_ERROR,
                message=f"Failed to send message: {e}",
                retryable=True
            )
    
    async def get_floor_state(self) -> FloorState:
        """
        Get current floor state
        
        Returns:
            Current floor state information
            
        Raises:
            AITuberTalkError: If state retrieval fails
        """
        try:
            self._client.logger.debug("Getting floor state")
            
            # TODO: Implement actual floor state API call
            
            # Simulate API call
            await asyncio.sleep(0.05)
            
            # Mock floor state
            current_holder = None
            if self._current_floor_token:
                current_holder = self._current_floor_token.participant_id
            
            floor_state = FloorState(
                current_holder=current_holder,
                state="idle" if not current_holder else "speaking",
                queue=[],  # Empty queue for mock
                last_state_change=datetime.now()
            )
            
            return floor_state
            
        except Exception as e:
            self._client.logger.error(f"Floor state retrieval failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.NETWORK_ERROR,
                message=f"Failed to get floor state: {e}",
                retryable=True
            )
    
    def on_floor_state_change(self, callback: Callable[[FloorState], None]) -> Callable[[], None]:
        """
        Register callback for floor state changes
        
        Args:
            callback: Function to call when floor state changes
            
        Returns:
            Unsubscribe function
        """
        self._floor_state_callbacks.append(callback)
        
        def unsubscribe() -> None:
            if callback in self._floor_state_callbacks:
                self._floor_state_callbacks.remove(callback)
        
        return unsubscribe
    
    def on_floor_granted(self, callback: Callable[[FloorToken], None]) -> Callable[[], None]:
        """
        Register callback for floor granted events
        
        Args:
            callback: Function to call when floor is granted
            
        Returns:
            Unsubscribe function
        """
        self._floor_granted_callbacks.append(callback)
        
        def unsubscribe() -> None:
            if callback in self._floor_granted_callbacks:
                self._floor_granted_callbacks.remove(callback)
        
        return unsubscribe
    
    def on_floor_denied(self, callback: Callable[[str, int], None]) -> Callable[[], None]:
        """
        Register callback for floor denied events
        
        Args:
            callback: Function to call when floor is denied (reason, queue_position)
            
        Returns:
            Unsubscribe function
        """
        self._floor_denied_callbacks.append(callback)
        
        def unsubscribe() -> None:
            if callback in self._floor_denied_callbacks:
                self._floor_denied_callbacks.remove(callback)
        
        return unsubscribe
    
    def on_message_received(self, callback: Callable[[Message], None]) -> Callable[[], None]:
        """
        Register callback for message received events
        
        Args:
            callback: Function to call when message is received
            
        Returns:
            Unsubscribe function
        """
        self._message_received_callbacks.append(callback)
        
        def unsubscribe() -> None:
            if callback in self._message_received_callbacks:
                self._message_received_callbacks.remove(callback)
        
        return unsubscribe
    
    def _notify_floor_granted(self, token: FloorToken) -> None:
        """
        Notify registered callbacks of floor granted
        
        Args:
            token: Floor token that was granted
        """
        for callback in self._floor_granted_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(token))
                else:
                    callback(token)
            except Exception as e:
                self._client.logger.error(f"Error in floor granted callback: {e}")
    
    def _notify_floor_denied(self, reason: str, position: int) -> None:
        """
        Notify registered callbacks of floor denied
        
        Args:
            reason: Reason for denial
            position: Position in queue
        """
        for callback in self._floor_denied_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(reason, position))
                else:
                    callback(reason, position)
            except Exception as e:
                self._client.logger.error(f"Error in floor denied callback: {e}")
    
    def _notify_message_received(self, message: Message) -> None:
        """
        Notify registered callbacks of message received
        
        Args:
            message: Received message
        """
        for callback in self._message_received_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(message))
                else:
                    callback(message)
            except Exception as e:
                self._client.logger.error(f"Error in message received callback: {e}")