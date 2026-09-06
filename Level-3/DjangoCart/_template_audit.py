import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangocart.settings")
django.setup()

from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.template.loader import get_template
from django.test import RequestFactory

from accounts.forms import RegisterForm
from products.models import Product

rf = RequestFactory()
req = rf.get("/")
req.user = AnonymousUser()
setattr(req, "session", {})
req._messages = FallbackStorage(req)


def render(name, ctx=None):
    html = get_template(name).render(ctx or {}, req)
    navs = html.count('<nav class="bg-white/90')
    foots = html.count('<footer class="bg-gray-900')
    docs = html.count("<!DOCTYPE html>")
    print(f"{name}: doctype={docs} navbar={navs} footer={foots} bytes={len(html)}")
    if docs != 1 or navs != 1 or foots != 1:
        raise SystemExit(f"Duplication issue in {name}")
    return html


render("home.html")
render("accounts/login.html", {"form": AuthenticationForm()})
render("accounts/register.html", {"form": RegisterForm()})
render("accounts/password_reset.html", {"form": PasswordResetForm()})
render("accounts/password_reset_done.html")
render(
    "accounts/password_reset_confirm.html",
    {"validlink": False, "form": None},
)
render("accounts/password_reset_complete.html")
render(
    "products/product_list.html",
    {"products": Product.objects.select_related("category").all()[:8], "query": ""},
)
product = Product.objects.select_related("category").first()
if product:
    render("products/product_detail.html", {"product": product})
render("products/product_search.html", {"products": [], "query": "test"})
render("cart/cart.html")
render("orders/checkout.html")
render("orders/order_success.html")
render("orders/order_list.html")
render("orders/order_details.html")
render("registration/logged_out.html")

req.user = User(username="demo", email="a@b.c")
render("accounts/profile.html", {"user": req.user})
print("OK")
