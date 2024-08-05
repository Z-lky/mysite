import decimal

from django.db import models

from goods.models import Goods, GoodsSize
from usersapp.models import UserInfo


# Create your models here.
class CartItem(models.Model):
    goodsid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    isdelete = models.BooleanField(default=False)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    class Meta:
        # 绑定在一起的字段，联合唯一索引
        unique_together = ('goodsid', 'sizeid')

    def getGoods(self):
        return Goods.objects.get(id=self.goodsid)

    def getSize(self):
        return GoodsSize.objects.get(id=self.sizeid)

    def getTotalPrice(self):
        return float(self.getGoods().gprice) * int(self.count)
