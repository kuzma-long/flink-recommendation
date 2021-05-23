from django.conf.urls import url, include
from . import views

app_name = 'shop'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'show_case/', views.show_case, name='show_case'),
    url(r'^squery/', views.query_case, name='query'),
    url(r'^show_case_item/([0-9]+)/', views.show_case_item, name='show_case_item'),
    url(r'dafen/([0-9]+)/$', views.dafen, name='dafen'),
]
