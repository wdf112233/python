import json
import requests

# 设置RPC连接
RPC_URL = "https://lb.drpc.org/ogrpc?network=solana&dkey=Ak0gCMU0-EsepypDp8ZT8fDYBZU2j7gR77t6TgFkVp5j"

# Solana API 端点
API_URL_BIND = "https://erratic.finance/api/code/record"
API_URL_TASK = "https://erratic.finance/api/point/add"

# 邀请码
INVITE_CODE = "zYEfJlK"


def bind_invite_code(wallet_address):
    """绑定邀请码"""
    data = {
        "other_user_invite_code": INVITE_CODE,
        "login_wallpaper_id": wallet_address  # 直接使用钱包地址
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL_BIND, json=data, headers=headers)

    if response.status_code == 200:
        print(f"邀请码绑定成功：{wallet_address}")
    else:
        print(f"绑定失败：{wallet_address}, 错误: {response.text}")


def do_task(wallet_address, task_id):
    """执行任务"""
    data = {
        "wallpaper_id": wallet_address,  # 直接使用钱包地址
        "task_id": task_id
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL_TASK, json=data, headers=headers)

    if response.status_code == 200:
        print(f"任务 {task_id} 执行成功：{wallet_address}")
    else:
        print(f"任务 {task_id} 执行失败：{wallet_address}, 错误: {response.text}")


def process_wallets_from_file(file_path):
    """从文件中读取钱包地址并执行任务"""
    # 读取钱包地址列表
    with open(file_path, "r") as f:
        wallet_addresses = [line.strip() for line in f.readlines()]

    for wallet_address in wallet_addresses:
        # 绑定邀请码
        bind_invite_code(wallet_address)

        # 执行任务，任务顺序是1, 5, 6, 7, 8, 9
        task_ids = [1, 5, 6, 7, 8, 9]
        for task_id in task_ids:
            do_task(wallet_address, task_id)


def main():
    file_path = "wallt.txt"  # 钱包地址文件路径
    process_wallets_from_file(file_path)


if __name__ == "__main__":
    main()
