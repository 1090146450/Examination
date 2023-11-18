# Generated by Django 4.1.5 on 2023-11-15 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentExamination', '0004_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('pdName', models.CharField(max_length=255, verbose_name='商品名称')),
                ('purchasePlatform', models.PositiveIntegerField(choices=[(0, '拼多多'), (1, '淘宝'), (2, '京东'), (3, '其他')], default=3, verbose_name='购买平台')),
                ('buyDate', models.DateTimeField(verbose_name='购买日期')),
                ('goonDate', models.DateTimeField(verbose_name='发走日期')),
                ('expectDate', models.DateTimeField(verbose_name='预期到达日期')),
                ('price', models.SmallIntegerField(verbose_name='购买价格')),
                ('sellPrice', models.SmallIntegerField(verbose_name='出售价格')),
                ('purchaseState', models.PositiveIntegerField(choices=[(0, '未结算'), (1, '已结算')], default=0, verbose_name='商品状态')),
            ],
        ),
    ]