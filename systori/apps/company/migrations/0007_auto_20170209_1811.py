# Generated by Django 2.0 on 2017-02-09 17:11

from django.db import migrations
from postgres_schema import migrations as schema_migrations
CLONE_SCHEMA = getattr(schema_migrations, "0001_initial").CLONE_SCHEMA


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20170201_1457'),
    ]

    operations = [
        migrations.RunSQL(sql=CLONE_SCHEMA, reverse_sql='DROP FUNCTION clone_schema(text, text)'),
    ]
