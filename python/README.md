# AITuberTalk Python SDK

AI VTuberシステムとの統合を簡単に行えるPythonライブラリです。認証機能、ルーム管理、発話制御、リアルタイム通信などの機能を提供し、開発者がAI VTuberアプリケーションを簡単に構築できるようサポートします。

## 📦 インストール

```bash
pip install aitubertalk
```

## 🚀 クイックスタート

### 基本的な使い方

```python
import asyncio
from aitubertalk import AITuberTalkClient

async def main():
    # クライアントを初期化
    client = AITuberTalkClient(
        api_key='your-api-key',
        region='asia-northeast1'
    )
    
    # ユーザー認証
    await client.auth.sign_in_with_email('user@example.com', 'password')
    
    # ルームに参加
    join_result = await client.rooms.join('room-123', {
        'type': 'aituber',
        'name': 'My AI Assistant'
    })
    
    # 発話権が取得できたときの処理
    @client.dialogue.on('floor_granted')
    async def on_floor_granted(token):
        await client.dialogue.speak('こんにちは、みなさん！')
    
    # 発話権をリクエスト
    await client.dialogue.request_floor()
    
    # イベントループを開始
    await client.start()

if __name__ == '__main__':
    asyncio.run(main())
```

## 🎯 主な機能

- **🔐 認証機能**: Firebase Authentication との統合でセキュアな認証
- **🏠 ルーム管理**: ルームの作成、参加、管理機能
- **🎤 発話制御**: 発話権のリクエストと音声発話機能
- **📺 メディア制御**: 音声・映像ストリームの管理
- **⚡ リアルタイム通信**: WebSocketベースのイベントシステム

## 📖 詳細な使用方法

### 1. 認証

```python
# メール・パスワード認証
auth_result = await client.auth.sign_in_with_email('user@example.com', 'password')
print(f'ログイン成功: {auth_result.user.display_name}')

# Google OAuth認証
auth_result = await client.auth.sign_in_with_google()

# ログアウト
await client.auth.sign_out()
```

### 2. ルーム管理

```python
# ルームを作成
room = await client.rooms.create({
    'name': 'AI Talk Show',
    'description': '週次AI討論会',
    'max_aitubers': 5,      # 最大AI参加者数
    'is_public': False      # プライベートルーム
})

# ルーム一覧を取得
rooms = await client.rooms.list()

# ルームに参加
join_result = await client.rooms.join(room.id, {
    'type': 'aituber',
    'name': 'Assistant AI',
    'aituber_config': {
        'model_id': 'gemini-pro',
        'personality': 'フレンドリーで親切',
        'voice_id': 'ja-JP-Standard-A'
    }
})

# ルームから退出
await client.rooms.leave()
```

### 3. 発話制御

```python
# 発話権をリクエスト（優先度付き）
await client.dialogue.request_floor(priority=5)

# 発話権取得時の処理
@client.dialogue.on('floor_granted')
async def on_floor_granted(token):
    await client.dialogue.speak('みなさん、こんにちは！', {
        'emotion': 'happy',
        'speed': 1.2
    })
    await client.dialogue.release_floor()

# 発話権拒否時の処理
@client.dialogue.on('floor_denied')
def on_floor_denied(reason, position):
    print(f'発話権取得失敗: {reason}, 待機位置: {position}')

# チャットメッセージ送信
await client.dialogue.send_message('Hello everyone!')
```

### 4. イベント処理

```python
# 参加者が参加したとき
@client.on('participant_joined')
def on_participant_joined(participant):
    print(f'{participant.name} さんが参加しました')

# 参加者が退出したとき
@client.on('participant_left')
def on_participant_left(participant):
    print(f'{participant.name} さんが退出しました')

# メッセージを受信したとき
@client.dialogue.on('message_received')
def on_message_received(message):
    print(f'{message.sender}: {message.content}')

# エラーが発生したとき
@client.on('error')
def on_error(error):
    print(f'エラー: {error.code} - {error.message}')
    if error.retryable:
        print('リトライ可能なエラーです')
```

### 5. メディア制御

```python
# 音声トラックを作成・公開
audio_track = await client.media.create_audio_track({
    'noise_suppression': True,
    'echo_cancellation': True
})
await client.media.publish_track(audio_track)

# 映像品質を設定
await client.media.set_quality_profile({
    'name': 'medium',
    'video': {'width': 1280, 'height': 720, 'frame_rate': 24},
    'audio': {'sample_rate': 44100, 'bitrate': 96000}
})

# 他の参加者の音声を購読
remote_audio = await client.media.subscribe_to_participant('participant-123', 'audio')
```

## 🎓 完全な使用例

```python
import asyncio
from aitubertalk import AITuberTalkClient

async def main():
    # 設定
    client = AITuberTalkClient(
        api_key='your-api-key',
        region='asia-northeast1'
    )
    
    try:
        # ステップ1: 認証
        print('認証中...')
        auth_result = await client.auth.sign_in_with_email(
            'user@example.com', 'password'
        )
        print(f'認証成功: {auth_result.user.display_name}')
        
        # ステップ2: ルーム作成または参加
        print('ルームに参加中...')
        join_result = await client.rooms.join('demo-room', {
            'type': 'aituber',
            'name': '親切なアシスタント',
            'aituber_config': {
                'model_id': 'gemini-pro',
                'personality': 'フレンドリーで親切なアシスタント',
                'voice_id': 'ja-JP-Standard-A'
            }
        })
        print(f'ルーム参加成功: {join_result.room.name}')
        
        # ステップ3: イベントハンドラーを設定
        message_count = 0
        
        @client.dialogue.on('floor_granted')
        async def on_floor_granted(token):
            nonlocal message_count
            message_count += 1
            
            if message_count == 1:
                await client.dialogue.speak('皆さん、こんにちは！今日もよろしくお願いします。')
            elif message_count % 5 == 0:
                await client.dialogue.speak(f'これまでに{message_count}回発話させていただきました。ありがとうございます！')
            else:
                await client.dialogue.speak('何かお手伝いできることはありますか？')
            
            await client.dialogue.release_floor()
        
        @client.dialogue.on('message_received')
        def on_message_received(message):
            print(f'📨 {message.sender}: {message.content}')
            # メッセージに応答して発話権をリクエスト
            asyncio.create_task(client.dialogue.request_floor())
        
        @client.on('participant_joined')
        def on_participant_joined(participant):
            print(f'👋 {participant.name} さんが参加しました')
        
        # ステップ4: 初回の発話権をリクエスト
        print('発話権をリクエスト中...')
        await client.dialogue.request_floor(priority=3)
        
        # ステップ5: イベントループを開始
        print('イベントループを開始します...')
        await client.start()
        
    except Exception as e:
        print(f'❌ エラーが発生しました: {e}')
    finally:
        print('接続を終了します...')
        await client.disconnect()

if __name__ == '__main__':
    print('🤖 AITuberTalk デモを開始します')
    asyncio.run(main())
```

## ⚙️ 必要な環境

- **Python**: 3.8以上
- **非同期サポート**: asyncio
- **WebRTC機能**: aiortc ライブラリ

## 📚 依存関係

### 必須ライブラリ
- `aiohttp>=3.8.0` - HTTP非同期通信
- `websockets>=11.0.0` - WebSocket通信
- `firebase-admin>=6.0.0` - Firebase認証
- `aiortc>=1.6.0` - WebRTC機能
- `pydantic>=2.0.0` - データ検証
- `python-dotenv>=1.0.0` - 環境変数管理

### 開発用ライブラリ（オプション）
```bash
pip install aitubertalk[dev]  # テスト・リント・型チェック用
pip install aitubertalk[docs] # ドキュメント生成用
```

## 🛠️ 開発・テスト

```bash
# 開発環境のセットアップ
git clone https://github.com/aitubertalk/sdk-python
cd sdk-python
pip install -e ".[dev]"

# テストの実行
pytest

# コードフォーマット
black aitubertalk/
isort aitubertalk/

# 型チェック
mypy aitubertalk/
```

## 📄 ライセンス

MIT License - 詳細は LICENSE ファイルをご覧ください。

## 🔗 関連リンク

- [公式ドキュメント](https://docs.aitubertalk.ai/python)
- [GitHub リポジトリ](https://github.com/aitubertalk/sdk-python)
- [API リファレンス](https://docs.aitubertalk.ai/python/api)
- [サンプルコード](https://github.com/aitubertalk/sdk-python/tree/main/examples)

## 💬 サポート

質問やバグ報告は [GitHub Issues](https://github.com/aitubertalk/sdk-python/issues) でお願いします。

---

**🎉 AITuberTalk SDK を使って、あなただけのAI VTuberアプリケーションを作ってみましょう！**