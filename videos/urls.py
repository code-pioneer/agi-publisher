from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_themes, name="video"),
    path('topic/<str:theme_id>/', views.select_topic, name="select_topic"),
    path('team/', views.get_team, name="videoteam"),
    path('myvideos/', views.myvideos, name="myvideos"),
    path('create', views.create, name="create_video"),
    path('theme', views.save_theme, name="save_theme"),
    path('myvideos/<str:id>/', views.playvideo, name="playvideo"),
    path('mysocial/<str:id>/', views.retrieve_socials_by_id, name="retrieve_video_socials_by_id"),
    path('delete/<str:id>/', views.delete_by_id, name="delete_video_by_id"),
    path('task', views.process_task, name="process_task"),
    path('select_task/<str:selection_type>/<str:video_id>/<str:task_name>/', views.select_task, name="select_task"),

]