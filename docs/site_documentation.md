# GlowBook Uganda Site Documentation

## Overview

GlowBook Uganda is a Django-powered beauty and wellness booking website for salons, spas, and grooming businesses in Uganda. It allows visitors to view services, create customer accounts, book appointments, manage bookings, and review service information.

The application combines a public storefront with an authenticated customer experience and a staff-only admin dashboard.

## Purpose

The platform is designed to:

- Make appointment booking easy for customers
- Help salon teams keep bookings organized
- Centralize service catalog management
- Support customer self-service for scheduling and cancellations
- Provide a lightweight admin dashboard for quick business insights

## Site structure

### Public pages

- `/` — Home page with featured services and brand overview
- `/about/` — About page describing the business
- `/services/` — Service catalog grouped by category
- `/contact/` — Contact form for customer inquiries
- `/register/` — New customer registration
- `/login/` — Customer login

### Customer pages

- `/dashboard/` — Personal customer dashboard
- `/booking/` — New appointment booking form
- `/booking/<id>/confirmation/` — Booking confirmation page with WhatsApp booking message
- `/my-bookings/` — Upcoming, completed, and cancelled bookings
- `/bookings/<id>/cancel/` — Booking cancellation action
- `/logout/` — Logout action

### Admin pages

- `/admin-dashboard/` — Staff/admin dashboard with booking summary metrics
- `/admin/` — Django admin interface for service and appointment management

## User roles

### Visitor

A visitor can browse the public site and learn about services and pricing, but cannot create or manage bookings unless they register.

### Registered customer

A registered customer can:

- Log in to the system
- Book appointments for available services
- View personal dashboard information
- Review their upcoming and past bookings
- Cancel future appointments

### Staff/admin

A staff user can access the admin dashboard and manage booking data via Django admin. The admin dashboard exposes summary statistics such as total users, customers, services, and appointments.

## Key application modules

### Core app

The main Django app is `core/` and contains the business logic for:

- service management
- user registration
- appointment booking
- admin metrics
- contact form handling
- WhatsApp and Telegram booking notifications

### Models

#### Service

Represents a beauty or wellness service offered by the business.

Fields:

- `name`
- `description`
- `category`
- `audience`
- `price`
- `duration`
- `image`
- `available`
- `created_at`

Supported categories include:

- Hair Care
- Skin Care
- Nail Care
- Spa & Wellness
- Grooming

#### CustomerProfile

Stores additional customer profile metadata linked to the Django user model.

Fields:

- `user`
- `phone`
- `bio`
- `created_at`

#### Appointment

Stores a booking made by a customer.

Fields:

- `customer`
- `service`
- `appointment_date`
- `appointment_time`
- `phone_number`
- `notes`
- `status`
- `created_at`

Status values include:

- Pending
- Confirmed
- Completed
- Cancelled

## Business flow

### Registration flow

1. The user visits `/register/`
2. They provide a username, email, full name, and optional phone number
3. The registration form creates a Django user and a matching `CustomerProfile`
4. The user is signed in and redirected to the dashboard

### Booking flow

1. Authenticated user opens `/booking/`
2. They choose a service, date, time, phone number, and optional notes
3. The system validates the future date and phone number length
4. The appointment is saved to the database
5. A Telegram notification is sent to the configured admin channel
6. The user is redirected to the confirmation page

### Confirmation flow

Each booking confirmation page generates a WhatsApp message containing the selected service, date, time, and phone contact. This helps customers quickly confirm or discuss their appointment through WhatsApp.

### Cancellation flow

A customer can cancel a non-completed, non-cancelled booking from `/my-bookings/`. The appointment status is changed to `Cancelled` and a notification is sent.

## Forms and validation

### RegistrationForm

- Validates unique email addresses
- Splits full names into first and last name fields
- Creates the related `CustomerProfile`

### ContactForm

Collects:

- name
- email
- phone
- message

### BookingForm

Validates:

- service selection
- future appointment date
- reasonably valid phone number
- optional notes format

## Frontend and templates

Templates are stored in `core/templates/core/` and include pages such as:

- `home.html`
- `services.html`
- `about.html`
- `contact.html`
- `register.html`
- `login.html`
- `dashboard.html`
- `admin_dashboard.html`
- `booking.html`
- `booking_success.html`
- `my_bookings.html`
- `base.html`

The site uses Django templating with a Bootstrap-like visual style and custom CSS/JavaScript assets in `core/static/core/`.

## Static assets and frontend behavior

The frontend includes:

- custom styles in `core/static/core/styles.css`
- JavaScript interactions in `core/static/core/app.js`
- responsive layout styling for mobile and desktop views

## Deployment and environment configuration

The project is ready for cloud deployment and supports environment-based configuration.

Key environment settings include:

- `DEBUG`
- `DJANGO_SECRET_KEY`
- `ALLOWED_HOSTS`
- `DATABASE_URL`

Production dependencies include:

- Django
- Gunicorn
- WhiteNoise
- PostgreSQL support via `dj-database-url` and `psycopg2-binary`

The repository includes deployment helpers:

- `build.sh`
- `Procfile`
- `render.yaml`
- `runtime.txt`

## Local development setup

1. Create and activate a virtual environment
2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Apply database migrations:

```bash
python manage.py migrate
```

4. Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

## Health and monitoring

The site exposes a small health endpoint:

- `/health/` — returns `GlowBook Uganda is running`

There is also a `robots.txt` endpoint for crawling rules and sitemap information.

## Security notes

- Sensitive environment variables are meant to live in `.env` and should not be committed
- Do not expose production secrets in version control
- Admin and account features should be restricted to authenticated staff users

## Maintenance recommendations

- Review bookings and service inventory regularly in Django admin
- Keep service images and pricing updated
- Monitor Telegram notifications for new bookings and cancellations
- Back up the database before production changes
- Apply migrations after model changes

## Summary

GlowBook Uganda is a complete booking and service-management site for beauty and wellness businesses. It offers a customer-facing booking experience, an authenticated dashboard, and an admin management layer in a compact Django architecture.
