from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import BlogPost
from .utils import resize_image

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
    'бесплатно', 'обман', 'полиция', 'радар'
]

class BlogForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        label='Описание',
        widget=CKEditorWidget()
    )
    preview = forms.ImageField(
        label='Изображение',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview']
        labels = {
            'title': 'Заголовок',
            'content': 'Описание',
            'preview': 'Изображение',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in title:
                raise forms.ValidationError(f'Слово "{word}" запрещено использовать в заголовке.')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in content:
                raise forms.ValidationError(f'Слово "{word}" запрещено использовать в содержимом статьи.')
        return content

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('preview'):
            instance.preview = resize_image(self.cleaned_data['preview'])

        instance.is_published = True
        if commit:
            instance.save()
        return instance
