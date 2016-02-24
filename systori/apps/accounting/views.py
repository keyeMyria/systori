from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from .models import *
from .forms import *


class PaymentCreate(FormView):
    form_class = SplitPaymentFormSet
    template_name = 'accounting/payment_form.html'

    def get_form_kwargs(self):
        kwargs = {'jobs': self.request.project.jobs.all()}
        if 'invoice_pk' in self.kwargs:
            invoice = Invoice.objects.get(id=self.kwargs['invoice_pk'])
            kwargs['initial'] = {
                'invoice': invoice,
                'amount': invoice.json['debit_gross'],
            }
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST.copy()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.project.get_absolute_url()


class PaymentDelete(DeleteView):
    model = Transaction
    template_name = 'accounting/payment_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        if not object.is_reconciled:
            object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.project.get_absolute_url()


class AdjustmentCreate(FormView):
    form_class = AdjustJobFormSet
    template_name = 'accounting/adjustment_form.html'

    def get_form_kwargs(self):
        kwargs = {
            'jobs': self.request.project.jobs.prefetch_related('taskgroups__tasks__taskinstances__lineitems').all()
        }
        if 'invoice_pk' in self.kwargs:
            invoice = Invoice.objects.get(id=self.kwargs['invoice_pk'])
            kwargs['initial'] = {
                'invoice': invoice,
                'amount': invoice.json['debit_gross'],
            }
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST.copy()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.project.get_absolute_url()


class AdjustmentDelete(DeleteView):
    model = Transaction
    template_name = 'accounting/adjustment_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        if not object.is_reconciled:
            object.delete()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.request.project.get_absolute_url()


class AccountList(TemplateView):
    template_name = 'accounting/account_list.html'

    def get_context_data(self, **kwargs):
        context = super(AccountList, self).get_context_data(**kwargs)
        context['banks'] = Account.objects.banks()
        context['other'] = Account.objects.exclude(account_type=Account.ASSET)
        return context


class AccountView(DetailView):
    model = Account

    def get_queryset(self):
        queryset = super(AccountView, self).get_queryset()
        return queryset


class AccountUpdate(UpdateView):
    model = Account
    form_class = AccountForm

    def get_success_url(self):
        return reverse('accounts')


class BankAccountCreate(CreateView):
    model = Account
    form_class = BankAccountForm

    def get_success_url(self):
        return reverse('accounts')


class BankAccountUpdate(UpdateView):
    model = Account
    form_class = BankAccountForm

    def get_success_url(self):
        return reverse('accounts')


class BankAccountDelete(DeleteView):
    model = Account
    success_url = reverse_lazy('accounts')
