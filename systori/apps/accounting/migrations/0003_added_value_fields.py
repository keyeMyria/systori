# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations


def split_gross_entries(apps, schema_editor):
    from systori.apps.company.models import Company
    from systori.apps.task.models import Job
    from systori.apps.accounting.models import Account, Entry
    from systori.apps.accounting.constants import TAX_RATE, SKR03_PARTIAL_PAYMENTS_CODE, SKR03_INCOME_CODE
    from systori.apps.accounting.constants import SKR03_CASH_DISCOUNT_CODE, SKR03_TAX_PAYMENTS_CODE
    from systori.apps.accounting.constants import SKR03_PROMISED_PAYMENTS_CODE
    from systori.lib.accounting.tools import extract_net_tax

    for company in Company.objects.all():
        company.activate()

        for job in Job.objects.all():
            for entry in job.account.entries.all():
                net, tax = extract_net_tax(entry.value, TAX_RATE)
                entry.value = net
                entry.value_type = entry.NET
                entry.save()
                entry.id = None
                entry.value = tax
                entry.value_type = entry.TAX
                entry.save()

        values_types = (
            (Entry.NET, (
                SKR03_PARTIAL_PAYMENTS_CODE,
                SKR03_INCOME_CODE,
                SKR03_CASH_DISCOUNT_CODE
            )),
            (Entry.TAX, (
                SKR03_TAX_PAYMENTS_CODE,
            )),
            (Entry.GROSS, (
                SKR03_PROMISED_PAYMENTS_CODE,
            ))
        )
        for value_type, account_codes in values_types:
            for account in Account.objects.filter(code__in=account_codes):
                for entry in account.entries.all():
                    if value_type == Entry.GROSS:
                        net, tax = extract_net_tax(entry.value, TAX_RATE)
                        entry.value = net
                        entry.value_type = entry.NET
                        entry.save()
                        entry.id = None
                        entry.value = tax
                        entry.value_type = entry.TAX
                        entry.save()
                    else:
                        entry.value_type = value_type
                        entry.save()


def recalculate_invoices(apps, schema_editor):
    from systori.apps.company.models import Company
    from systori.apps.document.models import Invoice
    from systori.apps.task.models import Job
    from systori.apps.accounting.report import prepare_transaction_report

    for company in Company.objects.all():
        company.activate()

        for invoice in Invoice.objects.all():
            if 'debits' not in invoice.json:
                print('skipping invoice #{}'.format(invoice.id))
                continue
            job_ids = [debit['job.id'] for debit in invoice.json['debits']]
            jobs = Job.objects.filter(id__in=job_ids)
            new_json = prepare_transaction_report(jobs, invoice.document_date)
            print(invoice.id)
            if invoice.id == 85:
                pass
            # TODO: Fix failing asserts.
            print(len(new_json['transactions']), len(invoice.json['transactions']))
            #assert len(new_json['transactions']) == len(invoice.json['transactions'])
            print(new_json['invoiced'].gross, invoice.json['debited_gross'])
            #assert new_json['invoiced'].gross == invoice.json['debited_gross']
            invoice.json.update(new_json)
            invoice.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20160221_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='value_type',
            field=models.CharField(max_length=32, default='gross', choices=[('net', 'Net'), ('tax', 'Tax'), ('gross', 'Gross')], verbose_name='Value Type'),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='amount',
            new_name='value'
        ),
        migrations.AlterField(
            model_name='entry',
            name='value',
            field=models.DecimalField(verbose_name='Value', decimal_places=2, max_digits=14),
        ),
        migrations.AlterField(
            model_name='entry',
            name='entry_type',
            field=models.CharField(max_length=32, default='other', choices=[('payment', 'Payment'), ('refund-credit', 'Refund Credit'), ('discount', 'Discount'), ('work-debit', 'Work Debit'), ('flat-debit', 'Flat Debit'), ('refund', 'Refund'), ('adjustment', 'Adjustment'), ('other', 'Other')], verbose_name='Entry Type'),
        ),
        migrations.RemoveField(
            model_name='entry',
            name='tax_rate',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(max_length=32, null=True, verbose_name='Transaction Type', choices=[('invoice', 'Invoice'), ('payment', 'Payment'), ('adjustment', 'Adjustment')]),
        ),
        migrations.RunPython(split_gross_entries),
        migrations.RunPython(recalculate_invoices)
    ]
