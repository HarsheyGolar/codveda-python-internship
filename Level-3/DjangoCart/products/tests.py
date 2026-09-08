from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class ProductCatalogTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Audio")
        self.product = Product.objects.create(
            category=category,
            name="Wireless Headphones",
            description="Noise cancelling headphones",
            price="99.99",
            stock=4,
            image="products/Gaming_Headset.jpg",
        )

    def test_product_listing_uses_static_image_path(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/static/products/Gaming_Headset")

    def test_product_detail_uses_static_image_path(self):
        response = self.client.get(
            reverse("product_detail", args=[self.product.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/static/products/Gaming_Headset")

    def test_search_matches_name_description_and_category(self):
        response = self.client.get(reverse("product_list"), {"q": "headphones"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
