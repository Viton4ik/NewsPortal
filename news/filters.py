


from django_filters import FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter, CharFilter, DateFromToRangeFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Author, Category
from django.forms import DateInput
from django import forms

# translation function
from django.utils.translation import gettext_lazy as _


# Создаем свой набор фильтров для модели Post.
class PostFilter(FilterSet):

    topic = CharFilter(field_name='topic',
                       lookup_expr='contains',
                       label=_('Topic:'))

    author = ModelChoiceFilter(
        field_name='author',
        queryset=Author.objects.all(),
        label=_('Author:'),
        empty_label='any',
    )

#### or like that
    # author = ModelMultipleChoiceFilter(
    #     field_name='author',
    #     queryset=Author.objects.all(),
    #     label='Author',
    #     conjoined=True,
    # )
#####

    postCategory = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label=_('Category:'),
        empty_label='any',
    )

    # add time widget
    createTime_filer = DateTimeFilter(
        field_name='createTime',
        lookup_expr='gte',
        label=_('Creation date:'),
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M', # there is no reaction on this!
            attrs={'type': 'date'}, #attrs={'type': 'datetime-local'}, ,
        ),
    )

    class Meta:
       model = Post
       fields = {
           # 'topic': ['contains'],
           # 'author': ['exact'],
           # 'postCategory': ['exact'],
           # 'rating': ['contains'],
           # 'createTime': [
           #     'date__gte'],
           #     'date__lte',
           # ],
       }

