from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from django.conf import settings

from .models import BlogPost
from .forms import BlogForm  # <--- подключаем кастомную форму


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'object_list'
    paginate_by = 5

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        if obj.views_count == 100:
            send_mail(
                subject='Поздравляем!',
                message=f'Статья "{obj.title}" набрала 100 просмотров!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['evgeniabalackaa6@gmail.com'],
            )
        return obj


class BlogCreateView(CreateView):
    model = BlogPost
    form_class = BlogForm  # <-- используем кастомную форму
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogForm  # <-- используем кастомную форму
    template_name = 'blog/blog_update.html'
    success_url = reverse_lazy('blog:blog_list')

    def get_success_url(self):
        return self.object.get_absolute_url()


class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
