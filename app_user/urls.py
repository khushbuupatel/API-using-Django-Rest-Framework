from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ChangePassword.as_view())
]