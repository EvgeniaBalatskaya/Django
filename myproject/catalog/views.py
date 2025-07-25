from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from collections import OrderedDict
from django.conf import settings
from .models import Product, Category
from .forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.http import Http404
from django.http import HttpResponseForbidden
def is_moderator(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name='Модератор продуктов').exists())



class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_authenticated and (user.is_staff or is_moderator(user)):
            return qs  # показать все
        return qs.filter(is_published=True)  # только опубликованные

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context


class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('contacts')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        context = {'success': True, 'name': name}
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})



class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        print(
            f"Product is_published={obj.is_published}, user={user}, user.is_staff={user.is_staff}, is_moderator={is_moderator(user)}"
        )
        if not obj.is_published and not (user.is_authenticated and is_moderator(user)):
            raise Http404("Продукт не найден")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL

        user = self.request.user
        product = self.get_object()

        context['is_author'] = user.is_authenticated and user == product.author
        context['is_moderator'] = is_moderator(user)

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        category_id = self.request.GET.get('category')
        if category_id:
            initial['category'] = category_id
        return initial


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object
        return context

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.object.author
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.author


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return user == product.author or user.has_perm('catalog.delete_product')


def user_products_view(request):
    categories = Category.objects.all()
    user_products = Product.objects.filter(author=request.user)
    products_by_category = OrderedDict()

    for category in categories:
        products_by_category[category] = list(user_products.filter(category=category))

    return render(request, 'catalog/user_products.html', {
        'products_by_category': products_by_category,
        'MEDIA_URL': settings.MEDIA_URL,
    })


class ProductPublishView(View):
    def post(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, pk=pk)

        is_author = user == product.author
        if not (is_author or user.has_perm('catalog.can_publish_product')):
            return HttpResponseForbidden("Нет прав публиковать")

        product.is_published = True
        product.save()
        return redirect(product.get_absolute_url())

class ProductUnpublishView(View):
    def post(self, request, pk):
        user = request.user
        product = get_object_or_404(Product, pk=pk)

        is_author = user == product.author
        if not (is_author or user.has_perm('catalog.can_unpublish_product')):
            return HttpResponseForbidden("Нет прав снимать с публикации")

        product.is_published = False
        product.save()
        return redirect(product.get_absolute_url())