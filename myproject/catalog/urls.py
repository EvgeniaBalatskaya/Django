from .views import (
    HomeView,
    ContactsView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductUnpublishView,
    ProductPublishView,
    CategoryProductListView,
)
from django.urls import path
from .views import user_products_view
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),  # ✅ кеширование
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('my-products/', user_products_view, name='user_products'),
    path('product/<int:pk>/publish/', ProductPublishView.as_view(), name='product_publish'),
    path('product/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path('category/<int:category_id>/', CategoryProductListView.as_view(), name='category_products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
