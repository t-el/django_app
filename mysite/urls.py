"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rusty import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     path('admin/', admin.site.urls),
     path('', views.home),
     path('articles', views.articles),
     path('login', views.__login),
     path('logout', views.__logout),
     path('register', views.__register),
     path('completeprofile', views.__cp),
     path('profile/<username>', views.__profile),
     path('relation', views.__relation),
     path('upload_files', views.__upload),
     path('add_post', views.__add_post),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
