# Generated by Django 3.1.7 on 2021-03-17 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_link_wishlist_wishlistitem'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlistitem',
            unique_together={('wishlist', 'index')},
        ),
    ]