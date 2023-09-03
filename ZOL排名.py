import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

#解析网站，并保存
url = "https://top.zol.com.cn/compositor/28/cpu.html"
html_content = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_content, 'html.parser')

#提取商品名称与其价格
shops = soup.findAll("div", {"class":"rank__name"})
moneys = soup.findAll('div',{"class":"rank__price"})

#用来获取前50排名的充电宝
for i in range(0,50):
    shop_name = shops[i].get_text(strip=True)
    money_text = moneys[i].get_text(strip=True).replace('￥','')
    rank=i+1
    print(f"{rank}.型号：{shop_name}，价格：{money_text}")

