from django.contrib import admin
from . import models


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password')


admin.site.site_header = '商品推荐管理系统'
admin.site.site_title = '登录系统后台'
admin.site.index_title = '后台管理'

# 在admin中注册绑定
admin.site.register(models.Users, BlogAdmin)
admin.site.register(models.Case_item)
admin.site.register(models.XinWei)
admin.site.register(models.Dianji)
