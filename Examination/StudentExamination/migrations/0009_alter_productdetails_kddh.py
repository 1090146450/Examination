# Generated by Django 4.1.5 on 2023-11-24 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentExamination', '0008_productdetails_kddh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productdetails',
            name='kddh',
            field=models.CharField(max_length=100, verbose_name='快递单号'),
        ),
    ]
