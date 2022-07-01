from django.urls import path, include
from .views import RegisterView, CustomAuthToken, logout
from rest_framework.authtoken import views


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    # path('login/', views.obtain_auth_token, name='login'),
    path('logout/', logout, name='logout'),
]