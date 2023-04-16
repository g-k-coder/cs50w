# Generated by Django 4.1.5 on 2023-04-12 10:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('a2036f19-d2d3-487e-a3b9-eeb40904d492'), editable=False, verbose_name='UUID'),
        ),
    ]
