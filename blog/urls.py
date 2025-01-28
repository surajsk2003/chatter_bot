from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Existing index path
    path('getUserResponse', views.getResponse, name='getResponse'),  # Define the new path
]
