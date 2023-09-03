import requests
from bs4 import BeautifulSoup
html='https://read.zongheng.com/chapter/672340/38704886.html'
response= requests.get(html).text
soup= BeautifulSoup(response, 'html.parser')
chapter_content = soup.find('div', class_='content')
print(chapter_content.text)


