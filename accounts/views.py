from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.admin import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from Employe_app.models import Employee_request


class Login_view(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user_obj = authenticate(request, username=username, password=password)
        if user_obj is not None:
            if user_obj.groups.filter(name='Stock Head').exists():
                if user_obj.last_login is None:
                    login(request, user_obj)
                    return redirect('change_password')
                else:
                    login(request, user_obj)
                    return redirect('index')
            elif user_obj.groups.filter(name='Employee').exists():
                if user_obj.last_login is None:
                    login(request, user_obj)
                    return redirect('change_password_emp')
                else:
                    login(request, user_obj)
                    return redirect('employee_index')
            elif user_obj.groups.filter(name='stock keeper').exists():
                login(request, user_obj)
                return redirect('home')
            else:
                messages.error(request, 'Unknown Group')
                return render(request, 'account/login.html')
        else:
            messages = 'Invalid Username or Password'
            return render(request, 'account/login.html', {'messages': messages})


class Change_password_view(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'account/change_pass.html')

    def post(self, request):
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if request.user.check_password(current_password):
            if len(new_password) < 8:
                messages.success(
                    request, 'Password length have to be above 8 characters')
                return render(request, 'account/change_pass.html')
            elif new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(
                    request, 'Password has been changed successfully!')
                return redirect('login')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')
        return render(request, 'account/change_pass.html')


class Change_password__emp_view(View):
    @method_decorator(login_required)
    def get(self, request):
        employe_notification_accepted = Employee_request.objects.filter(
            Request_status='accepted', user=request.user, order_number=None).count()
        employe_notification_rejected = Employee_request.objects.filter(
            Request_status='rejected', user=request.user).count()
        total_request = employe_notification_accepted + employe_notification_rejected
        return render(request, 'account/change_pass_for_emp.html', {'total_request': total_request})

    def post(self, request):
        employe_notification_accepted = Employee_request.objects.filter(
            Request_status='accepted', user=request.user, order_number=None).count()
        employe_notification_rejected = Employee_request.objects.filter(
            Request_status='rejected', user=request.user).count()
        total_request = employe_notification_accepted + employe_notification_rejected
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if request.user.check_password(current_password):
            if len(new_password) < 8:
                messages.success(
                    request, 'Password length have to be above 8 characters')
                return render(request, 'account/change_pass_for_emp.html', {'total_request': total_request})
            elif new_password == confirm_password:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password has been changed successfully!', {
                                 'total_request': total_request})
                return redirect('login')
            else:
                messages.error(request, 'New passwords do not match with.')
        else:
            messages.error(request, 'Current password is incorrect.')
            return render(request, 'account/change_pass_for_emp.html', {'total_request': total_request})
