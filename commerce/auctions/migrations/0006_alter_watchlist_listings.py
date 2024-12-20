# Generated by Django 4.2.7 on 2024-05-26 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_listing_watchlist_listings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listings',
            field=models.ManyToManyField(related_name='listing_to_watch', to='auctions.listing'),
        ),
    ]
