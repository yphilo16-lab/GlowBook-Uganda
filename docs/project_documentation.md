# GlowBook Uganda Project Documentation

## 1. Project introduction

GlowBook Uganda is a Django web application designed for beauty and wellness businesses that want to offer online appointment booking. The platform allows customers to browse services, register accounts, choose preferred treatments, and reserve time slots. The admin side provides a dashboard showing key activity and recent bookings.

## 2. Project purpose

The app was built to simplify salon booking for clients in Uganda and to make appointment management easier for the business team. It reduces the need for manual scheduling and keeps a structured record of services, user profiles, and appointments.

## 3. Technologies used

- Python 3
- Django 6.1.1
- SQLite for local development
- PostgreSQL-ready deployment configuration
- HTML, CSS, and Bootstrap-inspired custom styling
- JavaScript used for frontend interactions in static assets
- WhiteNoise for static file serving in production
- Gunicorn for production hosting

## 4. Functional modules

### 4.1 Homepage and service discovery
The home page presents the brand, highlights featured services, and encourages users to book. The services page groups treatments by category to make browsing simple.

### 4.2 Registration and user account system
Users can create an account using a registration form. The user model stores the username, email, first name, last name, and phone number. A `CustomerProfile` record is created automatically for each registered customer.

### 4.3 Booking flow
Authenticated users can create appointments by choosing a service, date, time, and optional notes. The booking form validates future dates and valid phone numbers before saving the appointment.

### 4.4 Customer dashboard
The dashboard gives each customer a summary of their profile, available services, and upcoming/previous appointments. It acts as a personal booking management area.

### 4.5 Admin dashboard
The admin dashboard displays total users, customers, services, appointments, and counts of each booking status. It also lists recent bookings for quick operational oversight.

### 4.6 Contact form
The contact form allows visitors to send messages. Once submitted successfully, the app displays a success message and redirects back to the contact page.

## 5. Data model summary

### Service
Represents a beauty or wellness treatment.

Fields:
- name
- description
- category
- audience
- price
- duration
- image
- available
- created_at

### CustomerProfile
Represents a user’s profile for the beauty platform.

Fields:
- user
- phone
- bio
- created_at

### Appointment
Represents a customer booking request.

Fields:
- customer
- service
- appointment_date
- appointment_time
- phone_number
- notes
- status
- created_at

## 6. Application routes

- `/` — Home page
- `/services/` — Services listing
- `/about/` — About page
- `/contact/` — Contact page
- `/register/` — Registration
- `/login/` — Login
- `/logout/` — Logout
- `/dashboard/` — Customer dashboard
- `/admin-dashboard/` — Admin dashboard
- `/booking/` — New appointment booking
- `/booking/<id>/confirmation/` — Booking confirmation
- `/my-bookings/` — User booking history
- `/bookings/<id>/cancel/` — Cancel appointment
- `/admin/` — Django admin panel

## 7. Configurations and deployment readiness

The project has been updated to support hosted deployment:

- `DEBUG` reads from environment variables
- `ALLOWED_HOSTS` can be configured through environment variables
- `DATABASE_URL` supports PostgreSQL in production
- `whitenoise` is enabled for static file management
- Gunicorn is included for deployment with a `Procfile`
- `requirements.txt` includes the required production packages

## 8. Local installation steps

1. Clone the repository to your workspace.
2. Create a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Run migrations with `python manage.py migrate`.
5. Create a superuser with `python manage.py createsuperuser`.
6. Launch the site with `python manage.py runserver`.

## 9. Production hosting checklist

- Set `DJANGO_SECRET_KEY`
- Set `DEBUG=False`
- Set `ALLOWED_HOSTS` to your production domain
- Configure `DATABASE_URL` for your database provider
- Run `python manage.py collectstatic --noinput`
- Start the app using Gunicorn or the platform’s default web process

## 10. Future enhancements

- Email notifications for booking confirmation
- WhatsApp reminders and automated messages
- Product inventory or package-selling features
- Payment integration for premium services
- Multi-admin roles and staff scheduling
- Advanced analytics and reporting

## 11. Summary

GlowBook Uganda is a complete booking solution for beauty and wellness services. The platform is structured, scalable, and hosting-ready, making it suitable for real-world launch on a cloud hosting provider.
