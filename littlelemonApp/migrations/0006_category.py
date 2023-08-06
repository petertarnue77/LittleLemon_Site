# Generated by Django 4.2.3 on 2023-08-04 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("littlelemonApp", "0005_menu_inventory"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("slug", models.CharField(max_length=50)),
            ],
        ),
    ]
