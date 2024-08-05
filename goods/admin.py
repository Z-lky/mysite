from django.contrib import admin

# Register your models here.
from goods.models import Goods, GoodsStyle
from django.utils.html import format_html

from mysite import settings

#设置登录主题
admin.site.site_header = '如梦令管理系统'
admin.site.site_title = '如梦令管理系统'

# admin 密码123456
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'gname', 'gprice', 'gspan', 'category_name']
    ordering = ['id']

    def category_name(self, obj):
        return obj.category_id

    category_name.short_description = '商品所属分类'
    def image_tag(self, obj):
        image_filename = obj.gimage
        # 构建完整的图片URL
        image_url = f"/{image_filename}"
        # 返回图片的HTML标签
        return format_html('<img src="{}" alt="Image" width="50" height="80" />'.format(image_url))

    image_tag.short_description = '商品图片'
    image_tag.allow_tags = True
admin.site.register(Goods, GoodsAdmin)


class GoodsStyleAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag', 'goodid']
    ordering = ['id']

    def goodid(self, obj):
        return obj.goods_id

    goodid.short_description = '所属商品ID'
    def image_tag(self, obj):
        image_filename = obj.gstyle
        # 构建完整的图片URL
        image_url = f"/{image_filename}"
        # 返回图片的HTML标签
        return format_html('<img src="{}" alt="Image" width="50" height="60" />'.format(image_url))

    image_tag.short_description = '商品风格图片'
    image_tag.allow_tags = True

admin.site.register(GoodsStyle, GoodsStyleAdmin)
