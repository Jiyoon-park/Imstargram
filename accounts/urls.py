from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signup_confirm/', views.signup_confirm, name='signup_confirm'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/follow', views.follow, name='follow'),
]
