from django import forms
from .models import BlogPost
from .utils import resize_image
from ckeditor.widgets import CKEditorWidget



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
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10
        })
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
        return self.cleaned_data['title']

    def clean_content(self):
        content = self.cleaned_data.get('content', '').lower()
        for word in FORBIDDEN_WORDS:
            if word in content:
                raise forms.ValidationError(f'Слово "{word}" запрещено использовать в содержимом статьи.')
        return self.cleaned_data['content']

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('preview'):
            instance.preview = resize_image(self.cleaned_data['preview'])

        instance.is_published = True
        if commit:
            instance.save()
        return instance

