from django.shortcuts import render
from .models import Product

def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    print(latest_products)  # временно вывод в консоль
    return render(request, 'catalog/home.html', {'latest_products': latest_products})

def contacts(request):
    if request.method == 'POST':
        # обработка формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        context = {'success': True, 'name': name}
        return render(request, 'catalog/contacts.html', context)
    return render(request, 'catalog/contacts.html')
