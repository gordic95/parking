from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from . models import Post
from . serializers import PostSerializer


def posts_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    # print(posts)
    # print(serializer)
    return render(request, 'news_app/posts_list.html', {'posts': serializer.data})


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    pagination_class = PageNumberPagination


class PostRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'




