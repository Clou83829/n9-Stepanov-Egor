from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('vacancy/<int:pk>/', views.vacancy_detail, name='vacancy_detail'),
]