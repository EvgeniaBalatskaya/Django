from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Персональные данные'), {'fields': ('first_name', 'last_name', 'avatar', 'phone', 'country')}),
        (_('Права доступа'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('id',)  # если нужно показать id в форме

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
