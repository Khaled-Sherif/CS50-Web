# Generated by Django 4.2.7 on 2024-05-26 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_rename_auction_lister_listing_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(related_name='listing_to_watch', to='auctions.listing'),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
