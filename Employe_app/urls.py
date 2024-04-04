from django.urls import path
from .views import *
urlpatterns = [
    path('employee_index/', employee_index_view.as_view(), name='employee_index'),
    path('employee_request/', employee_request.as_view(), name='employee_request'),
    path('emp_req_notification/', notfication_for_request.as_view(),
         name='emp_req_notification'),
    path('detail_for_accepted_request/<str:pk>/',
         Detail_for_accepted_req.as_view(), name='detail_for_accepted_request')
]
