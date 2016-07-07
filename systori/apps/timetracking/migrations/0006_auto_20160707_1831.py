# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20160707_1831'),
        ('timetracking', '0005_auto_20160630_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='job_site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.JobSite'),
        ),
        migrations.AddField(
            model_name='timer',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='timer',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True),
        ),
    ]
