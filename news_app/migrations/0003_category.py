# Generated by Django 5.1.4 on 2025-01-23 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0002_author_alter_post_content_alter_post_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('politics', 'Политика'), ('economy', 'Экономика'), ('sport', 'Спорт')], max_length=100, verbose_name='Категория')),
            ],
        ),
    ]
