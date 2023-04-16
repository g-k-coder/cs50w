# Generated by Django 4.1.5 on 2023-04-12 10:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='UUID'),
        ),
    ]