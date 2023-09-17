#https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/505/505-bigskin-1.jpg
#https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/505/505-bigskin-2.jpg
#https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/505/505-bigskin-3.jpg
import requests
import re
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
url='https://pvp.qq.com/web201605/herodetail/505.shtml'
response=requests.get(url,headers=headers)
response.encoding='gbk'
heros=re.findall('data-imgname="(.*?)">',response.text)[0].split('|')
num=1
for hero in heros:
    hero=hero.split('&')[0]
    link=f'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/505/505-bigskin-{num}.jpg'
    num+=1
    jpg=requests.get(link,headers=headers).content
    with open('img\\'+hero+'.jpg','wb') as f:
        f.write(jpg)
    print(link,hero)