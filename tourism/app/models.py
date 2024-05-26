from django.conf import settings
from django.db import models
from authapi.models import CustomUser


class TourPackage(models.Model):
    """Model for tour packages"""
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_persons = models.IntegerField()
    description = models.TextField()
    rating = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    image = models.ImageField(upload_to='packageimages/')
    # Animation delay for frontend
    delay = models.DecimalField(max_digits=3, decimal_places=1, default=0.1)

    def __str__(self):
        return self.name


class Booking(models.Model):
    """Model for bookings"""
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Confirmed'),
        (2, 'Cancelled')
    )
    CANCELLED_BY_CHOICES = (
        ('a', 'Admin'),
        ('u', 'User')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    from_date = models.DateField()
    to_date = models.DateField()
    comment = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    cancelled_by = models.CharField(
        choices=CANCELLED_BY_CHOICES, max_length=1, blank=True, null=True)
    updation_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.name} from {self.from_date} to {self.to_date}"


class Guide(models.Model):
    """Model for travel guides"""
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='guideimages/')
    facebook_link = models.URLField(max_length=200, blank=True, null=True)
    twitter_link = models.URLField(max_length=200, blank=True, null=True)
    instagram_link = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.full_name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
