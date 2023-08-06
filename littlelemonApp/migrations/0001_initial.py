# Generated by Django 4.2.3 on 2023-07-16 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Menu",
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
                ("name", models.CharField(max_length=10)),
                ("price", models.DecimalField(decimal_places=2, max_digits=4)),
            ],
            options={"db_table": "Menu",},
        ),
    ]
