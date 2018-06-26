from django.conf.urls import url
from . import views
from . import ajax_handler



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^team/', views.team, name='team'),
    url(r'^algorithm/', views.algorithm, name='algorithm'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^search/$', views.search),
    url(r'^error/$', views.error),
    url(r'^output/', views.output, name='output'),
    url(r'^get_car_data/$', ajax_handler.get_car_data, name='get_car_data'),
    url(r'^get_geo_data/$', views.get_geo_data, name='get_geo_data'),
]