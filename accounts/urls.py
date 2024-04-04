from .views import *
from django.urls import path
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/',Login_view.as_view(),name='login'),
    path('change_password/',Change_password_view.as_view() , name='change_password'),
    path('change_password_emp/',Change_password__emp_view.as_view() , name='change_password_emp'),
    path('logout/',LogoutView.as_view(next_page = 'login'),name = 'logout'),
]