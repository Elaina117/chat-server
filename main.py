import asyncio
import websockets

clients = {}  # {websocket: username}

async def notify_user_list():
    usernames = list(clients.values())
    message = "users:" + ",".join(usernames)
    await asyncio.gather(*[client.send(message) for client in clients])

async def handler(websocket, path):
    try:
        # 最初のメッセージをユーザー名として受け取る
        username = await websocket.recv()
        clients[websocket] = username
        print(f"[CONNECT] {username} 接続 from {websocket.remote_address}", flush=True)

        # 接続後にユーザー一覧を全員に送信
        await notify_user_list()

        async for message in websocket:
            print(f"[MESSAGE] {message}", flush=True)
            for client in clients:
                if client != websocket:
                    await client.send(message)

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"[DISCONNECT] クライアント切断: {e}", flush=True)
    finally:
        if websocket in clients:
            username = clients[websocket]
            del clients[websocket]
            print(f"[DISCONNECT] {username} 切断", flush=True)
            await notify_user_list()

async def main():
    async with websockets.serve(handler, "0.0.0.0", 10000):
        print("[INFO] WebSocketサーバー起動（ポート10000）", flush=True)
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
