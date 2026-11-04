# GlowBook Uganda

GlowBook Uganda is a Django-based beauty and wellness booking platform built for salon and grooming businesses. It includes customer registration, appointment booking, login, dashboards, service listings, admin management, and a WhatsApp booking confirmation flow.

## Documentation

- [Site documentation](docs/site_documentation.md)
- [Project documentation](docs/project_documentation.md)

## Features

- Home, about, services, contact and booking pages
- User registration and secure login
- Customer dashboard with upcoming and previous appointments
- Admin dashboard with booking summaries and recent activity
- Booking form with validation for future dates and phone numbers
- Booking cancellation flow
- WhatsApp confirmation link for each appointment
- Responsive Bootstrap-style frontend for desktop and mobile

## Tech stack

- Django 6.1.1
- PostgreSQL-ready configuration for production
- WhiteNoise for static files in production
- Gunicorn for Render deployment
- dj-database-url and psycopg2-binary for database configuration

## Local development

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy the sample environment file and update the values locally:
   ```bash
   copy .env.example .env
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the app:
   ```bash
   python manage.py runserver
   ```

## Production environment variables

Create these values in your Render dashboard or local `.env` file:

```bash
DEBUG=False
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
ALLOWED_HOSTS=your-app.onrender.com,localhost,127.0.0.1
DATABASE_URL=postgres://user:password@host:5432/database_name
```

Do not commit `.env` or any real secret values to GitHub.

## Deploying to Render

1. Push this project to a GitHub repository.
2. In Render, create a new Web Service and connect the GitHub repo.
3. Set the build command to:
   ```bash
   bash build.sh
   ```
4. Set the start command to:
   ```bash
   gunicorn shamse.wsgi:application --bind 0.0.0.0:$PORT
   ```
5. Add these environment variables in the Render dashboard:
   - `DJANGO_SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app.onrender.com`
   - `DATABASE_URL` from the PostgreSQL database created in Render
6. Create a PostgreSQL database in Render and link it to the web service.
7. Deploy the service.

## Render PostgreSQL setup

On Render, create a PostgreSQL database and then copy its connection string into `DATABASE_URL` in the Web Service environment variables.

Example:

```bash
DATABASE_URL=postgres://username:password@host:5432/dbname
```

## Files used for deployment

- `Procfile` starts the app with Gunicorn
- `build.sh` installs dependencies and runs `collectstatic`
- `requirements.txt` includes Django, Gunicorn, WhiteNoise, PostgreSQL client and related production packages
- `.gitignore` excludes local virtual environments, caches, secrets, and the SQLite database

## GitHub upload checklist

- Keep `venv/` and your local `db.sqlite3` off GitHub
- Never upload `.env` files or real credentials
- Commit the code, not local secrets
- Push to GitHub and deploy from the repository in Render

## Admin account

After deployment, create a superuser with:

```bash
python manage.py createsuperuser
```

Then visit `/admin/` and log in to manage services and bookings.
