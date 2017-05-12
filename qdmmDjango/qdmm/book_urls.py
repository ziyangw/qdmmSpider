from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<key>[0-9]+)/$', views.book, name='book'),
]