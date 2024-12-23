"""
URL configuration for board_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from board import views as board_views

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('board/', include('board.urls', namespace='board')),
    path('accounts/logout/', board_views.logout_view, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', board_views.home, name='home'),
    path('signup/', board_views.signup, name='signup'),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
               + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
