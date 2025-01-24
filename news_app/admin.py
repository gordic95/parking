from django.contrib import admin
from .models import Post, Author, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'author', 'category')
    list_filter = ('title', 'created_at', 'author', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(Author, AuthorAdmin)






#



