from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_create_videos, name="video"),
    path('team/', views.get_team, name="videoteam"),
    path('myvideos/', views.myvideos, name="myvideos"),
    path('create', views.create, name="create_video"),
    path('myvideos/<str:id>/', views.playvideo, name="playvideo"),
    path('mysocial/<str:id>/', views.retrieve_socials_by_id, name="retrieve_video_socials_by_id"),
    path('delete/<str:id>/', views.delete_by_id, name="delete_video_by_id"),

]