from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<page_num>[0-9]+)/$', views.index_page, name='index_page'),
]