from django.urls import path
from django.contrib.auth.decorators import login_required
from blogs import views

urlpatterns = [
    path('<int:id>', login_required(views.UserBlogView.as_view())),
    path('post/create', login_required(views.PostCreateView.as_view()), name='post_create'),
    path('news/', login_required(views.NewsListView.as_view()), name='list_of_news'),
    path('mark/<int:id>', views.mark_about_read, name='mark_as_read'),
    path('post/detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]
