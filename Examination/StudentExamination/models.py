from django.db import models


# Create your models here.
class teacher(models.Model):
    """教师账号"""
    user = models.CharField(max_length=12, verbose_name="账号")
    passwd = models.CharField(max_length=100, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")


class admin(models.Model):
    """管理员账号"""
    user = models.CharField(max_length=12, verbose_name="账号")
    passwd = models.CharField(max_length=100, verbose_name="密码")
    email = models.EmailField(verbose_name="邮箱")


class test_paper(models.Model):
    """试卷内容"""
    subject = models.TextField(verbose_name="题目")
    option_a = models.CharField(max_length=10, verbose_name="选项A")
    option_b = models.CharField(max_length=10, verbose_name="选项B")
    option_c = models.CharField(max_length=10, verbose_name="选项C")
    option_d = models.CharField(max_length=10, verbose_name="选项D")
    answer = models.CharField(max_length=10, verbose_name="答案")
