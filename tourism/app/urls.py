from django.urls import path
from .import views

urlpatterns = [
    path('', views.HomeView, name='home'),
    path('change-password/', views.ChangepassView, name='change_password'),
    path('profile/', views.ProfileView, name='user_profile'),
    path('packages/', views.AllPackagesView, name='package_list'),
    path('package/<int:pkg_id>/', views.PackageDetailsView, name='package_details'),
    path('guides/', views.AllGuidesView, name='guide_list'),
    path('package/<int:pkg_id>/book/', views.BookPackageView, name='book_package'),
    path('tour_history/', views.TourHistoryView, name='tour_history'),
    path('contact/', views.ContactView, name='contact'),
]
