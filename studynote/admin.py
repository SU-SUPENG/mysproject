from django.contrib import admin
from .models import Topic,Entry    #导入需要注册的模块
# Register your models here.
admin.site.register(Topic)     #让Django通过管理网站管理模块
admin.site.register(Entry)