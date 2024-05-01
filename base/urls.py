from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create-block/', views.create_block, name='create-block'),
]
