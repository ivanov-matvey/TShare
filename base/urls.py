from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

    path('', views.index, name='index'),
    path('create-block/', views.create_block, name='create-block'),
    path('edit-block/<str:url>/', views.edit_block, name='edit-block'),
    path('delete-block/<str:url>/', views.delete_block, name='delete-block'),
    path('<str:url>', views.block, name='block'),
]
