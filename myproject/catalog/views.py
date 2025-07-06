from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator


def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 3)  # 3 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/home.html', {'page_obj': page_obj})

def contacts(request):
    if request.method == 'POST':
        # обработка формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        context = {'success': True, 'name': name}
        return render(request, 'catalog/contacts.html', context)
    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

