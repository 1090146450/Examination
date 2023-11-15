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


class ProductDetails(models.Model):
    """商品详情"""
    pid = models.IntegerField()  # 商品编号
    pdName = models.CharField(max_length=255, verbose_name="商品名称")  # 商品名称
    Platform_Pdd = 0
    Platform_Tb = 1
    Platform_Jd = 2
    Platform_Other = 3
    Platform_Index = (
        (Platform_Pdd, "拼多多"),
        (Platform_Tb, "淘宝"),
        (Platform_Jd, "京东"),
        (Platform_Other, "其他")
    )
    purchasePlatform = models.PositiveIntegerField(choices=Platform_Index, default=Platform_Other,
                                                   verbose_name="购买平台")  # 购买平台
    buyDate = models.DateTimeField(verbose_name="购买日期")  # 购买日期
    goonDate = models.DateTimeField(verbose_name="发走日期")  # 发走日期
    expectDate = models.DateTimeField(verbose_name="预期到达日期")
    price = models.SmallIntegerField(verbose_name="购买价格")
    sellPrice = models.SmallIntegerField(verbose_name="出售价格")
    # 利润
    stateOpen = 0
    stateEnd = 1
    state = ((stateOpen, "未结算"),
             (stateEnd, "已结算"))
    purchaseState = models.PositiveIntegerField(choices=state,default=stateOpen,verbose_name="商品状态")
