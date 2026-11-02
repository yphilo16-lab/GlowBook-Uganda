from django.conf import settings
from django.db import models


class Service(models.Model):
    AUDIENCE_CHOICES = [
        ('Women', 'Women'),
        ('Men', 'Men'),
        ('Unisex', 'Unisex'),
    ]

    CATEGORY_CHOICES = [
        ('Hair Care', 'Hair Care'),
        ('Skin Care', 'Skin Care'),
        ('Nail Care', 'Nail Care'),
        ('Spa & Wellness', 'Spa & Wellness'),
        ('Grooming', 'Grooming'),
    ]

    name = models.CharField(max_length=120)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Hair Care')
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='Unisex')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=60, default='60 minutes')
    image = models.URLField(default='https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=900&q=80')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customerprofile')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    phone_number = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']

    def __str__(self):
        return f'{self.customer} - {self.service.name} - {self.appointment_date}'