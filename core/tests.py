from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Appointment, CustomerProfile, Service


class GlowBookTests(TestCase):
    def test_robots_txt_returns_expected_plain_text(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers['Content-Type'].startswith('text/plain'))
        self.assertEqual(
            response.content.decode('utf-8'),
            (
                'User-agent: *\n'
                'Allow: /\n'
                'Disallow: /admin/\n'
                'Disallow: /dashboard/\n'
                'Disallow: /admin-dashboard/\n'
                'Disallow: /my-bookings/\n\n'
                'Sitemap: https://glowbook-uganda.onrender.com/sitemap.xml\n'
            ),
        )

    def test_health_check_endpoint_returns_expected_response(self):
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers['Content-Type'].startswith('text/plain'))
        self.assertEqual(response.content.decode('utf-8'), 'GlowBook Uganda is running')

    def test_contact_page_uses_updated_business_email_and_keeps_whatsapp(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'mailto:glowbookuganda@gmail.com')
        self.assertContains(response, 'glowbookuganda@gmail.com')
        self.assertContains(response, 'https://wa.me/256789251543')

    def test_home_page_uses_licensed_photo_assets(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'images.unsplash.com/photo-1524504388940-b1c1722653e1')
        self.assertContains(response, 'images.unsplash.com/photo-1521590832167-7bcbfaa6381f')

    def test_services_page_uses_licensed_photo_assets(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'images.unsplash.com/photo-1524504388940-b1c1722653e1')
        self.assertContains(response, 'images.unsplash.com/photo-1556228578-0be9b6db1a94')

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_services_page_displays_database_services(self):
        Service.objects.create(
            name='Hair Braiding',
            description='Beautiful braids.',
            category='Hair Care',
            audience='Women',
            price='50000.00',
            duration='60 minutes',
            available=True,
        )

        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hair Braiding')

    def test_registration_creates_user_and_profile(self):
        response = self.client.post(
            reverse('register'),
            {
                'full_name': 'Aisha Nakato',
                'email': 'aisha@example.com',
                'username': 'aisha',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            },
        )

        self.assertEqual(response.status_code, 302)
        user = get_user_model().objects.get(username='aisha')
        self.assertTrue(CustomerProfile.objects.filter(user=user).exists())

    def test_booking_requires_authentication(self):
        response = self.client.get(reverse('booking'))
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_requires_staff_access(self):
        normal_user = get_user_model().objects.create_user(username='guest', email='guest@example.com', password='StrongPass123')
        self.client.login(username='guest', password='StrongPass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

        staff_user = get_user_model().objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='StrongPass123',
            is_staff=True,
        )
        self.client.login(username='staffuser', password='StrongPass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_appointment_booking_saves_for_logged_in_user(self):
        service = Service.objects.create(
            name='Haircut and Fade',
            description='Modern male haircut.',
            category='Hair Care',
            audience='Men',
            price='40000.00',
            duration='45 minutes',
            available=True,
        )
        user = get_user_model().objects.create_user(username='sam', email='sam@example.com', password='StrongPass123')
        CustomerProfile.objects.create(user=user, phone='0771234567', bio='Beauty lover')

        self.client.login(username='sam', password='StrongPass123')
        response = self.client.post(
            reverse('booking'),
            {
                'service': str(service.id),
                'appointment_date': '2030-12-20',
                'appointment_time': '10:00',
                'phone_number': '0771234567',
                'notes': 'Please be gentle.',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Appointment.objects.filter(customer=user.customerprofile, service=service).exists())
