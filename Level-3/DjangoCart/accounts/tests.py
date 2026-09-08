from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from allauth.socialaccount.models import SocialApp


class AuthenticationTests(TestCase):
    def setUp(self):
        site, _ = Site.objects.update_or_create(
            pk=settings.SITE_ID,
            defaults={"domain": "127.0.0.1:8000", "name": "DjangoCart"},
        )
        google = SocialApp.objects.create(
            provider="google",
            name="DjangoCart Google",
            client_id="test-client-id",
            secret="test-client-secret",
        )
        google.sites.add(site)
        self.user = get_user_model().objects.create_user(
            username="existing",
            email="existing@example.com",
            password="ValidPassword123!",
        )

    def test_registration_logs_user_in_and_creates_regular_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "new-user",
                "email": "new@example.com",
                "password1": "ValidPassword123!",
                "password2": "ValidPassword123!",
            },
        )

        self.assertRedirects(response, reverse("profile"))
        created = get_user_model().objects.get(username="new-user")
        self.assertTrue(created.check_password("ValidPassword123!"))
        self.assertFalse(created.is_staff)
        self.assertFalse(created.is_superuser)
        self.assertEqual(str(self.client.session["_auth_user_id"]), str(created.pk))

    def test_correct_login_redirects_home(self):
        response = self.client.post(
            reverse("login"),
            {"username": "existing", "password": "ValidPassword123!"},
        )
        self.assertRedirects(response, reverse("home"))

    def test_wrong_password_uses_normal_authentication_error(self):
        response = self.client.post(
            reverse("login"),
            {"username": "existing", "password": "WrongPassword123!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password")
        self.assertNotContains(response, "You are not registered")

    def test_unknown_username_redirects_to_registration(self):
        response = self.client.post(
            reverse("login"),
            {"username": "missing", "password": "WrongPassword123!"},
        )
        self.assertRedirects(response, reverse("register"))
        self.assertEqual(
            list(response.wsgi_request._messages)[0].message,
            "You are not registered. Please register first.",
        )

    def test_logout_ends_session(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("profile"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
        )

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_sends_email(self):
        response = self.client.post(
            reverse("password_reset"),
            {"email": "existing@example.com"},
        )
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("password-reset-confirm", mail.outbox[0].body)
