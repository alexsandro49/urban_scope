from django.urls import path
from . import views

app_name = 'municipalities'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('<int:page_number>/', views.list_view, name='list')
]
