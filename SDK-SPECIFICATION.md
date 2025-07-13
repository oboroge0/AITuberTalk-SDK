# AITuberTalk SDK仕様書

> **ドキュメント種別**: SDK仕様書  
> **対象読者**: SDK利用開発者、サードパーティ開発者  
> **公開レベル**: パブリック（Phase 3以降）  
> **最終更新**: 2025-07-06

## 1. SDK概要

### 1.1 目的
AITuberTalk SDKは、開発者がAI VTuberシステムを簡単に統合できるよう設計されたクライアントライブラリです。3つのプラットフォーム（TypeScript/JavaScript、Python、Unity C#）で統一されたAPIを提供します。

### 1.2 主要機能
- **認証管理**: Firebase Authenticationとの統合
- **ルーム管理**: ルーム作成、参加、退出
- **発話制御**: 発話権リクエスト、発話権解放
- **メディア制御**: 画面共有ストリームの管理
- **リアルタイム通信**: WebSocketによるイベント受信

### 1.3 対象開発者（開発優先順）
- **AI開発者**: Python SDK（最優先開発・MLエンジニア向け）
- **Webアプリケーション開発者**: TypeScript/JavaScript SDK
- **ゲーム・VR開発者**: Unity C# SDK

## 2. 統一APIデザイン

### 2.1 基本設計原則
1. **シンプルさ**: 最小限のコードで基本機能を実現
2. **一貫性**: 3プラットフォームで同じメソッド名・動作
3. **型安全性**: 強い型付けによるコンパイル時エラー検出
4. **エラーハンドリング**: 明確なエラーコードと回復可能性
5. **非同期対応**: Promise/async/await パターンの採用

### 2.2 共通インターフェース
```typescript
interface AITuberTalkClient {
  // 接続管理
  connect(options: ConnectionOptions): Promise<void>;
  disconnect(): Promise<void>;
  
  // 認証
  auth: AuthModule;
  
  // ルーム管理
  rooms: RoomModule;
  
  // 発話制御
  dialogue: DialogueModule;
  
  // メディア制御
  media: MediaModule;
  
  // イベント管理
  on(event: string, handler: Function): void;
  off(event: string, handler: Function): void;
}
```

## 3. モジュール別仕様

### 3.1 AuthModule（認証モジュール）

#### 目的
Firebase Authenticationとの統合により、安全な認証フローを提供

#### インターフェース
```typescript
interface AuthModule {
  // メール/パスワード認証
  signInWithEmail(email: string, password: string): Promise<AuthResult>;
  signUpWithEmail(email: string, password: string): Promise<AuthResult>;
  
  // Google OAuth認証
  signInWithGoogle(): Promise<AuthResult>;
  
  // 認証状態管理
  onAuthStateChange(callback: (user: User | null) => void): Unsubscribe;
  getCurrentUser(): User | null;
  
  // ログアウト
  signOut(): Promise<void>;
}

interface AuthResult {
  user: User;
  token: string;
  expiresAt: Date;
}

interface User {
  uid: string;
  email: string;
  displayName?: string;
  photoURL?: string;
}
```

#### 使用例
```typescript
// TypeScript
const client = new AITuberTalkClient({ apiKey: "your-key" });
const authResult = await client.auth.signInWithEmail("user@example.com", "password");
console.log("Signed in as:", authResult.user.displayName);
```

```python
# Python
client = AITuberTalkClient(api_key="your-key")
auth_result = await client.auth.sign_in_with_email("user@example.com", "password")
print(f"Signed in as: {auth_result.user.display_name}")
```

```csharp
// C#
var client = new AITuberTalkClient("your-key");
var authResult = await client.Auth.SignInWithEmailAsync("user@example.com", "password");
Debug.Log($"Signed in as: {authResult.User.DisplayName}");
```

### 3.2 RoomModule（ルーム管理モジュール）

#### 目的
ルームの作成、参加、管理機能を提供

#### インターフェース
```typescript
interface RoomModule {
  // ルーム作成
  create(config: CreateRoomConfig): Promise<Room>;
  
  // ルーム一覧取得
  list(filter?: RoomFilter): Promise<Room[]>;
  
  // ルーム詳細取得
  get(roomId: string): Promise<Room>;
  
  // ルーム参加
  join(roomId: string, participant: ParticipantConfig): Promise<JoinResult>;
  
  // ルーム退出
  leave(): Promise<void>;
  
  // 現在のルーム取得
  getCurrentRoom(): Room | null;
}

interface CreateRoomConfig {
  name: string;
  description?: string;
  maxAITubers?: number;  // デフォルト: 5、最大: 10
  isPublic?: boolean;    // デフォルト: false
}

interface ParticipantConfig {
  type: "human" | "aituber";
  name: string;
  aituberConfig?: {
    modelId: string;
    personality?: string;
    voiceId?: string;
  };
}

interface Room {
  id: string;
  name: string;
  description?: string;
  ownerId: string;
  participants: Participant[];
  maxAITubers: number;
  isPublic: boolean;
  createdAt: Date;
}

interface JoinResult {
  room: Room;
  participant: Participant;
  livekitToken: string;
}
```

#### 使用例
```typescript
// ルーム作成
const room = await client.rooms.create({
  name: "AI Talk Show",
  description: "Weekly AI discussion",
  maxAITubers: 5,  // 最大10名まで設定可能
  isPublic: false
});

// ルーム参加
const result = await client.rooms.join(room.id, {
  type: "aituber",
  name: "Assistant AI",
  aituberConfig: {
    modelId: "gemini-pro",
    personality: "friendly and helpful",
    voiceId: "ja-JP-Standard-A"
  }
});
```

### 3.3 DialogueModule（発話制御モジュール）

#### 目的
発話権の管理と音声・テキストメッセージの送信

#### インターフェース
```typescript
interface DialogueModule {
  // 発話権リクエスト
  requestFloor(priority?: number): Promise<FloorToken>;
  
  // 発話実行
  speak(text: string, options?: SpeakOptions): Promise<void>;
  
  // 発話権解放
  releaseFloor(): Promise<void>;
  
  // メッセージ送信（チャット）
  sendMessage(message: string, targetAITuber?: string): Promise<void>;
  
  // 発話権状態取得
  getFloorState(): Promise<FloorState>;
  
  // イベントリスナー
  onFloorStateChange(callback: (state: FloorState) => void): Unsubscribe;
  onFloorGranted(callback: (token: FloorToken) => void): Unsubscribe;
  onFloorDenied(callback: (reason: string, position: number) => void): Unsubscribe;
  onMessageReceived(callback: (message: Message) => void): Unsubscribe;
}

interface FloorToken {
  roomId: string;
  participantId: string;
  grantedAt: Date;
  expiresAt: Date;
  maxDuration: number; // 秒
}

interface SpeakOptions {
  targetAITuber?: string;
  emotion?: "neutral" | "happy" | "sad" | "excited" | "angry";
  speed?: number; // 0.5-2.0
}

interface FloorState {
  currentHolder: string | null;
  state: "idle" | "thinking" | "preparing" | "speaking" | "cooldown";
  queue: QueuedParticipant[];
  lastStateChange: Date;
}

interface QueuedParticipant {
  participantId: string;
  priority: number;
  queuedAt: Date;
}
```

#### 使用例
```typescript
// 発話権リクエスト
const token = await client.dialogue.requestFloor(5); // 優先度5

// 発話権取得イベント
client.dialogue.onFloorGranted(async (token) => {
  await client.dialogue.speak("こんにちは、みなさん！");
  await client.dialogue.releaseFloor();
});

// 発話権拒否イベント
client.dialogue.onFloorDenied((reason, position) => {
  console.log(`発話権取得失敗: ${reason}, キュー位置: ${position}`);
});
```

### 3.4 MediaModule（メディア制御モジュール）

#### 目的
音声・映像ストリームの管理と品質制御

#### インターフェース
```typescript
interface MediaModule {
  // ローカルトラック管理
  createAudioTrack(options?: AudioTrackOptions): Promise<LocalAudioTrack>;
  createVideoTrack(options?: VideoTrackOptions): Promise<LocalVideoTrack>;
  
  // トラック公開
  publishTrack(track: LocalTrack, options?: PublishOptions): Promise<void>;
  unpublishTrack(track: LocalTrack): Promise<void>;
  
  // リモートトラック購読
  subscribeToParticipant(participantId: string, trackType: "audio" | "video"): Promise<RemoteTrack>;
  unsubscribeFromParticipant(participantId: string, trackType: "audio" | "video"): Promise<void>;
  
  // 品質制御
  setQualityProfile(profile: QualityProfile): Promise<void>;
  getCurrentQuality(): QualityProfile;
  
  // ミュート制御
  setMuted(trackType: "audio" | "video", muted: boolean): Promise<void>;
  isMuted(trackType: "audio" | "video"): boolean;
  
  // イベントリスナー
  onTrackPublished(callback: (track: LocalTrack) => void): Unsubscribe;
  onTrackSubscribed(callback: (track: RemoteTrack, participant: Participant) => void): Unsubscribe;
  onQualityChanged(callback: (profile: QualityProfile) => void): Unsubscribe;
}

interface AudioTrackOptions {
  deviceId?: string;
  sampleRate?: number;
  channelCount?: number;
  noiseSuppression?: boolean;
  echoCancellation?: boolean;
}

interface VideoTrackOptions {
  deviceId?: string;
  width?: number;
  height?: number;
  frameRate?: number;
  facingMode?: "user" | "environment";
}

interface QualityProfile {
  name: "high" | "medium" | "low" | "audioOnly";
  video?: {
    width: number;
    height: number;
    frameRate: number;
    bitrate: number;
  };
  audio: {
    sampleRate: number;
    bitrate: number;
    channels: number;
  };
}
```

#### 使用例
```typescript
// 音声トラック作成・公開
const audioTrack = await client.media.createAudioTrack({
  noiseSuppression: true,
  echoCancellation: true
});
await client.media.publishTrack(audioTrack);

// 品質プロファイル設定
await client.media.setQualityProfile({
  name: "medium",
  video: { width: 1280, height: 720, frameRate: 24, bitrate: 1200000 },
  audio: { sampleRate: 44100, bitrate: 96000, channels: 2 }
});

// 他の参加者の音声を購読
const remoteAudioTrack = await client.media.subscribeToParticipant("participant-123", "audio");
```

## 4. イベントシステム

### 4.1 システムイベント
```typescript
enum SystemEvent {
  // 接続関連
  CONNECTED = "connected",
  DISCONNECTED = "disconnected", 
  RECONNECTING = "reconnecting",
  RECONNECTED = "reconnected",
  
  // 認証関連
  AUTH_STATE_CHANGED = "auth-state-changed",
  
  // ルーム関連
  ROOM_JOINED = "room-joined",
  ROOM_LEFT = "room-left",
  PARTICIPANT_JOINED = "participant-joined",
  PARTICIPANT_LEFT = "participant-left",
  
  // 発話権関連
  FLOOR_STATE_CHANGED = "floor-state-changed",
  FLOOR_GRANTED = "floor-granted",
  FLOOR_DENIED = "floor-denied",
  FLOOR_RELEASED = "floor-released",
  
  // メディア関連
  TRACK_PUBLISHED = "track-published",
  TRACK_UNPUBLISHED = "track-unpublished",
  TRACK_SUBSCRIBED = "track-subscribed",
  TRACK_UNSUBSCRIBED = "track-unsubscribed",
  QUALITY_CHANGED = "quality-changed",
  
  // メッセージ関連
  MESSAGE_RECEIVED = "message-received",
  AI_RESPONSE_GENERATED = "ai-response-generated",
  
  // エラー関連
  ERROR = "error",
  WARNING = "warning"
}
```

### 4.2 イベントハンドリング
```typescript
// TypeScript
client.on(SystemEvent.PARTICIPANT_JOINED, (participant: Participant) => {
  console.log(`${participant.name} が参加しました`);
});

client.on(SystemEvent.ERROR, (error: AITuberTalkError) => {
  console.error(`エラー発生: ${error.code} - ${error.message}`);
  if (error.retryable) {
    // リトライ処理
  }
});
```

```python
# Python
@client.on(SystemEvent.PARTICIPANT_JOINED)
def on_participant_joined(participant: Participant):
    print(f"{participant.name} が参加しました")

@client.on(SystemEvent.ERROR)
def on_error(error: AITuberTalkError):
    print(f"エラー発生: {error.code} - {error.message}")
    if error.retryable:
        # リトライ処理
        pass
```

```csharp
// C#
client.On(SystemEvent.ParticipantJoined, (Participant participant) => {
    Debug.Log($"{participant.Name} が参加しました");
});

client.On(SystemEvent.Error, (AITuberTalkError error) => {
    Debug.LogError($"エラー発生: {error.Code} - {error.Message}");
    if (error.Retryable) {
        // リトライ処理
    }
});
```

## 5. エラーハンドリング

### 5.1 エラー分類
```typescript
enum ErrorCode {
  // 接続エラー
  CONNECTION_FAILED = "CONNECTION_FAILED",
  CONNECTION_LOST = "CONNECTION_LOST",
  RECONNECTION_FAILED = "RECONNECTION_FAILED",
  
  // 認証エラー
  AUTH_FAILED = "AUTH_FAILED",
  AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED",
  AUTH_INSUFFICIENT_PERMISSION = "AUTH_INSUFFICIENT_PERMISSION",
  
  // ルームエラー
  ROOM_NOT_FOUND = "ROOM_NOT_FOUND",
  ROOM_FULL = "ROOM_FULL",
  ROOM_ACCESS_DENIED = "ROOM_ACCESS_DENIED",
  
  // 発話権エラー
  FLOOR_DENIED = "FLOOR_DENIED",
  FLOOR_TIMEOUT = "FLOOR_TIMEOUT",
  FLOOR_CONFLICT = "FLOOR_CONFLICT",
  
  // メディアエラー
  MEDIA_DEVICE_NOT_FOUND = "MEDIA_DEVICE_NOT_FOUND",
  MEDIA_PERMISSION_DENIED = "MEDIA_PERMISSION_DENIED",
  MEDIA_TRACK_FAILED = "MEDIA_TRACK_FAILED",
  
  // ネットワークエラー
  NETWORK_ERROR = "NETWORK_ERROR",
  RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED",
  
  // 不明なエラー
  UNKNOWN_ERROR = "UNKNOWN_ERROR"
}

class AITuberTalkError extends Error {
  constructor(
    public code: ErrorCode,
    public message: string,
    public retryable: boolean = false,
    public details?: any
  ) {
    super(message);
    this.name = "AITuberTalkError";
  }
}
```

### 5.2 リトライ機構
```typescript
interface RetryConfig {
  maxAttempts: number;      // 最大リトライ回数
  initialDelay: number;     // 初期遅延（ms）
  maxDelay: number;         // 最大遅延（ms）
  backoffMultiplier: number; // バックオフ倍率
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxAttempts: 3,
  initialDelay: 1000,
  maxDelay: 10000,
  backoffMultiplier: 2
};
```

## 6. プラットフォーム別実装（開発優先順）

### 6.1 Python SDK（最優先開発）

#### インストール
```bash
pip install aitubertalk
```

#### 基本使用法
```python
import asyncio
from aitubertalk import AITuberTalkClient

async def main():
    client = AITuberTalkClient(
        api_key='your-api-key',
        region='asia-northeast1'
    )
    
    # 認証
    await client.auth.sign_in_with_email('user@example.com', 'password')
    
    # ルーム参加
    join_result = await client.rooms.join('room-123', {
        'type': 'aituber',
        'name': 'My AI Assistant'
    })
    
    # 発話権管理
    @client.dialogue.on('floor_granted')
    async def on_floor_granted(token):
        await client.dialogue.speak('Hello, everyone!')
    
    await client.dialogue.request_floor()
    
    # イベントループ開始
    await client.start()

if __name__ == '__main__':
    asyncio.run(main())
```

#### 環境要件
- Python 3.8+
- asyncio サポート
- WebRTC ライブラリ（aiortc）

### 6.2 TypeScript/JavaScript SDK

#### インストール
```bash
npm install @aitubertalk/sdk
# or
yarn add @aitubertalk/sdk
```

#### 基本使用法
```typescript
import { AITuberTalkClient } from '@aitubertalk/sdk';

const client = new AITuberTalkClient({
  apiKey: 'your-api-key',
  region: 'asia-northeast1'
});

// 認証
await client.auth.signInWithEmail('user@example.com', 'password');

// ルーム参加
const joinResult = await client.rooms.join('room-123', {
  type: 'aituber',
  name: 'My AI Assistant'
});

// 発話権管理
client.dialogue.onFloorGranted(async (token) => {
  await client.dialogue.speak('Hello, everyone!');
});

await client.dialogue.requestFloor();
```

#### 環境要件
- Node.js 18+ または最新ブラウザ
- WebRTC対応
- ES2020+ support

### 6.3 Unity C# SDK（最後開発）

#### インストール
Unity Package Manager経由:
```
https://github.com/aitubertalk/sdk-unity.git
```

#### 基本使用法
```csharp
using UnityEngine;
using AITuberTalk.SDK;
using System.Threading.Tasks;

public class AITuberController : MonoBehaviour
{
    private AITuberTalkClient client;
    
    async void Start()
    {
        client = new AITuberTalkClient("your-api-key", "asia-northeast1");
        
        // 認証
        await client.Auth.SignInWithEmailAsync("user@example.com", "password");
        
        // ルーム参加
        var joinResult = await client.Rooms.JoinAsync("room-123", new ParticipantConfig
        {
            Type = ParticipantType.AITuber,
            Name = "My AI Assistant"
        });
        
        // 発話権管理
        client.Dialogue.OnFloorGranted += OnFloorGranted;
        await client.Dialogue.RequestFloorAsync();
    }
    
    private async void OnFloorGranted(FloorToken token)
    {
        await client.Dialogue.SpeakAsync("Hello, everyone!");
    }
}
```

#### 環境要件
- Unity 2022.3 LTS+
- WebRTC for Unity
- .NET Standard 2.1

## 7. 設定とカスタマイズ

### 7.1 クライアント設定
```typescript
interface ClientConfig {
  apiKey: string;
  region: string;
  endpoint?: string;         // カスタムエンドポイント
  timeout?: number;          // リクエストタイムアウト
  retryConfig?: RetryConfig; // リトライ設定
  logLevel?: "debug" | "info" | "warn" | "error";
  autoReconnect?: boolean;   // 自動再接続
}
```

### 7.2 環境変数
```bash
# TypeScript/JavaScript
AITUBERTALK_API_KEY=your-api-key
AITUBERTALK_REGION=asia-northeast1
AITUBERTALK_LOG_LEVEL=info

# Python
AITUBERTALK_API_KEY=your-api-key
AITUBERTALK_REGION=asia-northeast1
AITUBERTALK_LOG_LEVEL=info

# Unity (PlayerSettings)
```

## 8. セキュリティガイド

### 8.1 APIキー管理
- **フロントエンド**: 環境変数または設定ファイルで管理
- **バックエンド**: サーバーサイドでプロキシ経由のアクセス推奨
- **モバイル**: アプリの難読化とサーバーサイド検証

### 8.2 認証フロー
```typescript
// 推奨: サーバーサイド認証
const customToken = await getCustomTokenFromYourServer(userId);
await client.auth.signInWithCustomToken(customToken);

// 非推奨: クライアントサイド認証（開発時のみ）
await client.auth.signInWithEmail(email, password);
```

### 8.3 入力検証
```typescript
// 送信前に入力を検証
const sanitizedMessage = message.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
await client.dialogue.sendMessage(sanitizedMessage);
```

## 9. パフォーマンス最適化

### 9.1 接続プール
```typescript
// 複数のクライアントインスタンスの共有
const connectionPool = new AITuberTalkConnectionPool({
  maxConnections: 10,
  keepAliveInterval: 30000
});
```

### 9.2 メモリ管理
```typescript
// イベントリスナーの適切な解除
const unsubscribe = client.dialogue.onFloorGranted(handler);
// コンポーネント破棄時
unsubscribe();

// メディアトラックの解放
await client.media.unpublishTrack(audioTrack);
audioTrack.stop();
```

### 9.3 バンドルサイズ最適化
```typescript
// 必要なモジュールのみインポート
import { DialogueModule } from '@aitubertalk/sdk/dialogue';
import { AuthModule } from '@aitubertalk/sdk/auth';
```

## 10. テストとデバッグ

### 10.1 テスト環境
```typescript
// テスト用クライアント
const testClient = new AITuberTalkClient({
  apiKey: 'test-api-key',
  endpoint: 'https://test-api.aitubertalk.ai',
  logLevel: 'debug'
});
```

### 10.2 ログとデバッグ
```typescript
// ログレベル設定
client.setLogLevel('debug');

// イベントログ
client.on('*', (eventName, ...args) => {
  console.log(`Event: ${eventName}`, args);
});
```

### 10.3 モック対応
```typescript
// テスト時のモック使用
const mockClient = new MockAITuberTalkClient();
mockClient.setMockResponse('rooms.join', { 
  room: { id: 'test-room', name: 'Test Room' }
});
```

---

このSDK仕様書は、AITuberTalkをクライアントアプリケーションから利用するための完全なガイドです。開発者はこの仕様に従ってアプリケーションを構築し、AITuberTalkシステムと統合できます。