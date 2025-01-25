import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3
import time
import openpyxl
from openpyxl import Workbook

# 目标 URL 和请求头
generate_payload_url = "https://game.keitokun.com/api/v1/user/generatePayload"
login_url = "https://game.keitokun.com/api/v1/user/loginWithAddress"
headers = {
    "origin": "https://game.keitokun.com",
    "referer": "https://game.keitokun.com/?start=82747890482",
}

# 连接到以太坊节点
w3 = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))
if not w3.is_connected():
    raise ConnectionError("连接以太坊节点失败")

# 创建 Excel 工作簿
wb = Workbook()
ws = wb.active
ws.append(["私钥", "UID"])

# 生成和登录函数
def generate_and_login(target_count):
    count = 0
    while count < target_count:
        count += 1

        # 生成新的以太坊账户
        account = Account.create()
        private_key = account.key.hex()
        wallet_address = account.address

        # 发送 POST 请求获取 payload
        for _ in range(5):  # 尝试最多5次
            try:
                response = requests.post(generate_payload_url, headers=headers)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                print(f"获取 payload 失败: {e}")
                time.sleep(2)  # 等待2秒后重试
        else:
            continue

        response_data = response.json()
        payload_data = response_data.get("data", {}).get("payload", "")
        if not payload_data:
            print("未能获取有效的 payload")
            continue

        # 对 payload_data 进行编码并签名
        message = encode_defunct(text=payload_data)
        signed_message = w3.eth.account.sign_message(message, private_key=private_key)

        # 登录请求载荷
        login_payload = {
            "address": wallet_address,
            "payload": payload_data,
            "signature": f'0x{signed_message.signature.hex()}',
            "nickName": "",
            "avatar": "",
            "inviter": "66425469431"
        }

        # 发送登录请求
        for _ in range(2):  # 尝试最多2次
            try:
                login_response = requests.post(login_url, headers=headers, json=login_payload)
                login_response.raise_for_status()
                break
            except requests.RequestException as e:
                print(f"登录请求失败: {e}")
                time.sleep(2)  # 等待2秒后重试
        else:
            continue

        login_response_data = login_response.json()
        if not login_response_data or 'data' not in login_response_data:
            print("登录响应无效")
            continue

        # 获取 UID 并保存到 Excel
        uid = login_response_data['data'].get('uid', '')
        if uid:
            ws.append([private_key, uid])
            wb.save("uids_and_keys.xlsx")
            print(f"成功获取 UID: {uid}")

        # 增加请求间隔，防止频繁请求导致429
        time.sleep(5)

# 设置刷取账号数量
target_count = int(input("请输入要刷取的账号数量："))

# 执行生成和登录函数
generate_and_login(target_count)

print(f"所有操作已完成，共生成 {target_count} 个账号，数据已保存到 uids_and_keys.xlsx")
