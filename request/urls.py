from django.urls import path
from .views import home, request_blood,dashboard,accept_request,donor_list

urlpatterns = [
    path('', home, name='home'),
    path('request/', request_blood, name='request_blood'),
    path('dashboard/', dashboard, name='dashboard'),
    path('accept/<int:request_id>/', accept_request, name='accept_request'),
    path('donors/', donor_list, name='donor_list'),
]
