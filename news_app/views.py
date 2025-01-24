from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from . models import Post
from . serializers import PostSerializer
from . forms import PostForm


def posts_list(request):
    posts = Post.objects.all()   # получить все записи
    serializer = PostSerializer(posts, many=True)   # сериализовать
    # print(posts)
    # print(serializer)
    return render(request, 'news_app/posts_list.html', {'posts': serializer.data})

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'news_app/post_detail.html', {'post': post})


def create_post(requests):
    if requests.method == 'POST':   #если метод POST
        form = PostForm(requests.POST)   # создать объект формы
        if form.is_valid():     # если форма корректна
            post = form.save()    # сохранить объект
            return render(requests, 'news_app/post_detail.html', {'post': post})   # отобразить объект
    else:  # если метод GET
        form = PostForm()   # создать объект формы
    return render(requests, 'news_app/create_post.html', {'form': form})   # отобразить форму




        


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    pagination_class = PageNumberPagination





class PostRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'




