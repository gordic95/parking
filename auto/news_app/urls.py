from django.urls import path
from . views import posts_list, PostListView, PostRUDView

app_name = 'news_app'

urlpatterns = [
    path('', posts_list, name='posts_list'),
    path('posts_list/', PostListView.as_view(), name='posts_list'),
    path('posts_list/<int:pk>', PostRUDView.as_view(), name='posts_list'),
]