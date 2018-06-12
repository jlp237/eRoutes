from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index, name='index'),
    url(r'^routing/', views.routing, name='routing'),
    url(r'^team/', views.team, name='team'),
    url(r'^algorithm/', views.algorithm, name='algorithm'),
    url(r'^search/$', views.search),
    url(r'^my_view/', views.my_view, name='my_view'),
    url(r'^output/', views.output, name='output'),
    url(r'^get_car_data/$', views.get_car_data, name='get_car_data'),
    url(r'^get_geo_data/$', views.get_geo_data, name='get_geo_data'),
]