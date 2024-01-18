from . import views
from django.urls import path

urlpatterns = [
    path('register', views.register_user),
    path('auth', views.user_authenticate),
    path('authorize', views.authorized_endpoint),
    path('weather', views.get_api_data)
]