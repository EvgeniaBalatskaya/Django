from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import AuthForm
from blog.models import BlogPost
from catalog.models import Product, Category
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login
import logging
logger = logging.getLogger(__name__)
User = get_user_model()


def get_user_profile_context(user):
    products = Product.objects.filter(author=user).select_related('category').order_by('category__name', 'name')
    categories = Category.objects.all().order_by('name')

    products_by_category = {category: [] for category in categories}

    for product in products:
        products_by_category[product.category].append(product)

    return {
        'user': user,
        'products_by_category': products_by_category,
        'product_count': products.count(),
        'article_count': BlogPost.objects.filter(author=user).count(),
        'blog_posts': BlogPost.objects.filter(author=user, is_published=True).order_by('-created_at'),
        'MEDIA_URL': settings.MEDIA_URL,
    }

class AuthCreateView(CreateView):
    form_class = AuthForm
    template_name = 'authentication/auth_create.html'

    def form_valid(self, form):
        response = super().form_valid(form)  # сохраняет пользователя
        user = self.object  # только что созданный пользователь
        login(self.request, user)  # логиним пользователя
        self.send_welcome_email(user.email)  # отправляем письмо
        return response

    def get_success_url(self):
        return reverse('authentication:auth_detail', kwargs={'pk': self.object.pk})

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо, что зарегистрировались в нашем сервисе!'
        recipient_list = [user_email]
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
        except Exception as e:
            logger.error(f"Ошибка отправки письма: {e}")


class AuthDetailView(DetailView):
    model = CustomUser
    template_name = 'authentication/auth_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_profile_context(self.object))
        return context


@login_required
def profile_view(request):
    context = get_user_profile_context(request.user)
    return render(request, 'authentication/auth_detail.html', context)


@login_required
def profile_edit_photo(request):
    if request.method == "POST":
        photo = request.FILES.get('photo')
        if photo and photo.content_type.startswith('image/'):
            request.user.avatar = photo
            request.user.save()
    return redirect('authentication:auth_detail', pk=request.user.pk)


