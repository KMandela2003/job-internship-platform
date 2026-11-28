from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('post/', views.create_opportunity_view, name='create_opportunity'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('opportunity/<int:pk>/', views.opportunity_detail_view, name='opportunity_detail'),
]