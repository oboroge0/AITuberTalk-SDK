"""
Tests for AITuberTalk client
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from aitubertalk import AITuberTalkClient, AITuberTalkError, ErrorCode


@pytest.fixture
def client():
    """Create test client"""
    return AITuberTalkClient(api_key="test-key", region="test-region")


@pytest.mark.asyncio
async def test_client_initialization(client):
    """Test client initialization"""
    assert client.config.api_key == "test-key"
    assert client.config.region == "test-region"
    assert not client.connected
    assert client.auth is not None
    assert client.rooms is not None
    assert client.dialogue is not None
    assert client.media is not None


@pytest.mark.asyncio
async def test_client_connect(client):
    """Test client connection"""
    await client.connect()
    assert client.connected


@pytest.mark.asyncio
async def test_client_disconnect(client):
    """Test client disconnection"""
    await client.connect()
    assert client.connected
    
    await client.disconnect()
    assert not client.connected


@pytest.mark.asyncio
async def test_event_handlers(client):
    """Test event handler registration and removal"""
    handler_called = False
    
    def test_handler(*args):
        nonlocal handler_called
        handler_called = True
    
    # Register handler
    unsubscribe = client.on("test-event", test_handler)
    
    # Emit event
    client._emit_event("test-event")
    assert handler_called
    
    # Unsubscribe and test
    handler_called = False
    unsubscribe()
    client._emit_event("test-event")
    assert not handler_called


@pytest.mark.asyncio
async def test_client_requires_api_key():
    """Test that client requires API key"""
    with pytest.raises(ValueError):
        AITuberTalkClient()