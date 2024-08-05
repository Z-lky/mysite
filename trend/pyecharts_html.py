# @时间 2024/7/30 21:52
# @Author：郑摇2021210510
# @File : pyecharts_html.py
from pyecharts.charts import Pie, Bar, WordCloud, Page
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.charts import Pie
from pyecharts.charts import Liquid
#大屏展示饼图
def title()-> Pie:
    # 创建 Pie 图表实例
    title = Pie(
        init_opts=opts.InitOpts(
            chart_id='view_pie',
            width='100vw',
            height='800px',  # 可以指定高度
            theme='dark'  # 使用暗色主题，或者你可以定义一个自定义主题
        )
    )

    # 设置全局选项
    title.set_global_opts(
        title_opts=opts.TitleOpts(
            title="基于中国汉服行情趋势数据可视化大屏",
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=32,
                color='white'
            ),
            pos_left='center'  # 标题居中
        ),
        legend_opts=opts.LegendOpts(is_show=False),  # 不显示图例
        # 可以添加更多全局选项，如工具箱等
    )
    return title

#连接数据库获取数据
import pymysql
# 数据库连接参数
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'mysitedb',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}

# 连接数据库
connection = pymysql.connect(**db_config)
try:
    with connection.cursor() as cursor:
        # 编写SQL查询，这里假设你的表名为brands，你关心的列名为name
        sql = "SELECT bname FROM trend_brandtrend LIMIT 10"
        cursor.execute(sql)

        # 获取所有查询结果
        results = cursor.fetchall()

        # 将结果转换为列表，这里假设我们只关心name列
        brands_list = [row['bname'] for row in results]

        # 提交事务（如果没有修改数据，这一步可以省略）
    # connection.commit()
finally:
    # 关闭数据库连接
    connection.close()

# 测试输出结果
# print(brands_list)
#品牌条形图右边
def bar()-> Bar():
    sales_amounts = [8002.7, 5288.1, 3709.2, 3248.8, 2940.6, 2796.8, 1641.9, 1453.8, 1384.8, 1196.1]
    x_data = brands_list
    bar = (
        # 条形图
        Bar(
            # 初始化配置项
            init_opts=opts.InitOpts(
                theme='chalk',  # 图表主题 white dark
                chart_id='view_bar'
            )
        )
        .set_global_opts(
            # 标题配置项
            title_opts=opts.TitleOpts(
                title="品牌热度排行top10",  # 主标题
            ),
            legend_opts=opts.LegendOpts(
                border_width=0,
                pos_left='right',  # 图例位置
            ),
            xaxis_opts=opts.AxisOpts(
                name="品牌名称",


            ),
            yaxis_opts=opts.AxisOpts(
                name="销售量",

            ),
        )
        # X轴配置
        .add_xaxis(xaxis_data=x_data)
        # Y轴配置
        .add_yaxis("销售金额（万元）", y_axis=sales_amounts, stack='all', is_realtime_sort=True)
        # 颜色配置
        .set_colors(['lightgreen'])
        .set_series_opts(
            label_opts=opts.LabelOpts(
                is_show=False
            ),
        )
    )
    return bar

#雷达图
from pyecharts.charts import Radar

def create_Radar() -> Radar():
    v1 = [[4300, 30000, 20000, 15000, 12000, 29000]]
    v2 = [[5000, 40000, 28000, 20000, 22000, 30000]]
    radar = (
        Radar(
            init_opts=opts.InitOpts(
                theme='chalk',
                chart_id='view_radar'
            )
        )
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="明制", max_=6000),
                opts.RadarIndicatorItem(name="唐制", max_=72000),
                opts.RadarIndicatorItem(name="汉制", max_=65000),
                opts.RadarIndicatorItem(name="宋制", max_=56000),
                opts.RadarIndicatorItem(name="民国", max_=46000),
                opts.RadarIndicatorItem(name="战国", max_=70000),
            ]
        )
        .add("消费规模TGI", v1)
        .add("销售额TGI", v2)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                border_width=0,
                pos_right='30px',
            ),
            title_opts=opts.TitleOpts(title="消费规模与销售额TGI对比图"),
        )
    )
    return radar


#词云图
def create_wordcloud()-> WordCloud:
    words_data = [
        ("唐制", "1580"),
        ("马面裙", "9999"),
        ("襦裙", "777"),
        ("旗袍", "688"),
        ("宋制汉服", "588"),
        ("中山装", "516"),
        ("长裙", "515"),
        ("魏晋南北朝服饰", "483"),
        ("战国袍", "6882"),
        ("齐胸襦裙", "449"),
        ("披帛", "429"),
        ("古装", "399"),
        ("交领", "329"),
        ("袄裙", "399"),
        ("女侠装", "399"),
        ("古风", "399"),
        ("满褶裙", "546"),
        ("裥裙", "136"),
        ("明清", "746"),
        ("民国时期", "1746"),
        ("簪花", "5460"),
        ("上衣下裙", "1246"),
        ("披风", "1556"),
        ("发饰", "1509"),
    ]
    wordcloud = (
        WordCloud(
            init_opts=opts.InitOpts(
                theme='chalk',  # 图表主题 white dark
                chart_id='view_wordcloud'
            )

        )
        # 标题
        .set_global_opts(
            title_opts=opts.TitleOpts(title="汉服主题词云图"),
            legend_opts=opts.LegendOpts(
                border_width=0,
                pos_right='30px',
            ),
        )
        # 词云数据
        .add("", words_data, word_size_range=[20, 100], shape='circle')
    )
    return wordcloud

def create_liquid_chart() -> Liquid:
    liquid = (
        Liquid(
            init_opts=opts.InitOpts(
            theme='chalk',  # 图表主题 white dark
            chart_id='view_liquid'
            ))
        .add("lq", [0.48, 0.56])
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                border_width=0,
                pos_left='right',
            ),
            title_opts=opts.TitleOpts(title="汉服网络口碑评分")
        )
    )
    return liquid

#中间大地图
from pyecharts.charts import Map
from pyecharts import options as opts

def create_map_chart() -> Map:
    # 创建地图
    map = (
        Map(init_opts=opts.InitOpts(
            theme='chalk',  # 图表主题 white dark
            chart_id='view_map'
            ))
        .add("汉服话题热度", [list(z) for z in zip(Faker.provinces, Faker.values())], "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="汉服话题热度地区分布"),
            legend_opts=opts.LegendOpts(
                border_width=0,
                pos_bottom='50px',
                pos_left='500px'
            ),
            visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=False),  # 根据需要设置最大值和是否分段
        )
    )
    return map

def page() -> Page():
    page = (
        Page(
            # 页面标题
            page_title='基于中国汉服行情趋势数据可视化大屏',
            # 布局配置项
            layout=Page.DraggablePageLayout
        )
        .add(title(),bar(),create_Radar(),create_wordcloud(),create_liquid_chart(),create_map_chart() )
    )
    page.render(path='visual.html')

    # 用于 DraggablePageLayout 布局重新渲染图表
    page.save_resize_html(
        # Page 第一次渲染后的 html 文件
        source="visual.html",
        # 布局配置文件
        cfg_file="visual.json",
        # 重新生成的 .html 存放路径
        dest="visual_new.html"
    )
    return page


if __name__ == '__main__':
    # 全局设置主题颜色
    theme_config = ThemeType.CHALK  # 颜色方案
    # 表格和标题的颜色
    table_color = ""
    if theme_config == ThemeType.DARK:
        table_color = '#333333'
    elif theme_config == ThemeType.CHALK:#ok
        table_color = '#293441'
    elif theme_config == ThemeType.PURPLE_PASSION:
        table_color = '#5B5C6E'
    elif theme_config == ThemeType.ROMANTIC:
        table_color = '#F0E8CD'
    elif theme_config == ThemeType.ESSOS:
        table_color = '#FDFCF5'
    else:
        table_color = ''
    page()





