import requests
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
import json
from datetime import datetime

# 初始化Web3实例
w3 = Web3(Web3.HTTPProvider("https://arbitrum.llamarpc.com"))

# 钱包地址和私钥（注意：私钥不要在生产环境中硬编码）
private_key = ""
account = Account.from_key(private_key)
wallet_address = account.address

# 请求URL
url = "https://auth.privy.io/api/v1/siwe/init"

# 请求头
headers = {
    "cookie": "__cf_bm=2BdY0LmaJ8jwLTLntF9lgHIMSmnbOMR_5sQ1EGAZqDE-1735056937-1.0.1.1-V3MPlThh3H6SKo9ogPo2o6q9Dcab1rWLsrVNyIYL3VOYyZtqfLavaXoA6Bnw0UcveSiW180bai6VRrukJLjDKA; _cfuvid=H9KaLuw8NUL9eeGQAf2vrOkMD3TVRtk5ytqUwBKqUu4-1735056937493-0.0.1.1-604800000",
    "origin": "https://abstract.deform.cc",
    "privy-app-id": "clphlvsh3034xjw0fvs59mrdc",
    "privy-ca-id": "5ef5ca04-3436-4e2d-a0ef-047288cc3ca9",
    "privy-client": "react-auth:1.80.0-beta-20240821191745",
    "referer": "https://abstract.deform.cc/",
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

# 请求体
payload = {
    "address": wallet_address
}
response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    response_data = response.json()
    nonce = response_data['nonce']
    expires_at = response_data['expires_at']
    print("请求成功:", response_data)
else:
    print("请求失败:", response.status_code, response.text)
    exit()

# 签名内容
message = f"""abstract.deform.cc wants you to sign in with your Ethereum account:\n{wallet_address}\n\nBy signing, you are proving you own this wallet and logging in. This does not initiate a transaction or cost any fees.\n\nURI: https://abstract.deform.cc\nVersion: 1\nChain ID: 42161\nNonce: {nonce}\nIssued At: {expires_at}\nResources:\n- https://privy.io"""

# 对消息进行编码
encoded_message = encode_defunct(text=message)

# 对消息进行签名
signed_message = w3.eth.account.sign_message(encoded_message, private_key=private_key)

# 签名值
signature = f"0x{signed_message.signature.hex()}"
print(signature)

# 请求URL
url = "https://auth.privy.io/api/v1/siwe/authenticate"

# 请求头
headers = {
    "cookie": "__cf_bm=2BdY0LmaJ8jwLTLntF9lgHIMSmnbOMR_5sQ1EGAZqDE-1735056937-1.0.1.1-V3MPlThh3H6SKo9ogPo2o6q9Dcab1rWLsrVNyIYL3VOYyZtqfLavaXoA6Bnw0UcveSiW180bai6VRrukJLjDKA; _cfuvid=H9KaLuw8NUL9eeGQAf2vrOkMD3TVRtk5ytqUwBKqUu4-1735056937493-0.0.1.1-604800000",
    "origin": "https://abstract.deform.cc",
    "privy-app-id": "clphlvsh3034xjw0fvs59mrdc",
    "privy-ca-id": "5ef5ca04-3436-4e2d-a0ef-047288cc3ca9",
    "privy-client": "react-auth:1.80.0-beta-20240821191745",
    "referer": "https://abstract.deform.cc/",
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

# 请求体
payload = {
    "message": message,
    "signature": signature,
    "chainId": "eip155:5611",
    "walletClientType": "okx_wallet",
    "connectorType": "injected"
}

# 发送POST请求
usertoken = requests.post(url, headers=headers, json=payload)

# 检查响应状态码
if usertoken.status_code == 200:
    # 打印响应内容
    print("请求成功:", usertoken.json())
else:
    print("请求失败:", usertoken.status_code, usertoken.text)



usertoken1=usertoken.json()
# 提取 token 和 identity_token
token = usertoken1.get('token')
identity_token = usertoken1.get('identity_token')

#绑定邀请码
# 请求URL
url = "https://api.deform.cc/"

# 请求荷载
payload = {
    "operationName": "UserLogin",
    "variables": {
        "data": {
            "externalAuthToken": token
        }
    },
    "query": "mutation UserLogin($data: UserLoginInput!) {\n  userLogin(data: $data)\n}"
}

# 发送请求并处理响应
response = requests.post(url, json=payload)
response_data1 = response.json()
print(response_data1)

# 提取 userLogin 的值
user_login = response_data1['data']['userLogin']

# 请求URL
url = "https://api.deform.cc/"

# 请求头
headers = {
    "authorization": f"Bearer {user_login}",
    "origin": "https://abstract.deform.cc",
    "referer": "https://abstract.deform.cc/",
    "privy-id-token": identity_token
}

# 请求荷载
payload = {
    "operationName": "VerifyActivity",
    "variables": {
        "data": {
            "activityId": "ff4d031f-c16b-4137-8cac-efc8983771e5",
            "metadata": {
                "referralCode": "Z7v19LJO2bKJ"#这里替换邀请码
            }
        }
    },
    "query": "mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
}

# 发送请求并处理响应
response = requests.post(url, headers=headers, json=payload)
response_data = response.json()
print(response_data)

#做任务一

url1 = "https://api.deform.cc/"

payload1={"operationName":"VerifyActivity","variables":{"data":{"activityId":"ef348b9f-20b1-41f7-929d-09d4f163cc0d"}},"query":"mutation VerifyActivity($data: VerifyActivityInput!) {\n  verifyActivity(data: $data) {\n    record {\n      id\n      activityId\n      status\n      properties\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    missionRecord {\n      id\n      missionId\n      status\n      createdAt\n      rewardRecords {\n        id\n        status\n        appliedRewardType\n        appliedRewardQuantity\n        appliedRewardMetadata\n        error\n        rewardId\n        reward {\n          id\n          quantity\n          type\n          properties\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"}
response1 = requests.post(url, headers=headers, json=payload1)
response_data1 = response1.json()
print(response_data1)
