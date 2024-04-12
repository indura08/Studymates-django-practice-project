"""
URL configuration for studymates project.

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
from django.contrib import admin
from django.urls import path, include
# from django.http import HttpResponse

#view hdnna function based views hdnwa api. ekiynne node js wla api route.get, route.post wage e a liynawa wage mekedi krnne menna meka

# def home(request):
#      return HttpResponse('Home page') 

# def room(request):
#      return HttpResponse('room page is this')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
    # path('', home),
    # path('room/', room),
]

#39:00 n nawtuwe
