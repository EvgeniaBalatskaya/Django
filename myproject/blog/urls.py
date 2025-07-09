from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),                # список
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),   # просмотр записи
    path('create/', BlogCreateView.as_view(), name='blog_create'),     # создание
    path('<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_update'),   # редактирование
    path('<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'), # удаление
]
