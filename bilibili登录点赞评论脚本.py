from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from chaojiying import Chaojiying_Client
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get(r'https://www.bilibili.com/')

# 使用 By.CSS_SELECTOR 来指定查找方式
#用来寻找登录接口
driver.find_element(By.CSS_SELECTOR, '#i_cecream > div.bili-feed4 > div.bili-header.large-header > div.bili-header__bar > ul.right-entry > li:nth-child(1) > li > div.right-entry__outside.go-login-btn > div').click()
time.sleep(1)
# 继续使用 By.CSS_SELECTOR 查找其他元素
#登录账号与密码输入
driver.find_element(By.CSS_SELECTOR, 'body > div.bili-mini-mask > div > div.bili-mini-login-right-wp > div.login-pwd-wp > form > div:nth-child(1) > input[type=text]').send_keys('账号')
driver.find_element(By.CSS_SELECTOR, 'body > div.bili-mini-mask > div > div.bili-mini-login-right-wp > div.login-pwd-wp > form > div:nth-child(3) > input[type=password]').send_keys('密码')
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, 'body > div.bili-mini-mask > div > div.bili-mini-login-right-wp > div.login-pwd-wp > div.btn_wp > div.btn_primary').click()


#获取验证码，并验证，登录账号
time.sleep(3)
img_label=driver.find_element(By.CSS_SELECTOR, '.geetest_holder.geetest_silver .geetest_widget')
img_label.screenshot('yzm.png')
time.sleep(1)
chaojiying=Chaojiying_Client('超级鹰账号','超级鹰密码','用户id，默认的：96001')
im=open('yzm.png','rb').read()
#打码类型，[pic_str]用来获取需要点击的x，与y轴
result=chaojiying.PostPic(im,'9004')['pic_str']
for res in result.split('|'):
    x=res.split(',')[0]
    y=res.split(',')[1]
    print(x,y)
    action = ActionChains(driver)
    action.move_to_element_with_offset(img_label, int(x), int(y)).click().perform()

time.sleep(5)
driver.find_element(By.CSS_SELECTOR, '.geetest_holder.geetest_silver .geetest_panel .geetest_commit').click()

#一键三连

import random
import requests

a=[
    '盖中盖',
    '我选e5',
    '垃圾佬'
]

url='https://api.bilibili.com/x/v2/reply/add'
data={
'oid': '320524290',
'type': '1',
'message': '垃圾佬了',
'plat': '1',
'at_name_to_mid': '{}',
'csrf': '39c8d689d2ff18e1f61cd6f8d58c341d',
}
headers={
    "Cookie":
"保密",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}
respone=requests.post(url=url,data=data,headers=headers)
print(respone.json())