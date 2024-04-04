from django.db import models
from django.contrib.auth.admin import User
from django.conf import settings
from django.utils import timezone


class user_department(models.Model):
    Department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.Department_name


class User_profile(models.Model):
    usre = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    user_img = models.ImageField(
        default='img/user_profile.jpg', upload_to='profile_pics')
    user_phone_num = models.CharField(max_length=20)
    Department = models.ForeignKey(user_department, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.usre)
