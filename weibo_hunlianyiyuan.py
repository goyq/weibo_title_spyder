
import requests  # 发送请求
from bs4 import BeautifulSoup  # 解析网页
import pandas as pd  # 存取csv
from time import sleep  # 等待时间

names = []
urls = []
times = []
coms = []
shares = []
stars = []
talks = []

def get_info(url, headers):
    res = requests.get(url, headers=headers)
    # print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)

    for movie in soup.select('div[action-type="feed_list_item"]'):
        link_elem = movie.select_one('a[href^="//weibo.com"]')
        if link_elem:
            url = link_elem['href']
            urls.append(url)
        else:
            urls.append(None)

        name_elem = movie.select_one('div.name-container > a.name')
        if name_elem:
            name = name_elem.text.strip()
            names.append(name)
        else:
            names.append(None)


        time_elem = movie.select_one('div.from > a')
        if time_elem:
            time = time_elem.text.strip()
            times.append(time)
        else:
            times.append(None)

        com_elem = movie.select_one('p[node-type="feed_list_content"]')  # 定位评论元素
        if com_elem:
            com = com_elem.get_text(strip=True).strip('“”')  # 提取评论文本内容，并去除双引号
            coms.append(com)
        else:
            coms.append(None)

        share_elem = movie.find('a', class_='woo-box-flex')  # 定位包含分享数量的<a>标签
        if share_elem:
            share = share_elem.get_text(strip=True)  # 提取分享数量
            shares.append(share)
        else:
            shares.append(None)

        talk_elem = movie.find('a', attrs={"action-type": "feed_list_comment"})  # 定位包含评论数量的<a>标签
        if not talk_elem:
            talks.append(None)
        else:
            talk = talk_elem.get_text(strip=True)  # 提取评论数量
            talks.append(talk)

        star_elem = movie.find('span', class_='woo-like-count')  # 定位包含点赞数的<span>标签
        if star_elem:
            star = star_elem.get_text(strip=True)  # 提取点赞数
            stars.append(star)
        else:
            stars.append(None)
def save_to_csv(csv_name):
    """
    	数据保存到csv
    	:return: None
    	"""
    df = pd.DataFrame()  # 初始化一个DataFrame对象
    df['链接'] = urls
    df['名称'] = names
    df['时间'] = times
    df['发表'] = coms
    df['分享'] = shares
    df['讨论'] = talks
    df['点赞'] = stars

    df.to_csv(csv_name, encoding='utf_8_sig')  # 将数据保存到csv文件


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://s.weibo.com/',
        'Cookie': 'SINAGLOBAL=4198425753724.6196.1703872393612; UOR=www.google.com.hk,s.weibo.com,www.baidu.com; ALF=1713359927; SUB=_2A25I_E9nDeRhGeFK4lUT9CvPyTuIHXVocM6vrDV8PUJbkNAGLVTlkW1NQqBwEg_JrJnsUutr1FVXsEAI4WIBVdF4; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhDfWU6BxxY0ZUDNxOWxNkK5JpX5KzhUgL.FoMX1KMESh-0eoM2dJLoI7UDIHLxPc4a; XSRF-TOKEN=B1NCWry9o0-4iCpjQ-iKoMYO; WBPSESS=6-XyTdLlPV8Zcuke6Ery56_lZzlkLc3kpRQNfmHhtu9o1zFpvhScIcc0gyNIclqjIIUMwtwOIpnaIlmouz9Rratg7EKA9vX_QzRgJohumcEFWA59KULgCYXSE14-kkUm3bFA7jWkJOLTKUkR1x3PEg==; _s_tentry=weibo.com; Apache=9904094592780.258.1710861267812; ULV=1710861267817:4:1:1:9904094592780.258.1710861267812:1706949909141'
    }

    for i in range(50):
        page_url = 'https://s.weibo.com/weibo?q=%E5%A9%9A%E6%81%8B%E6%84%8F%E6%84%BF&page={}'.format(str(i))

        print('开始爬取第{}页，地址是:{}'.format(str(i + 1), page_url))
        get_info(page_url, headers)
        sleep(2)  # 等待1秒(防止反爬)
    # 保存到csv文件
    save_to_csv(csv_name="weibo_myself.csv")