# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-06 14:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


def remove_company_access_content_type(apps, schema_editor):
    from django.contrib.contenttypes.models import ContentType

    ContentType.objects.filter(app_label="company", model="access").delete()


class Migration(migrations.Migration):

    dependencies = [("company", "0003_auto_20160403_0209")]

    operations = [
        migrations.RenameModel("Access", "Worker"),
        migrations.AlterField(
            model_name="company",
            name="users",
            field=models.ManyToManyField(
                blank=True,
                to=settings.AUTH_USER_MODEL,
                through="company.Worker",
                related_name="companies",
            ),
        ),
        migrations.AlterField(
            model_name="worker",
            name="company",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="workers",
                to="company.Company",
            ),
        ),
        migrations.AlterField(
            model_name="worker",
            name="user",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name="access",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(remove_company_access_content_type),
    ]
