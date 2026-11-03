from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import BookingForm, ContactForm, RegistrationForm
from .models import Appointment, CustomerProfile, Service
from .telegram_notifications import send_telegram_notification


def ensure_default_services():
    if Service.objects.exists():
        return

    default_services = [
        {
            'name': 'Signature Hair Spa',
            'description': 'Deep cleansing scalp treatment, nourishing mask, and smooth finish for healthy, glossy hair.',
            'category': 'Hair Care',
            'audience': 'Women',
            'price': '120000.00',
            'duration': '90 minutes',
            'image': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=900&q=80',
        },
        {
            'name': 'Glow Facial Therapy',
            'description': 'A refreshing facial designed to brighten skin, reduce dullness, and deeply hydrate.',
            'category': 'Skin Care',
            'audience': 'Women',
            'price': '95000.00',
            'duration': '60 minutes',
            'image': 'https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=900&q=80',
        },
        {
            'name': 'Luxury Manicure',
            'description': 'Nail shaping, cuticle care, and a polished finish for neat and confident hands.',
            'category': 'Nail Care',
            'audience': 'Unisex',
            'price': '45000.00',
            'duration': '45 minutes',
            'image': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=900&q=80',
        },
        {
            'name': 'Relaxation Full Body Massage',
            'description': 'A soothing body treatment that eases stress, improves circulation, and restores calm.',
            'category': 'Spa & Wellness',
            'audience': 'Unisex',
            'price': '150000.00',
            'duration': '90 minutes',
            'image': 'https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=900&q=80',
        },
        {
            'name': 'Beard Grooming',
            'description': 'Precision beard trim, shaping, and finishing care for a clean, refined look.',
            'category': 'Grooming',
            'audience': 'Men',
            'price': '60000.00',
            'duration': '40 minutes',
            'image': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=900&q=80',
        },
    ]

    for item in default_services:
        Service.objects.get_or_create(name=item['name'], defaults=item)


def robots_txt(request):
    content = (
        'User-agent: *\n'
        'Allow: /\n'
        'Disallow: /admin/\n'
        'Disallow: /dashboard/\n'
        'Disallow: /admin-dashboard/\n'
        'Disallow: /my-bookings/\n\n'
        'Sitemap: https://glowbook-uganda.onrender.com/sitemap.xml\n'
    )
    return HttpResponse(content, content_type='text/plain; charset=utf-8')


def home(request):
    ensure_default_services()
    featured_services = Service.objects.filter(available=True)[:3]
    return render(request, 'core/home.html', {'featured_services': featured_services})


def services(request):
    ensure_default_services()
    services = Service.objects.filter(available=True).order_by('category', 'name')
    grouped = {}
    for service in services:
        grouped.setdefault(service.category, []).append(service)
    return render(request, 'core/services.html', {'groups': grouped.items()})


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.cleaned_data
        messages.success(request, 'Your message has been received. Our team will contact you shortly.')
        return redirect('contact')
    return render(request, 'core/contact.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
    
        send_telegram_notification(
            f"🎉 NEW CUSTOMER REGISTRATION\n\n"
            f"Username: {user.username}\n"
            f"Email: {user.email}"
        )
        user = authenticate(username=user.username, password=form.cleaned_data['password1'])
        
        if user is not None:
            login(request, user)

        messages.success(request, 'Welcome to GlowBook Uganda! Your account is ready.')
        return redirect('dashboard')
    return render(request, 'core/register.html', {'form': form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'core/login.html')


def logout_page(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@user_passes_test(lambda user: user.is_active and user.is_staff, login_url='login')
def admin_dashboard(request):
    User = get_user_model()
    recent_bookings = Appointment.objects.select_related('customer__user', 'service').order_by('-created_at')[:8]
    pending_count = Appointment.objects.filter(status='Pending').count()
    confirmed_count = Appointment.objects.filter(status='Confirmed').count()
    completed_count = Appointment.objects.filter(status='Completed').count()
    cancelled_count = Appointment.objects.filter(status='Cancelled').count()

    return render(
        request,
        'core/admin_dashboard.html',
        {
            'total_users': User.objects.count(),
            'total_customers': User.objects.filter(customerprofile__isnull=False).count(),
            'total_services': Service.objects.count(),
            'total_appointments': Appointment.objects.count(),
            'pending_count': pending_count,
            'confirmed_count': confirmed_count,
            'completed_count': completed_count,
            'cancelled_count': cancelled_count,
            'recent_bookings': recent_bookings,
        },
    )


@login_required
def dashboard(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    today = timezone.localdate()
    upcoming = Appointment.objects.filter(customer=profile, appointment_date__gte=today).order_by('appointment_date', 'appointment_time')[:5]
    previous = Appointment.objects.filter(customer=profile).exclude(status='Pending').order_by('-appointment_date')[:5]
    return render(
        request,
        'core/dashboard.html',
        {
            'profile': profile,
            'upcoming': upcoming,
            'previous': previous,
            'service_count': Service.objects.filter(available=True).count(),
        },
    )


@login_required
def booking(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    initial = {'phone_number': profile.phone}
    service_id = request.GET.get('service_id')
    if service_id:
        initial['service'] = service_id

    form = BookingForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)
        appointment.customer = profile
        appointment.phone_number = form.cleaned_data['phone_number']
        appointment.save()
        send_telegram_notification(
        f"📅 NEW BOOKING RECEIVED!\n\n"
        f"Customer: {request.user.username}\n"
        f"Service: {appointment.service.name}\n"
        f"Date: {appointment.appointment_date}\n"
        f"Time: {appointment.appointment_time}\n"
        f"Status: {appointment.status}"
        )
        messages.success(request, 'Your appointment has been booked successfully.')
        return redirect('booking_confirmation', appointment_id=appointment.id)
    return render(request, 'core/booking.html', {'form': form})


@login_required
def booking_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, customer__user=request.user)
    whatsapp_message = (
        f"Hello GlowBook Uganda, I would like to confirm my booking for {appointment.service.name} on "
        f"{appointment.appointment_date} at {appointment.appointment_time}. "
        f"My contact number is {appointment.phone_number}. Thank you!"
    )
    whatsapp_url = 'https://wa.me/256789251543?text=' + quote(whatsapp_message)
    return render(
        request,
        'core/booking_success.html',
        {'appointment': appointment, 'whatsapp_url': whatsapp_url},
    )


@login_required
def my_bookings(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    today = timezone.localdate()
    upcoming = Appointment.objects.filter(customer=profile, appointment_date__gte=today).order_by('appointment_date', 'appointment_time')
    completed = Appointment.objects.filter(customer=profile, status='Completed').order_by('-appointment_date')
    cancelled = Appointment.objects.filter(customer=profile, status='Cancelled').order_by('-appointment_date')
    return render(
        request,
        'core/my_bookings.html',
        {'upcoming': upcoming, 'completed': completed, 'cancelled': cancelled},
    )


@require_POST
@login_required
def cancel_booking(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, customer__user=request.user)
    if appointment.status in ['Completed', 'Cancelled']:
        messages.info(request, 'This booking cannot be cancelled.')
    else:
        appointment.status = 'Cancelled'
        appointment.save()
        send_telegram_notification(
            f"❌ BOOKING CANCELLED\n\n"
            f"Customer: {request.user.username}\n"
            f"Service: {appointment.service.name}\n"
            f"Date: {appointment.appointment_date}\n"
            f"Time: {appointment.appointment_time}"
        )
        messages.success(request, 'Your appointment has been cancelled.')
    return redirect('my_bookings')
