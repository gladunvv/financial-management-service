# Generated by Django 2.2.5 on 2019-09-14 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_auto_20190914_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='comment',
            field=models.CharField(default='', max_length=70, verbose_name='User comment'),
            preserve_default=False,
        ),
    ]
