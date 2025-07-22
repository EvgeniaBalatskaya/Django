from django.contrib import admin
from .models import BlogPost
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')

    def save_model(self, request, obj, form, change):
        # Если создаём новый объект и автор не указан — ставим текущего пользователя
        if not change and not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)