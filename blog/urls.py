from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_create_blogs, name="blog"),
    path('myblogs/', views.myblogs, name="myblogs"),
    path('create', views.create, name="create"),
    path('myblogs/<str:id>/', views.retrieve_by_id, name="retrieve_by_id"),
]