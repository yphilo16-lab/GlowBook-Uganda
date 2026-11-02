from django.contrib import admin

from .models import Appointment, CustomerProfile, Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'audience', 'price', 'duration', 'available')
    list_filter = ('category', 'audience', 'available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'available')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'appointment_date', 'appointment_time', 'status', 'phone_number')
    list_filter = ('status', 'appointment_date', 'service__category')
    search_fields = ('customer__user__username', 'service__name', 'phone_number')
    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']

    @admin.action(description='Mark selected bookings as confirmed')
    def mark_confirmed(self, request, queryset):
        queryset.update(status='Confirmed')

    @admin.action(description='Mark selected bookings as completed')
    def mark_completed(self, request, queryset):
        queryset.update(status='Completed')

    @admin.action(description='Mark selected bookings as cancelled')
    def mark_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
