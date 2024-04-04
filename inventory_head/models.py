from django.db import models
# Create your models here.


class Asset_detail(models.Model):
    asset_code = models.IntegerField(unique=True)
    asset_group = models.CharField(max_length=100)

    def __str__(self):
        return self.asset_group


class Assets_tbl(models.Model):
    Asset_name = models.CharField(max_length=100)
    Amout_of_asset = models.IntegerField()
    Coast_of_single_asset = models.IntegerField()
    Total_coast = models.IntegerField()
    Receipt_number = models.CharField(max_length=100)
    Asset_code_and_group = models.CharField(max_length=100)
    measurment = models.CharField(max_length=20)
    Asset_Inserted_date = models.DateTimeField(auto_now_add=True)
    Assset_Registered_by = models.CharField(max_length=100)

    def __str__(self):
        return self.Asset_name
