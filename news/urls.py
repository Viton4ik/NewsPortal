
from django.urls import path

from django.views.decorators.cache import cache_page

# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostUpdate, PostDelete, PostSearch, create_post, \
   html_403, CategoryListView, subscribe, author_create, comment_create#, AuthorCreate #PostCreate

urlpatterns = [
   # path('', cache_page(60)(PostList.as_view()), name='posts_list'), #FIXME
   path('', PostList.as_view(), name='posts_list'), #FIXME
   # pk — это первичный ключ, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:id>', PostDetail.as_view(), name='post_detail'),
   # path('<int:id>', PostDetail.as_view(), name='post_detail'),
   path('create/', create_post, name='create_post'),
   # path('create/', PostCreate.as_view(), name='create_post'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('403/', html_403, name='403'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('author_create/', author_create, name='author_create'),
   path('<int:pk>/comments/', comment_create, name='comments'),

]
