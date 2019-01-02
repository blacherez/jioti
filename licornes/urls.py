from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.Add.as_view(), name="add"),
    path('etape/', views.etape, name="etape"),
    path('etape/<str:licorne>/', views.etape, name="etape"),
    path('licorne/<int:licorne_id>/', views.licorne, name="licorne"),
    path('media/<int:etape_id>/', views.media, name="media"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
