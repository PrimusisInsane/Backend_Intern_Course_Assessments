from django.urls import path
from . import views

urlpatterns = [
    path('', views.add, name='index'),
    path('authorization/', views.index, name='authorization'),
]