"""cw1proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from cw1app.views import login_author, logout_author, post_story, get_stories, delete_story

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login_author),
    path('api/logout/', logout_author),
    path('api/poststory/', post_story),
    path('api/getstories/', get_stories),
    path('api/deletestory/', delete_story),
]
