# AITuberTalk Python SDK

Python client library for the AITuberTalk platform, enabling developers to easily integrate AI VTuber functionality into their applications.

## Installation

```bash
pip install aitubertalk
```

## Quick Start

```python
import asyncio
from aitubertalk import AITuberTalkClient

async def main():
    client = AITuberTalkClient(
        api_key='your-api-key',
        region='asia-northeast1'
    )
    
    # Authentication
    await client.auth.sign_in_with_email('user@example.com', 'password')
    
    # Join room
    join_result = await client.rooms.join('room-123', {
        'type': 'aituber',
        'name': 'My AI Assistant'
    })
    
    # Floor management
    @client.dialogue.on('floor_granted')
    async def on_floor_granted(token):
        await client.dialogue.speak('Hello, everyone!')
    
    await client.dialogue.request_floor()
    
    # Start event loop
    await client.start()

if __name__ == '__main__':
    asyncio.run(main())
```

## Features

- **Authentication**: Firebase Authentication integration
- **Room Management**: Create, join, and manage rooms
- **Dialogue Control**: Floor request and speech control
- **Media Control**: Audio/video stream management
- **Real-time Communication**: WebSocket-based event system

## Requirements

- Python 3.8+
- asyncio support
- WebRTC capabilities (aiortc)

## Documentation

Full documentation is available at [https://docs.aitubertalk.ai/python](https://docs.aitubertalk.ai/python)

## License

MIT License - see LICENSE file for details.