from django.db import models

from goods.models import Goods
from usersapp.models import UserInfo


# Create your models here.
class Evaluation(models.Model):
    #评价内容
    content = models.TextField()
    #上传图片
    picture = models.ImageField(upload_to='static/images/evaluation/', blank=True, null=True)
    #评价时间
    time = models.DateTimeField(auto_now_add=True)
    #被评价的用户
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    #获取用户名称
    def getName(self):
        return self.user.uname
