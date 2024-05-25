from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/', views.DashboardView, name='home'),
    
    # profile Path
    path('profile', views.ProfileView, name='profile'),
    path('change-pass', views.ChangepassView, name='change_password'),
    
    # Packages Path
    path('add-package', views.AddPackageView, name='add_package'),
    path('manage-package', views.ManagePackageView, name='manage_package'),
    path('update-package/<str:pid>',
         views.UpdatePackageView, name='update_package'),
    
    # Guides Path
    path('add-guide', views.AddGuideView, name='add_guide'),
    path('manage-guide', views.ManageGuideView, name='manage_guide'),
    path('update-guide/<str:gid>', views.UpdateGuideView, name='update_guide'),

    # Manage
    path('manage-users/', views.ManageUserView, name='manage_users'),
    path('manage-bookings/', views.ManageBookingsView, name='manage_bookings'),
    path('user-bookings/<int:user_id>/', views.UserBookingsView,
         name='user_bookings'),

]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
