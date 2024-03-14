from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('movies/', views.list_movies),
    path('collection/', views.list_create_collections),
    path('collection/<uuid:collection_uuid>/',
         views.retrieve_update_delete_collection),
    path('request-count/', views.request_count),
    path('request-count/reset/', views.reset_request_count),
]
