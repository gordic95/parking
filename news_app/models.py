from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    def __str__(self):
        return f'{self.title} {self.created_at}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
