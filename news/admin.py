
# Не забываем зарегистрировать модели, иначе мы не увидим их в админке.
from django.contrib import admin
from .models import Post, Author, Category, Comment, PostCategory

# translation model
from modeltranslation.admin import TranslationAdmin 


def nullfy_authorRating(modeladmin, request, queryset):
    queryset.update(authorRating=0)
nullfy_authorRating.short_description = 'Обнулить рейтинг'

def nullfy_rating_comment(modeladmin, request, queryset):
    queryset.update(rating=0)
nullfy_rating_comment.short_description = 'Обнулить рейтинг'

def nullfy_rating_post(modeladmin, request, queryset):
    queryset.update(rating=0)
nullfy_rating_post.short_description = 'Обнулить рейтинг'

# создаём новый класс для представления товаров в админке
class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые мы хотим видеть в таблице
    # генерируем список имён всех полей для более красивого отображения
    list_display = [field.name for field in Comment._meta.get_fields()]
    actions = [nullfy_rating_comment]


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.get_fields()]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'authorRating')
    search_fields = ('authorUser',)
    list_filter = ('authorUser', )
    actions = [nullfy_authorRating]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('subscribers',)


# add translation area
class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'preview', 'contentType', 'author', 'createTime', 'rating', 'editTime')
    list_filter = ('author', 'createTime', 'rating')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('author', 'topic')
    actions = [nullfy_rating_post]


# add translation area
class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)

# admin.site.unregister(Post)
