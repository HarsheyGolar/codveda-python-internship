from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.shortcuts import render

from products.models import Product


def index(request):
    products = Product.objects.select_related("category").all()[:8]
    return render(request, "home.html", {"products": products})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index,name = "home"),

    path("accounts/", include("accounts.urls")),
    path("social/", include("allauth.urls")),
    path("products/", include("products.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)