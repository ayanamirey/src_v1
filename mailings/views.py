from django.http import JsonResponse
from django.conf import settings
from cases.models import Case
from .models import CommonMailingList, CaseMailingList
from .mailchimp_services import _get_mailchimp_client, _add_mailchimp_tag, _add_mailchimp_email_with_tag, \
    _add_email_to_mailchimp_audience, _get_mailchimp_subscriber_hash


def add_to_common_list_view(request):
    """Веб-сервис, добавляющий email в общий лист рассылки"""
    # Проверка email'а
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    _add_mailchimp_email_with_tag(audience_id=settings.MAILCHIMP_COMMON_LIST_ID,
                                  email=email,
                                  tag='COMMON TAG')

    # Добавления записи в базу данных
    CommonMailingList.objects.get_or_create(email=email)

    return JsonResponse({'success': True})


def add_to_case_list_view(request):
    """Веб-сервис, добавляющий email в лист рассылок по конкретному делу"""
    # Проверка email'а
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})
    case_id = request.GET.get('email')
    if not case_id:
        return JsonResponse({'success': False, 'message': 'Передайте case_id'})

    case = Case.objects.get(pk=case_id)
    case_tag = f'Case {case.name}'

    _add_mailchimp_email_with_tag(audience_id=settings.MAILCHIMP_CASE_LIST_ID,
                                  email=email,
                                  tag=case_tag)

    # Добавления записи в базу данных
    CaseMailingList.objects.get_or_create(email=email, case=case)

    return JsonResponse({'success': True})
