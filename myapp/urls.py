# myapp/urls.py

from django.urls import path
from .views import UserCreate, UserLogin, save_code, save_attendance

urlpatterns = [
    path('register/', UserCreate.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('save_code/', save_code, name='save_code'),
    path('save_attendance/', save_attendance, name='save_attendance'),
]
