import requests
from web3 import Web3
from eth_account import Account, messages
import os
import time # 用于添加延迟，避免请求过于频繁

# --- 配置 ---
RPC_URL = "https://testnet.dplabs-internal.com"
CHAIN_ID = 688688
MESSAGE_TO_SIGN = "pharos"

# --- API 端点配置 ---
API_BASE_URL = "https://api.pharosnetwork.xyz"
LOGIN_ENDPOINT = "/user/login"
SIGN_IN_ENDPOINT = "/sign/in"
WALLET_TYPE = "OKX Wallet"
INVITE_CODE = "M9vzbr27vscGczeB"

# --- 私钥文件路径 ---
PRIVATE_KEYS_FILE = "address.txt" # 你的私钥文件路径，每行一个私钥

# --- 其他设置 ---
REQUEST_DELAY_SECONDS = 3 # 每个私钥处理完毕后等待的秒数，避免请求过快被封禁

# --- Web3 连接 (全局一次性初始化) ---
try:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if w3.is_connected():
        print(f"成功连接到 RPC 网络: {RPC_URL}")
    else:
        print(f"警告：无法连接到 RPC 网络: {RPC_URL}，签名是离线操作，不影响签名本身。")
except Exception as e:
    print(f"初始化 Web3 连接失败: {e}")
    w3 = None # 如果连接失败，设置为 None

def process_private_key(private_key_str: str, account_index: int):
    """
    处理单个私钥的登录和签到流程。
    """
    print(f"\n{'='*50}")
    print(f"开始处理第 {account_index} 个账户...")
    print(f"私钥 (部分显示): {private_key_str[:6]}...{private_key_str[-4:]}")

    # 清除私钥字符串两端的空白符，防止读取文件时产生问题
    private_key_str = private_key_str.strip()

    if not private_key_str:
        print("跳过空行或无效私钥。")
        return

    # 为每个账户创建一个新的会话，避免会话状态交叉影响
    session = requests.Session()

    try:
        # --- 1. 从私钥创建账户对象并获取地址 ---
        account = Account.from_key(private_key_str)
        wallet_address = account.address
        print(f"账户地址: {wallet_address}")

        # --- 2. 签名消息 ---
        encoded_message = messages.encode_defunct(text=MESSAGE_TO_SIGN)
        signed_message = account.sign_message(encoded_message)
        signature_hex = Web3.to_hex(signed_message.signature)
        # print(f"生成的签名: {signature_hex}") # 签名较长，按需打印

        # --- 3. 发送登录请求 (POST /user/login) ---
        login_params = {
            "address": wallet_address,
            "signature": signature_hex,
            "wallet": WALLET_TYPE,
            "invite_code": INVITE_CODE
        }
        login_url = f"{API_BASE_URL}{LOGIN_ENDPOINT}"

        login_headers = {
            "Origin": "https://testnet.pharosnetwork.xyz",
            "Referer": "https://testnet.pharosnetwork.xyz/",
        }

        print(f"  > 正在尝试登录...")
        login_response = session.post(login_url, params=login_params, headers=login_headers)
        login_response.raise_for_status()

        login_json_response = login_response.json()
        if login_json_response.get("code") == 0:
            jwt_token = login_json_response.get("data", {}).get("jwt")
            if jwt_token:
                print(f"  > 登录成功，获取到 JWT。")
            else:
                raise ValueError("登录响应中未找到 JWT。")
        else:
            raise ValueError(f"登录失败或响应格式不正确: {login_json_response.get('msg', '未知错误')} (Code: {login_json_response.get('code')})")

        # --- 4. 发送签到请求 (POST /sign/in) ---
        sign_in_params = {
            "address": wallet_address,
        }
        sign_in_url = f"{API_BASE_URL}{SIGN_IN_ENDPOINT}"

        sign_in_headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Origin": "https://testnet.pharosnetwork.xyz",
            "Referer": "https://testnet.pharosnetwork.xyz/",
        }

        print(f"  > 正在尝试签到...")
        sign_in_response = session.post(sign_in_url, params=sign_in_params, headers=sign_in_headers)
        sign_in_response.raise_for_status()

        sign_in_json_response = sign_in_response.json()
        if sign_in_json_response.get("code") == 0:
            print(f"  > 签到成功！消息: {sign_in_json_response.get('msg', '无消息')}")
        else:
            print(f"  > 签到失败！消息: {sign_in_json_response.get('msg', '未知错误')} (Code: {sign_in_json_response.get('code')})")
            # 根据错误码判断是否已经签到过，或是否需要处理其他情况
            if "already signed in" in sign_in_json_response.get('msg', '').lower():
                print("  > 提示：该账户今天可能已经签到过了。")

    except requests.exceptions.RequestException as e:
        print(f"  > 请求发生错误: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  > 响应状态码: {e.response.status_code}")
            print(f"  > 响应内容: {e.response.text}")
    except ValueError as e:
        print(f"  > 处理数据或配置错误: {e}")
    except Exception as e:
        print(f"  > 发生未知错误: {e}")
    finally:
        print(f"完成处理第 {account_index} 个账户。")
        print(f"{'='*50}\n")


def main():
    """主函数，读取私钥文件并循环处理。"""
    try:
        with open(PRIVATE_KEYS_FILE, 'r') as f:
            private_keys = f.readlines()

        if not private_keys:
            print(f"错误：'{PRIVATE_KEYS_FILE}' 文件为空或不存在。请确保文件中每行有一个私钥。")
            return

        print(f"从 '{PRIVATE_KEYS_FILE}' 读取到 {len(private_keys)} 个私钥。")

        for i, pk in enumerate(private_keys):
            process_private_key(pk, i + 1) # i+1 作为账户序号，更直观
            if i < len(private_keys) - 1: # 如果不是最后一个账户，则等待
                print(f"等待 {REQUEST_DELAY_SECONDS} 秒后处理下一个账户...")
                time.sleep(REQUEST_DELAY_SECONDS)

    except FileNotFoundError:
        print(f"错误：私钥文件 '{PRIVATE_KEYS_FILE}' 未找到。请确保文件存在于脚本同目录下。")
    except Exception as e:
        print(f"读取私钥文件时发生错误：{e}")

if __name__ == "__main__":
    main()