# Generated by Django 2.0 on 2017-03-14 00:57

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=4, default=Decimal('0.00'), max_digits=14, verbose_name='Price')),
            ],
        ),
        migrations.AddField(
            model_name='material',
            name='material_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='materials', to='inventory.MaterialType'),
        ),
    ]
