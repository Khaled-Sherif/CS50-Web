# Generated by Django 4.2.7 on 2024-05-20 22:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(null=True, related_name='listing_to_watch', to=settings.AUTH_USER_MODEL),
        ),
    ]
