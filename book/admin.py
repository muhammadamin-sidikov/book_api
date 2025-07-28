from django.contrib import admin
from .models import Books, BookImage, Star, Comment, Like


class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'isbn', 'quantity', 'price', 'publication_date')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('publication_date', 'publisher', 'book_language')
    inlines = [BookImageInline]


@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'rating')
    list_filter = ('rating',)
    search_fields = ('user__email', 'book__title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'created_at')
    search_fields = ('user__email', 'book__title')
    list_filter = ('created_at',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'created_at')
    search_fields = ('user__email', 'book__title')
    list_filter = ('created_at',)


@admin.register(BookImage)
class BookImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'image')
    search_fields = ('book__title',)