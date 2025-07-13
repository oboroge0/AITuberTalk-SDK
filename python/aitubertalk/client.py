"""
Main client class for AITuberTalk SDK
"""

import asyncio
import logging
from typing import Any, Callable, Dict, Optional, Union

from .auth import AuthModule
from .core.client_config import ClientConfig
from .core.events import SystemEvent
from .core.exceptions import AITuberTalkError, ErrorCode
from .dialogue import DialogueModule
from .media import MediaModule
from .rooms import RoomModule


class AITuberTalkClient:
    """
    Main client class for AITuberTalk SDK
    
    This class provides the primary interface for interacting with the
    AITuberTalk platform, including authentication, room management,
    dialogue control, and media handling.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        region: str = "asia-northeast1",
        config: Optional[ClientConfig] = None,
        **kwargs: Any
    ) -> None:
        """
        Initialize AITuberTalk client
        
        Args:
            api_key: API key for authentication
            region: Service region
            config: Client configuration object
            **kwargs: Additional configuration options
        """
        if config is None:
            if api_key is None:
                raise ValueError("api_key is required")
            config = ClientConfig(api_key=api_key, region=region, **kwargs)
        
        self._config = config
        self._logger = self._setup_logger()
        self._event_handlers: Dict[str, list] = {}
        self._connected = False
        
        # Initialize modules
        self.auth = AuthModule(self)
        self.rooms = RoomModule(self)
        self.dialogue = DialogueModule(self)
        self.media = MediaModule(self)
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logger with configured level"""
        logger = logging.getLogger("aitubertalk")
        
        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARNING,
            "error": logging.ERROR,
        }
        
        logger.setLevel(level_map.get(self._config.log_level, logging.INFO))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    async def connect(self) -> None:
        """
        Connect to AITuberTalk service
        
        Raises:
            AITuberTalkError: If connection fails
        """
        try:
            self._logger.info("Connecting to AITuberTalk service...")
            
            # TODO: Implement actual connection logic
            # This would involve WebSocket connection, authentication, etc.
            
            self._connected = True
            self._emit_event(SystemEvent.CONNECTED.value)
            self._logger.info("Connected to AITuberTalk service")
            
        except Exception as e:
            self._logger.error(f"Connection failed: {e}")
            raise AITuberTalkError(
                code=ErrorCode.CONNECTION_FAILED,
                message=f"Failed to connect: {e}",
                retryable=True
            )
    
    async def disconnect(self) -> None:
        """
        Disconnect from AITuberTalk service
        """
        try:
            self._logger.info("Disconnecting from AITuberTalk service...")
            
            # TODO: Implement actual disconnection logic
            
            self._connected = False
            self._emit_event(SystemEvent.DISCONNECTED.value)
            self._logger.info("Disconnected from AITuberTalk service")
            
        except Exception as e:
            self._logger.error(f"Disconnection error: {e}")
    
    def on(self, event: Union[str, SystemEvent], handler: Callable) -> Callable[[], None]:
        """
        Register event handler
        
        Args:
            event: Event name or SystemEvent enum
            handler: Event handler function
            
        Returns:
            Unsubscribe function
        """
        event_name = event.value if isinstance(event, SystemEvent) else event
        
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        
        self._event_handlers[event_name].append(handler)
        
        def unsubscribe() -> None:
            if event_name in self._event_handlers:
                try:
                    self._event_handlers[event_name].remove(handler)
                except ValueError:
                    pass
        
        return unsubscribe
    
    def off(self, event: Union[str, SystemEvent], handler: Callable) -> None:
        """
        Remove event handler
        
        Args:
            event: Event name or SystemEvent enum
            handler: Event handler function to remove
        """
        event_name = event.value if isinstance(event, SystemEvent) else event
        
        if event_name in self._event_handlers:
            try:
                self._event_handlers[event_name].remove(handler)
            except ValueError:
                pass
    
    def _emit_event(self, event: str, *args: Any) -> None:
        """
        Emit event to registered handlers
        
        Args:
            event: Event name
            *args: Event arguments
        """
        if event in self._event_handlers:
            for handler in self._event_handlers[event]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        asyncio.create_task(handler(*args))
                    else:
                        handler(*args)
                except Exception as e:
                    self._logger.error(f"Error in event handler for {event}: {e}")
    
    async def start(self) -> None:
        """
        Start the client and begin event loop
        """
        if not self._connected:
            await self.connect()
            
        try:
            # Keep the client running
            while self._connected:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self._logger.info("Received interrupt signal, shutting down...")
        finally:
            await self.disconnect()
    
    @property
    def config(self) -> ClientConfig:
        """Get client configuration"""
        return self._config
    
    @property
    def logger(self) -> logging.Logger:
        """Get client logger"""
        return self._logger
    
    @property
    def connected(self) -> bool:
        """Check if client is connected"""
        return self._connected