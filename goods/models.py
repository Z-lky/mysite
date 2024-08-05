from django.db import models

# Create your models here.
class DynastySort(models.Model):
    dname = models.CharField(max_length=50, verbose_name='朝代名称')

    class Meta:
        verbose_name_plural = '朝代分类'

    def __str__(self):
        return f"DynastySort : {self.dname}"

class Category(models.Model):
    cname = models.CharField(max_length=50, verbose_name='分类名称')
    dynasty_sort = models.ForeignKey(DynastySort, on_delete=models.CASCADE, verbose_name='所属朝代')


    def __str__(self):
        return f"Category : {self.cname}"

    def get_dynasty_sort(self):
        return self.dynasty_sort.dname

    class Meta:
        verbose_name_plural = '商品分类'

class Goods(models.Model):
    gimage = models.ImageField(upload_to='static/images/clothing/', verbose_name='商品图片')
    gname = models.CharField(max_length=100, verbose_name='商品名称')
    gprice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    gspan = models.CharField(max_length=50, verbose_name='标签')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='商品所属分类')
    dynasty_sort = models.ForeignKey(DynastySort, on_delete=models.CASCADE, verbose_name='商品所属朝代')

    def __str__(self):
        return f"Goods : {self.gname}"

    class Meta:
        verbose_name_plural = '商品信息列表'



#商品尺码表
class GoodsSize(models.Model):
    sname = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = '商品尺码'


class GoodsStyle(models.Model):
    #整体样式
    gstyle = models.ImageField(upload_to='static/images/style/', verbose_name='商品样式图片')
    #外键关联商品
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='所属商品')

    def __str__(self):
        return f"GoodsStyle : {self.gstyle}"

    class Meta:
        verbose_name_plural = '商品样式'
