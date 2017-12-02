from django.conf.urls import url

from djinora_chat import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^slack/$', views.slack_chat, name='slack'),
]
