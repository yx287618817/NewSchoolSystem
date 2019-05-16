# Generated by Django 2.1.7 on 2019-05-16 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inform',
            name='send_from_dpt',
        ),
        migrations.RemoveField(
            model_name='inform',
            name='send_to_dpt',
        ),
        migrations.AddField(
            model_name='teacher',
            name='real_name',
            field=models.CharField(default=1, max_length=16, verbose_name='姓名'),
            preserve_default=False,
        ),
    ]
