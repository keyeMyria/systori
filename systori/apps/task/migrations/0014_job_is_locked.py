# Generated by Django 2.0.2 on 2018-03-06 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_auto_20171020_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]