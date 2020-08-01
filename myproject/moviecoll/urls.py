from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    # returns list of movies by hitting credy endpoint
    path('movies/', views.Movies.as_view(), name='movies_list'),
    # returns all collection for a user and creates new collection
    path('collection/', views.UserCollection.as_view(), name='user_collection'),

    # gets/edits/deletes details of a particular collection
    path('collection/<int:id>/', views.ParticularCollection.as_view(),
         name='user_collection'),

    path('request-count/reset/', views.RequestCountReset.as_view(),
         name='request_count_reset'),
    path('request-count/', views.RequestCount.as_view(), name='request_count'),

    path('b', views.home1, name='home_view'),
    path('', views.home, name='home_view'),
]
