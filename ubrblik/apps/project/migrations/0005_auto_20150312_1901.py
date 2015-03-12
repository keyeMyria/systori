# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20150311_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobsite',
            name='project',
            field=models.ForeignKey(related_name='jobsites', to='project.Project'),
            preserve_default=True,
        ),
    ]
