# Generated by Django 4.1.5 on 2023-02-06 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='auctions/static/auctions/profile/default_avatar.png', upload_to='auctions/static/auctions/profile/'),
        ),
    ]