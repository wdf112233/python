#视频学习地址：https://www.youtube.com/watch?v=exttkF7niKU&list=PL5y2P1AqpsZ8lcW-idM8wfJ2UuscAwrTV&index=8
import requests
from bs4 import BeautifulSoup

headers={
    "User-Agent":
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
for ks in range(0,250,25):

#这段代码使用了 requests.get 方法来获取指定URL的HTML内容，并使用了一个格式化字符串来动态地构建URL。其中的 {ks} 是一个占位符，它会被后面的变量替换。

#假设你在之前的代码中定义了 ks 变量，这个变量的值将被替换到URL中，从而构建一个完整的URL。这种做法通常用于构建具有动态参数的URL，以便根据不同的情况获取不同的网页内容。

#请确保在使用这个URL之前，ks 变量已经被正确地赋值，以便生成正确的URL并从网页获取内容。这种方式可以用于获取不同页面的内容，例如在你的代码中获取豆瓣电影Top 250列表的不同页面。

    htmla= requests.get(f"https://movie.douban.com/top250?start={ks}&filter=",headers=headers).text
    
    
#BeautifulSoup：这是BeautifulSoup库提供的主要类，用于将HTML文本解析为BeautifulSoup对象。

#htmla：这是你从网页获取的HTML文本内容。

#'html.parser'：这是指定解析器的名称，用于解析HTML文本。在这里，你使用了内置的 html.parser 解析器来解析HTML。

    soup=BeautifulSoup(htmla,'html.parser')


#通过创建一个BeautifulSoup对象，你可以使用其提供的方法和属性来搜索、提取和处理HTML文档中的各种元素和内容。
# 在你的代码中，你使用了 soup.findAll("span",attrs={"class":"title"}) 方法来查找所有具有 class 属性值为 "title" 的 <span> 元素，这些元素通常包含电影标题信息。
    books=soup.findAll("span",attrs={"class":"title"})

    for book in books:
        abook=book.string
        if "/" not in abook:
            print(abook)
