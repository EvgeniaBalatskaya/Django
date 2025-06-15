from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    if request.method == 'POST':
        # обработка формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        context = {'success': True, 'name': name}
        return render(request, 'catalog/contacts.html', context)
    return render(request, 'catalog/contacts.html')
