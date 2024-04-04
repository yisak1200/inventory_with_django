from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.admin import User
from .models import Employee_request
from inventory_head.models import Assets_tbl
import uuid


class employee_request(View):
    @method_decorator(login_required)
    def get(self, request):
        assets = Assets_tbl.objects.all()
        employe_notification_accepted = Employee_request.objects.filter(
            Request_status='accepted', user=request.user, order_number=None).count()
        employe_notification_rejected = Employee_request.objects.filter(
            Request_status='rejected', user=request.user).count()
        total_request = employe_notification_accepted + employe_notification_rejected
        return render(request, 'employee_temp/request_asset.html', {'assets': assets, 'total_request': total_request})

    def post(self, request):
        assets = Assets_tbl.objects.all()
        employe_notification_accepted = Employee_request.objects.filter(
            Request_status='accepted', user=request.user, order_number=None).count()
        employe_notification_rejected = Employee_request.objects.filter(
            Request_status='rejected', user=request.user).count()
        total_request = employe_notification_accepted + employe_notification_rejected
        asset_name = request.POST['asset_name']
        amount_of_asset = int(request.POST["amount_of_asset"])
        reson_for_requsting_asset = request.POST['Reason_why']
        emp_name = request.user.first_name + " " + request.user.last_name

        asset = Assets_tbl.objects.get(Asset_name=asset_name)
        user_pg = request.user.username
        user_filter = User.objects.filter(username=user_pg).first()
        if not asset_name:
            messages.error(request, 'asset name is required')
            return render(request, 'employee_temp/request_asset.html', {'assets': assets, 'total_request': total_request})
        if not amount_of_asset:
            messages.error(request, 'amount of asset is required')
            return render(request, 'employee_temp/request_asset.html', {'total_request': total_request})
        if not reson_for_requsting_asset:
            messages.error(
                request, 'Reason Why You need for the asset is required')
            return render(request, 'employee_temp/request_asset.html', {'assets': assets, 'total_request': total_request})
        if Assets_tbl.objects.filter(Asset_name=asset_name).exists():
            asset_amount = Assets_tbl.objects.get(Asset_name=asset_name)
            amount_of_asset_tbl = int(asset_amount.Amout_of_asset)
            if Employee_request.objects.filter(Asset_name=asset, user=user_filter, Request_status='pending').exists():
                messages.error(
                    request, 'You have already request for this asset wait until you get Response')
                return render(request, 'employee_temp/request_asset.html', {'assets': assets, 'total_request': total_request})
            elif amount_of_asset_tbl < amount_of_asset:
                messages.error(
                    request, 'the amount of asset You are asking is larger than the amount in the  store')
                return render(request, 'employee_temp/request_asset.html', {'assets': assets, 'total_request': total_request})
            else:
                emp_req = Employee_request(
                    user=user_filter, Asset_name=asset, Amount_of_asset=amount_of_asset, Reaso_why_you_need_asset=reson_for_requsting_asset)
                emp_req.save()
                success = 'Asset Requsted sucessfully'
                return render(request, 'employee_temp/request_asset.html', {'amount': amount_of_asset_tbl, 'success': success, 'assets': assets, 'total_request': total_request})
        else:
            messages.error(request, 'there is no such Asset in the store')
            return render(request, 'employee_temp/request_asset.html', {'assets': assets, 'total_request': total_request})


class employee_index_view(View):
    @method_decorator(login_required)
    def get(self, request):
        employe_notification_accepted = Employee_request.objects.filter(
            Request_status='accepted', user=request.user, order_number=None).count()
        employe_notification_rejected = Employee_request.objects.filter(
            Request_status='rejected', user=request.user).count()
        total_request = employe_notification_accepted + employe_notification_rejected
        return render(request, 'employee_temp/employee_index.html', {'total_request': total_request})


class notfication_for_request (View):
    @method_decorator(login_required)
    def get(self, request):
        accepted = Employee_request.objects.filter(
            Request_status='accepted', user=request.user)
        rejected = Employee_request.objects.filter(
            Request_status='rejected', user=request.user)
        employe_notification_accepted = Employee_request.objects.filter(
            Request_status='accepted', user=request.user, order_number=None).count()
        employe_notification_rejected = Employee_request.objects.filter(
            Request_status='rejected', user=request.user).count()
        total_request = employe_notification_accepted + employe_notification_rejected
        return render(request, 'employee_temp/notification_for_request.html', {'accepted': accepted, 'rejected': rejected, 'total_request': total_request})


class Detail_for_accepted_req(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        employe_notification_accepted = Employee_request.objects.filter(
            Request_status='accepted', user=request.user, order_number=None).count()
        employe_notification_rejected = Employee_request.objects.filter(
            Request_status='rejected', user=request.user).count()
        total_request = employe_notification_accepted + employe_notification_rejected
        accepted_req_detail = Employee_request.objects.get(id=pk)
        return render(request, 'employee_temp/detail_about_accepted_req.html', {'accepted_req_detail': accepted_req_detail, 'total_request': total_request})

    def post(self, request, pk):
        accepted_req_detail = Employee_request.objects.get(id=pk)
        accepted_req_detail.order_number = uuid.uuid4().hex[:6]
        accepted_req_detail.save()
        employe_notification_accepted = Employee_request.objects.filter(
            Request_status='accepted', user=request.user, order_number=None).count()
        employe_notification_rejected = Employee_request.objects.filter(
            Request_status='rejected', user=request.user).count()
        total_request = employe_notification_accepted + employe_notification_rejected
        return render(request, 'employee_temp/detail_about_accepted_req.html', {'total_request': total_request, 'accepted_req_detail': accepted_req_detail})
