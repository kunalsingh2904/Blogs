# Generated by Django 2.2.2 on 2019-09-10 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0013_auto_20190714_0702'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentsblog',
            name='user',
            field=models.CharField(default='unknown', max_length=120),
        ),
    ]
