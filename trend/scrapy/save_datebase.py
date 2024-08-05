# @时间 2024/7/30 21:37
# @Author：郑摇2021210510
# @File : save_datebase.py

import pandas as pd
import pymysql

# 数据库连接配置
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'mysitedb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# 读取CSV文件
df = pd.read_csv('brand.csv', encoding='utf-8-sig')  # 注意：有时需要指定编码为'utf-8-sig'来处理BOM

# 连接到数据库
connection = pymysql.connect(**config)

try:
    with connection.cursor() as cursor:
        # 遍历DataFrame的每一行
        for index, row in df.iterrows():
            # 构造SQL插入语句（这里使用参数化查询来防止SQL注入）
            sql = "INSERT INTO trend_brandtrend (id, bname) VALUES (%s, %s)"
            # 注意：pandas的DataFrame索引默认从0开始，但你的CSV文件序号从1开始，如果你想要保留序号，可以+1
            # 但如果id是自动增长的，你可以忽略序号列
            # 这里假设id是自增的，所以我们只插入content
            cursor.execute(sql, (None, row['内容']))  # None表示不插入id，因为数据库会自增

    # 提交事务
    connection.commit()
finally:
    connection.close()

print("数据已成功插入数据库")