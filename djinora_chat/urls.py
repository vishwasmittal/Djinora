from django.conf.urls import url

from djinora_chat import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
