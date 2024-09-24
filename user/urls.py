from django.urls import path
from .views import logout_view
from .views import UserRegistrationView,UserLoginView,ActivateAccountView,profile_view


urlpatterns = [
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('profile/',profile_view, name='profile'),
]
