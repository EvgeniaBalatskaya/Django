from django.contrib import admin
from .models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'author')
    list_filter = ('category', 'author')
    search_fields = ('name', 'description')
    fields = ('name', 'description', 'price', 'category', 'author')

    def save_model(self, request, obj, form, change):
        if not change and not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)
