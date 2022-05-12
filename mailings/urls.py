from django.urls import path, include
from .views import add_to_common_list_view, add_to_case_list_view

urlpatterns = [
    path('add_to_common_list/', add_to_common_list_view),
    path('add_to_case_list/', add_to_case_list_view),
]
