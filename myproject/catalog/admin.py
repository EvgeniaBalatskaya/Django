from django.contrib import admin
from .models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'author', 'is_published')
    list_filter = ('category', 'author', 'is_published')
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'price', 'category', 'author', 'is_published')

    actions = ['publish_products', 'unpublish_products']

    def publish_products(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} продукт(ов) опубликовано.")
    publish_products.short_description = "Опубликовать выбранные продукты"

    def unpublish_products(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} продукт(ов) снято с публикации.")
    unpublish_products.short_description = "Снять с публикации выбранные продукты"

    def save_model(self, request, obj, form, change):
        if not change and not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)