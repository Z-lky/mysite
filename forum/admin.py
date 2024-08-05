from django.contrib import admin
from forum.models import Writings
# Register your models here.
class WritingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_time', 'title', 'content', 'userid']
    ordering = ['id']

    def userid(self, obj):
        return obj.user_id

    userid.short_description = '意见所属用户id'

admin.site.register(Writings, WritingsAdmin)