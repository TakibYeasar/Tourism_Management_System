# Generated by Django 5.0.6 on 2024-05-24 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourpackage',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True),
        ),
    ]
