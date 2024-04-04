from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.views import View
from inventory_head.models import Assets_tbl
from Employe_app.models import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from inventory_head.models import Assets_tbl
from datetime import datetime
# Create your views here.


class casher_index(View):
    @method_decorator(login_required)
    def get(self, request):
        req_accepted = Employee_request.objects.filter(
            Request_status='accepted').count()
        if 'search' in request.GET:
            q = request.GET['search']
            multiple_q = Q(Q(Asset_name__icontains=q))
            asset_tbl = Assets_tbl.objects.filter(multiple_q)
        else:
            asset_tbl = Assets_tbl.objects.all()
        return render(request, 'casher_page/home_page.html', {'asset_tbl': asset_tbl})


class accepted_req_casher(View):
    def get(self, request):
        accepted_request = Employee_request.objects.filter(
            Request_status='accepted')
        return render(request, 'casher_page/accepted_req_casher.html', {'accepted_request': accepted_request})


class check_order_num(View):
    def get(self, request):
        return render(request, 'casher_page/give_asset.html')

    def post(self, request):
        order_number = request.POST.get('order_number')
        employe_req_order_ftlter = Employee_request.objects.filter(
            order_number=order_number, Request_status='accepted')
        if employe_req_order_ftlter.exists():
            employe_req_order_num = Employee_request.objects.get(
                order_number=order_number)
            return redirect('detail_about_given_asset', pk=employe_req_order_num.pk)
        else:
            messages.error(request, "There is no such order number")
            return render(request, 'casher_page/give_asset.html')


class detail_about_given_asset(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        employe_req_order_num = get_object_or_404(Employee_request, pk=pk)
        return render(request, 'casher_page/detail_about_given_asset.html', {'employe_req_order_num': employe_req_order_num})

    def post(self, request, pk):
        employe_req_order_num = get_object_or_404(Employee_request, pk=pk)
        # Retrieve the updated values from the form data
        asset_name_to_be_given = employe_req_order_num .Asset_name.Asset_name
        asset_name_in_tbl = Assets_tbl.objects.get(
            Asset_name=asset_name_to_be_given)
        amount_of_asset_tobe_given = int(employe_req_order_num.Amount_of_asset)
        amount_of_asset_tbl = int(asset_name_in_tbl.Amout_of_asset)
        total_amount = amount_of_asset_tbl - amount_of_asset_tobe_given
        asset_name_in_tbl.Amout_of_asset = total_amount
        asset_coast_in_tbl = Assets_tbl.objects.get(
            Asset_name=asset_name_to_be_given)
        updated_total = int(asset_coast_in_tbl.Total_coast) - int(
            asset_coast_in_tbl.Coast_of_single_asset) * int(amount_of_asset_tobe_given)
        coast_asset_tobe_given = int(
            asset_coast_in_tbl.Coast_of_single_asset) * int(amount_of_asset_tobe_given)
        asset_name_in_tbl.Total_coast = updated_total
        asset_name_in_tbl.save()
        Serial_num = request.POST.get('serial_number')
        Asset_pin_num = request.POST.get('asset_pin_number')
        asset_given_by = request.user.first_name + " " + request.user.last_name
        # Update the Employee_request object with the new values
        employe_req_order_num.Serial_num = Serial_num
        employe_req_order_num.Aseet_pin_num = Asset_pin_num
        employe_req_order_num.Asset_given_by = asset_given_by
        employe_req_order_num.Request_status = 'given'
        employe_req_order_num.Coast_for_given_items = coast_asset_tobe_given
        employe_req_order_num.Asset_given_date = datetime.now()
        employe_req_order_num.save()
        return redirect('check_order_num')
