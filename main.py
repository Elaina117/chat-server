# main.py
import asyncio
import websockets

clients = set()

async def handler(websocket, path):
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"[MESSAGE] {message}")  # 送信者＋メッセージ内容をログに出力
            for client in clients:
                if client != websocket:
                    await client.send(message)
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):
        print("[INFO] WebSocketサーバー起動済み（ポート10000）")
        await asyncio.Future()  # 永久に待機

if __name__ == "__main__":
    asyncio.run(main())
