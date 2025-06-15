from django.shortcuts import render
from django.http import HttpResponse

def example_view(request):
    return render(request, 'app/example.html')


def show_data(request):
    if request.method == 'GET':
        return render(request, 'app/data.html')


def submit_data(request):
    if request.method == 'POST':
        # Обработка данных формы
        return HttpResponse("Данные отправлены!")


def show_item(request, item_id):
    # Логика для обработки данных элемента с указанным ID
    return render(request, 'app/item.html', {'item_id': item_id})

def about(request):
    return render(request, 'catalog/home.html')