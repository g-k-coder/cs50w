# Generated by Django 4.1.5 on 2023-02-06 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='auctions/profile/default_avatar.png', upload_to='auctions/static/auctions/profile/'),
        ),
    ]