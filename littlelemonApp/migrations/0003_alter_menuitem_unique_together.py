# Generated by Django 4.2.3 on 2023-08-08 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "littlelemonApp",
            "0002_booking_cart_category_menuitem_order_orderitem_and_more",
        ),
    ]

    operations = [
        migrations.AlterUniqueTogether(name="menuitem", unique_together={("title",)},),
    ]