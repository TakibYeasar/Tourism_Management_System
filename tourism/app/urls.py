from django.urls import path
from .import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('change-password/', views.ChangepassView, name='change_password'),
    path('profile/', views.ProfileView, name='profile'),
    path('packages/', views.AllPackagesView, name='package_list'),
    path('package/<int:pkg_id>/', views.PackageDetailsView, name='package_details'),
    path('package/<int:pkg_id>/book/', views.BookPackageView, name='book_package'),
    path('confirmation/', views.ConfirmationView, name='confirmation'),
    path('tour-history/', views.TourHistoryView, name='tour_history'),
]
