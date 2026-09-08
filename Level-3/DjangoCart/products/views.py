from django.shortcuts import get_object_or_404, render

from .models import Product
from .search import search_products


def product_list(request):
    query = request.GET.get("q", "").strip()
    products = search_products(query) if query else Product.objects.select_related("category").all()

    return render(
        request,
        "products/product_list.html",
        {"products": products, "query": query},
    )


def product_detail(request, product_id):
	product = get_object_or_404(
		Product.objects.select_related("category"),
		pk=product_id,
	)
	return render(request, "products/product_detail.html", {"product": product})
