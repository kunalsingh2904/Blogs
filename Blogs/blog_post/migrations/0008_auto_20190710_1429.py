# Generated by Django 2.2.2 on 2019-07-10 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0007_auto_20190710_1406'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-publish_date', '-updated', '-timestamp']},
        ),
    ]
