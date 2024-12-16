import requests
import json
import random
import string

# 代理配置 (use a list of proxies if there are multiple)
tunnel = "i361.kdltpspro.com:15818"
username = "t13436622362077"
password = "gwu1ohhi"
proxies_list = [
    {"http": f"http://{username}:{password}@{tunnel}/", "https": f"http://{username}:{password}@{tunnel}/"},
    # Add more proxies as needed
]

# 读取 btcaddress.txt 中的地址
with open('btcaddress.txt', 'r') as f:
    btc_addresses = f.readlines()

# 随机生成一个数字或者字母组合
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_number():
    return random.randint(100000000, 999999999)

# 目标URL
url = "https://jndhgf5jnn6ehb0h.mikecrm.com/handler/web/form_runtime/handleSubmit.php"

# 设置请求头
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": (
        "uvi=KVEOuK6gSicMG8NvSfu9Ac5VJ8hEXXZDdbxwFiW97IyyvGjqE4wERf6L7tQLEO5f; "
        "uvis=KVEOuK6gSicMG8NvSfu9Ac5VJ8hEXXZDdbxwFiW97IyyvGjqE4wERf6L7tQLEO5f; "
        "mk_seed=14"
    ),
    "Host": "jndhgf5jnn6ehb0h.mikecrm.com",
    "Origin": "https://jndhgf5jnn6ehb0h.mikecrm.com",
    "Pragma": "no-cache",
    "Referer": "https://jndhgf5jnn6ehb0h.mikecrm.com/Bs7L3Gz",
    "Sec-CH-UA": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "X-Requested-With": "XMLHttpRequest",
}

# 构建请求负载
def create_payload(btc_address):
    return {
        "cvs": {
            "i": 200776590,
            "t": "Bs7L3Gz",
            "s": 202154977,
            "acc": "3YXZbgdmEBfCCrz8SxY0LojHYQp4QUvz",
            "r": "",
            "c": {
                "cp": {
                    "207979530": [generate_random_number()],
                    "207979532": [f"@{generate_random_string(6)}"],
                    "207979542": btc_address,  # Extracted Bitcoin address
                    "207979627": [generate_random_string(6)],
                    "207980908": [generate_random_string(6)],
                },
                "ext": {
                    "uvd": [207979627, 207979532, 207980908]
                }
            }
        }
    }

# 发送请求并处理响应
for index, btc_address in enumerate(btc_addresses):
    # 清理地址中的换行符
    btc_address = btc_address.strip()

    # 随机选择代理
    proxies = proxies_list[index % len(proxies_list)]  # Cycle through proxies if there are more BTC addresses than proxies

    payload = create_payload(btc_address)
    data = {"d": json.dumps(payload)}

    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, data=data, proxies=proxies, timeout=30)

        if response.status_code == 200:
            try:
                # 尝试解析JSON响应
                response_json = response.json()
                print(f"地址提交成功: {btc_address}")
                print(json.dumps(response_json, indent=4, ensure_ascii=False))
            except ValueError:
                # 如果响应不是JSON格式，打印文本内容
                print(f"地址提交成功: {btc_address}")
                print(response.text)
        else:
            print(f"请求失败，状态码: {response.status_code} 地址: {btc_address}")
            print("响应内容:")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"请求过程中出现错误，地址: {btc_address}")
        print(e)
