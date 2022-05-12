from django.shortcuts import render
from mailings.mailchimp_services import add_mailchimp_email_with_tag


def webhook(request):
    """Обработчик вебхука от платежной системы"""
    add_mailchimp_email_with_tag(audience_name='DONATES',
                                 email=request.POST.get('email'),
                                 tag='DONATE')
