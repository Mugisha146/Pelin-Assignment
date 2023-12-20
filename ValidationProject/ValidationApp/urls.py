from django.urls import path
from . import views

urlpatterns = [
    path('', views.participant_list, name='participant_list'),
    path('<int:pk>/', views.participant_detail, name='participant_detail'),
    path('create/', views.participant_create, name='participant_create'),
    path('vehicle/create/<int:participant_id>/', views.vehicle_create, name='vehicle_create'),
    path('<int:pk>/edit/', views.participant_edit, name='participant_edit'),
    path('<int:pk>/delete/', views.participant_delete, name='participant_delete'),
]
