from django.contrib import admin

from .models import Post, Author, Category


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('name','status','creation_date')
    search_fields = ['name']


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_publicated', 'author', 'description', 'status', 'publicated_date')
    search_fields = ['title','author']
    prepopulated_fields = {'slug': ('title',)}

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','last_name','email','description','creation_date')
    search_fields = ['name','last_name','email']


admin.site.register(Category, CategoriaAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)