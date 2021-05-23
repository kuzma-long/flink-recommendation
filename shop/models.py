from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Users(AbstractUser):
    address = models.CharField(verbose_name='地址', max_length=1024, default='')

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = '用户表'


class Case_item(models.Model):
    name = models.CharField(verbose_name='商品名', max_length=320, default='')
    xinghao = models.CharField(verbose_name='商品型号', max_length=320, default='')
    lianjie = models.CharField(verbose_name='商品链接', max_length=320, default='')

    image = models.CharField(verbose_name='商品主图', max_length=320, default='')
    price = models.FloatField(verbose_name='价格', default=0)
    text = models.CharField(verbose_name='介绍', max_length=1024, default='')
    pingpai = models.CharField(verbose_name='品牌', max_length=32, default='')

    cpu = models.CharField(verbose_name='cpu', max_length=32, default='')
    leixing = models.CharField(verbose_name='类型', max_length=32, default='')
    neicun = models.CharField(verbose_name='内存', max_length=32, default='')
    xitong = models.CharField(verbose_name='系统', max_length=32, default='')
    cangdi = models.CharField(verbose_name='产地', max_length=32, default='')
    caizhi = models.CharField(verbose_name='材质', max_length=32, default='')
    yanse = models.CharField(verbose_name='颜色', max_length=32, default='')

    date = models.DateTimeField(verbose_name='时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品表'
        verbose_name_plural = '商品表'


class XinWei(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    case_item = models.ForeignKey(Case_item, on_delete=models.CASCADE)
    nums = models.IntegerField(verbose_name='次数', default=0)
    date = models.DateTimeField(verbose_name='时间', auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '行为表'
        verbose_name_plural = verbose_name


class Dianji(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    case_item = models.ForeignKey(Case_item, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='时间', auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '点击表'
        verbose_name_plural = verbose_name


class DaFen(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    case_item = models.ForeignKey(Case_item, on_delete=models.CASCADE)
    fenshu = models.FloatField(verbose_name='分数', default=0)
    date = models.DateTimeField(verbose_name='时间', auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '打分表'
        verbose_name_plural = verbose_name
