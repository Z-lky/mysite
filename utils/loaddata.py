from goods.models import *  # 从 goods 应用的 models.py 中导入所有模型
from django.db.transaction import atomic  # 导入 Django 的事务装饰器


# Django 的事务装饰器 @atomic 来确保数据库操作的原子性。原子性：一个事务中所做的全部操作，要么全部成功，要么全部失败。
# 使用事务装饰器，确保下面的函数内所有数据库操作都是原子的
@atomic
def test_model():
    with open('utils/jiukuaijiu.json') as fr:  # 打开文件'utils/jiukuaijiu.json'并准备读取
        import json  # 导入json模块（尽管这通常放在文件顶部）
        datas = json.loads(fr.read())  # 读取文件内容并解析为Python列表
        for data in datas:  # 遍历解析后的数据
            cate = Category.objects.create(cname=data['category'])  # 创建一个新的Category实例

            _goods = data['goods']  # 从当前数据中获取'goods'列表

            for goods in _goods:  # 遍历goods列表
                # 创建一个新的Goods实例
                good = Goods.objects.create(gname=goods['goodsname'],  # 设置商品名称
                                            gdesc=goods['goods_desc'],  # 设置商品描述
                                            price=goods['goods_price'],  # 设置商品价格
                                            oldprice=goods['goods_oldprice'],  # 设置商品原价
                                            category=cate)  # 设置商品分类

                sizes = []  # 初始化一个空列表来存储Size实例
                for _size in goods['sizes']:  # 遍历商品尺寸列表
                    if Size.objects.filter(sname=_size[0]).count() == 1:  # 检查尺寸是否已存在
                        size = Size.objects.get(sname=_size[0])  # 如果存在，则获取它
                    else:  # 如果不存在，则创建新的 Size 实例
                        size = Size.objects.create(sname=_size[0])
                    sizes.append(size)  # 将 Size 实例添加到列表中

                colors = []  # 初始化一个空列表来存储 Color 实例
                for _color in goods['colors']:  # 遍历商品颜色列表
                    color = Color.objects.create(colorname=_color[0], colorurl=_color[1])  # 创建新的 Color 实例
                    colors.append(color)  # 将 Color 实例添加到列表中

                for _spec in goods['specs']:  # 遍历商品规格列表
                    goodsdetails = Goodsdetailname.objects.create(gdname=_spec[0])  # 创建规格名称
                    for img in _spec[1]:  # 遍历规格下的图片列表
                        Goodsdetail.objects.create(goods=good, gdname=goodsdetails, gdurl=img)  # 创建规格详情（包括图片）

                for c in colors:  # 遍历颜色列表
                    for s in sizes:  # 遍历尺寸列表
                        Inventory.objects.create(count=100, goods=good, color=c, size=s)  # 为每种颜色和尺寸组合创建库存记录

#在控制台，运行以下命令：删除回滚
def deleteall():
    Category.objects.filter().delete()
    Color.objects.filter().delete()
    Size.objects.filter().delete()
