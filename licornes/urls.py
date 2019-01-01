from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.Add.as_view(), name="add"),
    path('etape/', views.etape, name="etape"),
    path('etape/<str:licorne>/', views.etape, name="etape"),
]
