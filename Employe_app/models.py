from django.db import models
from django.contrib.auth.admin import User
from inventory_head.models import Assets_tbl
# Create your models here.


class Employee_request(models.Model):
    order_number = models.CharField(max_length=20, unique=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    Asset_name = models.ForeignKey(Assets_tbl, on_delete=models.PROTECT)
    Amount_of_asset = models.IntegerField(null=True)
    Coast_for_given_items = models.IntegerField(null=True)
    Reaso_why_you_need_asset = models.TextField()
    Request_status = models.CharField(max_length=20, default='pending')
    Request_checked_by = models.CharField(max_length=100, null=True)
    Requested_date = models.DateField(auto_now_add=True)
    Request_accepted_date = models.DateField(null=True)
    Asset_given_by = models.CharField(null=True, max_length=100)
    Serial_num = models.TextField(null=True)
    Aseet_pin_num = models.TextField(null=True)
    Asset_given_date = models.DateField(null=True)
