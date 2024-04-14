#by.鲨鱼辣椒
#作者不易，禁止外传！
#注册前先去官网自行尝试是否可以发送邮箱
import requests
import json
import time  # 添加延迟
import email
import imaplib
import re
from random import choice


# 函数：清理 URL
def clean_url(url):
    url = url.replace('=\r\n', '')
    url = re.sub(r"=[0-9A-Fa-f]{2}", lambda x: bytes.fromhex(x.group(0)[1:]).decode('utf-8'), url)
    return url


# 函数：打开 URL
def open_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"URL {url} opened successfully. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to open URL {url}. Error: {e}")


# 函数：模拟登录
def login(email, password):
    url = 'https://multisynq.io/users/login'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Origin': 'https://multisynq.io',
        'Referer': 'https://multisynq.io/auth',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
    }
    payload = {
        "email": email,
        "password": password,
        "reactivationToken": None
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print(f"登录成功 - {email}")
        with open('成功.txt', 'a') as file:
            file.write(f"{email}----{password}\n")  # 将成功的邮箱和密码写入文件
        return response.json()
    else:
        print(f"登录失败 - {email}", response.text)
        return None


# 函数：生成随机名称
def generate_random_name():
    first_names = ["John", "Jane", "Alex", "Emily", "Arthur", "Grace"]
    last_names = ["Doe", "Smith", "Johnson", "Lee", "Brown", "Davis"]
    return choice(first_names), choice(last_names)


# 函数：更新用户详细信息
def update_user_details(login_response):
    first_name, last_name = generate_random_name()
    user_details_id = login_response["user"]["userDetails"]["_id"]
    token = login_response["token"]

    url = 'https://multisynq.io/users/updateUserDetails'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    payload = {
        "_id": user_details_id,
        "firstName": first_name,
        "lastName": last_name,
        "onboarded": True,
        "isCoder": False,
        "isNoder": True,
        "createdAt": "2024-04-14T13:28:50.405Z",
        "updatedAt": "2024-04-14T13:36:12.287Z",
        "__v": 0,
        "user": login_response["user"]["_id"]
    }
    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("用户详细信息已更新")
        print(response.json())
    else:
        print("更新用户详细信息失败", response.text)
        with open('失败.txt', 'a') as file:
            file.write(f"更新用户详细信息失败 - {response.text}\n")


# 从文件中读取邮箱和密码
def read_emails_from_file(file_path):
    emails = []
    with open(file_path, 'r') as file:
        for line in file:
            email, password = line.strip().split('----')
            emails.append((email, password))
    return emails


# 主程序
emails = read_emails_from_file('email.txt')
for email, password in emails:
    # 注册账户
    url_signup = 'https://multisynq.io/users/signup'
    headers_signup = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Content-Type': 'application/json',
        'Origin': 'https://multisynq.io',
        'Referer': 'https://multisynq.io/auth?referral=0827634c42250bd0',  # 这里换你的邀请码
        'Sec-Ch-Ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
    }
    payload_signup = {
        "email": email,
        "password": password,
        "confirmPassword": password,
        "subscribedToNewsletter": "true",
        "acceptedTerms": "true",
        "referralCode": "0827634c42250bd0"  # 这里也要换上你的邀请码
    }
    payload_json_signup = json.dumps(payload_signup)
    response_signup = requests.post(url_signup, headers=headers_signup, data=payload_json_signup)
    print(f"注册账户 - 状态码: {response_signup.status_code} - {email}")
    print(f"注册账户 - 响应内容: {response_signup.text}")

    # 登录并更新用户详细信息
    login_response = login(email, password)
    if login_response:
        update_user_details(login_response)

    # 添加延迟
    time.sleep(5)  # 暂停1秒
