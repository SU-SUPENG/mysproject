from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# 创建一个数据库user表模型
# class User(models.Model):
#     # 如果没有的话，默认会生成一个名称为 id 的列，如果要显示的自定义一个自增列
#     id = models.AutoField(primary_key=True)
#     # 类里面的字段代表数据表中的字段(username)，数据类型则由CharField（相当于varchar）
#     username = models.CharField(max_length=100)
#     # 密码
#     password = models.CharField(max_length=100)

class Topic(models.Model):
    #用户学习的主题
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)   #记录日期和时间
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        #返回模型的字符串表示
        return self.text

class Entry(models.Model):
    #学到的有关某个主题的具体知识
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]}..."