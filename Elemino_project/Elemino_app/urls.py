from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/add/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pets/<int:pk>/edit/', views.pet_update, name='pet_update'),
    path('pets/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
]