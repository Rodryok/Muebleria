from django.urls import path
from . import views

urlpatterns = [

path('home/', views.home, name='home'),
path('login/', views.loginView, name='login'),
path('index/', views.index, name='index'),
path('home/', views.home, name='home'),
path('base/', views.base, name='base'),
path('dashboard/', views.dashboard, name='dashboard'),
path('logout/', views.logoutView, name='logout'),
]