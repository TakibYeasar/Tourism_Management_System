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
    guide_count = Guide.objects.count()
    booking_count = Booking.objects.count()
    new_booking_count = Booking.objects.filter(status__isnull=True).count()
    cancelled_booking_count = Booking.objects.filter(status='2').count()
    confirmed_booking_count = Booking.objects.filter(status='1').count()

    context = {
        'user_count': user_count,
        'package_count': package_count,
        'guide_count': guide_count,
        'booking_count': booking_count,
        'new_booking_count': new_booking_count,
        'cancelled_booking_count': cancelled_booking_count,
        'confirmed_booking_count': confirmed_booking_count,
    }

    return render(request, 'adminuser/dashboard.html', context)


@login_required
def ProfileView(request, admin_id):
    if 'alogin' not in request.session:
        return redirect('home')

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
                name=form.cleaned_data['name'],
                location=form.cleaned_data['location'],
                duration=form.cleaned_data['duration'],
                price=form.cleaned_data['price'],
                max_persons=form.cleaned_data['max_persons'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data['image']
            )
            package.save()
            messages.success(request, 'Package Created Successfully')
            return redirect('home')
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
        return redirect('manage_package')

    packages = TourPackage.objects.all()
    return render(request, 'adminuser/manage_packages.html', {'packages': packages})


@login_required
def UpdatePackageView(request, pid):
    # if 'alogin' not in request.session:
    #     return redirect('home')

    package = TourPackage.objects.get(pk=pid)

    if request.method == 'POST':
        package.name = request.POST['name']
        package.location = request.POST['location']
        package.duration = request.POST['duration']
        package.price = request.POST['price']
        package.max_persons = request.POST['max_persons']
        package.description = request.POST['description']
        if 'image' in request.FILES:
            package.image = request.FILES['image']
        package.save()
        return redirect('update_package', pid=pid)

    return render(request, 'adminuser/update_packages.html', {'package': package})



@login_required
def AddGuideView(request):
    if request.method == 'POST':
        form = GuideCreationForm(request.POST, request.FILES)
        if form.is_valid():
            guide= Guide(
                full_name=form.cleaned_data['full_name'],
                designation=form.cleaned_data['designation'],
                image=form.cleaned_data['image'],
                facebook_link=form.cleaned_data['facebook_link'],
                twitter_link=form.cleaned_data['twitter_link'],
                instagram_link=form.cleaned_data['instagram_link']
            )
            guide.save()
            messages.success(request, 'Guide Created Successfully')
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong. Please try again')
    else:
        form = GuideCreationForm()

    return render(request, 'adminuser/add_guides.html', {'form': form})


@login_required
def ManageGuideView(request):
    if 'action' in request.GET and request.GET.get('action') == 'delete':
        gid = int(request.GET.get('id'))
        Guide.objects.filter(id=gid).delete()
        messages.success(request, "Guide deleted.")
        return redirect('manage_packages')

    guides = Guide.objects.all()
    return render(request, 'adminuser/manage_guides.html', {'guides': guides})


@login_required
def UpdateGuideView(request, gid):
    if 'alogin' not in request.session:
        return redirect('home')

    guide = Guide.objects.get(pk=gid)

    if request.method == 'POST':
        guide.full_name = request.POST['full_name']
        guide.designation = request.POST['designation']
        guide.facebook_link = request.POST['facebook_link']
        guide.twitter_link = request.POST['twitter_link']
        guide.instagram_link = request.POST['instagram_link']
        if 'image' in request.FILES:
            guide.image = request.FILES['image']
        guide.save()
        return redirect('update_guide', gid=gid)

    return render(request, 'adminuser/update_guides.html', {'guide': guide})



@login_required
def ManageUserView(request):
    users = User.objects.all()
    return render(request, 'adminuser/manage_users.html', {'users': users})


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
    return render(request, 'adminuser/manage_bookings.html', {'bookings': bookings, 'msg': msg})


def UserBookingsView(request):
    context = {}
    try:
        bookings = Booking.objects.filter(user=request.user)
        context['results'] = bookings
        context['uname'] = request.user.username  # Assuming user has username
    except Exception as e:
        context['error'] = str(e)
    return render(request, 'adminuser/manage_bookings.html', context)

