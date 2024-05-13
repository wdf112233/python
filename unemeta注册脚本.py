#by：鲨鱼辣椒
#vx：xiaofe999666
#项目网站:https://www.unemeta.com/rewards?invitationCode=kajugz

from web3 import Web3, HTTPProvider
from eth_account import Account
from eth_account.messages import encode_defunct
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 设置您的Web3连接
w3 = Web3(HTTPProvider('https://eth.llamarpc.com'))

def process_account(private_key):
    # Your existing code to process the account goes here
    # I've integrated your code into this function
    address = Account.from_key(private_key).address
    headers = {
        'Origin': 'https://www.unemeta.com',
        'Referer': 'https://www.unemeta.com/rewards?invitationCode=kajugz',
    }
    payload = {"walletAddress": address, "type": 1}
    response = requests.post('https://www.unemeta.com/api/backend/api/user/v1/users/nonce', json=payload, headers=headers)
    response_json = response.json()
    nonce = response_json['data']['noce']
    message_encoded = encode_defunct(text=nonce)
    signature = w3.eth.account.sign_message(message_encoded, private_key=private_key)
    sigtoken = signature.signature.hex()
    payload1 = {"wallet_address": address, "signData": sigtoken, "metamask": True}
    response1 = requests.post('https://www.unemeta.com/api/backend/api/user/v1/users/login', json=payload1, headers=headers)
    response_json1 = response1.json()
    token = response_json1['data']['accessToken']
    headers1 = {
        'Authorization': f'Bearer {token}',
        'Cookie': f'_ga=GA1.1.263651902.1715596689; UserWalletAddress={address}; Authorization={token}; _ga_D4LVCPH5H4=GS1.1.1715596688.1.1.1715596862.41.0.0',
        'Referer': 'https://www.unemeta.com/rewards?invitationCode=kajugz'
    }
    response2 = requests.get('https://www.unemeta.com/api/backend/api/project/v1/check/code?code=kajugz&is_score_code=1', headers=headers1)
    #code后面换上你的邀请码，测试无效，批量签到即可
    if response2.json()['code'] == 200:
        response3 = requests.get('https://www.unemeta.com/api/backend/api/project/v1/signin?source=2', headers=headers1)
        if response3.json()['code'] == 200:
            return True  # Process successful
    return False  # Process failed

def worker(private_key):
    try:
        if process_account(private_key):
            with open('registered.txt', 'a') as outfile:
                outfile.write(private_key + '\n')
            return f"Success: {private_key}"
        else:
            return f"Failed: {private_key}"
    except Exception as e:
        print(f"Error processing {private_key}: {e}")
        return f"Error: {private_key}"

def main():
    delay = 0  # 延迟时间，单位秒
    max_iterations = 1000  # 最大迭代次数
    current_iteration = 0  # 当前迭代计数器

    with open('unregistered.txt', 'r') as infile:
        private_keys = [line.strip() for line in infile if line.strip()]

    for private_key in private_keys:
        if current_iteration >= max_iterations:  # 检查是否达到迭代次数上限
            print("Reached the maximum number of iterations.")
            break  # 跳出循环

        result = worker(private_key)
        print(result)
        time.sleep(delay)  # 在每次处理后添加延迟
        current_iteration += 1  # 增加迭代计数器

if __name__ == "__main__":
    main()
