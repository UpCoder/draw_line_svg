"""draw_line URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from googlechart import views

urlpatterns = [
    url(r'show_chart/$', views.show_chart),
    url(r'update_data/$', views.update_data),
    url(r'show_attributes/$', views.show_attributes),
    url(r'get_show_data/$', views.get_show_data),
    url(r'example_download/$', views.file_download),
]
