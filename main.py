import asyncio
import websockets

clients = {}  # {websocket: username}
typing_users = set()  # 入力中のユーザーを追跡

async def notify_user_list():
    usernames = list(clients.values())
    message = "users:" + ",".join(usernames)
    await asyncio.gather(*[client.send(message) for client in clients])

async def notify_typing_status():
    typing_list = list(typing_users)
    message = "typing:" + ",".join(typing_list)
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
            if message.startswith("typing:"):
                # 入力状態の更新
                _, username, status = message.split(":", 2)
                if status == "true":
                    typing_users.add(username)
                else:
                    typing_users.discard(username)
                await notify_typing_status()
            else:
                # 通常のチャットメッセージ
                print(f"[CHAT] {message}", flush=True)
                for client in clients:
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
