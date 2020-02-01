# Generated by Django 2.2.2 on 2019-07-14 07:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0012_auto_20190714_0557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentsblog',
            options={'ordering': ['-publish_date', '-updated', '-timestamp']},
        ),
        migrations.AddField(
            model_name='commentsblog',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='commentsblog',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commentsblog',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]