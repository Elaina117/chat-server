import asyncio
import websockets

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    print(f"[CONNECT] クライアント接続: {websocket.remote_address}", flush=True)
    try:
        async for message in websocket:
            print(f"[MESSAGE] {message}", flush=True)
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"[DISCONNECT] クライアント切断: {e}", flush=True)
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):
        print("[INFO] WebSocketサーバー起動（ポート10000）", flush=True)
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
