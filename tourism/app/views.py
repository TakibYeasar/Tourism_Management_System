
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from authapi.models import CustomUser
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TourPackage, Booking
from .forms import BookingForm


def HomeView(request):
    return render(request, 'app/home.html')


def ChangepassView(request):
    if not request.session.get('login'):
        return redirect('index')

    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmpassword')
        email = request.session.get('login')

        user = User.objects.filter(email=email, password=password).first()
        if user:
            if new_password == confirm_password:
                user.password = new_password
                user.save()
                msg = "Your password was changed successfully."
            else:
                error = "New password and confirm password do not match."
        else:
            error = "Your current password is wrong."

    return render(request, 'change_password.html', {'error': error, 'msg': msg})


def ProfileView(request):
    if 'login' not in request.session:
        return redirect('index')
    user_email = request.session['login']
    user = User.objects.get(email=user_email)
    if request.method == 'POST':
        user.full_name = request.POST.get('name')
        user.mobile_number = request.POST.get('mobileno')
        user.save()
        msg = "Profile Updated Successfully"
        return render(request, 'profile.html', {'user': user, 'msg': msg})
    return render(request, 'profile.html', {'user': user})


def AllPackagesView(request):
    packages = TourPackage.objects.all()[:4]
    return render(request, 'app/packages.html', {'packages': packages})


def PackageDetailsView(request, pkg_id):
    package = TourPackage.objects.get(pk=pkg_id)
    return render(request, 'package_details.html', {'package': package})


def BookPackageView(request, pkg_id):
    package = get_object_or_404(TourPackage, id=pkg_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.save()
            return redirect('thank_you')  # or another success page
    else:
        form = BookingForm()
    return render(request, 'package-details.html', {'package': package, 'form': form})
    return redirect('index')  # Redirect to index page after booking


def ConfirmationView(request):
    msg = request.session.get('msg', '')
    return render(request, 'confirmation.html', {'msg': msg})


def TourHistoryView(request):
    if not request.session.get('login'):
        return redirect('index')

    if request.method == 'POST':
        bkid = request.POST.get('bkid')
        try:
            booking = Booking.objects.get(id=bkid)
            from_date = booking.from_date
            today = datetime.now().date()
            difference = (from_date - today).days
            if difference > 1:
                booking.status = 2
                booking.cancelled_by = 'u'
                booking.save()
                messages.success(request, 'Booking Cancelled successfully')
            else:
                messages.error(
                    request, "You can't cancel booking before 24 hours")
        except Booking.DoesNotExist:
            messages.error(request, "Booking does not exist")

    user_email = request.session.get('login')
    bookings = Booking.objects.filter(user_email=user_email)
    return render(request, 'tour_history.html', {'bookings': bookings})


