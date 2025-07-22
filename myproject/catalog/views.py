from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from collections import OrderedDict
from django.conf import settings
from .models import Product, Category
from .forms import ProductForm
from django.shortcuts import render


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    paginate_by = 3

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MEDIA_URL'] = settings.MEDIA_URL
        return context


class ProductCreateView(CreateView):
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


class ProductUpdateView(UpdateView):
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


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')


# --- Добавляем функцию представления ---

def user_products_view(request):
    categories = Category.objects.all()
    user_products = Product.objects.filter(author=request.user)

    products_by_category = OrderedDict()

    for category in categories:
        products_in_cat = user_products.filter(category=category)
        products_by_category[category] = list(products_in_cat)

    return render(request, 'catalog/user_products.html', {
        'products_by_category': products_by_category,
        'MEDIA_URL': settings.MEDIA_URL,
    })