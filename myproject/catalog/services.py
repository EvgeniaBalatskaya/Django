from django.core.cache import cache
from .models import Product

def get_products_by_category(category_id):
    cache_key = f'products_in_category_{category_id}'
    products = cache.get(cache_key)

    if products is None:
        print(f"Cache miss for category {category_id} — делаем запрос в БД")
        products = Product.objects.filter(
            category_id=category_id,
            is_published=True
        ).select_related('category')
        cache.set(cache_key, products, 60 * 15)  # кэш на 15 минут
    else:
        print(f"Cache hit for category {category_id} — берем из кэша")

    return products
