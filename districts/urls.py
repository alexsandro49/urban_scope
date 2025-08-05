from django.urls import path
from . import views

app_name = 'districts'

urlpatterns = [
    path('', views.list_view, name='list')
]
