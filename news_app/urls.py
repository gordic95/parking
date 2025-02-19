from django.urls import path
from . views import posts_list, PostListView, PostRUDView, create_post, post_detail

app_name = 'news_app'

urlpatterns = [
    path('', posts_list, name='posts_list'),
    path('posts_list/', PostListView.as_view(), name='posts_list'),
    path('posts_list/<int:pk>', PostRUDView.as_view(), name='posts_list'),
    path('create_post', create_post, name='create_post'),
    path('post_detail/<int:pk>', post_detail, name='post_detail')
]