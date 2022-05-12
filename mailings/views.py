from mailchimp3 import MailChimp
from django.http import JsonResponse
from django.conf import settings

from cases.models import Case
from .models import CommonMailingList, CaseMailingList


def add_to_common_list_view(request):
    """Веб-сервис, добавляющий email в общий лист рассылки"""
    # Проверка email'а
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    # Получение mailchimp клиента
    mailchimp_client = MailChimp(
        mc_api=settings.MAILCHIMP_API_KEY,
        mc_user=settings.MAILCHIMP_USERNAME)
    # Добавления в mailchimp аудиторию новые email'ы

    mailchimp_client.lists.members.create(settings.MAILCHIMP_COMMON_LIST_ID, {
        'email_address': email,
        'status': 'subscribed'
    })

    # Получения subscriber hash
    subscriber_hash = mailchimp_client \
        .search_members \
        .get(query=email,
             fields='exact_matches.members.id') \
        .get('exact_matches') \
        .get('members')[0].get('id')

    # Добавления тега
    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_COMMON_LIST_ID,
        subscriber_hash=subscriber_hash,
        data={'tags': [{'name': 'COMMON TAG', 'status': 'active'}]})

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

    # Получение mailchimp клиента
    mailchimp_client = MailChimp(
        mc_api=settings.MAILCHIMP_API_KEY,
        mc_user=settings.MAILCHIMP_USERNAME)
    # Добавления в mailchimp аудиторию новые email'ы

    mailchimp_client.lists.members.create(settings.MAILCHIMP_CASE_LIST_ID, {
        'email_address': email,
        'status': 'subscribed'
    })

    # Получения subscriber hash
    subscriber_hash = mailchimp_client \
        .search_members \
        .get(query=email,
             fields='exact_matches.members.id') \
        .get('exact_matches') \
        .get('members')[0].get('id')

    case = Case.objects.get(pk=case_id)
    case_tag = f'Case {case.name}'

    # Добавления тега
    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_CASE_LIST_ID,
        subscriber_hash=subscriber_hash,
        data={'tags': [{'name': case_tag, 'status': 'active'}]})

    # Добавления записи в базу данных
    CaseMailingList.objects.get_or_create(email=email, case=case)

    return JsonResponse({'success': True})
