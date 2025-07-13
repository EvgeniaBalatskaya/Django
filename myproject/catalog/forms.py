from django import forms
from .models import Product, Category

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
    'бесплатно', 'обман', 'полиция', 'радар'
]

class ProductForm(forms.ModelForm):
    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        empty_label='Выберите категорию',
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    image = forms.ImageField(
        label='Изображение',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'category':
                field.widget.attrs['class'] = 'form-control'

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category is None:
            raise forms.ValidationError('Пожалуйста, выберите категорию.')
        return category

    def clean_name(self):
        name = self.cleaned_data['name']
        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(f'Слово "{word}" запрещено использовать в названии.')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        description_lower = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in description_lower:
                raise forms.ValidationError(f'Слово "{word}" запрещено использовать в описании.')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price
