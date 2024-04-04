from django.urls import path
from .views import *
urlpatterns = [
    path('home/', casher_index.as_view(), name='home'),
    path('accepted_req_chasher/', accepted_req_casher.as_view(),
         name='accepted_req_chasher'),
    path('check_order_num/', check_order_num.as_view(), name='check_order_num'),
    path('detail_about_given_asset/<str:pk>/',
         detail_about_given_asset.as_view(), name='detail_about_given_asset'),
]
