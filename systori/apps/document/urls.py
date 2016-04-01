from django.conf.urls import url
from ..user.authorization import office_auth, owner_auth
from ..accounting.views import *
from .views import *

urlpatterns = [

    url(r'^project-(?P<project_pk>\d+)/create-proposal$', office_auth(ProposalCreate.as_view()), name='proposal.create'),
    url(r'^project-(?P<project_pk>\d+)/proposal-(?P<format>(email|print))-(?P<pk>\d+).pdf$', office_auth(ProposalPDF.as_view()), name='proposal.pdf'),
    url(r'^project-(?P<project_pk>\d+)/proposal-(?P<pk>\d+)/transition/(?P<transition>\w+)$', office_auth(ProposalTransition.as_view()), name='proposal.transition'),
    url(r'^project-(?P<project_pk>\d+)/proposal-(?P<pk>\d+)/delete$', office_auth(ProposalDelete.as_view()), name='proposal.delete'),
    url(r'^project-(?P<project_pk>\d+)/proposal-(?P<pk>\d+)/update$', office_auth(ProposalUpdate.as_view()), name='proposal.update'),

    url(r'^project-(?P<project_pk>\d+)/create-invoice$', office_auth(InvoiceCreate.as_view()), name='invoice.create'),
    url(r'^project-(?P<project_pk>\d+)/create-next-invoice/(?P<previous_pk>\d+)$', office_auth(InvoiceCreate.as_view()), name='invoice.create'),
    url(r'^project-(?P<project_pk>\d+)/invoice-(?P<format>(email|print))-(?P<pk>\d+).pdf$', office_auth(InvoicePDF.as_view()), name='invoice.pdf'),
    url(r'^project-(?P<project_pk>\d+)/invoice-(?P<pk>\d+)/transition/(?P<transition>\w+)$', office_auth(InvoiceTransition.as_view()), name='invoice.transition'),
    url(r'^project-(?P<project_pk>\d+)/invoice-(?P<pk>\d+)/update$', office_auth(InvoiceUpdate.as_view()), name='invoice.update'),
    url(r'^project-(?P<project_pk>\d+)/invoice-(?P<pk>\d+)/delete$', office_auth(InvoiceDelete.as_view()), name='invoice.delete'),

    url(r'^project-(?P<project_pk>\d+)/create-adjustment$', office_auth(AdjustmentCreate.as_view()), name='adjustment.create'),
    url(r'^project-(?P<project_pk>\d+)/create-adjustment-for-invoice/(?P<invoice_pk>\d+)$', office_auth(AdjustmentCreate.as_view()), name='adjustment.create'),
    url(r'^project-(?P<project_pk>\d+)/adjustment-(?P<pk>\d+)/delete$', office_auth(AdjustmentDelete.as_view()), name='adjustment.delete'),

    url(r'^project-(?P<project_pk>\d+)/create-payment$', office_auth(PaymentCreate.as_view()), name='payment.create'),
    url(r'^project-(?P<project_pk>\d+)/create-payment-for-invoice/(?P<invoice_pk>\d+)$', office_auth(PaymentCreate.as_view()), name='payment.create'),
    url(r'^project-(?P<project_pk>\d+)/payment-(?P<pk>\d+)/delete$', office_auth(PaymentDelete.as_view()), name='payment.delete'),

    url(r'^project-(?P<project_pk>\d+)/create-refund$', office_auth(RefundCreate.as_view()), name='refund.create'),
    url(r'^project-(?P<project_pk>\d+)/refund-(?P<pk>\d+)/delete$', office_auth(RefundDelete.as_view()), name='refund.delete'),
    url(r'^project-(?P<project_pk>\d+)/refund-(?P<pk>\d+)/update$', office_auth(RefundUpdate.as_view()), name='refund.update'),
    url(r'^project-(?P<project_pk>\d+)/refund-(?P<format>(email|print))-(?P<pk>\d+).pdf$', office_auth(RefundPDF.as_view()), name='refund.pdf'),

    url(r'^project-(?P<project_pk>\d+)/evidence.pdf$', office_auth(EvidencePDF.as_view()), name='evidence.pdf'),

    url(r'^project-(?P<project_pk>\d+)/itemized_listing-(?P<format>(email|print)).pdf$', office_auth(ItemizedListingPDF.as_view()), name='itemized_listing.pdf'),

    url(r'^invoices$', owner_auth(InvoiceList.as_view()), name='invoices'),

    url(r'^templates/create-document-template$', office_auth(DocumentTemplateCreate.as_view()), name='document-template.create'),
    url(r'^templates/document-template-(?P<pk>\d+)$', office_auth(DocumentTemplateView.as_view()), name='document-template.view'),
    url(r'^templates/document-template-(?P<pk>\d+)/edit$', office_auth(DocumentTemplateUpdate.as_view()), name='document-template.edit'),
    url(r'^templates/document-template-(?P<pk>\d+)/delete$', office_auth(DocumentTemplateDelete.as_view()), name='document-template.delete'),

    url(r'^templates/create-letterhead$', office_auth(LetterheadCreate.as_view()), name='letterhead.create'),
    url(r'^templates/letterhead-(?P<pk>\d+)$', office_auth(LetterheadView.as_view()), name='letterhead.view'),
    url(r'^templates/letterhead-(?P<pk>\d+)/update$', office_auth(LetterheadUpdate.as_view()), name='letterhead.update'),
    url(r'^templates/letterhead-(?P<pk>\d+)/delete$', office_auth(LetterheadDelete.as_view()), name='letterhead.delete'),
    url(r'^templates/letterhead-(?P<pk>\d+)/preview$', office_auth(LetterheadPreview.as_view()), name='letterhead.preview'),

    url(r'^templates/create-document-settings$', office_auth(DocumentSettingsCreate.as_view()), name='document-settings.create'),
    url(r'^templates/document-settings-(?P<pk>\d+)/edit$', office_auth(DocumentSettingsUpdate.as_view()), name='document-settings.edit'),
    url(r'^templates/document-settings-(?P<pk>\d+)/delete$', office_auth(DocumentSettingsDelete.as_view()), name='document-settings.delete'),

]
