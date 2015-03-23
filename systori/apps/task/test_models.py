from django.test import TestCase
from django.contrib.auth import get_user_model
from ..project.models import *
from .models import *

User = get_user_model()


def create_task_data(self):
    self.user = User.objects.create_user('lex', 'lex@damoti.com', 'pass')
    self.template_project = Project.objects.create(name="Template Project", is_template=True)
    self.project = Project.objects.create(name="my project")
    self.project2 = Project.objects.create(name="my project 2")
    self.job = Job.objects.create(name="Default", project=self.project)
    self.job2 = Job.objects.create(name="Default 2", project=self.project)
    self.group = TaskGroup.objects.create(name="my group", job=self.job)
    self.group2 = TaskGroup.objects.create(name="my group 2", job=self.job)
    self.task = Task.objects.create(name="my task one", qty=1, taskgroup=self.group)
    TaskInstance.objects.create(task=self.task,selected=True)
    self.lineitem = LineItem.objects.create(name="my line item 1", unit_qty=8, price=120, taskinstance=self.task.instance)
    self.task2 = Task.objects.create(name="my task two", qty=0, taskgroup=self.group)
    TaskInstance.objects.create(task=self.task2,selected=True)
    self.lineitem2 = LineItem.objects.create(name="my line item 2", unit_qty=0, price=0, taskinstance=self.task2.instance)


class TaskInstanceTotalTests(TestCase):

    def setUp(self):
        create_task_data(self)
    
    def test_zero_total(self):
        task = TaskInstance.objects.get(pk=self.task2.instance.pk)
        self.assertEqual(0, task.fixed_price_estimate)
        self.assertEqual(0, task.fixed_price_billable)
        self.assertEqual(0, task.time_and_materials_estimate)
        self.assertEqual(0, task.time_and_materials_billable)

    def test_non_zero_total(self):
        lineitem1 = LineItem.objects.create(name="do stuff", price=10, unit_qty=8, unit="hour", taskinstance=self.task.instance)
        self.assertEqual(80, lineitem1.price_per_task_unit)
        task = TaskInstance.objects.get(pk=self.task.instance.pk)
        self.assertEqual(1040, task.fixed_price_estimate)


class JobQuerySetTests(TestCase):

    def setUp(self):
        create_task_data(self)
        self.job2 = Job.objects.create(name="Empty Job", project=self.project)
    
    def test_zero_total(self):
        jobs = Job.objects.filter(pk=self.job2.id)
        self.assertEqual(0, jobs.estimate_total())
        self.assertEqual(0, jobs.estimate_tax_total())
        self.assertEqual(0, jobs.estimate_gross_total())
        self.assertEqual(0, jobs.billable_total())
        self.assertEqual(0, jobs.billable_tax_total())
        self.assertEqual(0, jobs.billable_gross_total())

    def test_nonzero_total(self):
        jobs = Job.objects
        self.assertEqual(Decimal(960), jobs.estimate_total())
        self.assertEqual(Decimal(0), jobs.billable_total())
        self.assertEqual(round(Decimal(960*.19),2), round(jobs.estimate_tax_total(),2))
        self.assertEqual(round(Decimal(960*1.19),2), round(jobs.estimate_gross_total(),2))


class JobOffsetTests(TestCase):
    def setUp(self):
        create_task_data(self)

    def test_no_offset(self):
        self.assertEqual('1', self.job.code)

    def test_offset_4(self):
        self.project.job_offset = 4
        self.assertEqual('5', self.job.code)

class TaskGroupOffsetTests(TestCase):
    def setUp(self):
        create_task_data(self)

    def test_no_offset(self):
        self.assertEqual('1.1', self.group.code)

    def test_offset_4(self):
        self.project.job_offset = 2
        self.job.taskgroup_offset = 3
        self.assertEqual('3.4', self.group.code)

class JobEstimateModificationTests(TestCase):
    
    def setUp(self):
        create_task_data(self)

    def test_increase_total(self):
        self.assertEqual(Decimal(960), self.job.estimate_total)
        self.job.estimate_total_modify(self.user, 'increase')
        self.assertEqual(Decimal(960*(Job.ESTIMATE_INCREMENT+1)), self.job.estimate_total)

    def test_2x_increase_total(self):
        self.assertEqual(Decimal(960), self.job.estimate_total)
        self.job.estimate_total_modify(self.user,'increase')
        self.job.estimate_total_modify(self.user,'increase')
        first = Decimal(960)*Decimal(Job.ESTIMATE_INCREMENT)
        second = first + (Decimal(960)+first)*Decimal(Job.ESTIMATE_INCREMENT)
        self.assertEqual(round(Decimal(960)+second, 2), round(self.job.estimate_total, 2))

    def test_decrease_total(self):
        self.assertEqual(Decimal(960), self.job.estimate_total)
        self.job.estimate_total_modify(self.user,'decrease')
        self.assertEqual(Decimal(960*(1-Job.ESTIMATE_INCREMENT)), self.job.estimate_total)

    def test_2x_decrease_total(self):
        self.assertEqual(Decimal(960), self.job.estimate_total)
        self.job.estimate_total_modify(self.user, 'decrease')
        self.job.estimate_total_modify(self.user, 'decrease')
        first = Decimal(960)*Decimal(Job.ESTIMATE_INCREMENT)*-1
        second = first - (Decimal(960)+first)*Decimal(Job.ESTIMATE_INCREMENT)
        self.assertEqual(round(Decimal(960)+second, 2), round(self.job.estimate_total, 2))

    def test_decrease_increase_total(self):
        self.assertEqual(Decimal(960), self.job.estimate_total)
        self.job.estimate_total_modify(self.user, 'decrease')
        self.job.estimate_total_modify(self.user, 'increase')
        first = Decimal(960)*Decimal(Job.ESTIMATE_INCREMENT)*-1
        second = first + (Decimal(960)+first)*Decimal(Job.ESTIMATE_INCREMENT)
        self.assertEqual(round(Decimal(960)+second, 2), round(self.job.estimate_total, 2))

    def test_reset_total(self):
        self.job.estimate_total_modify(self.user, 'increase')
        self.job.estimate_total_modify(self.user, 'reset')
        self.assertEqual(Decimal(960), self.job.estimate_total)

class TaskCloneTests(TestCase):

    def setUp(self):
        create_task_data(self)

    def test_clone(self):
        new_job = Job.objects.create(name="New", project=self.project)
        self.assertEqual(new_job.taskgroups.count(), 0)
        self.job.clone_to(new_job)

        job = Job.objects.get(pk=new_job.pk)
        self.assertEqual(job.taskgroups.count(), 2)
        group = job.taskgroups.get(name="my group")
        self.assertNotEqual(group.id, self.group.id)
        self.assertEqual(group.tasks.count(), 2)