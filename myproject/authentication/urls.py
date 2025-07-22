from django.urls import path
from .views import AuthCreateView, AuthDetailView, profile_edit_photo
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'authentication'

urlpatterns = [
    path("login/", LoginView.as_view(template_name='authentication/auth_login.html'), name="auth_login"),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('create/', AuthCreateView.as_view(), name='auth_create'),
    path('<int:pk>/', AuthDetailView.as_view(), name='auth_detail'),
    path('edit_photo/', profile_edit_photo, name='profile_edit_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
