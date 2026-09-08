import re

from django.db.models import Case, IntegerField, Q, When

from .models import Product


SEARCH_SYNONYMS = {
    "mobile": ("phone", "smartphone"),
    "cellphone": ("phone", "smartphone"),
    "phone": ("mobile", "smartphone"),
    "earbuds": ("headphones", "wireless"),
    "headphones": ("headphone", "earbuds"),
    "charger": ("charging", "adapter"),
    "charging": ("charger", "adapter"),
    "laptop": ("notebook", "computer"),
    "gaming": ("gamer",),
    "wireless": ("bluetooth", "cordless"),
    "audio": ("sound", "music"),
    "tv": ("television",),
}

INTENT_WORDS = {
    "a",
    "an",
    "and",
    "for",
    "in",
    "of",
    "the",
    "with",
}

PRICE_INTENTS = {
    "cheap": "low",
    "budget": "low",
    "affordable": "low",
    "expensive": "high",
    "premium": "high",
}


def _tokens(query):
    return [
        token
        for token in re.findall(r"[a-z0-9]+", query.lower())
        if token not in INTENT_WORDS and len(token) > 1
    ]


def _expanded_tokens(tokens):
    expanded = set(tokens)
    for token in tokens:
        expanded.update(SEARCH_SYNONYMS.get(token, ()))
    return sorted(expanded)


def search_products(query):
    """Return products matching query terms, ranked for a SQLite database."""
    normalized_query = " ".join(query.lower().split())
    tokens = _tokens(normalized_query)
    expanded_tokens = _expanded_tokens(tokens)

    products = Product.objects.select_related("category")
    if not expanded_tokens:
        return products

    matches = Q()
    for token in expanded_tokens:
        matches |= (
            Q(name__icontains=token)
            | Q(description__icontains=token)
            | Q(category__name__icontains=token)
        )

    relevance = Case(
        When(name__iexact=normalized_query, then=1000),
        When(name__icontains=normalized_query, then=700),
        default=0,
        output_field=IntegerField(),
    )

    for token in tokens:
        relevance += Case(
            When(name__icontains=token, then=100),
            When(category__name__icontains=token, then=55),
            When(description__icontains=token, then=30),
            default=0,
            output_field=IntegerField(),
        )

    for token in expanded_tokens:
        if token in tokens:
            continue
        relevance += Case(
            When(name__icontains=token, then=45),
            When(category__name__icontains=token, then=25),
            When(description__icontains=token, then=12),
            default=0,
            output_field=IntegerField(),
        )

    products = products.filter(matches).annotate(relevance=relevance)
    price_intents = {PRICE_INTENTS[token] for token in tokens if token in PRICE_INTENTS}
    if "low" in price_intents:
        return products.order_by("-relevance", "price", "-created_at")
    if "high" in price_intents:
        return products.order_by("-relevance", "-price", "-created_at")
    return products.order_by("-relevance", "-created_at")
