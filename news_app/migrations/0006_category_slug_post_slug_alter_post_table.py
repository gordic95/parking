# Generated by Django 5.1.4 on 2025-01-24 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0005_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='Слаг'),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, null=True, verbose_name='Слаг'),
        ),
        migrations.AlterModelTable(
            name='post',
            table='posts',
        ),
    ]
