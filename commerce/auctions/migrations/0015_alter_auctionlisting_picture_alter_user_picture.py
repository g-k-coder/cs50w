# Generated by Django 4.1.5 on 2023-02-09 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='picture',
            field=models.ImageField(default='default_listing.png', upload_to='listing/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='default_avatar.png', upload_to='profile/'),
        ),
    ]
