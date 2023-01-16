
from django.urls import path

from django.views.decorators.cache import cache_page

# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostUpdate, PostDelete, PostSearch, create_post, \
   html_403, CategoryListView, subscribe, author_create, comment_create, get_news_list, get_news, create_news, edit_news, delete_news

# rest_framework
from django.urls import path, include
from rest_framework import routers
from news import views
router = routers.DefaultRouter()
router.register(r'news', views.PostViewset)
router.register(r'catergory', views.CategoryViewset)
router.register(r'author', views.AuthorViewset)
router.register(r'user', views.UserViewset)
router.register(r'comment', views.CommentViewset)

urlpatterns = [
   path('', cache_page(60)(PostList.as_view()), name='posts_list'), 
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

   # add REST API
   path('api/news/', get_news_list),
   path('api/news/<int:pk>', get_news),
   path('api/create_news/', create_news),
   path('api/edit_news/<int:pk>', edit_news),
   path('api/delete_news/<int:pk>', delete_news),

   # rest_framework_routers
   #  path('', include(router.urls)),
   #  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   path('api-auth/', include(router.urls), name='api'),
]
