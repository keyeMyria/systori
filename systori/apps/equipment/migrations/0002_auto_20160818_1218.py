# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-18 10:18
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("equipment", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Maintenance",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="date"
                    ),
                ),
                (
                    "mileage",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=9,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                        verbose_name="mileage",
                    ),
                ),
                ("description", models.TextField(verbose_name="description")),
                (
                    "contractor",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="contractor"
                    ),
                ),
                (
                    "cost",
                    models.DecimalField(
                        decimal_places=4,
                        default=Decimal("0"),
                        max_digits=14,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                        verbose_name="cost",
                    ),
                ),
            ],
            options={
                "verbose_name": "maintenance",
                "verbose_name_plural": "maintenances",
            },
        ),
        migrations.CreateModel(
            name="RefuelingStop",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "datetime",
                    models.DateTimeField(
                        db_index=True, default=django.utils.timezone.now
                    ),
                ),
                (
                    "mileage",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=9,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                        verbose_name="mileage",
                    ),
                ),
                (
                    "distance",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=9,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                        verbose_name="distance",
                    ),
                ),
                (
                    "liters",
                    models.DecimalField(
                        decimal_places=2,
                        default=Decimal("0"),
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                        verbose_name="refueled liters",
                    ),
                ),
                (
                    "price_per_liter",
                    models.DecimalField(
                        decimal_places=3,
                        max_digits=6,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.001"))
                        ],
                        verbose_name="price per liter",
                    ),
                ),
                (
                    "average_consumption",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        max_digits=6,
                        null=True,
                        verbose_name="average consumption",
                    ),
                ),
            ],
            options={
                "verbose_name": "refueling stop",
                "verbose_name_plural": "refueling stops",
            },
        ),
        migrations.RemoveField(model_name="equipment", name="purchase_date"),
        migrations.RemoveField(model_name="equipment", name="purchase_price"),
        migrations.AddField(
            model_name="equipment",
            name="active",
            field=models.BooleanField(default=True, verbose_name="active"),
        ),
        migrations.AddField(
            model_name="equipment",
            name="fuel",
            field=models.CharField(
                choices=[
                    ("gasoline", "gasoline"),
                    ("premium_gasoline", "premium gasoline"),
                    ("diesel", "diesel"),
                    ("premium_diesel", "premium diesel"),
                    ("electric", "electric"),
                ],
                default="diesel",
                max_length=255,
                verbose_name="fuel",
            ),
        ),
        migrations.AddField(
            model_name="equipment",
            name="icon",
            field=models.ImageField(blank=True, upload_to="", verbose_name="Icon"),
        ),
        migrations.AddField(
            model_name="equipment",
            name="last_refueling_stop",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last refueling stop"
            ),
        ),
        migrations.AddField(
            model_name="equipment",
            name="license_plate",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="license plate"
            ),
        ),
        migrations.AddField(
            model_name="equipment",
            name="number_of_seats",
            field=models.IntegerField(default=2, verbose_name="number of seats"),
        ),
        migrations.AddField(
            model_name="refuelingstop",
            name="equipment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="equipment.Equipment",
                verbose_name="equipment",
            ),
        ),
        migrations.AddField(
            model_name="maintenance",
            name="equipment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="equipment.Equipment",
                verbose_name="equipment",
            ),
        ),
    ]
