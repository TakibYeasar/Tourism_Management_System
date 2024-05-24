from django.shortcuts import render
from .models import *
from .forms import *
from app.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from authapi.models import CustomUser
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def DashboardView(request):
    user_count = User.objects.count()
    package_count = TourPackage.objects.count()
    booking_count = Booking.objects.count()
    new_booking_count = Booking.objects.filter(status__isnull=True).count()
    cancelled_booking_count = Booking.objects.filter(status='2').count()
    confirmed_booking_count = Booking.objects.filter(status='1').count()

    context = {
        'user_count': user_count,
        'package_count': package_count,
        'booking_count': booking_count,
        'new_booking_count': new_booking_count,
        'cancelled_booking_count': cancelled_booking_count,
        'confirmed_booking_count': confirmed_booking_count,
    }

    return render(request, 'adminuser/dashboard.html', context)


@login_required
def ProfileView(request):
    if 'alogin' not in request.session:
        return redirect('index')

    admin_id = request.session['alogin']
    admin = CustomUser.objects.get(user_name=admin_id)

    if request.method == 'POST':
        admin.name = request.POST['name']
        admin.email = request.POST['email']
        admin.mobile_number = request.POST['mobile']
        admin.save()

        return redirect('profile')

    return render(request, 'adminuser/profile.html', {'admin': admin})


@login_required
def ChangepassView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            user = request.user

            if not user.check_password(current_password):
                messages.error(request, 'Your current password is wrong.')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, 'Your password was successfully updated!')
                return redirect('dashboard')
    else:
        form = PasswordChangeForm()

    return render(request, 'adminuser/change_password.html', {'form': form})



@login_required
def AddPackageView(request):
    if request.method == 'POST':
        form = PackageCreationForm(request.POST, request.FILES)
        if form.is_valid():
            package = TourPackage(
                package_name=form.cleaned_data['package_name'],
                package_type=form.cleaned_data['package_type'],
                package_location=form.cleaned_data['package_location'],
                package_price=form.cleaned_data['package_price'],
                package_features=form.cleaned_data['package_features'],
                package_details=form.cleaned_data['package_details'],
                package_image=form.cleaned_data['package_image']
            )
            package.save()
            messages.success(request, 'Package Created Successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Something went wrong. Please try again')
    else:
        form = PackageCreationForm()
        
    return render(request, 'adminuser/add_packages.html', {'form': form})


@login_required
def ManagePackageView(request):
    if 'action' in request.GET and request.GET.get('action') == 'delete':
        pid = int(request.GET.get('id'))
        TourPackage.objects.filter(id=pid).delete()
        messages.success(request, "Package deleted.")
        return redirect('manage_packages')

    packages = TourPackage.objects.all()
    return render(request, 'adminuser/manage_packages.html', {'packages': packages})


@login_required
def UpdatePackageView(request, pid):
    if 'alogin' not in request.session:
        return redirect('index')

    package = TourPackage.objects.get(pk=pid)

    if request.method == 'POST':
        package.name = request.POST['packagename']
        package.type = request.POST['packagetype']
        package.location = request.POST['packagelocation']
        package.price = request.POST['packageprice']
        package.features = request.POST['packagefeatures']
        package.details = request.POST['packagedetails']
        package.save()
        return redirect('update_package', pid=pid)

    return render(request, 'adminuser/update_packages.html', {'package': package})


@login_required
def AddGuideView(request):
    if request.method == 'POST':
        form = PackageCreationForm(request.POST, request.FILES)
        if form.is_valid():
            package = TourPackage(
                package_name=form.cleaned_data['package_name'],
                package_type=form.cleaned_data['package_type'],
                package_location=form.cleaned_data['package_location'],
                package_price=form.cleaned_data['package_price'],
                package_features=form.cleaned_data['package_features'],
                package_details=form.cleaned_data['package_details'],
                package_image=form.cleaned_data['package_image']
            )
            package.save()
            messages.success(request, 'Package Created Successfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Something went wrong. Please try again')
    else:
        form = PackageCreationForm()

    return render(request, 'adminuser/add_guides.html', {'form': form})


@login_required
def ManageGuideView(request):
    if 'action' in request.GET and request.GET.get('action') == 'delete':
        pid = int(request.GET.get('id'))
        TourPackage.objects.filter(id=pid).delete()
        messages.success(request, "Package deleted.")
        return redirect('manage_packages')

    packages = TourPackage.objects.all()
    return render(request, 'adminuser/manage_guides.html', {'packages': packages})


@login_required
def UpdateGuideView(request, pid):
    if 'alogin' not in request.session:
        return redirect('index')

    package = TourPackage.objects.get(pk=pid)

    if request.method == 'POST':
        package.name = request.POST['packagename']
        package.type = request.POST['packagetype']
        package.location = request.POST['packagelocation']
        package.price = request.POST['packageprice']
        package.features = request.POST['packagefeatures']
        package.details = request.POST['packagedetails']
        package.save()
        return redirect('update_package', pid=pid)

    return render(request, 'adminuser/update_Guides.html', {'package': package})



@login_required
def ManageUserView(request):
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})


@login_required
def ManageBookingsView(request):
    if not request.user.is_staff:  # Ensure the user is an admin
        return redirect('index')

    if 'bkid' in request.GET:
        booking_id = int(request.GET['bkid'])
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 2
        booking.cancelled_by = 'a'
        booking.save()
        msg = "Booking Cancelled successfully"
    elif 'bckid' in request.GET:
        booking_id = int(request.GET['bckid'])
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 1
        booking.save()
        msg = "Booking Confirmed successfully"
    else:
        msg = ""

    bookings = Booking.objects.select_related('user', 'package').all()
    return render(request, 'manage_bookings.html', {'bookings': bookings, 'msg': msg})


def UserBookingsView(request):
    context = {}
    try:
        bookings = Booking.objects.filter(user=request.user)
        context['results'] = bookings
        context['uname'] = request.user.username  # Assuming user has username
    except Exception as e:
        context['error'] = str(e)
    return render(request, 'manage_bookings.html', context)
