from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_user_blogs, name= "user_blogs"),
    path('create', views.create, name="create"),
    path('retrieve', views.retrieve, name="retrieve"),
]