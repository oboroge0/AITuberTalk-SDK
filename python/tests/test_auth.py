"""
Tests for authentication module
"""

import pytest
from aitubertalk import AITuberTalkClient, AITuberTalkError, ErrorCode


@pytest.fixture
def client():
    """Create test client"""
    return AITuberTalkClient(api_key="test-key")


@pytest.mark.asyncio
async def test_sign_in_with_email(client):
    """Test email sign in"""
    result = await client.auth.sign_in_with_email("test@example.com", "password")
    
    assert result.user.email == "test@example.com"
    assert result.token is not None
    assert result.expires_at is not None
    assert client.auth.get_current_user() is not None


@pytest.mark.asyncio
async def test_sign_up_with_email(client):
    """Test email sign up"""
    result = await client.auth.sign_up_with_email("new@example.com", "password")
    
    assert result.user.email == "new@example.com"
    assert result.token is not None
    assert client.auth.get_current_user() is not None


@pytest.mark.asyncio
async def test_sign_in_with_google(client):
    """Test Google sign in"""
    result = await client.auth.sign_in_with_google()
    
    assert result.user.email == "user@gmail.com"
    assert result.token is not None
    assert client.auth.get_current_user() is not None


@pytest.mark.asyncio
async def test_sign_out(client):
    """Test sign out"""
    # Sign in first
    await client.auth.sign_in_with_email("test@example.com", "password")
    assert client.auth.get_current_user() is not None
    
    # Sign out
    await client.auth.sign_out()
    assert client.auth.get_current_user() is None


@pytest.mark.asyncio
async def test_auth_state_change_callback(client):
    """Test auth state change callback"""
    callback_called = False
    user_from_callback = None
    
    def auth_callback(user):
        nonlocal callback_called, user_from_callback
        callback_called = True
        user_from_callback = user
    
    # Register callback
    unsubscribe = client.auth.on_auth_state_change(auth_callback)
    
    # Sign in
    await client.auth.sign_in_with_email("test@example.com", "password")
    
    assert callback_called
    assert user_from_callback is not None
    assert user_from_callback.email == "test@example.com"
    
    # Clean up
    unsubscribe()