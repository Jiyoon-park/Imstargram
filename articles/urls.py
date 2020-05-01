from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/detail/', views.detail, name='detail'),
    path('<int:article_pk>/like/', views.like, name='like'),
    path('<int:article_pk>/comments/', views.comments_create, name='comments_create'),
]