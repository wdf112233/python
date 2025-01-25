import asyncio
import websockets
import json
import time

# 读取 UID 文件
def read_uids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# WebSocket 连接并发送数据
async def send_requests(uid):
    uri = f"wss://game.keitokun.com/api/v1/ws?uid={uid}"
    async with websockets.connect(uri) as websocket:
        # 构建发送数据
        timestamp = int(time.time() * 1000)
        data = {
            "id": 1,
            "cmd": 1001,
            "uid": uid,
            "data": {
                "amount": 10000,
                "collectNum": 1,
                "timestamp": timestamp
            }
        }

        # 发送数据
        await websocket.send(json.dumps(data))
        print(f"Sent data for UID {uid}")

        # 接收响应
        response = await websocket.recv()
        response_data = json.loads(response)
        print(f"Received response for UID {uid}: {response_data}")

# 主函数
async def main():
    uids = read_uids('uid.txt')
    for uid in uids:
        await send_requests(uid)

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())
