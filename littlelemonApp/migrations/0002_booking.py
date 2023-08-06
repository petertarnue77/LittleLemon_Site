# Generated by Django 4.2.3 on 2023-07-17 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("littlelemonApp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
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
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                ("booking_time", models.TimeField(auto_now=True)),
                ("number_of_person", models.IntegerField()),
                ("notes", models.TextField()),
            ],
            options={"db_table": "Booking",},
        ),
    ]
