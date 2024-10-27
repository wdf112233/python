import requests
import json
import time
from datetime import datetime

# 明文定义 Server酱的 SendKey
sendkey = "SCT251772Tyk0ZX5ogJZhbZmEq5112HK8D"

# 示例请求头
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "_ga=GA1.1.459772012.1728732451; acw_tc=ba6550cdfb4deb682237891e660a72b9e03f1d67233c02a023c42dfb14e6a24f; locale=zh-cn;",
    "referer": "https://app.trendx.tech/strategy/35",
    "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "x-authorization": "7353b420d63ddc6f35f922aa5b670be36f595701da917aea12a47b3995fdb72c",
    "x-chain-id": "56"
}

# 上次检测到的最大 trigger_time
last_trigger_time = 0
# 已推送的代币地址集合
pushed_tokens = set()

# 格式化市值为k和m的简洁形式
def format_market_cap(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}m"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}k"
    else:
        return str(value)

# Server酱推送消息
def push_to_wechat(title, content):
    url = f"https://sctapi.ftqq.com/{sendkey}.send"
    data = {
        "title": title,
        "desp": content
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("推送成功。")
    else:
        print("推送失败。")

# 定义一个函数来进行检测
def check_tokens():
    global last_trigger_time  # 使用全局变量来存储上次检测的时间
    triggers_url = "https://app.trendx.tech/v1/dao/strategies/35/performances/triggers"
    response = requests.get(triggers_url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        try:
            triggers_data = response.json().get("data", {}).get("rows", [])

            if not triggers_data:
                print("没有触发器数据。")
                return

            # 获取所有比上次检测时间更新的触发器
            new_triggers = [trigger for trigger in triggers_data if json.loads(trigger["data"])["tokens"][0]["trigger_time"] > last_trigger_time]

            if not new_triggers:
                print("没有新的代币，跳过...")
                return

            # 更新上次检测的 trigger_time 为本次获取的最大值
            last_trigger_time = max(json.loads(trigger["data"])["tokens"][0]["trigger_time"] for trigger in new_triggers)

            # 遍历每个新触发的代币并推送
            for trigger in new_triggers:
                latest_token_data = json.loads(trigger.get("data", "{}"))
                latest_token_info = latest_token_data["tokens"][0]
                latest_token_address = latest_token_info["contract_address"]
                latest_token_name = latest_token_info["name"]
                trigger_time = latest_token_info["trigger_time"]

                # 打印监控时间和代币符号
                formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"监控时间: {formatted_time}")
                print(f"追踪到符合策略的代币: {latest_token_name}")

                # 如果这个代币已经推送过，就跳过
                if latest_token_address in pushed_tokens:
                    continue

                # 请求代币详细信息
                token_details_url = f"https://app.trendx.tech/v1/dao/public/token/{latest_token_address}/details"
                token_response = requests.get(token_details_url, headers=headers)

                if token_response.status_code == 200:
                    try:
                        token_details = token_response.json().get("data", {})
                        market_cap = float(token_details.get("marketCap", 0))
                        price = float(token_details.get("price", 0))

                        # 格式化市值并准备推送内容
                        formatted_market_cap = format_market_cap(market_cap)
                        content = (
                            f"代币名称: {latest_token_name}\n"
                            f"合约地址: {latest_token_address}\n"
                            f"当前市值: {formatted_market_cap}\n"
                            f"当前价格: ${price:.8f}\n"
                            f"查看详情: [点击查看]({token_details_url})\n"  # 添加查看详情链接
                        )
                        print(content)

                        # 推送到微信
                        push_to_wechat("新代币信息", content)

                        # 添加到已推送集合
                        pushed_tokens.add(latest_token_address)

                    except json.JSONDecodeError:
                        print("解析代币详情的JSON数据失败。")
                else:
                    print(f"请求代币详情失败，状态码: {token_response.status_code}")

        except json.JSONDecodeError:
            print("解析触发器数据的JSON数据失败。")
    else:
        print(f"请求触发器数据失败，状态码: {response.status_code}")

# 每5分钟检测一次
while True:
    print("开始新的检测...")
    check_tokens()
    print("检测结束，等待5分钟后再次检测。\n")
    time.sleep(300)  # 等待300秒（5分钟）
