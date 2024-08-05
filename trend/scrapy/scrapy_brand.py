# @时间 2024/7/20 10:48
# @Author：郑摇2021210510
# @File : scrapy_brand.py

import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.weili.tv/information/news/2021/05/18/archives/13345"

response = requests.get(url=url)
soup = BeautifulSoup(response.content, 'html.parser')

# 查找所有的<p>标签
p_tags = soup.find_all('p', limit=55)

# 遍历<p>标签，查找并打印<strong>标签的内容
content = []
for p in p_tags:
    strong_tags = p.find_all('strong')
    if strong_tags:  # 确保<p>标签内存在<strong>标签
        for strong in strong_tags:
            content.append(strong.text.strip())

#因为p标签有<p>&nbsp;</p>这种空白标签，所以只取到48条数据
print(content)


# CSV文件名称
filename = 'brand.csv'

# 打开文件以写入
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # 写入标题（可选）
    writer.writerow(['序号', '内容'])

    # 遍历数据列表
    for item in content:
        # 使用split方法分割字符串，这里假设使用逗号分割
        # 如果实际是中文全角顿号，请替换为'、'
        number, content = item.split('、', 1)  # 第二个参数限制分割次数，避免过度分割

        # 写入CSV文件
        writer.writerow([number, content])

print(f'数据已保存到 {filename}')
