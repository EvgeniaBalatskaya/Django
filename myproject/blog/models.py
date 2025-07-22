from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings

class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = RichTextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='blog_previews/', verbose_name='Изображение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='blog_posts',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:blog_detail', kwargs={'pk': self.pk})

    def short_content(self):
        return self.content[:100] + '...'
