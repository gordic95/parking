from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='Пользователь')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'



class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория', null=True, blank=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, verbose_name='Автор', null=True, blank=True)




    def __str__(self):
        return f'{self.title} {self.created_at}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Category(models.Model):
    cat = [
        ('Политика', 'Политика'),
        ('Экономика', 'Экономика'),
        ('Спорт', 'Спорт'),
    ]
    name = models.CharField(max_length=100, verbose_name='Категория', choices=cat)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
