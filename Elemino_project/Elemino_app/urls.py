from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/gallery/', views.pet_gallery, name='pet_gallery'),
    path('accounts/create/', views.account_create, name='account_create'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            template_name='Elemino_app/login.html',
            redirect_authenticated_user=True,
            next_page='dashboard',
        ),
        name='login',
    ),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('pets/add/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pets/<int:pk>/edit/', views.pet_update, name='pet_update'),
    path('pets/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
]