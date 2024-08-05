from django.db import models

from usersapp.models import Address, UserInfo
from goods.models import Goods,GoodsSize
# Create your models here.
class Order(models.Model):
    # 订单编号
    out_trade_num = models.UUIDField()
    #交易号
    order_num = models.CharField(max_length=50)
    trade_no = models.CharField(max_length=120, default='')
    status = models.CharField(max_length=20, default='待支付')
    payway = models.CharField(max_length=20, default='alipay')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class OrderItem(models.Model):
    goodsid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    #获取商品大图
    def getGimages(self):
        good = Goods.objects.get(id=self.goodsid)
        return good.gimage

    #获取商品名称
    def getGname(self):
        good = Goods.objects.get(id=self.goodsid)
        return good.gname

    #获取商品单价
    def getGunitprice(self):
        good = Goods.objects.get(id=self.goodsid)
        return good.gprice

    #获取商品总价格价格
    def getGprice(self):
        good = Goods.objects.get(id=self.goodsid)
        return good.gprice * self.count

    #获取商品尺码
    def getGsize(self):
        size = GoodsSize.objects.get(id=self.sizeid)
        return size.sname