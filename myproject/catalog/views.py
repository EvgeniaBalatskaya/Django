from django.views.generic import ListView, DetailView, CreateView, FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'  # чтобы совпадало с тем, что в шаблоне
    paginate_by = 3

class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('contacts')  # чтобы обновить страницу после отправки

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

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})

