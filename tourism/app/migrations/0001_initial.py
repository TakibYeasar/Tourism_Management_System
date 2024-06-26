# Generated by Django 5.0.6 on 2024-05-24 15:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='guideimages/')),
                ('facebook_link', models.URLField(blank=True, null=True)),
                ('twitter_link', models.URLField(blank=True, null=True)),
                ('instagram_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TourPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('duration', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_persons', models.IntegerField()),
                ('description', models.TextField()),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('image', models.ImageField(upload_to='packageimages/')),
                ('delay', models.DecimalField(decimal_places=1, default=0.1, max_digits=3)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('comment', models.TextField(blank=True)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Confirmed'), (2, 'Cancelled')], default=0)),
                ('cancelled_by', models.CharField(blank=True, choices=[('a', 'Admin'), ('u', 'User')], max_length=1, null=True)),
                ('updation_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tourpackage')),
            ],
        ),
    ]
