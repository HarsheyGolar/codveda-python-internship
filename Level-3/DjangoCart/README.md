# DjangoCart

## A Django e-commerce internship project with production-ready deployment basics

## Overview

DjangoCart is a Django 6.1.1 product-catalog application developed for the CodVeda internship. It provides a styled storefront, catalog search, username/password authentication, Google OAuth integration, password reset email support, and Render deployment configuration.

The project remains in its required internship location:

```text
codveda-python-internship/
└── Level-3/
    └── DjangoCart/
```

## Project Goals

- Build a maintainable Django storefront.
- Practice authentication, authorization, templates, ORM queries, and deployment.
- Support SQLite for local development and PostgreSQL on Render.
- Serve catalog images safely as committed static assets in production.
- Keep deployment configuration simple and environment-driven.

## Key Features

- Product and category catalog.
- Product detail pages with stock and price information.
- Case-insensitive keyword search with partial matching and synonym expansion.
- Relevance-aware search ordering.
- Registration with required username, email, and validated passwords.
- Username/password login and CSRF-protected logout.
- Google OAuth through django-allauth.
- Authenticated profile page.
- Gmail SMTP password reset flow.
- Django admin.
- WhiteNoise static-file serving on Render.

The `cart` and `orders` applications currently contain placeholder files/templates and are not wired into the root URL configuration. Checkout, payment, and order persistence are therefore not presented as implemented features.

## Live Demo

https://djangocart-1iro.onrender.com

## Technology Stack

- Python 3.12.10
- Django 6.1.1
- django-allauth
- Google OAuth
- PostgreSQL on Render
- SQLite locally
- Gunicorn
- WhiteNoise
- Gmail SMTP
- HTML, CSS, and JavaScript

## Architecture

```text
Browser
   ↓
Django views, templates, forms, and ORM
   ↓
SQLite locally / PostgreSQL on Render
```

Static catalog images are collected from `static/products/` and served by WhiteNoise. Django media storage remains available for local development, but Render's local filesystem is ephemeral and is not used as permanent catalog storage.

## Project Structure

```text
codveda-python-internship/
└── Level-3/
    └── DjangoCart/
        ├── manage.py
        ├── djangocart/
        ├── accounts/
        ├── products/
        ├── cart/
        ├── orders/
        ├── templates/
        ├── static/
        ├── media/
        ├── requirements.txt
        ├── render.yaml
        ├── build.sh
        └── .python-version
```

## Authentication System

Registration uses Django's `UserCreationForm`, requiring a username, email, password, and password confirmation. Passwords are hashed by Django's password hasher. Newly registered users are regular users and are logged in explicitly through Django's `ModelBackend`.

Login uses `AuthenticationForm`. Unknown usernames receive a registration prompt, while an existing username with an incorrect password receives Django's normal invalid-credentials error. Logout is a POST action protected by CSRF and redirects to the home page.

Google OAuth is provided by django-allauth. Password reset uses Django's built-in views and sends reset messages through the configured Gmail SMTP backend.

## User Roles & Permissions

- **Regular user:** Can register, sign in, view the catalog, search, and access their profile.
- **Staff:** Can access the Django admin according to assigned permissions.
- **Superuser:** Has full Django admin permissions.

The deployment initializer can create one configured superuser when bootstrap environment variables are supplied. It never replaces the password of an existing user.

## Product Management

Products belong to categories and contain a name, description, price, stock count, optional image, and creation timestamp. Product images for the existing catalog are tracked in `static/products/`. Templates convert database paths such as `products/Gaming_Headset.jpg` into static URLs such as `/static/products/Gaming_Headset.jpg`.

## Intelligent Search

Search is a lightweight Django ORM implementation, not vector search. It supports case-insensitive partial matches across product names, descriptions, and category names. Multi-word searches are tokenized, common intent words are ignored, selected synonyms are expanded, and results are ranked with stronger weights for name and category matches. Price-intent words such as “cheap” and “premium” influence ordering.

Example:

```text
/products/?q=headphones
```

## Cart & Orders

The repository includes `cart` and `orders` app placeholders and presentation templates, but these apps are not currently connected to the root URL configuration and do not contain persistence models or checkout logic. They are documented as future implementation areas rather than claimed production functionality.

## Static & Media Strategy

`STATIC_URL` is `/static/`, `STATICFILES_DIRS` points to the project `static/` directory, and `STATIC_ROOT` is `staticfiles/`. WhiteNoise uses compressed manifest storage in production.

Existing catalog images are committed under `static/products/` because Render's application filesystem is ephemeral. The Product model is unchanged and still uses `media/products/` for uploaded media during local development.

## Database Strategy

When `DATABASE_URL` is present, Django uses the Render PostgreSQL database through `dj-database-url`. Without it, local development uses SQLite from `db.sqlite3`. Migrations are applied during deployment and no production database reset is performed.

## Email / Password Reset

Password reset uses Django's built-in authentication views and Gmail SMTP. SMTP host, port, username, password, TLS, and sender address are all environment variables. Site configuration is initialized for the active deployment domain so reset links do not use `example.com`.

## Google OAuth

Google credentials are supplied through `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`. The `initialize_production` management command creates or updates one Google `SocialApp` and associates it with the configured Django Site. It is safe to run repeatedly and does not print secrets.

Local development uses `127.0.0.1:8000`; Render uses `djangocart-1iro.onrender.com`.

## Security

- Passwords are hashed by Django.
- Login, registration, and logout use CSRF protection.
- Secrets are read from environment variables.
- Production `DEBUG` is controlled by the `DEBUG` environment variable and is set to `False` in Render configuration.
- Google and SMTP credentials are never stored in source code.
- Both required authentication backends remain configured.
- `.env`, virtual environments, SQLite databases, and collected static output are ignored by Git.

## Local Development

From the project directory:

```powershell
cd Level-3\DjangoCart
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py initialize_production
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Environment Variables

Use a local `.env` file or Render environment settings. Do not commit real values.

```dotenv
SECRET_KEY=
DEBUG=False
DATABASE_URL=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=

DJANGO_SITE_DOMAIN=
DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_PASSWORD=
```

## Render Deployment

Render is configured with root directory:

```text
Level-3/DjangoCart
```

The deployment uses:

- `requirements.txt` for Python dependencies.
- `build.sh` to install dependencies, collect static files, migrate, and run idempotent production initialization.
- `render.yaml` for the web service, PostgreSQL database, root directory, environment variables, and Gunicorn command.
- `.python-version` and `PYTHON_VERSION` for Python 3.12.10.

The start command is:

```text
gunicorn djangocart.wsgi:application
```

## Deployment Troubleshooting

- **Missing dependency:** Confirm `requirements.txt` is installed from the configured Render root.
- **Wrong root directory:** Use `Level-3/DjangoCart`, not the repository root.
- **Missing static images:** Run `collectstatic` and verify files exist under `static/products/`.
- **Fresh PostgreSQL database:** Run migrations and the idempotent initializer; do not rerun a one-time product fixture.
- **Google OAuth failure:** Check Google environment variables, OAuth redirect URIs, the Site domain, and the single Google SocialApp.
- **Authentication failure:** Check `SITE_ID`, Site configuration, database migrations, and Render logs.

## Testing

The project includes focused tests for:

- Registration, hashing, regular-user permissions, and automatic login.
- Correct login, wrong-password errors, and unknown-user behavior.
- Logout and authenticated profile access.
- Password reset email generation.
- Product listing and detail image URLs.
- Search matching.

Run:

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --no-input
```

## CodVeda Internship Objectives

DjangoCart demonstrates Django project structure, models, forms, templates, authentication, database configuration, static assets, search, testing, environment-based settings, and deployment to Render with PostgreSQL.

## Limitations

- Render's free instance may spin down between requests.
- Render's local filesystem is ephemeral; uploaded media is not durable.
- The catalog is demo-scale.
- Search is lightweight ORM ranking, not vector search.
- Cart and order persistence/checkout are not currently implemented.

## Future Improvements

- Durable object storage for user-uploaded media.
- PostgreSQL full-text search.
- Optional vector search and recommendations.
- Payment processing and order tracking.
- Product reviews and wishlists.
- A complete cart and checkout workflow.

## Screenshots

No screenshots are included because no repository screenshots are currently available.

## Author

Harshey Golar
