# Generated by Django 4.1.5 on 2023-04-09 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_alter_post_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='likes',
            name='post',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='network.post', verbose_name='Post'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='likes',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='like', to=settings.AUTH_USER_MODEL, verbose_name='Liked by'),
            preserve_default=False,
        ),
    ]
