"""
Basic usage example for AITuberTalk Python SDK
"""

import asyncio
import os
from aitubertalk import AITuberTalkClient


async def main():
    """Basic usage example"""
    
    # Initialize client
    client = AITuberTalkClient(
        api_key=os.getenv('AITUBERTALK_API_KEY', 'your-api-key'),
        region='asia-northeast1'
    )
    
    try:
        # Connect to service
        await client.connect()
        
        # Authentication
        print("Signing in...")
        auth_result = await client.auth.sign_in_with_email(
            'user@example.com', 
            'password123'
        )
        print(f"Signed in as: {auth_result.user.display_name}")
        
        # Create a room
        print("Creating room...")
        room = await client.rooms.create({
            'name': 'AI Talk Demo',
            'description': 'Demo room for AITuberTalk SDK',
            'max_aitubers': 5,
            'is_public': False
        })
        print(f"Created room: {room.name} (ID: {room.id})")
        
        # Join the room as an AI Tuber
        print("Joining room as AITuber...")
        join_result = await client.rooms.join(room.id, {
            'type': 'aituber',
            'name': 'Demo AI Assistant',
            'aituber_config': {
                'model_id': 'gemini-pro',
                'personality': 'friendly and helpful',
                'voice_id': 'ja-JP-Standard-A'
            }
        })
        print(f"Joined as: {join_result.participant.name}")
        
        # Set up event handlers
        @client.dialogue.on_floor_granted
        async def on_floor_granted(token):
            print(f"Floor granted! Token expires at: {token.expires_at}")
            await client.dialogue.speak("Hello everyone! I'm ready to chat!")
            await client.dialogue.release_floor()
        
        @client.dialogue.on_floor_denied
        def on_floor_denied(reason, position):
            print(f"Floor denied: {reason}, Queue position: {position}")
        
        @client.dialogue.on_message_received
        def on_message_received(message):
            print(f"Message from {message.sender_name}: {message.content}")
        
        # Create and publish audio track
        print("Setting up media...")
        audio_track = await client.media.create_audio_track({
            'noise_suppression': True,
            'echo_cancellation': True
        })
        await client.media.publish_track(audio_track)
        print("Audio track published")
        
        # Request floor and send a message
        print("Requesting floor...")
        await client.dialogue.request_floor(priority=5)
        
        # Send a chat message
        await client.dialogue.send_message("Hello from the Python SDK!")
        
        # Keep the client running for demo
        print("Client running... Press Ctrl+C to stop")
        await asyncio.sleep(10)  # Run for 10 seconds in demo
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        if client.rooms.get_current_room():
            await client.rooms.leave()
        await client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())