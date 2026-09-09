# 🛒 DjangoCart

<div align="center">

### A Production-Oriented Django E-Commerce Catalog & Authentication Platform

**CodVeda Technologies · Python Development Internship · Level 3**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1.1-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=111111)](https://render.com/)

**Catalog · Search · Authentication · Google OAuth · Password Reset · Testing · Deployment**

[🚀 Live Demo](https://djangocart-1iro.onrender.com)

</div>

---

## 📖 Overview

**DjangoCart** is a Django-based e-commerce storefront and product-catalog application developed as part of the **CodVeda Python Development Internship — Level 3**.

The project combines a structured Django backend with a server-rendered storefront, product/category models, ORM-powered search, username/password authentication, Google OAuth, password reset, Django administration, environment-driven configuration, local SQLite support, production PostgreSQL support, WhiteNoise, Gunicorn, automated tests, and Render deployment configuration.

The repository also deliberately distinguishes implemented functionality from future work. The `cart` and `orders` applications contain scaffolding/templates, but the current project does **not** claim a complete persistent checkout, payment, or order-management system.

---

## ✨ Feature Matrix

| Feature | Status | Notes |
|---|:---:|---|
| Product catalog | ✅ | Category + product models |
| Product detail | ✅ | Individual product pages |
| Product images | ✅ | Static catalog asset strategy |
| Product search | ✅ | Django ORM search |
| Synonym expansion | ✅ | Related terms are expanded |
| Relevance ranking | ✅ | Weighted database expressions |
| Price intent | ✅ | Cheap/budget/premium style intent |
| Registration | ✅ | Django form-based |
| Login | ✅ | Django authentication |
| Logout | ✅ | CSRF-protected POST |
| Protected profile | ✅ | `login_required` |
| Google OAuth | ✅ | `django-allauth` |
| Password reset | ✅ | Django + SMTP |
| Django admin | ✅ | Standard admin |
| SQLite local DB | ✅ | Automatic fallback |
| PostgreSQL production DB | ✅ | `DATABASE_URL` |
| WhiteNoise | ✅ | Production static files |
| Gunicorn | ✅ | Production server |
| Render deployment | ✅ | `render.yaml` + build script |
| Automated tests | ✅ | Authentication/product/search coverage |
| Persistent cart | 🟡 | Scaffolding exists; full workflow not wired |
| Persistent orders | 🟡 | Scaffolding exists; checkout not implemented |
| Payments | ❌ | Not implemented |
| Durable media storage | ❌ | Future infrastructure |

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │       Browser        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Django URLs      │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
          ┌────────────┐     ┌────────────┐     ┌────────────┐
          │  Accounts  │     │  Products  │     │   Admin    │
          └─────┬──────┘     └─────┬──────┘     └────────────┘
                │                  │
                │                  ▼
                │          ┌──────────────┐
                │          │ Django ORM   │
                │          └──────┬───────┘
                │                 │
                └──────────┬──────┘
                           ▼
                 ┌─────────────────────┐
                 │ SQLite / PostgreSQL │
                 └─────────────────────┘

        External integrations
             ┌───────┴────────┐
             ▼                ▼
        Google OAuth       Gmail SMTP
```

Production deployment:

```text
GitHub
  │
  ▼
Render
  ├── Python 3.12.10
  ├── Django
  ├── Gunicorn
  ├── WhiteNoise
  └── PostgreSQL
```

---

## 🧰 Technology Stack

### Backend

- Python 3.12.10
- Django 6.1.1
- django-allauth
- Django ORM
- Django authentication
- Django Sites framework

### Database

- SQLite for local development
- PostgreSQL for Render production

### Authentication

- Django authentication framework
- `AuthenticationForm`
- `django-allauth`
- Google OAuth
- Django password-reset framework

### Deployment

- Render
- Gunicorn
- WhiteNoise
- `dj-database-url`

### Frontend

- Django Templates
- HTML
- CSS
- JavaScript

### Supporting packages

The repository pins packages including:

```text
Django==6.1.1
django-allauth==65.19.2
dj-database-url==3.1.2
gunicorn==26.2.0
Pillow==12.3.0
psycopg2-binary==2.9.12
python-dotenv==1.2.3
whitenoise==6.12.0
```

See `requirements.txt` for the complete dependency set.

---

## 📁 Project Structure

```text
codveda-python-internship/
└── Level-3/
    └── DjangoCart/
        ├── manage.py
        ├── build.sh
        ├── render.yaml
        ├── requirements.txt
        ├── .python-version
        ├── .gitignore
        │
        ├── djangocart/
        │   ├── settings.py
        │   ├── urls.py
        │   ├── asgi.py
        │   └── wsgi.py
        │
        ├── accounts/
        │   ├── forms.py
        │   ├── views.py
        │   ├── context_processors.py
        │   ├── tests.py
        │   ├── management/
        │   │   └── commands/
        │   │       └── initialize_production.py
        │   └── templates/accounts/
        │
        ├── products/
        │   ├── models.py
        │   ├── views.py
        │   ├── search.py
        │   ├── admin.py
        │   ├── tests.py
        │   ├── migrations/
        │   └── templates/products/
        │
        ├── cart/
        │   └── templates/cart/
        │
        ├── orders/
        │   └── templates/
        │
        ├── templates/
        ├── static/
        └── media/
```

---

# 🛍️ Product Catalog

The catalog is backed by two primary models.

### Category

```text
name
description
```

### Product

```text
category
name
description
price
stock
image
created_at
```

Products have a foreign-key relationship to categories and use `select_related("category")` in catalog/detail queries.

The price is represented with Django's `DecimalField`, providing an appropriate database representation for monetary values.

Products are ordered newest-first through model metadata.

---

# 🔎 Search Engine

One of DjangoCart's strongest backend features is its lightweight relevance-aware search implementation.

It is intentionally **not presented as vector search or AI search**. It is an ORM-based search engine using:

```text
Keyword tokenization
        +
Stop/intent-word filtering
        +
Synonym expansion
        +
Database filtering
        +
Weighted relevance
        +
Price intent
        =
Ranked QuerySet
```

## Search fields

Queries can match against:

- product name,
- product description,
- category name.

Example:

```text
/products/?q=headphones
```

## Synonym expansion

The search module contains mappings such as:

```text
mobile     → phone, smartphone
cellphone  → phone, smartphone
phone      → mobile, smartphone
earbuds    → headphones, wireless
charger    → charging, adapter
laptop     → notebook, computer
gaming     → gamer
wireless   → bluetooth, cordless
audio      → sound, music
tv         → television
```

This gives the catalog more useful matching than a simple exact-string lookup.

## Relevance scoring

The search gives stronger weights to:

1. exact name matches,
2. partial name matches,
3. name token matches,
4. category matches,
5. description matches,
6. synonym-derived matches.

The implementation uses Django `Case`, `When`, `Q`, annotations and ordered QuerySets.

## Price intent

The search also understands price-oriented words:

```text
cheap
budget
affordable
expensive
premium
```

Low-price intent can order matching results by lower price, while high-price intent can prioritize higher-priced products.

This is a deliberately lightweight approach that remains database-oriented and easy to understand.

---

# 🔐 Authentication

DjangoCart uses Django's authentication framework rather than implementing password handling from scratch.

## Registration

The flow is:

```text
Registration Form
       ↓
Validation
       ↓
Create User
       ↓
Hash Password
       ↓
Ensure Regular User
       ↓
Login
       ↓
Profile
```

The test suite verifies that a newly registered user:

- is created successfully,
- has a valid hashed password,
- is not staff,
- is not a superuser,
- is logged in after registration.

## Login

The login implementation uses Django's `AuthenticationForm`.

The project differentiates between:

- an unknown username → registration prompt,
- an existing username with a wrong password → normal Django authentication error.

## Logout

Logout is performed through Django's authentication system and is tested to ensure the session is ended.

## Profile

The profile is protected using:

```python
@login_required
```

Unauthenticated users are redirected to the login page.

---

# 🔵 Google OAuth

Google authentication is integrated through:

```text
django-allauth
```

Credentials are environment-driven:

```dotenv
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

The project includes an idempotent production initialization command that configures the Google SocialApp and associates it with the configured Django Site.

Secrets are not printed by the initializer.

---

# 📧 Password Reset

DjangoCart uses Django's built-in password reset functionality.

SMTP settings are environment-driven:

```dotenv
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=
```

The test suite overrides the email backend with Django's in-memory backend and verifies that a reset email is generated.

---

# 👥 Roles & Permissions

DjangoCart uses Django's standard user roles.

### Regular User

Can browse the catalog, search, authenticate and access their profile.

### Staff

Can access Django administration according to assigned permissions.

### Superuser

Has full Django admin permissions.

The deployment initializer can create a configured superuser from environment variables without replacing an existing user's password.

---

# 🗄️ Database Strategy

DjangoCart is environment-aware.

## Local

If `DATABASE_URL` is unavailable:

```text
SQLite
```

is used.

## Production

When `DATABASE_URL` is available:

```text
PostgreSQL
```

is configured through:

```text
dj-database-url
```

This keeps local setup lightweight while allowing the deployed application to use a production relational database.

---

# 🖼️ Static & Media Architecture

Static and media assets are intentionally treated differently.

### Static

```text
STATIC_URL   = /static/
STATIC_ROOT  = staticfiles/
```

The project uses WhiteNoise's compressed manifest storage for production static files.

### Product assets

Existing catalog images are stored under the project's static product assets so they remain available after deployment.

### Media

Django's media configuration remains available for local development.

For a production marketplace with user-uploaded files, durable object storage would be a better long-term solution because Render's application filesystem is not intended to be permanent user-media storage.

---

# 🛡️ Security

Security-related configuration includes:

- Django password hashing,
- CSRF middleware,
- protected authentication flows,
- environment-based secrets,
- production `DEBUG=False`,
- configured `ALLOWED_HOSTS`,
- configured `CSRF_TRUSTED_ORIGINS`,
- separate authentication backends,
- credentials kept outside source code.

Sensitive values should always be supplied through environment variables.

Never commit:

```text
SECRET_KEY
DATABASE_URL
GOOGLE_CLIENT_SECRET
EMAIL_HOST_PASSWORD
DJANGO_SUPERUSER_PASSWORD
```

---

# ⚙️ Environment Variables

Example local configuration:

```dotenv
SECRET_KEY=your-secret
DEBUG=True

DATABASE_URL=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=

DJANGO_SITE_DOMAIN=127.0.0.1:8000

DJANGO_SUPERUSER_USERNAME=
DJANGO_SUPERUSER_EMAIL=
DJANGO_SUPERUSER_PASSWORD=
```

Use real credentials only in your local environment or deployment secret store.

---

# 💻 Local Development

From the project directory:

```powershell
cd Level-3\DjangoCart
```

Create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

Install:

```powershell
pip install -r requirements.txt
```

Apply migrations:

```powershell
python manage.py migrate
```

Initialize deployment-related Django data:

```powershell
python manage.py initialize_production
```

Run the server:

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🧪 Testing

Run:

```powershell
python manage.py test
```

Recommended validation:

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --no-input
```

## Authentication coverage

Tests cover:

- registration,
- password hashing,
- regular-user privileges,
- automatic login,
- successful login,
- wrong-password behavior,
- unknown-user behavior,
- logout,
- protected profile access,
- password-reset email generation.

## Product coverage

The product tests cover catalog/detail behavior, image/static URL handling and search-related behavior.

This is important because the project is not solely dependent on manual browser testing.

---

# 🚀 Render Deployment

The repository contains Render configuration through:

```text
render.yaml
build.sh
```

The configured service uses:

```text
Root directory:
Level-3/DjangoCart
```

Production startup:

```text
gunicorn djangocart.wsgi:application
```

The deployment configuration includes:

- Python 3.12.10,
- generated production secret,
- `DEBUG=False`,
- PostgreSQL,
- Google OAuth environment variables,
- Gmail SMTP environment variables,
- Django Site domain,
- optional superuser bootstrap variables.

The database is provisioned as PostgreSQL.

---

# 🔄 Production Initialization

The custom management command:

```text
accounts/management/commands/initialize_production.py
```

exists to make production bootstrap repeatable.

It can configure deployment-specific:

- Django Site information,
- Google OAuth SocialApp,
- superuser initialization.

The command is designed to be safe to run repeatedly and does not expose credentials in its output.

---

# 🧭 Request Flows

## Catalog

```text
Browser
  ↓
Django URL
  ↓
product_list()
  ↓
Product QuerySet
  ↓
Template
  ↓
HTML
```

## Search

```text
GET /products/?q=headphones
             ↓
       Normalize query
             ↓
          Tokenize
             ↓
     Expand synonyms
             ↓
      Build Q filters
             ↓
    Calculate relevance
             ↓
      Price intent
             ↓
       Ranked results
```

## Registration

```text
POST registration
        ↓
Validate
        ↓
Create user
        ↓
Hash password
        ↓
Login
        ↓
Profile
```

## Login

```text
POST credentials
       ↓
AuthenticationForm
       ↓
 ┌─────┴─────┐
 │           │
Valid       Invalid
 │           │
 ▼           ▼
Home       Error
```

## Password reset

```text
Email address
     ↓
Django password-reset view
     ↓
Generate token
     ↓
SMTP email
     ↓
Reset link
```

---

# 🧠 Important Design Decisions

### Django ORM instead of raw SQL

The relational nature of products/categories makes the ORM a natural fit and keeps queries portable.

### `select_related()`

Product views use related-object loading where appropriate to reduce unnecessary database queries.

### SQLite + PostgreSQL

SQLite keeps local development simple while PostgreSQL provides the production database target.

### Environment-driven configuration

Deployment credentials and infrastructure settings should not be coupled to source code.

### WhiteNoise

WhiteNoise provides a practical static-file serving strategy for the Render deployment.

### Lightweight search

The search implementation intentionally remains understandable and database-oriented instead of introducing an external search engine for a project of this scope.

---

# 🛒 Cart & Orders Scope

The repository contains dedicated:

```text
cart/
orders/
```

applications and presentation templates.

However, the current implementation does **not** expose a complete persistent shopping-cart and checkout workflow.

Therefore this README does not falsely describe:

- persistent cart storage,
- checkout,
- payment processing,
- order persistence,
- order history,

as completed features.

They are natural next steps for the application.

---

# ⚠️ Current Limitations

### Persistent cart

Not currently implemented as a complete database-backed workflow.

### Checkout

No complete checkout pipeline exists at the current scope.

### Payments

No payment gateway is integrated.

### Orders

No complete persistent order lifecycle is currently implemented.

### Search

Search is relevance-aware keyword matching, not semantic/vector search.

### Media

Durable production media storage is not included.

### Scale

The current catalog is appropriate for an internship/demo application rather than a high-scale marketplace.

---

# 🗺️ Roadmap

## Phase 1 — Commerce Core

- [ ] Persistent cart
- [ ] Cart quantity management
- [ ] Stock validation
- [ ] Checkout
- [ ] Order creation
- [ ] Order history

## Phase 2 — Payments

- [ ] Payment gateway
- [ ] Payment model
- [ ] Webhook verification
- [ ] Failed-payment handling
- [ ] Refund workflow

## Phase 3 — Customer Experience

- [ ] Wishlist
- [ ] Reviews
- [ ] Ratings
- [ ] Saved addresses
- [ ] Customer order dashboard

## Phase 4 — Search

- [ ] PostgreSQL full-text search
- [ ] Typo tolerance
- [ ] Search analytics
- [ ] Faceted filtering
- [ ] Optional semantic/vector search

## Phase 5 — Infrastructure

- [ ] Object storage
- [ ] Background tasks
- [ ] Caching
- [ ] Rate limiting
- [ ] Observability
- [ ] CI/CD

---

# 🎓 What This Project Demonstrates

DjangoCart demonstrates practical experience with:

### Django

- Project/app architecture
- URL routing
- Views
- Templates
- Forms
- ORM
- Migrations
- Management commands
- Authentication
- Admin

### Backend Engineering

- Relational modeling
- Query optimization
- Relevance scoring
- Search normalization
- Environment configuration
- Error-aware authentication flows

### Security

- Password hashing
- CSRF protection
- Secret management
- Host/origin configuration
- Production debug configuration

### Deployment

- Render
- Gunicorn
- PostgreSQL
- WhiteNoise
- Production initialization

### Testing

- Django `TestCase`
- Authentication tests
- Redirect assertions
- Permission assertions
- Email backend overrides
- Product/search testing

---

# 🎓 CodVeda Internship Context

**DjangoCart** was developed as part of the:

> **CodVeda Technologies — Python Development Internship**

### Level 3

The project represents a move from standalone Python scripting toward structured web-application engineering.

The overall stack can be summarized as:

```text
Python
  +
Django
  +
ORM
  +
Authentication
  +
Database
  +
Search
  +
Testing
  +
Deployment
```

---

# 🌍 Live Demo

**DjangoCart:**  
https://djangocart-1iro.onrender.com

> Render free-tier services may sleep when inactive, so an initial request after inactivity may take longer.

---

# 🧰 Useful Commands

```powershell
# Django health check
python manage.py check

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic --no-input

# Initialize production configuration
python manage.py initialize_production
```

---

# 🤝 Contribution Workflow

A sensible extension workflow is:

```text
Fork
  ↓
Feature branch
  ↓
Implement feature
  ↓
Add tests
  ↓
python manage.py check
  ↓
python manage.py test
  ↓
Pull Request
```

For major features, tests should be developed alongside implementation.

---

# 📜 License

No separate license file is documented for the project scope covered here.

If the project is intended for public reuse or redistribution, add an explicit open-source license.

---

<div align="center">

# 👤 Harshey Golar

**Python Developer · AI/ML Enthusiast · Backend & Web Engineering**

[![GitHub](https://img.shields.io/badge/GitHub-HarsheyGolar-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/HarsheyGolar)

<br>

```text
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│              DJANGOCART · DJANGO · PYTHON                    │
│                                                              │
│      Catalog • Search • Authentication • OAuth               │
│          Testing • Security • Deployment                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Built with Python & Django during the CodVeda Python Development Internship.**

<sub>Designed as a maintainable internship project with a clear path toward a complete e-commerce platform.</sub>

<br><br>

⭐ **If this project helped you, consider starring the repository.**

</div>
