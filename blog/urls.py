from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_create_blogs, name="blog"),
    path('team/', views.get_team, name="team"),
    path('myblogs/', views.myblogs, name="myblogs"),
    path('create', views.create, name="create"),
    path('myblogs/<str:id>/', views.retrieve_by_id, name="retrieve_by_id"),
    path('mysocial/<str:id>/', views.retrieve_entries_by_id, name="retrieve_entries_by_id"),
]