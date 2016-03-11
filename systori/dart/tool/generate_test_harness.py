import os
import types
import django
from decimal import Decimal as D
from django.db import transaction
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.test.runner import setup_databases
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "systori.settings")

from systori.apps.company.factories import CompanyFactory
from systori.apps.project.factories import ProjectFactory
from systori.apps.task.factories import JobFactory
from systori.apps.user.factories import UserFactory
from systori.apps.accounting.models import Entry, create_account_for_job
from systori.apps.accounting.workflow import debit_jobs, create_chart_of_accounts
from systori.lib.accounting.tools import Amount as A


DART_APP_ROOT = os.path.dirname(os.path.dirname(__file__))


def write_test_html(name, html):
    file_path = os.path.join(DART_APP_ROOT, 'test', name+'_test.html')
    with open(file_path, 'wb') as test_file:
        test_file.write(html.content)
        test_file.write(b'<link rel="x-dart-test" href="'+name.encode()+b'_test.dart">\n')
        test_file.write(b'<script src="packages/test/dart.js"></script>\n')


def create_data():
    data = types.SimpleNamespace()
    data.company = CompanyFactory.create()
    create_chart_of_accounts()
    data.user = UserFactory.create(email='lex@damoti.com', company=data.company)
    data.project = ProjectFactory.create(name="Test Project")
    data.job = JobFactory.create(name="Test Job", project=data.project)
    data.job.account = create_account_for_job(data.job)
    data.job.save()
    debit_jobs([(data.job, A(D(388.8), D(91.2)), Entry.WORK_DEBIT)])
    return data


def generate_pages():
    data = create_data()
    client = Client()
    client.login(username=data.user.email, password='open sesame')
    editor = client.get(reverse('tasks', args=[data.project.id, data.job.id]))
    write_test_html('editor', editor)
    split_payment = client.get(reverse('payment.create', args=[data.project.id]))
    write_test_html('split_payment', split_payment)


if __name__ == "__main__":
    django.setup()
    setup_databases(verbosity=1, interactive=False, keepdb=True)

    # Start Transaction
    atom = transaction.atomic()
    atom.__enter__()

    create_data()
    generate_pages()

    # Rollback Transaction
    transaction.set_rollback(True)
    atom.__exit__(None, None, None)
