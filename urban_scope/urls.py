from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('states/', include(('states.urls', 'states'), namespace='states')),
    path('municipalities/', include(('municipalities.urls', 'municipalities'), namespace='municipalities')),
    path('districts/', include(('districts.urls', 'districts'), namespace='districts')),
    path('companies/', include(('companies.urls', 'companies'), namespace='companies')),
    path("__reload__/", include("django_browser_reload.urls")),
]
