# Generated by Django 2.1.7 on 2019-05-16 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_auto_20190516_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='gender',
            field=models.BooleanField(default=True, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='user_name',
            field=models.CharField(max_length=16, verbose_name='用户名'),
        ),
    ]