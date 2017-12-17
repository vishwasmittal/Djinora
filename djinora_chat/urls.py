from django.conf.urls import url

from django.conf.urls.static import static

from Djinora import settings
from djinora_chat import views

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'^slack/$', views.SlackResponseView.as_view(), name='slack'),
                  url(r'^register/$', views.register_chat, name='register-chat'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
