
from .models import *
from rest_framework import serializers

class PostSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Post
       fields = ['id', 'url', 'topic', 'content', 'author', 'contentType', 'rating', 'createTime', 'editTime',]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Category
       fields = ['id', 'name', 'url', ]
       depth = 1


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Author
       fields = ['id', 'url', ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = User
       fields = ['id', 'username', 'first_name', 'last_name', 'email', 'url', ] #'is_superuser', 


class CommentSerializer(serializers.HyperlinkedModelSerializer):
   class Meta:
       model = Comment
       fields = ['id', 'text', 'createTime', 'rating', 'commentPost', 'commentUser','url', 'is_active',] 
    