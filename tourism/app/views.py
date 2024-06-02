
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from authapi.models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


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
    if 'user_id' not in request.session:
        return redirect('home')
    user_id = request.session['user_id']
    user = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'app/profile.html', {'user': user})


# def AllPackagesView(request):
#     packages = TourPackage.objects.all()
#     return render(request, 'app/package_list.html', {'packages': packages})


def AllPackagesView(request):
  packages = TourPackage.objects.all()
  print(f"Number of packages retrieved: {len(packages)}")
  return render(request, 'app/package_list.html', {'packages': packages})


def PackageDetailsView(request, pkg_id):
    package = TourPackage.objects.get(pk=pkg_id)
    return render(request, 'app/package_details.html', {'package': package})


def AllGuidesView(request):
    guides = Guide.objects.all()
    return render(request, 'app/guides.html', {'guides': guides})


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
    return render(request, 'adminuser/package-details.html', {'package': package, 'form': form, 'pkg_id': pkg_id})


def TourHistoryView(request):
    if not request.session.get('login'):
        return redirect('home')

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
    try:
        user = CustomUser.objects.get(email=user_email)
        bookings = Booking.objects.filter(user=user)
    except CustomUser.DoesNotExist:
        bookings = []

    return render(request, 'app/tour_history.html', {'bookings': bookings})



def ContactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'app/contact.html', {'form': form})

