from django.urls import path, include
from . import views

urlpatterns = [
    path('appointments/', views.AppointmentList.as_view()),
    path('appointments/<int:pk>/', views.AppointmentDetail.as_view())
]
