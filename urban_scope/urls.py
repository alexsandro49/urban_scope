from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('states/', include(('states.urls', 'states'), namespace='states')),
    path("__reload__/", include("django_browser_reload.urls")),
]
