from django.urls import path

from . import views

urlpatterns = [

    # path(r'/s_map.html',views.s_map, name='s_map'),
    path('list/', views.test_list, name='post_list'),
    path('', views.index, name='index'),
    path('indextwo/', views.indextwo, name='indextwo'),
    path('200122/', views.tozi, name='200122'),
    path('gutozi/', views.gutozi, name='gutozi'),
    path('piechart/', views.piechart, name='piechart'),
    path('satis/', views.satis, name='satis'),
    path('lat/', views.lat, name='lat'),
    path('marker/', views.marker, name='marker'),






    path('post/', views.post_list, name='post'),
    path('test/<str:year_r>,<str:rate_r>,<str:poli_loc>/', views.make_map, name='test' ),#test/<str:year>/
    path('post/new/', views.post_new, name='post_new'),
    path('post/new/', views.post_new, name='post_new'),


]