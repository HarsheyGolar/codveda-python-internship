import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.sites.models import Site

from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = "Initialize the deployment Site, Google OAuth app, and optional admin."

    @transaction.atomic
    def handle(self, *args, **options):
        site = self._configure_site()
        self._configure_google(site)
        self._configure_superuser()
        self.stdout.write(self.style.SUCCESS("Production initialization complete."))

    def _configure_site(self):
        domain = (
            os.getenv("DJANGO_SITE_DOMAIN")
            or os.getenv("RENDER_EXTERNAL_HOSTNAME")
            or ("127.0.0.1:8000" if settings.DEBUG else "djangocart-1iro.onrender.com")
        ).strip().removesuffix("/")

        site, _ = Site.objects.update_or_create(
            pk=settings.SITE_ID,
            defaults={"domain": domain, "name": "DjangoCart"},
        )
        Site.objects.filter(domain=domain).exclude(pk=site.pk).delete()
        self.stdout.write(f"Configured Site domain: {domain}")
        return site

    def _configure_google(self, site):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        apps = list(SocialApp.objects.filter(provider="google").order_by("pk"))

        if not client_id or not client_secret:
            self.stdout.write(
                self.style.WARNING(
                    "Google OAuth was not initialized because credentials are not configured."
                )
            )
            return

        app = apps[0] if apps else SocialApp(provider="google")
        app.name = "DjangoCart Google"
        app.client_id = client_id
        app.secret = client_secret
        app.save()
        app.sites.set([site])
        SocialApp.objects.filter(provider="google").exclude(pk=app.pk).delete()
        self.stdout.write(self.style.SUCCESS("Configured one Google OAuth app."))

    def _configure_superuser(self):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not all((username, email, password)):
            self.stdout.write("Admin bootstrap skipped because credentials are not configured.")
            return

        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        changed = False
        if not user.is_staff:
            user.is_staff = True
            changed = True
        if not user.is_superuser:
            user.is_superuser = True
            changed = True
        if created:
            user.set_password(password)
            changed = True
        if changed:
            user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Admin bootstrap {'created' if created else 'verified'} for {username}."
            )
        )
