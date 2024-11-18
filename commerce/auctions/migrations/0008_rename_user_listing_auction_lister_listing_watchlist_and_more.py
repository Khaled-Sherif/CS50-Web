# Generated by Django 4.2.7 on 2024-05-26 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_watchlist_listings_watchlist_listings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='user',
            new_name='auction_lister',
        ),
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users_watching', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
