import asyncio
import websockets

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"[MESSAGE] {message}")
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"[INFO] クライアント切断: {e}")
    except Exception as e:
        print(f"[ERROR] 予期せぬエラー: {e}")
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):
        print("[INFO] WebSocketサーバー起動済み（ポート10000）")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
