from django.db import models
from ckeditor.fields import RichTextField


class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = RichTextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='blog_previews/', verbose_name='Изображение',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:blog_detail', kwargs={'pk': self.pk})