# Generated by Django 4.1.5 on 2023-02-23 21:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_auctionlisting_closed_alter_auctionlisting_sold_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='closed',
            field=models.IntegerField(default=0, max_length=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
    ]
