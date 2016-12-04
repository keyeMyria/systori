# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-06 14:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_worker'),
        ('document', '0006_documentsettings_timetracking_letterhead'),
        ('task', '0004_data_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timesheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('json', jsonfield.fields.JSONField(default={})),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('document_date', models.DateField(blank=True, default=datetime.date.today, verbose_name='Date')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('letterhead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timesheet_documents', to='document.Letterhead')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timesheets', to='company.Worker')),
            ],
            options={
                'verbose_name_plural': 'Timesheets',
                'abstract': False,
                'verbose_name': 'Timesheet',
                'ordering': ['id'],
            },
        ),
        migrations.RenameField(
            model_name='documentsettings',
            old_name='timetracking_letterhead',
            new_name='timesheet_letterhead',
        ),
        migrations.AlterField(
            model_name='proposal',
            name='jobs',
            field=models.ManyToManyField(verbose_name='Jobs', to='task.Job', related_name='proposals'),
        ),
    ]
