from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Load test data into the database'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        c1 = Category.objects.create(name='Смартфоны', description='...')
        Product.objects.create(name='Galaxy S24', description='Samsung', category=c1, price=90000)

        self.stdout.write(self.style.SUCCESS('Test data loaded successfully'))
