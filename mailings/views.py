from django.http import JsonResponse
from django.conf import settings
from cases.models import Case
from .models import CommonMailingList, CaseMailingList
from .mailchimp_services import add_mailchimp_email_with_tag
from .services import add_email_to_common_mailchimp_list


def add_to_common_list_view(request):
    """Веб-сервис, добавляющий email в общий лист рассылки"""

    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})
    add_email_to_common_mailchimp_list(email)
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



    return JsonResponse({'success': True})
