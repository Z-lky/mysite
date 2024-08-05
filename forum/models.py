from django.db import models
from usersapp.models import UserInfo
# Create your models here.
class Writings(models.Model):
    #创建时间
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    #用户外键
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


    def __str__(self):
        return f"title: { self.title}"

    class Meta:
        verbose_name_plural = '收集信息列表'

    def getUname(self):
        return UserInfo.objects.get(id=self.user_id).uname