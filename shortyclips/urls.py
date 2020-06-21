"""shortyclips URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shortyclipsAPI.views import login

from shortyclipsAPI import views

urlpatterns = [
    path('api/v1/user/register', views.UserCreate.as_view()),
    path('admin/', admin.site.urls),
    path('api/v1/user/<int:pk>', views.UserInfo.as_view()),
    path('api/v1/user/login', login),
    path('api/v1/clips/', views.ClipList.as_view()),
    path('api/v1/clip/<int:pk>', views.ClipDetail.as_view()),
    path('api/v1/clip/<int:pk>/like', views.postLike),
    path('api/v1/clip/new',views.ClipCreate.as_view()),
    path('api/v1/user/favorites',views.getUserFavorite)

]
