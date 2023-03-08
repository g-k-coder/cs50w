# Generated by Django 4.1.5 on 2023-02-06 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_auctionlisting_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='picture',
            field=models.ImageField(default='pictures/listing/default_listing.png', upload_to='pictures/listing/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='pictures/profile/default_avatar.png', upload_to='pictures/profile/'),
        ),
    ]
