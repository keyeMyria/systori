# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


def migrate_entry_type(apps, schema_editor):
    Entry = apps.get_model('accounting', 'Entry')
    from systori.apps.company.models import Company
    for company in Company.objects.all():
        company.activate()
        for entry in Entry.objects.all():
            if entry.is_discount:
                entry.entry_type = 'discount'
            elif entry.is_payment:
                entry.entry_type = 'payment'
            else:
                entry.entry_type = 'other'
            if entry.received_on:
                entry.transaction.transacted_on = entry.received_on
                entry.transaction.save()
            entry.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20150730_0445'),
        ('document', '0002_auto_20150615_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='amount',
            field=models.DecimalField(default=0.0, decimal_places=2, max_digits=14, verbose_name='Amount'),
        ),
        migrations.AddField(
            model_name='entry',
            name='entry_type',
            field=models.CharField(choices=[('payment', 'Payment'), ('discount', 'Discount'), ('work-debit', 'Work Debit'), ('flat-debit', 'Flat Debit'), ('final-debit', 'Final Debit'), ('adjustment', 'Adjustment'), ('other', 'Other')], default='other', verbose_name='Entry Type', max_length=32),
        ),
        migrations.AddField(
            model_name='entry',
            name='reconciled_on',
            field=models.DateField(verbose_name='Date Reconciled', null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='finalized_on',
            field=models.DateField(verbose_name='Date Finalized', null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='is_finalized',
            field=models.BooleanField(default=False, verbose_name='Finalized'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transacted_on',
            field=models.DateField(verbose_name='Date Transacted', default=datetime.date.today),
        ),
        migrations.RunPython(migrate_entry_type),
    ]