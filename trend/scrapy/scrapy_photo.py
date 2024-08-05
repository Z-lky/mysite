# @时间 2024/7/19 11:42
# @Author：郑摇2021210510
# @File : scrapy_photo.py
import os
import random

import requests
from bs4 import BeautifulSoup


def get_img_url(keyword):
    """发送请求，获取接口中的数据"""
    # 接口链接
    url = 'https://image.baidu.com/search/acjson?'

    # 请求头模拟浏览器
    headers_list = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    ]

    # 随机选择一个请求头
    headers = random.choice(headers_list)

    # 构造网页的params表单
    params = {
        'tn': 'resultjson_com',
        'logid': '6918515619491695441',
        'ipn': 'rj',
        'ct': '201326592',
        'is': '',
        'fp': 'result',
        'queryWord': f'{keyword}',
        'word': f'{keyword}',
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '-1',
        'z': '',
        'ic': '',
        'hd': '',
        'latest': '',
        'copyright': '',
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': '0',
        'istype': '2',
        'qc': '',
        'nc': '1',
        'fr': '',
        'expermode': '',
        'force': '',
        'cg': 'girl',
        'pn': 1,
        'rn': '10',
        'gsm': '1e',
    }

    proxie = get_proxy()
    proxies = {"http": proxie}
    # 携带请求头和params表达发送请求
    response = requests.get(url=url, headers=headers, params=params, proxies=proxies)
    # 设置编码格式
    response.encoding = 'utf-8'
    # 转换为json
    json_dict = response.json()
    # 定位到30个图片上一层
    data_list = json_dict['data']
    print(data_list)
    # 删除列表中最后一个空值
    del data_list[-1]
    # 用于存储图片链接的列表
    img_url_list = []
    img_name_list = []
    for i in data_list:
        img_url = i['thumbURL']
        img_name = i['fromPageTitle']
        # 打印一下图片链接
        print(img_url)
        img_url_list.append(img_url)
        img_name_list.append(img_name)
        print(img_name_list)
    # 返回图片列表
    return img_url_list, img_name_list


# 定义获取代理地址的方法
def get_proxy():
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    pages = 5
    # 定义proxy_ips列表存储代理地址
    proxy_ips = []
    # 设置headers
    headers = {"User-Agent": ua}
    # 从第一页开始循环访问
    for page in range(1, pages + 1):
        # print(f"正在爬取第{page}页!")
        url = "https://www.89ip.cn/index_{page}.html"
        res = requests.get(url, headers=headers)
        # 使用.text属性获取网页内容，赋值给html
        html = res.text
        # 用BeautifulSoup()传入变量html和解析器lxml，赋值给soup
        soup = BeautifulSoup(html, "html.parser")
        # 使用find_all()方法查找类名为layui-table的标签
        table = soup.find_all(class_="layui-table")[0]
        # 使用find_all()方法查找tr标签
        trs = table.find_all("tr")
        # 使用for循环逐个访问trs列表中的tr标签,一个tr代表一行，第一行为表头，不记录
        for i in range(1, len(trs)):
            # 使用find_all()方法查找td标签
            ip = trs[i].find_all("td")[0].text.strip()
            port = trs[i].find_all("td")[1].text.strip()
            # 拼接代理地址
            proxy_ip = f"http://{ip}:{port}"
            # 将获取的代理地址保存到proxy_ips列表
            proxy_ips.append(proxy_ip)
    return random.choice(proxy_ips)


def get_down_img(img_url_list, img_name_list, keyword):
    current_path = os.getcwd()
    target_directory = os.path.join(current_path, keyword)
    if os.path.exists(target_directory) and os.path.isdir(target_directory):
        print("slk")
    else:
        # # 在当前路径下生成存储图片的文件夹
        os.mkdir(f"{keyword}")

    # 定义图片编号
    n = 0
    for img_url in img_url_list:
        # 拼接图片存放地址和名字
        img_path = f'./{keyword}/' + img_name_list[n] + '.jpg'
        print(img_path)
        r = requests.get(f'{img_url}')
        # 将图片写入指定位置
        with open(img_path, 'wb') as f:
            f.write(r.content)
            print("已下载")
        # 图片编号递增
        n = n + 1


if __name__ == '__main__':
    # 1. 修改关键词
    keyword = input("-》》输入关键词：")
    # 2. 获取指定关键词的图片链接
    img_url_list, img_name_list = get_img_url(keyword)
    # 3. 下载图片到指定位置
    get_down_img(img_url_list, img_name_list, keyword)
